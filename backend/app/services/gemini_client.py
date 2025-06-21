from google import genai
from app.config.settings import settings

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"
    
    async def generate_content(self, prompt: str) -> str:
        """Generate content using Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate_json(self, prompt: str) -> dict:
        """Generate JSON response using Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return {"content": response.text.strip()}
        except Exception as e:
            return {"error": str(e)} 