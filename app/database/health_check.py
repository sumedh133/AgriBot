from app.database.mongodb import get_database


def check_database_connection():
    try:
        db = get_database()
        db.command("ping")
        return True
    except Exception as e:
        print("MongoDB connection failed:", e)
        return False