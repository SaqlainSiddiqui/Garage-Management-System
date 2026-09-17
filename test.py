from config.database import client, db

try:
    # Test MongoDB connection
    client.admin.command("ping")

    print("================================")
    print("MongoDB connection successful!")
    print("Database:", db.name)
    print("================================")

except Exception as error:
    print("MongoDB connection failed!")
    print("Error:", error)