# 🧠 Company Brain AI

### AI-Powered Company Knowledge Assistant Using Python and FalkorDB

Company Brain AI is a graph-based company knowledge assistant that helps users explore employee information, departments, projects, and organizational relationships through natural-language questions.

The project combines Python, Flask, and FalkorDB to make company information easier to search and understand through a conversational web interface.

## 🚀 Features

- **Employee Lookup:** Retrieve employee profiles, job titles, skills, departments, and other available details.
- **Department Insights:** Explore department information and employee distribution.
- **Project Exploration:** Query project records and employee-project relationships.
- **Graph-Based Retrieval:** Use connected entities and relationships to retrieve organizational information.
- **Interactive Chat Interface:** Ask questions through a clean, dark-themed web application.
- **Evidence Trail:** Display retrieved records when supported by the backend.
- **Modular Architecture:** Keep backend logic, database operations, and frontend code organized.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web application |
| FalkorDB | Graph database |
| Cypher-compatible queries | Graph retrieval |
| HTML, CSS, JavaScript | Frontend |
| Git and GitHub | Version control |

## 🏗️ How It Works

1. The user enters a question in the web interface.
2. The frontend sends the question to the Flask backend.
3. The backend processes the request and retrieves relevant graph data.
4. FalkorDB returns matching records and relationships.
5. The application formats and displays the response.

```text
User
  ↓
Web Interface (HTML, CSS, JavaScript)
  ↓
Flask Backend
  ↓
Query and Retrieval Logic
  ↓
FalkorDB Knowledge Graph
  ↓
Response and Evidence
```

## 📁 Project Structure

```text
company-brain-ai/
├── app.py
├── web_app.py
├── seed.py
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
└── .gitignore
```

- `app.py` — Core application and retrieval logic.
- `web_app.py` — Flask web application.
- `seed.py` — Database seeding and data import utilities.
- `static/` — Frontend JavaScript and CSS.
- `templates/` — HTML interface.
- `.gitignore` — Excludes local and sensitive files from Git.

## 💡 Example Questions

Try asking questions such as:

- Who is Kavya Gupta?
- Who is EMP-0040?
- Which department has the highest number of employees?
- Show all projects.
- Which employees work on Security Modernization?
- Show the projects connected to Kavya Gupta.

*Results depend on the available graph data and the query patterns supported by the current backend.*

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MrToji01/company-brain-ai.git
cd company-brain-ai
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the Python packages required by the project. If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

### 4. Configure FalkorDB

Start FalkorDB and configure the connection settings expected by the backend. For local development, the connection may use `localhost:6379`.

### 5. Configure Environment Variables

Create a local `.env` file if required and add the configuration variables expected by your code. Never publish real API keys, passwords, or database credentials.

### 6. Prepare the Database

If the graph needs to be populated, review the seeding script and provide an authorized dataset before running:

```bash
python seed.py
```

### 7. Run the Application

Start the Flask application:

```bash
python web_app.py
```

Open the local URL printed in the terminal, commonly `http://127.0.0.1:5000`.

## 🔐 Security

- Keep `.env` and API keys out of GitHub.
- Do not publish private employee records or confidential datasets.
- Keep virtual environments and generated cache files out of version control.
- Verify that no credentials are hardcoded in the source code.

## 🔮 Future Improvements

- More robust natural-language query handling.
- Dedicated agents for different company workflows.
- Improved graph retrieval and query accuracy.
- Automated testing and error handling.
- Authentication and role-based access control.
- Better evidence presentation and performance optimization.

## 👨‍💻 Author

**MrToji01**

GitHub: [@MrToji01](https://github.com/MrToji01)

Repository: [Company Brain AI](https://github.com/MrToji01/company-brain-ai)

---

*Company Brain AI — making connected company knowledge easier to explore.*
