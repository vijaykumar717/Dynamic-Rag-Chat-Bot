from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time
import google.generativeai as genai
import weaviate
import os
from sentence_transformers import SentenceTransformer

load_dotenv()

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Initialize Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Correct Weaviate Client Initialization (for v3)
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
)

# Load Pretrained Embedding Model
embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlList(BaseModel):
    urls: List[str]
    namespace: str

class UserQuery(BaseModel):
    query: str

def create_weaviate_schema():
    """Creates Weaviate Schema if it does not exist"""
    schema = {
        "classes": [
            {
                "class": "ScrapedData",
                "vectorizer": "none",  # Since we are providing embeddings manually
                "properties": [
                    {"name": "url", "dataType": ["string"]},
                    {"name": "text", "dataType": ["text"]},
                ]
            }
        ]
    }

    existing_classes = [c["class"] for c in client.schema.get()["classes"]]

    if "ScrapedData" not in existing_classes:
        client.schema.create(schema)
        print("✅ Weaviate Schema Created Successfully")
    else:
        print("✅ Schema Already Exists")

# Ensure schema is created on startup
create_weaviate_schema()

def scrape_content(url: str) -> str:
    """Scrape text content from a given URL using Selenium"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        time.sleep(3)  # Wait for page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        visible_text = soup.get_text(separator="\n", strip=True)
        driver.quit()

        return visible_text[:5000]

    except Exception as e:
        return f"Failed to scrape URL: {e}"


@app.post("/scrape")
def scrape_multiple_urls(data: UrlList):
    """Scrape multiple URLs and store embeddings in Weaviate"""
    results = {}
    namespace = data.namespace

    for url in data.urls:
        content = scrape_content(url)
        if content:
            results[url] = content
            try:
                embedding = generate_query_embedding(content)

                # Insert into Weaviate
                client.data_object.create(
                    class_name="ScrapedData",
                    data_object={"url": url, "text": content[:5000]},
                    vector=embedding
                )
                print(f"✅ Data inserted into Weaviate")
            except Exception as e:
                print(f"❌ Embedding failed for {url}: {e}")

    if not results:
        raise HTTPException(status_code=400, detail="No valid content retrieved.")
    return {"content": results}


@app.post("/ask")
def ask_question(data: UserQuery):
    """Retrieve relevant content using Weaviate and generate a response with Gemini"""
    query_embedding = generate_query_embedding(data.query)

    response = client.query.get(
    class_name="ScrapedData",
    properties=["url", "text"]
).with_near_vector({"vector": query_embedding}).with_limit(5).do()


    matches = response.get("data", {}).get("Get", {}).get("ScrapedData", [])

    if matches:
        context = "\n".join([match.get("text", "") for match in matches if "text" in match])

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Context: {context}\n\nAnswer the question: {data.query}")

        return {"answer": response.text if response and hasattr(response, "text") else "Response failed"}
    else:
        return {"answer": "No relevant content found."}


def generate_query_embedding(query: str):
    """Generate vector embedding for a query"""
    try:
        return embedding_model.encode(query).tolist()
    except Exception as e:
        raise Exception(f"Failed to generate query embedding: {e}")
