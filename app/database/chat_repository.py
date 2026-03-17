from bson import ObjectId
from datetime import datetime

from app.database.mongodb import get_database
from app.models.chat_model import (
    create_conversation_document,
    create_message_document
)

db = get_database()

conversations_collection = db["conversations"]
messages_collection = db["messages"]


def create_conversation(user_id):

    conversation = create_conversation_document(user_id)

    result = conversations_collection.insert_one(conversation)

    return result.inserted_id


def add_message(conversation_id, role, content):

    message = create_message_document(
        conversation_id,
        role,
        content
    )

    messages_collection.insert_one(message)

    # update conversation timestamp
    conversations_collection.update_one(
        {"_id": conversation_id},
        {"$set": {"updated_at": datetime.utcnow()}}
    )
    
    
def get_messages(conversation_id):

    return list(
        messages_collection
        .find({"conversation_id": conversation_id})
        .sort("timestamp", 1)
    )
    
    
def get_messages(conversation_id):

    return list(
        messages_collection
        .find({"conversation_id": conversation_id})
        .sort("timestamp", 1)
    )
    
def get_user_conversations(user_id):
    """
    Returns all conversations belonging to a user,
    sorted by most recently updated.
    """

    conversations = conversations_collection.find(
        {"user_id": user_id}
    ).sort("updated_at", -1)

    return list(conversations)

def update_conversation_title(conversation_id, title):

    conversations_collection.update_one(
        {"_id": conversation_id},
        {"$set": {"title": title}}
    )
    
    
def update_token_usage(conversation_id, input_tokens, output_tokens):

    conversations_collection.update_one(
        {"_id": conversation_id},
        {
            "$inc": {
                "tokens.input": input_tokens,
                "tokens.output": output_tokens,
                "tokens.total": input_tokens + output_tokens
            }
        }
    )