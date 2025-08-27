# 🏨 Simple Hotel Agent (LangGraph)

A tiny **LangGraph** agent that suggests **exactly 3 hotels** as **Pydantic-validated JSON**.  
Perfect first project for agent basics: clear flow, strict schema, and easy to extend.

---

## ✨ What you get
- **One-node graph:** `START → hotels → END`
- **Schema-first output** with Pydantic (predictable JSON)
- **Local console tracing** (no cloud, toggle with `TRACE_LEVEL`)
- **Model switch** via `OPENAI_MODEL` (e.g., `gpt-4o-mini`, `gpt-5-nano` *if available on your account*)

```

  START((START)) --> H[hotels node] H --> END((END))

🧱 Project structure


simple-hotel-agent-langraph/
├─ hotel_agent.py
├─ requirements.txt
├─ .env.example
└─ README.md

🧩 Stack

- LangGraph — agent flow orchestration

- LangChain OpenAI — chat model wrapper

- Pydantic — strict schema validation

- python-dotenv — loads your .env automatically

Requires Python 3.10+

🔐 Create your OpenAI API key (one-time)
Open platform.openai.com and sign in.

Click your profile → View API keys.

Click Create new secret key and copy it (store it somewhere safe).

In this project, create a file named .env (you can copy from .env.example) and paste your key:

env
Copy code
OPENAI_API_KEY=sk-...yourkey...

# optional: choose a model for this repo
# OPENAI_MODEL=gpt-4o-mini       # default if not set
# OPENAI_MODEL=gpt-5-nano        # use if available on your account

# optional: local tracing level (0=off, 1=basic, 2=verbose shows prompt)
# TRACE_LEVEL=1
💡 Thanks to python-dotenv, you don’t need to export the key globally; keeping it in .env is enough.
🛡️ Never commit .env to GitHub.

⚙️ Setup
bash
Copy code
git clone https://github.com/<you>/simple-hotel-agent-langraph.git
cd simple-hotel-agent-langraph
python3 -m venv .venv && source .venv/bin/activate   # Windows PowerShell:  .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env   # then edit .env and paste your OPENAI_API_KEY
▶️ Run
bash
Copy code
python hotel_agent.py
You’ll be prompted for inputs (defaults provided). The script prints validated JSON with exactly 3 hotel suggestions.

🔍 Local tracing (no cloud)
Console tracing is built in.

Basic (default):

bash
Copy code
python hotel_agent.py
Verbose (shows the actual prompt you sent):

bash
Copy code
TRACE_LEVEL=2 python hotel_agent.py           # macOS/Linux
# Windows (PowerShell)
$env:TRACE_LEVEL="2"; python hotel_agent.py
Off:

bash
Copy code
TRACE_LEVEL=0 python hotel_agent.py           # macOS/Linux
# Windows (PowerShell)
$env:TRACE_LEVEL="0"; python hotel_agent.py
Pick a model (optional):

bash
Copy code
OPENAI_MODEL=gpt-5-nano python hotel_agent.py   # if available on your account
# Windows (PowerShell)
$env:OPENAI_MODEL="gpt-5-nano"; python hotel_agent.py
🧾 Example output shape
json
Copy code
{
  "city": "Paris",
  "check_in": "2025-10-12",
  "nights": 3,
  "budget_total_usd": 1500,
  "suggestions": [
    {
      "name": "Hotel Example",
      "neighborhood": "Le Marais",
      "price_per_night_usd": 180,
      "total_estimated_usd": 540,
      "pros": ["walkable", "near cafes", "good reviews"]
    },
    { "...": "..." },
    { "...": "..." }
  ]
}
🧠 How it works (quick tour)
Pydantic models (Hotel, HotelsResponse) define the output contract (exact keys/types; 3 items).

Graph state (GraphState) is the small dict LangGraph passes between nodes.

Node (hotel_agent) reads state → calls the LLM with with_structured_output(HotelsResponse) → returns updated state.

Edges connect execution: START → hotels → END.

Tracing prints node start/end, (optional) prompt, and a summary of the structured result—purely local.

🛠️ Troubleshooting
Auth error: Ensure .env has a valid OPENAI_API_KEY.

Model not found: Remove OPENAI_MODEL or switch to a supported model (e.g., gpt-4o-mini).

Schema errors: Keep temperature=0 and the with_structured_output(...) line.