from datetime import datetime
from bson import ObjectId

from config.database import (
    inventory_transactions_collection
)


# =========================================================
# CREATE INVENTORY TRANSACTION
# =========================================================

def create_inventory_transaction(
    part_id,
    part_name,
    quantity_change,
    transaction_type,
    reference=None,
    notes="",
    service_id=None
):
    """
    Create an inventory transaction.

    service_id is optional and is used when
    the transaction is related to a vehicle service.
    """

    transaction = {
        "part_id": ObjectId(part_id),

        "part_name": part_name,

        "quantity_change": int(
            quantity_change
        ),

        "transaction_type": transaction_type,

        "reference": reference,

        "service_id": (
            ObjectId(service_id)
            if service_id
            else None
        ),

        "notes": notes,

        "created_at": datetime.utcnow()
    }

    result = (
        inventory_transactions_collection
        .insert_one(transaction)
    )

    return result.inserted_id


# =========================================================
# GET ALL TRANSACTIONS
# =========================================================

def get_all_inventory_transactions():

    return list(
        inventory_transactions_collection
        .find()
        .sort(
            "created_at",
            -1
        )
    )


# =========================================================
# GET TRANSACTIONS BY PART
# =========================================================

def get_transactions_by_part(
    part_id
):

    return list(
        inventory_transactions_collection
        .find({
            "part_id": ObjectId(part_id)
        })
        .sort(
            "created_at",
            -1
        )
    )


# =========================================================
# GET TRANSACTIONS BY SERVICE
# =========================================================

def get_transactions_by_service(
    service_id
):

    return list(
        inventory_transactions_collection
        .find({
            "service_id": ObjectId(
                service_id
            )
        })
        .sort(
            "created_at",
            -1
        )
    )