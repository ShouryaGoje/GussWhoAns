
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

class Recipe(BaseModel):
    Question_num: int
    Question: str
    Example: list[str]


class getQ:
    def __init__(self):
        
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.PROMPT = os.getenv("PROMPT")
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self.PROMPT = self.PROMPT.replace('[X]', '10').replace('[Y]','50%')
        self.client = genai.Client(api_key=self.API_KEY)
    def get(self):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=self.PROMPT, config={
                "response_mime_type": "application/json",
                "response_schema": list[Recipe],
            }
        )
        return(response.text)\


if __name__ == "__main__":
    pass