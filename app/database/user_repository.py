from app.database.mongodb import get_database
from bson import ObjectId


class UserRepository:

    def __init__(self):
        self.db = get_database()
        self.collection = self.db["users"]

    def create_user(self, user_data: dict):
        return self.collection.insert_one(user_data)

    def get_user_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def get_user_by_id(self, user_id: str):
        return self.collection.find_one({"_id": ObjectId(user_id)})