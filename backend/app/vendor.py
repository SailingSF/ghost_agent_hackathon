import os
import google.generativeai as genai
import typing_extensions as typing



class GeminiAgent:
    def __init__(self, model_name: str, system_prompt: str):
        self.api_key = os.environ["GOOGLE_GEMINI_API_KEY"]
        genai.configure(api_key=self.api_key)
        self.system_prompt = system_prompt
        self.model_name = model_name

    def reply(self, prompt: str, chat_history: list[dict]) -> str:
        model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_prompt)
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(
            prompt,
            generation_config = genai.GenerationConfig(
                max_output_tokens=250,
                temperature=0.3
            )
        )
        return response.text

    def reply_structured(self, prompt: str, chat_history: list[dict], response_schema) -> str:
        model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_prompt)
        response = model.generate_content(
            prompt,
            generation_config = genai.GenerationConfig(
                max_output_tokens=250,
                temperature=0.3,
                response_mime_type="application/json", response_schema=response_schema
            ),
            
        )
        return response

    