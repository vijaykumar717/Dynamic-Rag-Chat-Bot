🌍 ABEX Chat Bot - AI-Powered Web Scraper & Chat Interface
🔗 Public URL: http://13.127.96.122/

🚀 ABEX Chat Bot is an advanced AI-powered web scraper and chatbot that extracts web content, stores it in a vector database (Weaviate), and provides intelligent responses using Google Gemini AI.

## 📌 Project Structure
 
```
/RAG                   # Root directory
│── /frontend          # Next.js frontend
│   ├── package.json   # Next.js dependencies
│   ├── next.config.js # Next.js configuration
│   ├── /public        # Static assets
│   ├── /pages         # Frontend pages (React)
│   ├── /components    # Reusable components
│   ├── /styles        # CSS styles
│   ├── /node_modules  # Installed dependencies (after npm install)
│   ├── .next          # Build files (after npm run build)
│── /backend           # FastAPI backend
│   ├── app.py         # FastAPI main entry point
│   ├── requirements.txt  # Python dependencies
│   ├── /static        # Static files (if needed)
│   ├── /templates     # HTML templates (if needed)
```




🔥 Key Features


✅ Web Scraping with BeautifulSoup and Requests

✅ AI Chatbot with Multiple Personalities (Formal 🎓, Casual 😎, Humorous 🤡)

✅ Efficient Vector Search with Weaviate

✅ Optimized Embeddings using Sentence Transformers

✅ FastAPI Backend + Next.js Frontend


--------------------------------------------------------------------------------------------------------------------------------


📌 Tech Stack


Frontend -	Next.js (React)

Backend -	FastAPI

Vector Database -	Weaviate (Semantic Search)

Web Scraping -	Requests & BeautifulSoup

AI Model -	Google Gemini API

Embeddings -	sentence-transformers/all-mpnet-base-v2

Hosting -	AWS EC2


-------------------------------------------------------------------------------------------------------------------------------



📥 Installation & Running Locally

This project consists of two main folders:

📂 backend/ → Handles scraping, AI interactions, and vector storage 

📂 frontend/ → UI for the chatbot and scraping interface



--------------------------------------------------------------------------------------------------------------------------------------------------------------


🚀 Backend Setup (FastAPI)


1️⃣ Create a virtual environment & activate it

python -m venv venv

source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows



2️⃣ Install dependencies

pip install -r requirements.txt



3️⃣ Set up environment variables (.env file in backend/)


Create a .env file and add the following:

GEMINI_API_KEY=your-gemini-api-key
WEAVIATE_URL=your-weaviate-url
WEAVIATE_API_KEY=your-weaviate-api-key



4️⃣ Start the FastAPI server

uvicorn app:app --host 0.0.0.0 --port 8000 --reload



-------------------------------------------------------------------------------------------------------------------------------------------------



🌐 Frontend Setup (Next.js)


1️⃣ Navigate to the frontend directory

cd frontend




2️⃣ Install dependencies

npm install



3️⃣ Run the Next.js development server

npm run dev


----------------------------------------------------------------------------------------------------------------------------------------------


# Deployment Setup (AWS EC2)
 
This guide provides step-by-step instructions to deploy the **Next.js frontend** and **FastAPI backend** on an **Ubuntu EC2 instance** with **PM2 (for Next.js) and Systemd (for FastAPI)**.
 
 
## 🚀 Deployment Environment
 
- **EC2 Instance Type:** t2.Xlarge(4vCPU ,16 GB RAM) (Ubuntu 22.04 LTS)
- 
- **Frontend:** Next.js (Node.js 20)
- 
- **Backend:** FastAPI (Python 3.10)
- 
- **Process Manager:** PM2 (Next.js), Systemd (FastAPI)
- 
- **Web server:** Nginx 
 
---

 
## ✅ Prerequisites
 
Before proceeding, ensure you have:
- A **running EC2 Ubuntu 22.04 instance** 
- **SSH access** to the instance


- 
- Installed dependencies:
  ```sh
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3-pip python3-venv nginx
  ```
 
---

 
## ⚙️ Step 1: Install Node.js (Version 20)
 
```sh
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v  # Verify Node.js version
npm -v   # Verify NPM version
```
 
---


 
## ⚙️ Step 2: Set Up Next.js Frontend

 
### 2.1 Navigate to the frontend directory and install dependencies:
```sh
cd /RAG/frontend
npm install
```

 
### 2.2 Build the Next.js application:
```sh
npm run build
```

 
### 2.3 Start the Next.js app in the background using PM2:
```sh
npm install -g pm2
pm run start  # Test if Next.js runs successfully
pm2 start "npm run start" --name "nextjs"
pm2 save
pm2 startup
```


 
---
 
## ⚙️ Step 3: Set Up FastAPI Backend

 
### 3.1 Navigate to the backend directory:
```sh
cd /RAG/backend
```

 
### 3.2 Create a Python virtual environment and activate it:
```sh
python3 -m venv venv
source venv/bin/activate
```

 
### 3.3 Install FastAPI dependencies:
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

 
### 3.4 Test if FastAPI runs successfully:
```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

 
If it works, stop the process (`CTRL + C`).

 
### 3.5 Create a Systemd Service for FastAPI
 
Create a new systemd service file:
```sh
sudo nano /etc/systemd/system/fastapi.service
```

 
Paste the following:
```ini
[Unit]
Description=FastAPI service
After=network.target
 
[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/RAG/backend
ExecStart=/RAG/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
 
[Install]
WantedBy=multi-user.target
```


 
### 3.6 Start and Enable FastAPI Service
```sh
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi
```
 
Check status:
```sh
sudo systemctl status fastapi
```
 
---

 
## ⚙️ Step 4: Configure Nginx 

 
### 4.1 Install Nginx:
```sh
sudo apt install nginx -y
```

 
### 4.2 Create an Nginx Configuration File
```sh
sudo nano /etc/nginx/sites-available/rag
```
 
Paste the following:
```nginx
server {
    listen 80;
    server_name your_domain_or_ip;
 
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
 
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


 
### 4.3 Enable Nginx Configuration
```sh
sudo ln -s /etc/nginx/sites-available/rag /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

 
---
 
## 🔥 Final Steps
 
   
1. **Access your app**:

-`http://your_domain_or_ip`
 

 



⚠️ Assumptions & Limitations

Weaviate Setup: Ensure Weaviate is running either locally or via Weaviate Cloud. Update WEAVIATE_URL accordingly.

Google Gemini API: Requires a valid API key for AI responses.

Scraping Limitations: Some websites may not contain texts inside html

AI Model Restrictions: Gemini API might filter responses based on safety rules.

No Database Persistence: Current version does not persist data beyond active Weaviate sessions.



📄 License
This project is open-source and licensed under the MIT License.




