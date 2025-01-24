
""" Pre-check module """
import os

def check_env_vars():
    """
    Checks if the following environment variables are set:
    
    API_KEY
    RATE_LIMIT
    PINECONE_API_KEY
    PINECONE_ENVIRONMENT
    PINECONE_INDEX_NAME
    """
    environ = os.environ

    env_vars = [
        # "API_KEY", 
        # "RATE_LIMIT", 
        # "PINECONE_API_KEY", 
        # "PINECONE_ENVIRONMENT", 
        # "PINECONE_INDEX_NAME"
        "MODEL",
        "URL",

    ]
    
    for var in env_vars:
        if var not in os.environ:
            raise Exception(f"Environment variable {var} is not set")
    
    return True