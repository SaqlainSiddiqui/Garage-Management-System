import bcrypt

from models.user import create_user, find_user_by_email


name = "System Administrator"
email = "admin@garage.com"
password = "Admin@123"


# Check if user already exists
existing_user = find_user_by_email(email)

if existing_user:
    print("Admin user already exists.")
else:
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create user
    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash
    )

    print("Admin user created successfully!")
    print("User ID:", user_id)