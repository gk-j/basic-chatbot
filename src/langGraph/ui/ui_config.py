from configparser import ConfigParser

class Config:

    def __init__(self,config_file="./src/langGraph/ui/ui_config.ini"):
        ## Reading the config file
        self.config = ConfigParser()
        self.config.read(config_file)
    
    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_usecase_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")

# onfig = Config() 
# print(onfig.get_groq_model_options())
# print(onfig.get_llm_options())
# print(onfig.get_usecase_options())
# print(onfig.get_title())
