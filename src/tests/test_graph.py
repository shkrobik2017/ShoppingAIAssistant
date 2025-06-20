import pytest
import pytest_asyncio

from src.db.db_setup import DB
from src.llm.graph import build_graph
from src.llm.graph_schema import AgentState


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_teardown():
    """
    Session-wide fixture to initialize and close shared resources like DB and Redis.
    """
    await DB.init_orm()
    yield
    await DB.close_orm()


@pytest_asyncio.fixture
async def graph():
    """
    Fixture to build and return a compiled LangGraph instance.
    """
    return build_graph()


@pytest.mark.asyncio
async def test_graph_structure(graph):
    """
    Verify that the graph contains all expected nodes.
    """
    node_names = set(graph.get_graph().nodes.keys())
    expected_nodes = {"Planner", "Recipe", "ProductFinder", "Budgeting", "Finalizer", "Supervisor"}
    missing_nodes = expected_nodes - node_names

    assert not missing_nodes, f"Graph is missing expected nodes: {missing_nodes}"


@pytest.mark.asyncio
async def test_graph_execution_with_minimal_state(graph):
    """
    Run the graph with minimal valid input and ensure it generates a final message.
    """
    initial_state = AgentState(user_input="Prepare a simple dinner", budget=50)
    result = await graph.ainvoke(initial_state)

    assert "final_message" in result, "Graph did not produce a final message."
    assert isinstance(result["final_message"], str), "Final message should be a string."


@pytest.mark.asyncio
async def test_graph_budget_retry_logic(graph):
    """
    Test that retry logic activates when the budget is insufficient.
    """
    initial_state = AgentState(user_input="Expensive meal", budget=1)
    result = await graph.ainvoke(initial_state)

    assert "final_message" in result, "Graph did not produce a final message."
    assert (
        result.get("retry_attempts", 0) >= 1 or result.get("within_budget") is False
    ), "Retry logic did not trigger as expected."
