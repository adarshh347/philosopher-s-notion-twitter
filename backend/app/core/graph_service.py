from typing import TypedDict, Literal, List, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


# brain state
class AgentState(TypedDict):
    messages: List[Any]  # Chat history
    user_query: str  # The raw latest input
    detected_intent: str  # "philosophical", "casual", "historical"
    active_lenses: List[str]  # e.g. ["existentialist", "poetic"]
    final_response: str

# node A: router Node
def router_node(state: AgentState):
    # We use a smaller/faster model for routing if possible, but 70b is fast on Groq too.
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    prompt = f"""
    Analyze this user message: "{state['user_query']}"
    Classify intent (philosophical/casual/historical).
    Suggest 1-2 'lenses' to apply to the persona (e.g., poetic, angry, logical, abstract).
    Return format: INTENT: <intent> | LENSES: <lens1>,<lens2>
    """

    try:
        result = llm.invoke(prompt).content
        # Simple parsing logic
        intent = result.split("|")[0].split(":")[1].strip()
        lenses = result.split("|")[1].split(":")[1].strip().split(",")
    except:
        # Fallback if LLM format fails
        intent = "casual"
        lenses = ["helpful"]

    print(f"🔀 [Groq] Routing: Intent={intent}, Lenses={lenses}")

    return {"detected_intent": intent, "active_lenses": lenses}


# 3. Node B: The Assembler (The Alchemist)
def assembler_node(state: AgentState):
    lens_prompts = {
        "poetic": "Speak in metaphors. Use imagery of nature and water.",
        "logical": "Be rigorous. Use numbered arguments and syllogisms.",
        "abstract": "Focus on the void and the formless. Be vague but profound.",
        "existentialist": "Focus on the suffering and burden of choice.",
        "helpful": "Be kind and direct."
    }

    # Core Persona
    system_prompt = "You are Adi Shankara. You believe in Advaita Vedanta (Non-duality).\n"

    # Inject Lenses
    for lens in state['active_lenses']:
        cleaned_lens = lens.strip().lower()
        if cleaned_lens in lens_prompts:
            system_prompt += f"CURRENT MOOD: {lens_prompts[cleaned_lens]}\n"

    system_prompt += "REFERENCE: You remember discussing 'The Blue Illusion' previously."

    return {"messages": [SystemMessage(content=system_prompt)]}


# 4. Node C: The Generator (The Speaker)
def generator_node(state: AgentState):
    # Using a slightly higher temperature for creativity
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6)

    messages = state['messages'] + [HumanMessage(content=state['user_query'])]

    response = llm.invoke(messages)

    return {"final_response": response.content}


# 5. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("assembler", assembler_node)
workflow.add_node("generator", generator_node)

workflow.set_entry_point("router")

workflow.add_edge("router", "assembler")
workflow.add_edge("assembler", "generator")
workflow.add_edge("generator", END)

app_brain = workflow.compile()

