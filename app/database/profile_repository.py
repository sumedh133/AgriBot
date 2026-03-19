from app.database.mongodb import get_database
from app.models.profile_model import FarmerProfile
from typing import Optional

class ProfileRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["profiles"]

    def get_profile(self, user_id: str) -> Optional[FarmerProfile]:
        """Retrieves a farmer profile by user ID."""
        data = self.collection.find_one({"user_id": user_id})
        if data:
            return FarmerProfile(**data)
        return None

    def save_profile(self, profile: FarmerProfile):
        """Saves or updates a farmer profile."""
        self.collection.update_one(
            {"user_id": profile.user_id},
            {"$set": profile.dict()},
            upsert=True
        )

    def update_location(self, user_id: str, location: str):
        """Updates only the location for a farmer."""
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"location": location}},
            upsert=True
        )
