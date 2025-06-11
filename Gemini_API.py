import google.generativeai as genai
from configuracion import GEMINI_API_KEY

class GeminiChat:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash")


    def ask(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
