PUBLIC URL OF THE APPLICATION:http://13.127.96.122/


ABEX Chat Bot - AI-Powered Web Scraper & Chat Interface


🚀 ABEX Chat Bot is an advanced AI-powered web scraper and chatbot that can extract web content, store it in a vector database (Weaviate), and provide intelligent responses using Google Gemini AI.



It includes:

✅ Web Scraping with Beautifulsoup and requests

✅ AI Chatbot with Multiple Personalities (Formal, Casual, Humorous)

✅ Efficient Vector Search with Weaviate

✅ Optimized Embeddings with Sentence Transformers

✅ FastAPI Backend + Next.js Frontend




📌 Tech Stack Used

Frontend: Next.js (React)

Backend: FastAPI

Vector Database: Weaviate (Semantic Search)

Web Scraping: Requests & BeautifulSoup

AI Model: Google Gemini API

Embeddings: sentence-transformers/all-mpnet-base-v2

Hosting: AWS EC2



📥 Installation & Running Locally

This project consists of two folders:

📂 backend/ → Handles scraping, AI interactions, and vector storage

📂 frontend/ → UI for the chatbot and scraping interface



🚀 Backend Setup (FastAPI)

1.Create a virtual environment & activate it

python -m venv venv

venv/scripts/activate



2.Install dependencies

pip install -r requirements.txt



3.Set up environment variables (.env file in backend/)

GEMINI_API_KEY=your-gemini-api-key

WEAVIATE_URL=your-url

WEAVIATE_API_KEY=your-weaviate-api-key



4.Start the FastAPI server

uvicorn app:app --host 0.0.0.0 --port 8000 --reload



🌐Frontend Setup (Next.js)

1.cd frontend


2.Install dependencies

npm install


3.Run the Next.js development server

npm run dev



Deployment Setup (AWS EC2)













⚠️ Assumptions & Limitations

Weaviate Setup: Ensure Weaviate is running either locally or via Weaviate Cloud. Update WEAVIATE_URL accordingly.

Google Gemini API: Requires a valid API key for AI responses.

Scraping Limitations: Some websites may not contain texts inside html

AI Model Restrictions: Gemini API might filter responses based on safety rules.

No Database Persistence: Current version does not persist data beyond active Weaviate sessions.



📄 License
This project is open-source and licensed under the MIT License.




