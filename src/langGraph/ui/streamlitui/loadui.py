import streamlit as st
import os 

from src.langGraph.ui.ui_config import Config


class LoadStreamLitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_title(),layout='wide')
        st.header(self.config.get_title())

        with st.sidebar:
            # Get options
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM Selection
            self.user_controls["select_llm"]= st.selectbox("Select LLM",llm_options)

            if self.user_controls["select_llm"]=="Groq":
                # Model Selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state['GROQ_API_KEY']=st.text_input("API_KEY",type="password")

                #Validate GROQ_API
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your groq_api_key to proceed")
            
            # Usecase options
            self.user_controls["USE_CASE_OPTIONS"]= st.selectbox("Select Usecase",usecase_options)
        
        return self.user_controls
    
# load= LoadStreamLitUI()
# print(load.load_streamlit_ui())