import subprocess
from typing import List


class OllamaService:
    def __init__(self):
        """initialize the ollama service."""
        self.models = []
        self.refresh_models()
    
    def refresh_models(self) -> None:
        """Refresh the list of available models."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=True
            )
            
            
            lines = result.stdout.strip().split('\n')
            if len(lines) <= 1:  # Only header, no models
                self.models = []
                return
            
            model_lines = lines[1:]
            
            # get model names 
            models = []
            for line in model_lines:
                if line.strip():  # ignore empty lines
                    # get model name from the line
                    model_name = line.strip().split()[0]
                    models.append(model_name)
            
            self.models = models
        except subprocess.SubprocessError:
            # handle the case where ollama is not running or installed
            self.models = []
    
    def get_models(self) -> List[str]:
        """get the list of available models."""
        return self.models
    
    def generate_response(self, model: str, prompt: str, context: str = "") -> str:
        """
        generate a response using the specified ollama model.
        
        args:
            model: The name of the Ollama model to use
            prompt: The user prompt to send to the model
            context: Optional context from previous messages
            
        returns:
            the model's response as a string
        """
        try:
            # prepare the complete prompt with context if provided
            full_prompt = f"{context}\nUser: {prompt}\nAssistant:"
            cmd = ["ollama", "run", model, full_prompt]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            response = result.stdout.strip()
            
            if context and response.startswith(context):
                response = response[len(context):].strip()
            if response.startswith(f"User: {prompt}"):
                response = response[len(f"User: {prompt}"):].strip()
            if response.startswith("Assistant:"):
                response = response[len("Assistant:"):].strip()
            
            return response
        except subprocess.SubprocessError as e:
            return f"Error generating response: {str(e)}"