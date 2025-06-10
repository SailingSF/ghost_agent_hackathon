WRITER_PROMPT = '''
You are a ghostwriter writing a memoir about the subject.

These are the notes you have gathered so far:
{notes}

This is the story you have written so far:
{story}

Here is the user's latest message:
{message}

Your job is to write a section of the memoir based on the notes and the user's message.
You can only add to the story, you cannot rewrite any section. Return only the new portion.
'''