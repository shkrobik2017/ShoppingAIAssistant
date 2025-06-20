from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.llm.graph_schema import AgentState
from src.llm.agents.budgeting.budgeting import BudgetingAgent
from src.llm.agents.finalizer.finalizer import FinalizerAgent
from src.llm.agents.planner.planner import PlannerAgent
from src.llm.agents.product_finder.product_finder import ProductFinderAgent
from src.llm.agents.recipe.recipe import RecipeAgent
from src.llm.agents.supervisor.supervisor import SupervisorAgent

def build_graph() -> CompiledStateGraph:
    """
    Build and compile the LangGraph multi-agent state graph.

    Returns:
        StateGraph: The compiled state graph ready for execution.
    """
    builder = StateGraph(state_schema=AgentState)

    builder.add_node("Planner", PlannerAgent().generate)
    builder.add_node("Recipe", RecipeAgent().generate)
    builder.add_node("ProductFinder", ProductFinderAgent().generate)
    builder.add_node("Budgeting", BudgetingAgent().generate)
    builder.add_node("Finalizer", FinalizerAgent().generate)
    builder.add_node("Supervisor", SupervisorAgent().generate)

    builder.set_entry_point("Supervisor")
    builder.set_finish_point("Finalizer")

    builder.add_conditional_edges(
        source="Supervisor",
        path=lambda state: state.get("__next__"),
        path_map={
            "Planner": "Planner",
            "Recipe": "Recipe",
            "ProductFinder": "ProductFinder",
            "Budgeting": "Budgeting",
            "Finalizer": "Finalizer"
        }
    )

    builder.add_edge("Planner", "Supervisor")
    builder.add_edge("Recipe", "Supervisor")
    builder.add_edge("ProductFinder", "Supervisor")
    builder.add_edge("Budgeting", "Supervisor")

    return builder.compile()

graph = build_graph()
