#
# Utility functions
#

def system(content: str):
    return {"role": "system", "content": content}

def assistant(content: str):
    return {"role": "assistant", "content": content}

def user(content: str):
    return {"role": "user", "content": content}