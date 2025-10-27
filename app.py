import streamlit as st
import sqlite3
import pandas as pd
import re
from langchain_community.llms import Ollama
import whisper
import tempfile

# ------------------------------
# Step 0: SQLite database
# ------------------------------
if 'conn' not in st.session_state:
    st.session_state.conn = sqlite3.connect(':memory:', check_same_thread=False)
    st.session_state.c = st.session_state.conn.cursor()
    c = st.session_state.c

    # Inventory table
    c.execute('''
    CREATE TABLE Inventory (
        "item no" INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE,
        quantity INTEGER
    )
    ''')

    # Seed Inventory
    items = [
        ("Potato", 25),
        ("Tomato", 40),
        ("Onion", 30),
        ("Carrot", 15),
        ("Apple", 20),
    ]
    c.executemany("INSERT INTO Inventory (item_name, quantity) VALUES (?, ?)", items)
    st.session_state.conn.commit()
else:
    c = st.session_state.c

# ------------------------------
# Step 1: Streamlit UI
# ------------------------------
st.title(" Inventory Manager - NL → SQL (LLaMA 3.2 3B)")

st.write("### Current Inventory")
c.execute('SELECT "item no", item_name, quantity FROM Inventory')
data = c.fetchall()
st.dataframe(pd.DataFrame(data, columns=["Item No", "Item Name", "Quantity"]))

# ------------------------------
# Step 2: Audio Input (Optional)
# ------------------------------
st.write("###  Audio Input (Optional)")
audio_file = st.file_uploader(
    "Upload audio instruction (WAV, MP3, M4A, OPUS)", 
    type=["wav", "mp3", "m4a", "opus"]
)

user_instruction = ""

if audio_file is not None:
    st.info("Transcribing audio...")
    model = whisper.load_model("medium", device="cpu")  # default is CPU
  # use "small" or "base" for CPU
    # Save uploaded file to temp
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}")
    temp_file.write(audio_file.read())
    temp_file.close()

    # Transcribe audio
    result = model.transcribe(temp_file.name, task="translate")
    user_instruction = result["text"]
    st.success(f"Transcribed Instruction: {user_instruction}")

# ------------------------------
# Step 3: Manual text input (optional)
# ------------------------------
typed_instruction = st.text_input(
    "Or type your instruction (e.g., 'add 2 Potato', 'remove 1 Tomato', 'show all items'):"
)

# Use typed instruction only if there was no audio
if not user_instruction.strip() and typed_instruction.strip():
    user_instruction = typed_instruction.strip()

if user_instruction:
    st.info(f"Instruction to process: {user_instruction}")

# ------------------------------
# Step 4: LLaMA SQL Generation & Execution
# ------------------------------
if st.button("Generate SQL & Update") and user_instruction.strip():
    try:
        st.info("Generating SQL query using LLaMA 3.2 3B...")

        llm_model = Ollama(model="llama3.2:3b")

        prompt_text = f"""
You are a helpful assistant that converts natural language inventory instructions
into simple, direct SQL queries for SQLite.

Table: Inventory
Columns:
- "item no" INTEGER PRIMARY KEY AUTOINCREMENT
- item_name TEXT (must match exactly: Potato, Tomato, Onion, Carrot, Apple)
- quantity INTEGER

Instructions:
1. For simple commands like 'add N ITEM' or 'remove N ITEM', generate minimal SQL:
   - Use UPDATE to increment/decrement quantity of existing items.
   - Only use INSERT if the item does not exist.
2. For 'update ITEM to N', set quantity to N.
3. For 'show all items', generate SELECT * FROM Inventory.
4. Only generate multiple statements if multiple commands are given (use semicolons).
5. Do NOT generate unnecessary JOINs, CASE statements, or complex queries for simple instructions.
6. Use exact column names and make statements SQLite-compatible.
7. Return SQL statements that directly update the database. No explanations.

User Instruction: "{user_instruction}"
"""

        # Ollama generate requires list of prompts
        llm_result = llm_model.generate([prompt_text])
        raw_sql = llm_result.generations[0][0].text.strip()

        # Convert INSERT to UPSERT
        sql_lines = []
        for line in raw_sql.splitlines():
            line = line.strip()
            if line.upper().startswith(("INSERT", "UPDATE", "DELETE", "SELECT")):
                if line.upper().startswith("INSERT"):
                    m = re.match(r"INSERT INTO Inventory \(item_name, quantity\) VALUES \('(.+?)',\s*(\d+)\);?", line, re.IGNORECASE)
                    if m:
                        item, qty = m.group(1), m.group(2)
                        line = f"INSERT INTO Inventory (item_name, quantity) VALUES ('{item}', {qty}) ON CONFLICT(item_name) DO UPDATE SET quantity = quantity + {qty}"
                sql_lines.append(line)
        sql_query = ";\n".join(sql_lines) + ";"

        st.success("SQL Query Generated:")
        st.code(sql_query, language="sql")

        # Execute SQL safely
        try:
            c.executescript(sql_query)
            st.session_state.conn.commit()

            c.execute('SELECT "item no", item_name, quantity FROM Inventory')
            updated_data = c.fetchall()
            st.info(" Updated Inventory:")
            st.dataframe(pd.DataFrame(updated_data, columns=["Item No", "Item Name", "Quantity"]))

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

    except Exception as e:
        st.error(f" LLM Error: {e}")





