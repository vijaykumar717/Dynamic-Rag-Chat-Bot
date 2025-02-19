ABEX Chat Bot - AI-Powered Web Scraper & Chat Interface
🚀 ABEX Chat Bot is an AI-powered application that scrapes web content, processes it using Weaviate for semantic search, and provides intelligent responses using Google's Gemini AI.

It features:
✅ Web scraping using Selenium
✅ AI-powered chatbot with personality modes (Formal, Casual, Humorous)
✅ Optimized embeddings using Sentence Transformers
✅ Vector search with Weaviate
✅ FastAPI backend with Next.js frontend

📌 Tech Stack Used
Component	Technology
Frontend	Next.js (React)
Backend	FastAPI
Database	Weaviate (Vector Search)
Web Scraping	Selenium & BeautifulSoup
AI Model	Google Gemini API
Embeddings	sentence-transformers/all-mpnet-base-v2
Hosting	Local (or Cloud)
📥 Installation & Running Locally
This project consists of two folders:
1️⃣ backend/ → FastAPI Server (Handles scraping, AI requests, and Weaviate storage)
2️⃣ frontend/ → Next.js UI (Chatbot UI & Scraping Interface)

🚀 Backend Setup (FastAPI)
Create a virtual environment & activate it:

sh
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
Install dependencies:

sh
Copy
Edit
pip install -r requirements.txt
Set up environment variables (.env file in backend/):

ini
Copy
Edit
GEMINI_API_KEY=your-gemini-api-key
WEAVIATE_URL=http://localhost:8080  # If using local Weaviate
WEAVIATE_API_KEY=your-weaviate-api-key
Start the FastAPI server:

sh
Copy
Edit
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
🌐 Frontend Setup (Next.js)
Navigate to the frontend folder:

sh
Copy
Edit
cd ../frontend
Install dependencies:

sh
Copy
Edit
npm install
Run the Next.js development server:

sh
Copy
Edit
npm run dev
Open http://localhost:3000 in your browser to interact with the chatbot.

⚠️ Assumptions & Limitations
🔹 Weaviate Setup: The application assumes Weaviate is running either locally or via a cloud instance. If using Weaviate Cloud, update WEAVIATE_URL.
🔹 Google Gemini API: You must have a valid API key for Google's Gemini AI model to process queries.
🔹 Scraping Limitations: Some sites may block Selenium-based scraping due to bot detection.
🔹 AI Model Restrictions: Gemini API may filter responses based on content safety guidelines.
🔹 No Database Persistence: Current version does not persist data beyond active Weaviate sessions.
