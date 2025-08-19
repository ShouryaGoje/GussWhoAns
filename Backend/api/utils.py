import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import List


class MyQuestions(BaseModel):
    Question_num: int
    Question: str
    Example: List[str]


class GetQ:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.PROMPT = os.getenv("PROMPT")
        self.client = genai.Client(api_key=self.API_KEY)

    def get(self, X=10, Y=0):
        # replace variables safely each call
        prompt = self.PROMPT.replace("[X]", str(X)).replace("[Y]", f"{Y}%")

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[MyQuestions],
            }
        )

        return response.text