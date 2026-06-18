# ⚕️ Medical Report Q&A — RAG System

> Ask questions about your medical test results in plain English. Get instant, cited, safe answers — powered by RAG + Groq LLM.

🔗 **[https://medical-a2lx4bgjn-puja-rani-bhuyan-s-projects.vercel.app/](#)** · 👩‍💻 **[Puja Rani Bhuyan](https://github.com/pujaux)**

---

## 📸 Preview
<img width="1366" height="638" alt="Screenshot (2767)" src="https://github.com/user-attachments/assets/6ecf8ce1-a6e8-4761-b007-018c589f905d" />

<img width="1366" height="643" alt="Screenshot (2769)" src="https://github.com/user-attachments/assets/a50fee3c-524e-4a09-9845-b963613a45fb" />

<img width="1366" height="647" alt="Screenshot (2770)" src="https://github.com/user-attachments/assets/45b00579-22a3-4805-8ea6-ce42c36c7038" />

---

## 🤔 The Problem

Most people in India receive lab reports filled with numbers they don't understand — *"Hemoglobin: 10.2 g/dL"* or *"TSH: 6.8 mIU/L"* — without any explanation. Doctor consultations are expensive, time-consuming, and often unavailable in rural areas. This project bridges that gap by explaining what your test results mean in plain language, for free, instantly.

---
## 📁 Project Structure

```
medical-rag/
├── backend/
│   ├── api.py                  # FastAPI server — main entry point
│   ├── rag_pipeline.py         # Core RAG: retrieve + generate answer
│   ├── safety_layer.py         # Blocks dangerous queries
│   ├── embedder.py             # Embeds chunks into FAISS index
│   ├── chunker.py              # Splits documents into 500-char chunks
│   ├── pdf_loader.py           # Loads medical text files
│   ├── create_data.py          # Creates medical reference documents
│   ├── evaluation.py           # Custom evaluation framework
│   ├── app.py                  # Streamlit UI (prototype version)
│   ├── faiss_index.bin         # Saved FAISS vector index
│   └── chunks_metadata.pkl     # Chunk metadata (source, category)
├── frontend/
│   ├── src/
│   │   ├── App.js              # Main React chat interface
│   │   └── index.css           # Tailwind CSS imports
│   ├── tailwind.config.js
│   └── package.json
├── data/
│   ├── blood_tests/            # CBC, glucose, ferritin references
│   ├── hormones/               # Thyroid (TSH) reference
│   └── urine_tests/            # Urinalysis reference
├── .gitignore
└── README.md
```
---

## ✨ Features

- 💬 Ask plain-language questions about blood tests, urine tests, and hormone results
- 📚 Every answer is grounded in **NIH / MedlinePlus** references — not hallucinated
- 🔒 Two-layer safety system blocks diagnosis and medication questions
- 📌 Sources shown alongside every answer so you can verify
- ⚡ Fast retrieval using FAISS vector search

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Tailwind CSS |
| Backend | FastAPI + Python |
| Vector Search | FAISS (Facebook AI) |
| Embeddings | all-MiniLM-L6-v2 (Sentence Transformers) |
| LLM | Groq API — Llama 3.3 70B (free tier) |
| Deployment | Vercel (frontend) + Railway (backend) |

---

## 🏗️ How It Works

```
User Question
     ↓
Safety Layer — blocks dangerous queries instantly
     ↓  (if safe)
FAISS retrieves top 3 relevant chunks from medical documents
     ↓
Groq LLM generates a cited answer from those chunks only
     ↓
Answer + Sources shown to user
```

This is **RAG (Retrieval-Augmented Generation)** — the LLM only uses what is retrieved from trusted documents, not its own memory. This prevents hallucination, which is critical in a medical context.

---

## 📄 Why Only 5 Documents?

This is a deliberate design choice, not a limitation.

The knowledge base covers the **5 most common lab tests** people ask about: CBC (blood count), blood glucose, ferritin, thyroid (TSH), and urinalysis. Here's why I kept it focused:

- **Quality over quantity** — with 5 well-curated documents, every retrieval is relevant. Adding 50 loosely-related PDFs makes retrieval noisy and answers worse.
- **Verified sources only** — all documents come from NIH and MedlinePlus (public domain). No random health websites that could introduce misinformation.
- **Easy to extend** — add any `.txt` file to the `data/` folder and re-run `chunker.py` + `embedder.py`. The system scales automatically.

---

## 🛡️ Safety System

Medical AI without guardrails is dangerous. This project uses two layers:

**Layer 1 — Keyword filter:** Instantly blocks queries asking for diagnosis, medication, or treatment — before the LLM is ever called. Fast, free, and reliable.

**Layer 2 — LLM system prompt:** Even if a query passes the filter, the LLM is instructed to never diagnose, never recommend medicine, and always end with a doctor consultation reminder.

**Result: 100% safety accuracy** on adversarial test cases.

---

## 📊 Evaluation

Built a custom evaluation framework (RAGAS was incompatible with Python 3.14).

| Metric | Score | Description |
|---|---|---|
| Retrieval Accuracy | 80% | Correct category retrieved for 4/5 test questions |
| Safety Accuracy | 100% | All 5 adversarial queries handled correctly |

---

## ⚠️ Known Limitations

- Covers 5 test types only — questions outside this scope get weaker answers
- English only — Hindi/regional language support not yet added
- Not clinically validated — for educational use only

---

## 🔭 Future Scope

- Add more test categories: lipid panel, liver function, kidney function, vitamin panels
- Hindi query support using IndicTrans translation layer
- RAGAS evaluation once Python 3.14 compatibility resolves
- Confidence score display so users know when an answer is uncertain

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/pujaux/medical-rag.git
cd medical-rag

# 2. Backend setup
cd backend
pip install fastapi uvicorn groq python-dotenv faiss-cpu sentence-transformers pdfplumber
echo "GROQ_API_KEY=your_key_here" > .env
python create_data.py
python chunker.py
python embedder.py
python -m uvicorn api:app --port 8000

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm start
```

Open `http://localhost:3000` — make sure the backend is running first.

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.

---

## 👩‍💻 Author

**Puja Rani Bhuyan**  
B.Tech Computer Science (AI/ML)  · 2027  
[GitHub](https://github.com/pujaux) · [LinkedIn](https://linkedin.com/in/pujaux)

---

> ⚠️ **Disclaimer:** This tool is for educational purposes only. It does not diagnose conditions, recommend medication, or replace professional medical advice. Always consult a qualified doctor.
