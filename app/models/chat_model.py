from datetime import datetime


def create_conversation_document(user_id: str, title: str = "New Chat"):
    """
    Creates a MongoDB conversation document.
    MongoDB will automatically generate the _id.
    """

    return {
        "user_id": user_id,
        "title": title,

        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        
         # aggregated token usage - placeholder for now, can be updated after each message
        "tokens": {
            "input": 0,
            "output": 0,
            "total": 0
        },

        # for future extensibility
        # "metadata": {}
    }


def create_message_document(
    conversation_id,
    role: str,
    content: str,
    tools_used=None,
    citations=None,
    metadata=None
):
    """
    Creates a MongoDB message document.
    conversation_id should be the ObjectId of the conversation.
    """

    return {
        "conversation_id": conversation_id,

        "role": role,  # user | assistant | system
        "content": content,

        "timestamp": datetime.utcnow(),

        # "tools_used": tools_used or [],
        # "citations": citations or [],
        # "metadata": metadata or {}
    }