from importlib.resources import files
import os
from open_codex.interfaces.llm_agent import LLMAgent

from dotenv import load_dotenv

# file path
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "resources", ".env")

load_dotenv(dotenv_path=dotenv_path)

class AgentBuilder:
    
    @staticmethod
    def get_system_prompt() -> str:
        return files("open_codex.resources") \
            .joinpath("prompt.txt") \
            .read_text(encoding="utf-8")
# plan to join the custom_prompt.txt to the system_prompt
    # @staticmethod
    # def get_phi_agent() -> LLMAgent:
    #     from open_codex.agents.phi_4_mini_agent import Phi4MiniAgent
    #     system_prompt = AgentBuilder.get_system_prompt()
    #     return Phi4MiniAgent(system_prompt=system_prompt)
    
    @staticmethod
    def get_ollama_agent(model: str, host: str) -> LLMAgent:
        from open_codex.agents.ollama_agent import OllamaAgent
        system_prompt = AgentBuilder.get_system_prompt()
        return OllamaAgent(system_prompt=system_prompt, 
                           model_name=model,
                           host=host)
    
    @staticmethod
    def get_litellm_agent() -> LLMAgent:
        from open_codex.agents.litellm_agent import LiteLLMAgent
        system_prompt = AgentBuilder.get_system_prompt()
        return LiteLLMAgent(system_prompt=system_prompt, 
                            model_name=os.environ['MODEL_NAME'],
                            api_base=os.environ['API_BASE'],
                            api_key=os.environ['API_KEY'],
                            extra_body=os.environ['EXTRA_BODY'])
    
    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
