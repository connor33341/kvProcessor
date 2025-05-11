import uuid

def uuidv4():
    """
    Generate a random UUID (Universally Unique Identifier) version 4.
    
    Returns:
        str: A string representation of the generated UUID.
    """
    return str(uuid.uuid4())