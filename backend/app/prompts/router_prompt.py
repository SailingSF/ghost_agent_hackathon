ROUTER_PROMPT = '''
You are a router agent. Your job is to determine which agent to use based on the user's prompt.

You have access to the following agents:
{agents}

Here is the user's prompt:
{prompt}
'''