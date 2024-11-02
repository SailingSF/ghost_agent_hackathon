from openai import OpenAI
import google.generativeai as genai
import os
import json
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OpenAIAgent:

    def __init__(self, instructions: str, tools_list: list[dict], tools_map: dict, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model
        self.instructions = instructions
        self.tools_list = tools_list
        self.tools_map = tools_map
        self.messages = [{"role": "system", "content": instructions}]
    
    def add_message(self, prompt: str):

        self.messages.append(
            {"role": "user", "content": prompt}
        )

    def run_thread(self, tool_choice: str = "auto"):

        completion = self._get_completion(tool_choice = tool_choice)

        tool_calls = completion.choices[0].message.tool_calls
        while tool_calls:
            self.messages.append(completion.choices[0].message)  # extend conversation with assistant's reply
            # handle tool call
            completion = self._handle_tool_call(tool_calls)
            tool_calls = completion.choices[0].message.tool_calls
        
        # add completion to messages    
        self.messages.append(completion.choices[0].message)
        
        return completion.choices[0].message.content

    def run_message(self, prompt: str):
        self.add_message(prompt)
        self.run_thread()
        return self.messages[-1].content

    def _get_completion(self, tool_choice = "auto"):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools_list,
            tool_choice=tool_choice,
        )
        return completion
    
    def _handle_tool_call(self, tool_calls):
        # handles tool calls, submits data
        logger.info("last message led to %s tool calls", len(tool_calls))
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.tools_map[function_name]
            function_args = json.loads(tool_call.function.arguments)
            logger.info("CALL tool %s with %s", function_name, function_args)
            
            function_response_json: str
            try:
                function_response = function_to_call(**function_args)
                function_response_json = json.dumps(function_response)
            except Exception as e:
                function_response_json = json.dumps(
                    {
                        "error": str(e),
                    }
                )

            logger.info("tool %s responded with %s", function_name, function_response_json[:200])
            self.messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response_json,
                }
            )  # extend conversation with function response

        return self._get_completion()

class GeminiAgent:
    def __init__(self, instructions: str, tools_map: dict, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=os.environ["GOOGLE_GEMINI_API_KEY"])
        
        # Convert tools_map to the format Gemini expects
        tools = []
        for name, func in tools_map.items():
            tools.append({
                "function_declarations": [{
                    "name": name,
                    "description": func.__doc__ or "No description provided",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }]
            })
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=tools  # Pass the formatted tools
        )
        self.instructions = instructions
        self.chat = self.model.start_chat(
            enable_automatic_function_calling=True if tools else False
        )
        self.tools_map = tools_map

    def submit(self, message: str) -> str:
        """Submit a message to the agent and get a response"""
        try:
            logging.info(f"Sending message to Gemini: {message[:100]}...")
            response = self.chat.send_message(
                message,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.7
                )
            )
            
            logging.info(f"Got response from Gemini. Parts: {len(response.parts)}")
            
            # Check for function calls in all parts of the response
            function_calls = []
            for i, part in enumerate(response.parts):
                logging.info(f"Examining response part {i}: {part}")
                if hasattr(part, 'function_call'):
                    function_calls.append(part.function_call)
                    logging.info(f"Found function call: {part.function_call.name}")
            
            if function_calls:
                logging.info(f"Processing {len(function_calls)} function calls")
                return self._handle_tool_call(function_calls)
            
            logging.info(f"No function calls, returning text: {response.text[:100]}...")
            return response.text

        except Exception as e:
            logging.exception("Error in submit()")
            return f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"

    def _get_completion(self):
        """Get the latest response from the chat history"""
        try:
            last_message = self.chat.history[-1]
            if last_message.role == "model":
                return last_message.parts[0]
            return None
        except Exception as e:
            return f"Error getting completion: {str(e)}"

    def _handle_tool_call(self, tool_calls):
        """Handle multiple tool calls from the model"""
        responses = {}
        
        # Execute all tool calls
        for tool_call in tool_calls:
            function_name = tool_call.name
            logging.info(f"Processing tool call for function: {function_name}")
            
            if function_name not in self.tools_map:
                logging.error(f"Function {function_name} not found in tools_map!")
                continue
                
            function_to_call = self.tools_map[function_name]
            try:
                # Convert MapComposite to dict directly instead of using json.loads
                function_args = dict(tool_call.args)
                logging.info(f"Function args: {function_args}")
            except Exception as e:
                logging.error(f"Failed to parse function args: {tool_call.args}")
                logging.error(f"Error: {str(e)}")
                continue
            
            try:
                function_response = function_to_call(**function_args)
                logging.info(f"Function {function_name} response: {function_response}")
                responses[function_name] = function_response
            except Exception as e:
                logging.exception(f"Error calling function {function_name}")
                responses[function_name] = {"error": str(e)}

        try:
            # Build response parts for all tool calls
            response_parts = [
                {
                    "function_response": {
                        "name": fn_name,
                        "response": {"result": response}
                    }
                }
                for fn_name, response in responses.items()
            ]
            
            logging.info(f"Sending {len(response_parts)} response parts back to chat")
            response = self.chat.send_message(response_parts)
            return response.text

        except Exception as e:
            logging.exception("Error in _handle_tool_call while processing responses")
            return f"Error processing tool responses: {str(e)}"
