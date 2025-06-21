from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel
from app.config.settings import settings
import json
import os

class VertexAIClient:
    def __init__(self):
        # Set API key for authentication
        if settings.GOOGLE_API_KEY:
            os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        
        # Initialize Vertex AI
        aiplatform.init(
            project=settings.GOOGLE_CLOUD_PROJECT_ID,
            location=settings.GOOGLE_CLOUD_LOCATION
        )
        self._model = None
    
    @property
    def model(self):
        if self._model is None:
            self._model = TextGenerationModel.from_pretrained("text-bison@001")
        return self._model
    
    async def generate_content(self, prompt: str) -> str:
        """Generate content using Vertex AI"""
        try:
            response = self.model.predict(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Vertex AI error: {str(e)}")
    
    async def generate_json(self, prompt: str) -> dict:
        """Generate JSON response using Vertex AI"""
        try:
            # Add JSON formatting instruction
            json_prompt = f"{prompt}\n\nReturn only valid JSON format."
            response = self.model.predict(json_prompt)
            
            # Try to parse JSON response
            try:
                return json.loads(response.text.strip())
            except json.JSONDecodeError:
                return {"content": response.text.strip()}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def analyze_with_context(self, context: str, question: str) -> dict:
        """Analyze with specific context"""
        prompt = f"""
        Context: {context}
        
        Question: {question}
        
        Provide a detailed analysis in JSON format.
        """
        return await self.generate_json(prompt) 