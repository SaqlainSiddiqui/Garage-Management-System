from datetime import datetime
from bson import ObjectId
import bcrypt

from config.database import users_collection


def create_user(name, email, password, role="admin"):
    """Create a new user with a securely hashed password."""

    existing_user = users_collection.find_one({
        "email": email.lower().strip()
    })

    if existing_user:
        return None

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = {
        "name": name.strip(),
        "email": email.lower().strip(),
        "password_hash": password_hash,
        "role": role,
        "theme": "Dark",
        "created_at": datetime.utcnow(),
        "is_active": True
    }

    result = users_collection.insert_one(user)

    return result.inserted_id


def authenticate_user(email, password):
    """Verify email and password against MongoDB."""

    user = users_collection.find_one({
        "email": email.lower().strip(),
        "is_active": True
    })

    if not user:
        return None

    password_hash = user.get("password_hash")

    if not password_hash:
        return None

    if bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    ):
        return user

    return None


def find_user_by_email(email):
    """Find a user by email."""

    return users_collection.find_one({
        "email": email.lower().strip()
    })


def find_user_by_id(user_id):
    """Find a user by MongoDB ObjectId."""

    return users_collection.find_one({
        "_id": ObjectId(user_id)
    })

def update_user_profile(user_id, name, email):
    """Update the user's name and email."""

    email = email.lower().strip()
    name = name.strip()

    if not name or not email:
        return False, "Name and email are required."

    # Check whether another user already
    # uses this email.
    existing_user = users_collection.find_one({
        "email": email,
        "_id": {
            "$ne": ObjectId(user_id)
        }
    })

    if existing_user:
        return False, "Another user already uses this email."

    result = users_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "name": name,
                "email": email,
                "updated_at": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        return False, "User not found."

    return True, "Profile updated successfully."


def change_user_password(
    user_id,
    current_password,
    new_password
):
    """Change the user's password."""

    user = users_collection.find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        return False, "User not found."

    password_hash = user.get(
        "password_hash"
    )

    if not password_hash:
        return False, "Password information is missing."

    # Verify current password
    if not bcrypt.checkpw(
        current_password.encode("utf-8"),
        password_hash.encode("utf-8")
    ):
        return False, "Current password is incorrect."

    # Basic password validation
    if len(new_password) < 6:
        return False, "New password must contain at least 6 characters."

    new_password_hash = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    users_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "password_hash": new_password_hash,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return True, "Password changed successfully."