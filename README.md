# 🧠 OppMatch – AI-Powered Opportunity Matcher

OppMatch is an intelligent, multi-agent platform designed to help students and early professionals discover grants and internships tailored to their unique skills—with zero manual search.

## 🔍 How It Works

1. 📄 Upload your CV
2. 🧠 Our agents extract key strengths and career goals
3. 🌐 They search across platforms—LinkedIn, Google Jobs, and grant portals
4. 🎯 And deliver personalized opportunities, instantly

No filters. No guesswork. Just smart, autonomous results.

---

## 📁 Project Structure

oppmatch/
├── backend → Laravel API (PHP)
├── frontend → React App (JavaScript)
└── agents → Flask Service (Python AI Agents)

---

## 🛠 Backend Setup (Laravel API)

### 📍 Location:

`/backend`

### ✅ Requirements:

- PHP 8.x
- Composer
- MySQL
- Laravel CLI

---

### ⚙️ Setup

1. **Navigate to the backend folder**
   ```bash
   cd backend
   ```

Install dependencies

bash
Copy
Edit
composer install
Create .env file

bash
Copy
Edit
cp .env.example .env
Update .env with your local DB config:

ini
Copy
Edit
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=oppmatch
DB_USERNAME=root
DB_PASSWORD=your_password
Generate application key

bash
Copy
Edit
php artisan key:generate
Run database migrations

bash
Copy
Edit
php artisan migrate
Start the Laravel development server

bash
Copy
Edit
php artisan serve
Laravel will run at: http://127.0.0.1:8000

💻 Frontend Setup (React App)
📍 Location:
/frontend

✅ Requirements:
Node.js 16+

npm or yarn

⚙️ Setup
Navigate to the frontend folder

bash
Copy
Edit
cd ../frontend
Install dependencies

bash
Copy
Edit
npm install
Create .env file

bash
Copy
Edit
cp .env.example .env
Update the .env file:

ini
Copy
Edit
REACT_APP_API_URL=http://127.0.0.1:8000/api
Start the React development server

bash
Copy
Edit
npm start
React will run at: http://localhost:3000

🤖 Agents Setup (Flask Service)
📍 Location:
/agents

✅ Requirements:
Python 3.9+

pip

Recommended: virtualenv

⚙️ Setup
Navigate to the agents folder

bash
Copy
Edit
cd ../agents
Create and activate virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Create .env file
Create a .env file in the agents directory and add:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_api_key_here
LAMA_API_KEY=your_lama_api_key_here_if_needed
🚀 Run Flask Server
bash
Copy
Edit
python app.py
Flask will run at: http://127.0.0.1:5000

📡 API Endpoints
POST /process-pdf
Upload a PDF (multipart/form-data, key: file)
Example:

bash
Copy
Edit
curl -X POST http://127.0.0.1:5000/process-pdf -F "file=@your_resume.pdf"
GET /health
Health check endpoint:

bash
Copy
Edit
curl http://127.0.0.1:5000/health
🔗 Inter-Service Integration
Service URL Role
Backend http://127.0.0.1:8000 API for data & auth
Frontend http://localhost:3000 User interface
Agents http://127.0.0.1:5000 CV parsing & opportunity matching logic

🧪 Quick Start Summary

# Backend

cd backend
cp .env.example .env
php artisan key:generate
php artisan migrate
php artisan serve

# Frontend

cd ../frontend
cp .env.example .env
npm install
npm start

# Agents

cd ../agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
