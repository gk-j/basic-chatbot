import streamlit as st 

from src.langGraph.ui.streamlitui.loadui import LoadStreamLitUI
from src.langGraph.llms.groqllm import GroqLLM
from src.langGraph.graph.graph_builder import GraphBuilder
from src.langGraph.ui.streamlitui.display_results import DisplayResultStreamlit
from langchain_core.messages import HumanMessage,AIMessage

def load_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.

    """
    ###load_ui
    ui=LoadStreamLitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from ui")
        return
    
    # Initialize thread_id if not already
    if "thread_id" not in st.session_state:
        import uuid
        st.session_state["thread_id"] = str(uuid.uuid4())
    
    # Initialize chat history
    st.session_state.setdefault("chat_history", [])
    
    
    print("chat_history:", st.session_state.get("chat_history"))
    # Display prior messages
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)
    
    user_message = st.chat_input("Enter the messsage:")

    if user_message:
        try:
            
            st.session_state["chat_history"].append(HumanMessage(content=user_message))

            ### CONFIGURE THE LLM
            llm_config = GroqLLM(user_controls_input=user_input)
            model= llm_config.get_llm_model()

            if not model:
                st.error('Error: LLM model could not be initialized')
                return

            ## Initialize and setup the graph based on use case
            usecase=user_input["USE_CASE_OPTIONS"]
            st.write("Selected usecase:", usecase)

            if not usecase:
                st.error("Error 1: No use case selected.")
                return
            
            ##GraphBuilder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase=usecase)
                DisplayResultStreamlit(usecase,graph,user_message,thread_id=st.session_state["thread_id"]).display_result_on_ui()
            except Exception as e:
                st.error(f"Error 2: graph set up failed - {e}")
                return

        except Exception as e:
            st.error(f"Error 3: graph set up failed - {e}")
            return

    