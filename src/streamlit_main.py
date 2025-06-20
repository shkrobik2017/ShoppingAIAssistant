import asyncio
import streamlit as st

from src.db.db_setup import DB
from src.llm.graph import graph
from src.llm.graph_schema import AgentState

st.set_page_config(page_title="🛒 Grocery AI Assistant", page_icon="🛒")
st.title("🛒 Grocery Shopping Assistant")
st.markdown("Enter what you want to prepare and specify your budget. The assistant will create a shopping list.")

user_input = st.text_input("What do you want to buy?", placeholder="For example: Dinner for 4 people")
budget = st.number_input("Maximum budget (USD)", min_value=1, value=25, step=1)


async def generate_state(*, input_content: str, user_budget: int):
    """
    Generate a shopping list by invoking the multi-agent graph.

    Args:
        input_content (str): The description of what the user wants to buy.
        user_budget (int): The maximum budget allowed for the shopping list.

    Returns:
        AgentState: The final state of the multi-agent graph, including the final message.
    """
    await DB.init_orm()
    try:
        initial_state: AgentState = {
            "user_input": input_content,
            "budget": user_budget
        }
        graph_result = await graph.ainvoke(initial_state)
    finally:
        await DB.close_orm()
    return graph_result


def main() -> None:
    """
    Main logic to handle Streamlit UI interaction and trigger the graph.
    """
    if st.button("Generate shopping list"):
        with st.spinner("Generating list..."):
            try:
                result = asyncio.run(generate_state(input_content=user_input, user_budget=budget))
                final_message = result.get("final_message", "No final message generated.")
                st.success("Shopping list ready!")
                st.subheader("🧾 Final shopping list:")
                st.markdown(final_message)
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()


