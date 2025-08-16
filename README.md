# Tirukural Chatbot — RAG + Streamlit

This project turns your Kaggle dataset (Thirukural + translations + explanations) into a **chatbot** with four modes:

1) **Kural Lookup**
   - By number, by first words, or by theme.
2) **Theme-based Inspiration**
3) **Conversational Advice**
4) **Kural in Context** (apply to a modern scenario)

The app supports two paths:

- **With OpenAI API key**: Uses GPT to craft beautiful, contextual answers.
- **No API key**: Falls back to a templated response using the dataset (still works!).

---

## Quick Start (VS Code, ~10–15 minutes)

### 0) Get the data ready
Place your Kaggle file **`Thirukural With Explanation.csv`** (or the zip that contains it) into the `data/` folder.  
If you have the Kaggle ZIP, simply drop it in `data/` (the app will auto-extract the needed CSV on first run).

### 1) Create & open the project
- Open **VS Code**
- Click **File → Open Folder...**, select this folder: `tirukural_chatbot`
- On the left sidebar, click the **Extensions** icon (four squares), search **“Python”**, install the **Python** extension by Microsoft.

### 2) Create a virtual environment (recommended)
- Click the **Terminal** icon in VS Code (or use `Ctrl+` backtick) → **New Terminal**.
- Run:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) (Optional) Enable LLM responses
- Copy `.env.example` to `.env`
- Paste your OpenAI key: `OPENAI_API_KEY=...`
- You can keep `OPENAI_MODEL=gpt-4o-mini` (or change to any available model).

### 5) Run the app
```bash
streamlit run app/streamlit_app.py
```
- A browser tab opens automatically. If not, click the local URL shown.

### 6) Use the four modes
- In the left sidebar, choose **Mode**. Try queries like:
  - **Lookup by number**: `312`
  - **Lookup by first words**: `இன்னா`
  - **Lookup by theme**: `friendship`
  - **Inspiration**: `self-control`
  - **Conversational**: _"I feel betrayed by a friend"_
  - **Context**: _"Should I forgive someone who cheated me?"_

---

## Repo layout

```
tirukural_chatbot/
├── app/
│   ├── streamlit_app.py     # UI + orchestration
│   ├── engine.py            # retrieval + formatting
│   ├── indexer.py           # index building + auto-extracts the CSV from zip
│   ├── llm.py               # OpenAI interface + graceful fallback
│   ├── prompts.py           # system prompts
│   └── utils.py             # text cleaning
├── data/                    # put your Kaggle zip or CSV here
│   └── PLACE_YOUR_DATA_HERE.txt
├── index/                   # created on first run
├── requirements.txt
├── .env.example
└── README.md
```

> If you want to start **super fast**, you can also run just `streamlit_app.py` — it will auto-build the index on first run.

---

## Troubleshooting

- **No data found?** Ensure `data/Thirukural With Explanation.csv` exists, or a zip containing it is in `data/`.
- **Tamil text has tabs/odd spacing**: The app cleans stray `\t` and extra spaces automatically.
- **No OpenAI key**: The app still works, but responses are simpler (templated from the dataset).

Enjoy! ✨
