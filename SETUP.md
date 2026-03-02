# Quick Setup

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure API Keys

Copy `.env.example` to `.env` and add your keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_groq_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional
```

## 3. Run

```bash
python -m streamlit run app.py
```

## 4. Test

1. Upload a PDF
2. Ask questions:
   - Simple: "What is the revenue?"
   - Complex: "Compare Q1 vs Q4 revenue"
3. Check "Agent Reasoning Trace" to see how it works

## Troubleshooting

**Module not found:**
```bash
pip install --upgrade -r requirements.txt
```

**Streamlit not found:**
```bash
pip install streamlit
python -m streamlit run app.py
```
