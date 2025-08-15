# NullAxis Agent

NullAxis Agent is an intelligent customer support assistant that classifies incoming queries and routes them appropriately as technical issues, product/feature requests, or sales leads. Built with a FastAPI backend and a React frontend, it uses a local LLM for NLP tasks like classification, information extraction, and department routing.

---

## 🛠️ Features

- Classifies queries into:
  - Technical issues (respond via semantic search or department routing)
  - Product/feature requests (logged)
  - Sales leads (contact details extracted interactively)
- Sentiment detection and logging of negative sentiment messages
- Local LLM support 
- UI for email + query submission
---

##  Project Structure
  NullAxis-Agent/
│
├── backend/
│ ├── main.py # FastAPI app
│ ├── router.py # Logic for routing queries
│ ├── utils.py # Sentiment, classification, extraction utils
│ ├── knowledge_base.json # Local tech support knowledge base
│ ├── tech_issues.json # Logged unresolved technical queries
│ ├── product_requests.json # Logged feature requests
│ ├── sales_leads.json # Logged sales leads
│ ├── negative_messages.json # Logged negative sentiment messages
│ └── models/ # LLM or embedding models (see below)
│
├── frontend1/
│ ├── public/
│ ├── src/
│ │ ├── pages/
│ │ │ ├── Index.jsx # Main UI
│ │ │ └── NotFound.jsx
│ │ ├── styles/
│ │ │ └── Index.css # Custom styles (no Tailwind)
│ │ └── App.jsx
│ └── package.json
│
└── myenv/ # venv Python environment

## 🧪 Requirements

First clone this repo using command :

git clone https://github.com/Rishabh-Sur/NullAxis-Agent.git

### Backend (Python 3.10+)

Navigate to the root directory
Create and activate a virtual environment:

bash
# Using venv
python -m venv myenv

source myenv/bin/activate for Linux/macOS
myenv\Scripts\activate   for  Windows

Next inside the created environment run the command: 
pip install -r requirements.txt

We use Gemini 1.5 flash API for the query classification and info extraction tasks

But for using this, API key is needed. Login to your google ai studio account and generate GOOGLE_API_KEY

Make a file .env in the root directory and store the api key there as:
 OPENAI_API_KEY= XXXXXXXXXX

### Frontend (React.js)

Navigate to the dir path_to_root_direc/frontend1
Run command : npm install    
to install node modules (use must have nodejs already installed on your system)

### Running the App

# Starting the Backend server

Go to root directory(outside backend folder) and activate the environment by running the script:

myenv\Scripts\activate (for Windows) and source myenv/bin/activate (for Linux/macOS) 
  
Then run the script:

uvicorn backend.main:app --reload 

# Starting the Frontend server

Go to frontend1 directory and run : npm start

Wait for both the servers to start, frontend server will run at "http://localhost:3000" and backend server at "http://localhost:8000".





