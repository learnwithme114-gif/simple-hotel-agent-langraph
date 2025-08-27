import json
import os
import time
from typing import List, TypedDict

from dotenv import load_dotenv
from pydantic import BaseModel, Field, conint, constr
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

load_dotenv()  # reads OPENAI_API_KEY from .env

# ========= Console tracing (no cloud) =========
TRACE_LEVEL = int(os.getenv("TRACE_LEVEL", "1"))  # 0=off, 1=basic, 2=verbose (shows full prompt)

COLORS = {
    "gray": "\033[90m",
    "cyan": "\033[36m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "reset": "\033[0m",
}

def log(level: int, msg: str = ""):
    if TRACE_LEVEL >= level:
        print(msg)

def color(c: str, s: str) -> str:
    return f"{COLORS.get(c,'')}{s}{COLORS['reset']}"

# ========= Pydantic output contract =========
class Hotel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    neighborhood: str
    price_per_night_usd: conint(ge=1)
    total_estimated_usd: conint(ge=1)
    pros: List[str] = Field(default_factory=list)

class HotelsResponse(BaseModel):
    city: str
    check_in: str
    nights: conint(ge=1)
    budget_total_usd: conint(ge=1)
    suggestions: List[Hotel] = Field(..., min_items=3, max_items=3)

# ========= LangGraph shared state =========
class GraphState(TypedDict):
    city: str
    check_in: str
    nights: int
    budget_total_usd: int
    hotels: HotelsResponse

# ========= Single-node agent =========
def hotel_agent(state: GraphState) -> GraphState:
    t0 = time.time()
    log(1, color("cyan", "\n▶ node:start  hotel_agent"))
    log(1, color("gray", f"   input → city={state['city']} | check_in={state['check_in']} | nights={state['nights']} | budget_total_usd={state['budget_total_usd']}"))

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # set OPENAI_MODEL=gpt-5-nano if you want
    llm = ChatOpenAI(model=model_name, temperature=0)
    structured = llm.with_structured_output(HotelsResponse)  # schema-validated output

    prompt = f"""
You are a travel assistant. Create exactly 3 hotel suggestions in {state['city']}
for a stay starting {state['check_in']} for {state['nights']} nights.
Ensure total_estimated_usd = price_per_night_usd * nights and it must not exceed {state['budget_total_usd']} USD total.
Prefer walkable areas, strong reviews, and price variety (value/mid/premium-but-within-budget).
Return JSON that strictly matches the schema.
"""
    if TRACE_LEVEL >= 2:
        log(2, color("yellow", "   prompt →"))
        for line in prompt.strip().splitlines():
            log(2, color("gray", "     " + line))

    result: HotelsResponse = structured.invoke(prompt)

    # summarize output (no hidden chain-of-thought—just the structured result)
    log(1, color("yellow", "   output summary →"))
    log(1, color("gray", f"     suggestions: {len(result.suggestions)}"))
    for i, h in enumerate(result.suggestions, 1):
        log(1, color("gray", f"       {i}. {h.name} ({h.neighborhood})  ${h.price_per_night_usd}/night  → total ${h.total_estimated_usd}"))

    log(1, color("green", f"✔ node:end    hotel_agent  ({time.time()-t0:.2f}s)"))
    return {**state, "hotels": result}

# ========= Wire graph: START → hotels → END =========
graph = StateGraph(GraphState)
graph.add_node("hotels", hotel_agent)
graph.add_edge(START, "hotels")
graph.add_edge("hotels", END)
app = graph.compile()

# ========= Tiny CLI =========
if __name__ == "__main__":
    print(color("gray", f"model={os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}  |  TRACE_LEVEL={TRACE_LEVEL}  (0=off,1=basic,2=verbose)"))

    city = input("City [Paris]: ").strip() or "Paris"
    check_in = input("Check-in [2025-10-12]: ").strip() or "2025-10-12"
    nights = int(input("Nights [3]: ").strip() or "3")
    budget = int(input("Budget total USD [1500]: ").strip() or "1500")

    out = app.invoke({
        "city": city,
        "check_in": check_in,
        "nights": nights,
        "budget_total_usd": budget,
    })

    print("\n=== Hotels (Structured JSON) ===")
    print(json.dumps(out["hotels"].model_dump(), indent=2))
