from datetime import datetime
from app.database.mongodb import get_database

db = get_database()
memory_collection = db["user_memories"]


class ConversationMemory:
    """
    Stores and retrieves key agricultural facts the user has shared across conversations.
    This gives the AI a 'long-term memory' that persists between chat sessions.
    """

    def save_memory(self, user_id: str, fact: str):
        """Save a new key fact for a user."""
        memory_collection.update_one(
            {"user_id": str(user_id), "fact": fact},
            {"$setOnInsert": {
                "user_id": str(user_id),
                "fact": fact,
                "created_at": datetime.utcnow()
            }},
            upsert=True  # Only insert if this exact fact doesn't exist yet
        )

    def get_memories(self, user_id: str) -> list[str]:
        """Retrieve all stored facts for a user."""
        docs = memory_collection.find(
            {"user_id": str(user_id)},
            sort=[("created_at", -1)]
        ).limit(10)  # Limit to the 10 most recent facts
        return [doc["fact"] for doc in docs]

    def extract_and_save_facts(self, user_id: str, user_message: str):
        """
        Checks if a user message contains a key agricultural fact worth remembering,
        and saves it without using any extra AI quota.
        """
        # Simple rule-based extraction: look for first-person statements about the farm
        keywords = [
            "i have", "my farm", "my field", "my crop", "my land", "i grow",
            "i plant", "my soil", "my village", "i am from", "i use", "my well",
            "my irrigation", "my cattle", "i own"
        ]
        lower_msg = user_message.lower()
        if any(kw in lower_msg for kw in keywords):
            # The message itself is the fact — store a cleaned version
            fact = user_message.strip()
            if len(fact) < 300:  # Don't store excessively long messages
                self.save_memory(user_id, fact)
