from datetime import datetime


def create_user_document(email: str, password_hash: str):

    return {
        "email": email,
        "password": password_hash,
        "created_at": datetime.utcnow()
    }