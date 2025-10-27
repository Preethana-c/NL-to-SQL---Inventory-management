# Intelligent Inventory Management (NL → SQL)

This project integrates **Natural Language Processing (NLP)**, **AI-driven SQL generation**, and **Streamlit** to manage an inventory database using **simple text or speech commands**.  
Users can say or type instructions like _“Add 2 Potatoes”_ or _“Show all items”_ — and the system automatically generates and executes corresponding **SQLite queries** using **LLaMA 3.2 (3B)**.

---

## Features

-  **Speech to Text** — Converts voice commands into text using OpenAI’s Whisper model.  
-  **Natural Language to SQL** — Uses **LLaMA 3.2 3B (Ollama)** via **LangChain** to generate accurate SQL queries.  
-  **SQLite Integration** — Dynamically updates, inserts, or fetches data.  
-  **Streamlit Frontend** — Interactive web dashboard to record, transcribe, execute, and display results — all in real-time.  
  - **AI-Powered Query Correction** — Ensures valid, minimal SQL for simple instructions.

---

##  File Structure
intelligent-inventory-management/
├── app.py # Main Streamlit application
├── requirements.txt # Dependencies list
├── README.md # Project documentation
├── presentation.pptx # (Optional) Presentation slides
└── report.pdf # (Optional) Detailed project report

#  NL-to-SQL Inventory Management

This project converts **natural language (or voice)** commands into **SQL queries** to manage an inventory database — powered by **Whisper**, **LLaMA 3.2**, and **Streamlit**.

---

## Setup Instructions

### 1️  Clone the repository
```bash
git clone https://github.com/Preethana-c/NL-to-SQL---Inventory-management.git
cd NL-to-SQL---Inventory-management
```

### 2️  Create and activate a virtual environment
```bash
python -m venv venv
```

#### On Windows:
```bash
venv\Scripts\activate
```

#### On Mac/Linux:
```bash
source venv/bin/activate
```

### 3️ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️  Run the app
```bash
streamlit run app.py
```

---

##  How It Works

1. Record or upload a voice instruction (e.g., “Add 5 Apples”).
2. Whisper transcribes the audio into text.
3. The **LLaMA 3.2 model** (via Ollama) converts text → SQL query.
4. The generated SQL is executed on an in-memory **SQLite database**.
5. The **Streamlit dashboard** displays the updated inventory in real time.

---

##  Example Commands

| Natural Language Input | Generated SQL | Description |
|------------------------|----------------|--------------|
| “Add 5 Tomatoes” | `UPDATE Inventory SET quantity = quantity + 5 WHERE item_name = 'Tomato';` | Increases quantity |
| “Remove 2 Apples” | `UPDATE Inventory SET quantity = quantity - 2 WHERE item_name = 'Apple';` | Decreases quantity |
| “Show all items” | `SELECT * FROM Inventory;` | Displays full inventory |

---

##  Requirements

Main dependencies used in the project:

- streamlit  
- sqlite3  
- pandas  
- langchain_community  
- ollama  
- whisper  
- tempfile  
- re  

 *(These are already included in `requirements.txt`)*

---

##  Files Included

- `app.py` — Streamlit frontend  
- `requirements.txt` — Required dependencies  
- `inventory.db` — SQLite database  
- `README.md` — This file  
- `ppt/` and `pdf/` folders for presentation materials  

---






