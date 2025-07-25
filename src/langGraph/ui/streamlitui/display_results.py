import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
from src.langGraph.state.state import State
import json
import uuid

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message,thread_id):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message
        self.thread_id=thread_id

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase =="Basic ChatBot":
                # state = State(messages=[("user", self.user_message)])
                state = State(messages=st.session_state["chat_history"] + [HumanMessage(content=self.user_message)])
                print("THREAD ID USED:", self.thread_id)
                with st.chat_message("user"):
                    st.write(self.user_message)
                
                for event in self.graph.stream(
                    state,
                    config={
                        "configurable": {
                            "thread_id": self.thread_id
                        }
                    }
                    ):
                    # print(event.values())
                    for value in event.values():
                        st.session_state["chat_history"].append(AIMessage(content=value["messages"].content))
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)
                        
                                