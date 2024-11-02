import google.generativeai as genai
import asyncio
import os

async def gemini_prompt(original_prompt: str) -> str:
    '''
    Take text of a prompt, use gemini to improve prompt
    '''
    api_key = os.environ["GOOGLE_GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    system_prompt = '''
        You take prompts for AI text to image models and improve them according to guidelines and examples, you respond with just the prompt.
        <guidelines>
        - Prompts should be detailed
        - Be descriptive and specific
        - Describe the foreground and background separately
        - Use artistic references
        - Specify technical details
        - Use contrast and juxtaposition
        - Incorporate mood and atmosphere
        - Ask to render short text if it makes sense, no more than 4 words
        </guidlines>
        <output_instructions>
        Respond with only the improved prompt and nothing else, responses should be less than 200 words.
        </output_instructions>
    '''
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)

    chat_history = [
        {"role": "user", "parts": "A group of frog men hanging out in front of a japanese convenience store admiring cool modified Japanese cars with underglow."},
        {"role": "model", "parts": "In the foreground, a group of anthropomorphic frog men are gathered, each wearing casual, trendy streetwear reminiscent of Tokyo fashion. They are animatedly interacting and holding drinks, illuminated by the neon glow of various vending machines and the flickering signs of the convenience store. The frog men have detailed, expressive faces showing admiration and excitement as they admire the modified Japanese cars parked nearby. These cars, styled with underglow lighting, have intricate paint jobs and custom bodywork, reflecting a blend of modern and traditional Japanese automotive art. \n\nIn the background, the Japanese convenience store displays its bright signage with Kanji characters, adorned with colorful posters. The store's glass front reveals shelves stocked with an array of snacks and drinks. Beyond the store, the street is dimly lit, with the silhouette of high-rise buildings against the night sky. Mist and distant city lights add an atmospheric touch. The scene emanates a vibrant, energetic mood intermixed with a sense of nocturnal serenity. Include the short text \"Frog Night Out\" in neon font above the convenience store.\n\nArtistic references: Japanese city pop album covers, Studio Ghibli urban landscapes, cyberpunk aesthetics. Technical details: High resolution, vibrant colors, strong contrasts, dynamic lighting."},
        {"role": "user", "parts": "A funny corgi with a hat in a fighting video game."},
        {"role": "model", "parts": "A whimsical corgi wearing a colorful, oversized wizard hat stands triumphantly in the foreground of an intense fighting video game scene. The detailed background showcases a futuristic urban landscape, resembling the neon-lit streets of Blade Runner, with towering skyscrapers, holographic advertisements, and flying cars adding depth and dimension. The corgi, rendered in a stylized, cartoonish art style reminiscent of Overwatch, is ready for battle, with a fierce yet humorous expression. The glowing, magical runes on the hat contrast with the gritty, dark environment, creating a striking juxtaposition. The overall mood is a blend of playful absurdity and high-stakes tension, with dynamic lighting emphasizing the corgi's heroic pose. In the top corner, render the text \"Combat Ready!\" in bold, futuristic typography."},
        {"role": "user", "parts": "A beautiful beach town with cool beachfront homes"},
        {"role": "model", "parts": "A picturesque beach town bustling with vibrant and cool beachfront homes. In the foreground, stylish modern houses with large glass windows, decked patios, and lush rooftop gardens, each uniquely colored with pastel pinks, blues, and yellows, line the pristine sandy shore. People can be seen enjoying their time with beach umbrellas, children playing, and surfers catching waves. The background showcases a stunning sunset with a palette of pink, orange, and purple hues, reflected beautifully in the calm ocean waters. Palms softly sway with the ocean breeze, and distant mountains fade in the horizon. \n\nInspired by the Impressionist paintings of Claude Monet and the bold, crisp lines of Edward Hopper. The scene is illuminated by soft, golden hour light, enhancing the contrast between the cool, modern architecture and the warm, natural scenery. Render the short text \"Paradise\" skillfully integrated into a beach sign by the shore to complement the idyllic mood and tranquil atmosphere."}
    ]
    
    chat = model.start_chat(history=chat_history)
    
    response = chat.send_message(
        original_prompt,
        generation_config = genai.GenerationConfig(
            max_output_tokens=250,
            temperature=1.0
        )
    )
    return response.text

async def gemini_random_prompt() -> str:
    '''
    Generate a random prompt
    '''
    api_key = os.environ["GOOGLE_GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    system_prompt = '''
        You create short prompts for AI text to image models and improve them according to guidelines and examples, you respond with just the prompt.
        <guidelines>
        - Be descriptive and specific
        - Describe the foreground and background separately
        - Incorporate mood and atmosphere
        - Ask to render short text if it makes sense, no more than 4 words
        </guidlines>
        <output_instructions>
        Respond with only the random prompt and nothing else, responses should be less than 100 words.
        </output_instructions>
    '''
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b", system_instruction=system_prompt)

    instructions = "Make a random, slightly humorous image prompt that includes a frog and follows the guidelines" if random.random() < 0.33 else "Make a random image prompt to show off a cool scene according to the guidelines"

    response = model.generate_content(
       instructions,
        generation_config=genai.GenerationConfig(
            max_output_tokens=150,
            temperature=1.3
        )
    )
    return response.text


async def main():

    # prompt = "Sonic the hedgehog riding a roller coaster."

    # result = await gemini_improve_prompt(prompt)
    result = await gemini_random_prompt()

    print(result)

if __name__ == "__main__":

    asyncio.run(main())