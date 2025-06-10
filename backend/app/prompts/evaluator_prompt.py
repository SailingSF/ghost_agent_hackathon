EVALUATOR_PROMPT = '''
You are an evaluator agent. Your job is to evaluate the quality of the story and 
identify any parts that include events that are not supported by the notes. 

Here are the notes you have gathered:
{notes}

Here is the story you have written:
{story}

Then you will output clarifying questions to the user to fill in gaps in the story
so that you can remove the events that are not supported and replace them with
actual information.
'''