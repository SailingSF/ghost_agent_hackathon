CHAT_PROMPT = '''
You will use multi-step reasoning to decide which tools to use and then use the tools to update the story notes.
When you have used all the applicable tools, reply to the user with a follow up question to enrich the notes.
Today's date is November 2nd, 2024.

Available tools:
update_characters(new_characters: str)
  
update_setting(new_setting: str)
  replaces the setting in the context with new_setting which completely replaces the old setting
update_timeline(new_timeline: str)
  replaces the timeline in the context with new_timeline which completely replaces the old timeline
update_themes(new_themes: str)
  replaces the themes in the context with new_themes which completely replaces the old themes

USER: {message}
CURRENT CONTEXT: {current_context}
'''