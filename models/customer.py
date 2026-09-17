from datetime import datetime
from bson import ObjectId

from config.database import customers_collection


def create_customer(name, phone, email, address):
    customer = {
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip().lower(),
        "address": address.strip(),
        "created_at": datetime.utcnow()
    }

    result = customers_collection.insert_one(customer)

    return result.inserted_id


def get_all_customers():
    return list(
        customers_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_customer(customer_id):
    return customers_collection.find_one({
        "_id": ObjectId(customer_id)
    })


def update_customer(
    customer_id,
    name,
    phone,
    email,
    address
):
    result = customers_collection.update_one(
        {
            "_id": ObjectId(customer_id)
        },
        {
            "$set": {
                "name": name.strip(),
                "phone": phone.strip(),
                "email": email.strip().lower(),
                "address": address.strip(),
                "updated_at": datetime.utcnow()
            }
        }
    )

    return result.modified_count


def delete_customer(customer_id):
    result = customers_collection.delete_one({
        "_id": ObjectId(customer_id)
    })

    return result.deleted_count


def search_customers(search_text):
    return list(
        customers_collection.find({
            "$or": [
                {
                    "name": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },
                {
                    "phone": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },
                {
                    "email": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                }
            ]
        }).sort(
            "created_at",
            -1
        )
    )