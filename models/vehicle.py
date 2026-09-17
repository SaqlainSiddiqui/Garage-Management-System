from datetime import datetime
from bson import ObjectId

from config.database import vehicles_collection


def create_vehicle(
    customer_id,
    vehicle_number,
    brand,
    model,
    year,
    fuel_type
):
    vehicle = {
        "customer_id": ObjectId(customer_id),
        "vehicle_number": vehicle_number.strip().upper(),
        "brand": brand.strip(),
        "model": model.strip(),
        "year": int(year) if year else None,
        "fuel_type": fuel_type,
        "created_at": datetime.utcnow()
    }

    result = vehicles_collection.insert_one(vehicle)

    return result.inserted_id


def get_all_vehicles():
    return list(
        vehicles_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_vehicles_by_customer(customer_id):
    return list(
        vehicles_collection.find({
            "customer_id": ObjectId(customer_id)
        }).sort(
            "created_at",
            -1
        )
    )


def get_vehicle(vehicle_id):
    return vehicles_collection.find_one({
        "_id": ObjectId(vehicle_id)
    })


def update_vehicle(
    vehicle_id,
    customer_id,
    vehicle_number,
    brand,
    model,
    year,
    fuel_type
):
    result = vehicles_collection.update_one(
        {
            "_id": ObjectId(vehicle_id)
        },
        {
            "$set": {
                "customer_id": ObjectId(customer_id),
                "vehicle_number": vehicle_number.strip().upper(),
                "brand": brand.strip(),
                "model": model.strip(),
                "year": int(year) if year else None,
                "fuel_type": fuel_type,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return result.modified_count


def delete_vehicle(vehicle_id):
    result = vehicles_collection.delete_one({
        "_id": ObjectId(vehicle_id)
    })

    return result.deleted_count


def search_vehicles(search_text):
    return list(
        vehicles_collection.find({
            "$or": [
                {
                    "vehicle_number": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },
                {
                    "brand": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },
                {
                    "model": {
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