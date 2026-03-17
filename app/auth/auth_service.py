from app.database.user_repository import UserRepository
from app.auth.password_utils import hash_password, verify_password
from app.auth.jwt_handler import create_token
from app.models.user_model import create_user_document
from app.utils.validation_utils import validate_email, validate_password

class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, email: str, password: str):
        
        email_valid, error = validate_email(email)
        if not email_valid:
            return None, None, error

        pass_valid, error = validate_password(password)
        if not pass_valid:
            return None, None, error

        existing = self.user_repo.get_user_by_email(email)

        if existing:
            return None, None, "User already exists"

        password_hash = hash_password(password)

        user_doc = create_user_document(email, password_hash)

        result = self.user_repo.create_user(user_doc)

        token = create_token(str(result.inserted_id))

        return token, user_doc, None

    def login(self, email: str, password: str):
        
        email_valid, error = validate_email(email)
        if not email_valid:
            return None, None, error

        pass_valid, error = validate_password(password)
        if not pass_valid:
            return None, None, error

        user = self.user_repo.get_user_by_email(email)

        if not user:
            return None, None, "Invalid credentials"

        if not verify_password(password, user["password"]):
            return None, None, "Invalid credentials"

        token = create_token(str(user["_id"]))

        return token, user, None