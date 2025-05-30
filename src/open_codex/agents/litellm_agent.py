from typing import List, Dict
import logging
import litellm

from open_codex.interfaces.llm_agent import LLMAgent

# Configure logger ?
logger = logging.getLogger(__name__)

class LiteLLMAgent(LLMAgent):
    """
    Agent that connects to LiteLLM to access language models 
    using the official Python client.
    """
    
    def __init__(self, 
                 system_prompt: str,
                 model_name: str,
                 api_base: str,
                 api_key: str = None,
                 temperature: float = 0.2,
                 max_tokens: int = 500):
        """
        Initialize the LiteLLM agent.
        
        Args:
            system_prompt: The system prompt to use for generating responses
            model_name: The name of the model to use
            api_base: The base URL of the LiteLLM API
            api_key: The API key for authentication (optional)
            temperature: The temperature to use for generation (default: 0.2)
            max_tokens: The maximum number of tokens to generate (default: 500)
        """
        self.system_prompt = system_prompt
        self.model_name = model_name
        self.api_base = api_base
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _check_litellm_available(self) -> None:
        """Check if LiteLLM server is available and the model exists."""
        try:
            # 这里假设 litellm 有类似 list_models 的方法，若无可省略
            # models = litellm.list_models(api_base=self.api_base, api_key=self.api_key)
            # available_models = [model['id'] for model in models]
            # if self.model_name not in available_models:
            #     logger.error(f"Model '{self.model_name}' not found in LiteLLM. Available models: {', '.join(available_models)}")
            #     raise ValueError(f"Model '{self.model_name}' not found in LiteLLM.")
            pass  # LiteLLM 可能没有模型列表接口，可省略此检查
        except Exception as e:
            logger.error(f"Could not connect to LiteLLM server at {self.api_base}.")
            raise ConnectionError(f"Could not connect to LiteLLM server at {self.api_base}: {str(e)}")

    def one_shot_mode(self, user_input: str) -> str:
        """
        Generate a one-shot response to the user input.
        
        Args:
            user_input: The user's input prompt
            
        Returns:
            The generated response as a string
        """
        self._check_litellm_available()
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        response = self._generate_completion(messages)
        return response.strip()

    def _generate_completion(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a completion using the LiteLLM API.
        
        Args:
            messages: The conversation history as a list of message dictionaries
            
        Returns:
            The generated text response
        """
        try:
            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                api_base=self.api_base,
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            if "choices" in response and response["choices"]:
                return response["choices"][0]["message"]["content"]
            else:
                raise ValueError(f"Unexpected response format from LiteLLM API: {response}")
        except Exception as e:
            raise ConnectionError(f"Error communicating with LiteLLM: {str(e)}")