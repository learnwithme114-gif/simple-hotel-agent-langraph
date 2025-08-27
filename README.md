# 🏨 Simple Hotel Agent (LangGraph)

A tiny **LangGraph** agent that suggests **exactly 3 hotels** as
**Pydantic-validated JSON**.\
Perfect first project for agent basics: clear flow, strict schema, and
easy to extend.

------------------------------------------------------------------------

## ✨ What you get

-   **One-node graph:** `START → hotels → END`
-   **Schema-first output** with Pydantic (predictable JSON)
-   **Local console tracing** (no cloud; toggle with `TRACE_LEVEL`)
-   **Model switch** via `OPENAI_MODEL` (e.g., `gpt-4o-mini`,
    `gpt-5-nano` *if available on your account*)

``` mermaid
flowchart LR
  START((START)) --> H[hotels node]
  H --> END((END))
```

------------------------------------------------------------------------

## 🧱 Project structure

    simple-hotel-agent-langraph/
    ├─ hotel_agent.py
    ├─ requirements.txt
    ├─ .env.example
    └─ README.md

------------------------------------------------------------------------

## 🧩 Tech stack

-   **LangGraph** → agent flow orchestration
-   **LangChain OpenAI** → OpenAI chat model wrapper
-   **Pydantic** → strict schema validation
-   **python-dotenv** → loads environment variables from `.env`

> Requires **Python 3.10+**

------------------------------------------------------------------------

## 🔐 Create your OpenAI API key

1.  Go to **[OpenAI API
    Keys](https://platform.openai.com/account/api-keys)**.
2.  Sign in and click **Create new secret key**.
3.  Copy your key and **keep it safe**.
4.  In this project, create a `.env` file (or copy `.env.example`) and
    add:

``` env
OPENAI_API_KEY=sk-...yourkey...

# optional: choose a model for this repo
# OPENAI_MODEL=gpt-4o-mini       # default if not set
# OPENAI_MODEL=gpt-5-nano        # use if available on your account

# optional: local tracing level
# 0 = off, 1 = basic, 2 = verbose (shows prompt)
TRACE_LEVEL=1
```

> 💡 Thanks to **python-dotenv**, you don't need to export keys
> globally; just keep them in `.env`.\
> 🛡️ Make sure `.env` is in `.gitignore` --- never commit secrets.

------------------------------------------------------------------------

## ⚙️ Setup

``` bash
git clone https://github.com/<you>/simple-hotel-agent-langraph.git
cd simple-hotel-agent-langraph
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env and paste your OPENAI_API_KEY
```

------------------------------------------------------------------------

## ▶️ Run the agent

``` bash
python hotel_agent.py
```

The script prompts you for: - **City** (e.g. `Paris`) - **Check-in
date** (e.g. `2025-10-12`) - **Nights** (e.g. `3`) - **Budget**
(e.g. `1500`)

Then it prints **validated JSON** with exactly 3 hotel suggestions.

------------------------------------------------------------------------

## 🔍 Local tracing (no cloud)

Console tracing is built in.

-   **Basic tracing (default):**

    ``` bash
    python hotel_agent.py
    ```

-   **Verbose (shows prompt too):**

    ``` bash
    # macOS/Linux
    TRACE_LEVEL=2 python hotel_agent.py

    # Windows PowerShell
    $env:TRACE_LEVEL="2"; python hotel_agent.py
    ```

-   **Disable tracing:**

    ``` bash
    # macOS/Linux
    TRACE_LEVEL=0 python hotel_agent.py

    # Windows PowerShell
    $env:TRACE_LEVEL="0"; python hotel_agent.py
    ```

**Pick a model (optional):**

``` bash
# macOS/Linux
OPENAI_MODEL=gpt-5-nano python hotel_agent.py

# Windows PowerShell
$env:OPENAI_MODEL="gpt-5-nano"; python hotel_agent.py
```

------------------------------------------------------------------------

## 🧾 Example JSON output

``` json
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
    {
      "name": "Grand Luxe Hotel",
      "neighborhood": "Champs-Élysées",
      "price_per_night_usd": 350,
      "total_estimated_usd": 1050,
      "pros": ["luxury amenities", "near attractions", "free breakfast"]
    },
    {
      "name": "BudgetStay Paris",
      "neighborhood": "Montmartre",
      "price_per_night_usd": 120,
      "total_estimated_usd": 360,
      "pros": ["affordable", "good transport links", "friendly staff"]
    }
  ]
}
```

------------------------------------------------------------------------

## 🧠 How it works

-   **Pydantic models** define the **output contract** (3 hotels,
    budget-respecting totals).
-   **Graph state** (`GraphState`) = shared data passed between nodes.
-   **Single node** (`hotel_agent`) → reads state → calls OpenAI →
    validates schema → returns updated state.
-   **Graph edges** = execution order: `START → hotels → END`.
-   **Tracing** = local console output showing inputs, prompt
    (optional), and summary of results.

------------------------------------------------------------------------

## 🛠️ Troubleshooting

-   **Auth error** → Make sure `.env` has a valid `OPENAI_API_KEY`.
-   **Model not found** → Remove `OPENAI_MODEL` or set a supported one
    (`gpt-4o-mini`).
-   **Schema errors** → Keep `temperature=0` and use
    `with_structured_output(...)`.

