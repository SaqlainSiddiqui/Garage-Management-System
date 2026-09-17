from datetime import datetime
from bson import ObjectId

from config.database import spare_parts_collection

from models.inventory_transaction import (
    create_inventory_transaction
)


# =========================================================
# CREATE SPARE PART
# =========================================================

def create_spare_part(
    name,
    part_number,
    category,
    supplier,
    purchase_price,
    selling_price,
    stock,
    minimum_stock,
    location
):
    """
    Create a new spare part.

    If opening stock is greater than zero,
    an inventory transaction is recorded.
    """

    stock = int(stock)

    if stock < 0:
        raise ValueError(
            "Stock cannot be negative."
        )

    part = {
        "name": name.strip(),

        "part_number": (
            part_number.strip().upper()
        ),

        "category": category.strip(),

        "supplier": supplier.strip(),

        "purchase_price": float(
            purchase_price
        ),

        "selling_price": float(
            selling_price
        ),

        "stock": stock,

        "minimum_stock": int(
            minimum_stock
        ),

        "location": location.strip(),

        "created_at": datetime.utcnow()
    }

    result = spare_parts_collection.insert_one(
        part
    )

    # ==========================================
    # RECORD OPENING STOCK
    # ==========================================

    if stock > 0:

        create_inventory_transaction(
            part_id=result.inserted_id,
            part_name=part["name"],
            quantity_change=stock,
            transaction_type="Opening Stock",
            reference=None,
            notes="Initial stock when part was created."
        )

    return result.inserted_id


# =========================================================
# GET ALL SPARE PARTS
# =========================================================

def get_all_spare_parts():

    return list(
        spare_parts_collection.find().sort(
            "created_at",
            -1
        )
    )


# =========================================================
# GET SINGLE SPARE PART
# =========================================================

def get_spare_part(part_id):

    return spare_parts_collection.find_one({
        "_id": ObjectId(part_id)
    })


# =========================================================
# UPDATE SPARE PART
# =========================================================

def update_spare_part(
    part_id,
    name,
    part_number,
    category,
    supplier,
    purchase_price,
    selling_price,
    stock,
    minimum_stock,
    location
):
    """
    Update spare part details.

    If stock changes during the update,
    the difference is recorded as a
    Stock Adjustment transaction.
    """

    part_id = ObjectId(part_id)

    stock = int(stock)

    if stock < 0:
        raise ValueError(
            "Stock cannot be negative."
        )

    # ==========================================
    # GET CURRENT PART
    # ==========================================

    existing_part = (
        spare_parts_collection.find_one({
            "_id": part_id
        })
    )

    if not existing_part:

        raise ValueError(
            "Spare part not found."
        )

    old_stock = int(
        existing_part.get(
            "stock",
            0
        )
    )

    # ==========================================
    # UPDATE PART
    # ==========================================

    result = spare_parts_collection.update_one(
        {
            "_id": part_id
        },
        {
            "$set": {

                "name": name.strip(),

                "part_number": (
                    part_number
                    .strip()
                    .upper()
                ),

                "category": category.strip(),

                "supplier": supplier.strip(),

                "purchase_price": float(
                    purchase_price
                ),

                "selling_price": float(
                    selling_price
                ),

                "stock": stock,

                "minimum_stock": int(
                    minimum_stock
                ),

                "location": location.strip(),

                "updated_at": datetime.utcnow()
            }
        }
    )

    # ==========================================
    # RECORD STOCK CHANGE
    # ==========================================

    stock_difference = (
        stock - old_stock
    )

    if (
        result.modified_count == 1
        and stock_difference != 0
    ):

        if stock_difference > 0:

            transaction_type = (
                "Stock Adjustment"
            )

            notes = (
                "Stock increased during "
                "part update."
            )

        else:

            transaction_type = (
                "Stock Adjustment"
            )

            notes = (
                "Stock decreased during "
                "part update."
            )

        create_inventory_transaction(
            part_id=part_id,
            part_name=name.strip(),
            quantity_change=stock_difference,
            transaction_type=transaction_type,
            reference=None,
            notes=notes
        )

    return result.modified_count


# =========================================================
# DELETE SPARE PART
# =========================================================

def delete_spare_part(part_id):

    result = spare_parts_collection.delete_one({
        "_id": ObjectId(part_id)
    })

    return result.deleted_count


# =========================================================
# SEARCH SPARE PARTS
# =========================================================

def search_spare_parts(search_text):

    return list(
        spare_parts_collection.find({
            "$or": [

                {
                    "name": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },

                {
                    "part_number": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },

                {
                    "category": {
                        "$regex": search_text,
                        "$options": "i"
                    }
                },

                {
                    "supplier": {
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


# =========================================================
# GET LOW STOCK PARTS
# =========================================================

def get_low_stock_parts():

    return list(
        spare_parts_collection.find({
            "$expr": {
                "$lte": [
                    "$stock",
                    "$minimum_stock"
                ]
            }
        }).sort(
            "stock",
            1
        )
    )


# =========================================================
# UPDATE STOCK
# =========================================================

def update_stock(
    part_id,
    quantity
):
    """
    Add or remove stock manually.

    Positive quantity:
        Stock increases.

    Negative quantity:
        Stock decreases.

    Every successful stock change
    creates an inventory transaction.
    """

    part_id = ObjectId(part_id)

    quantity = int(quantity)

    if quantity == 0:

        return 0

    # ==========================================
    # CHECK CURRENT PART
    # ==========================================

    existing_part = (
        spare_parts_collection.find_one({
            "_id": part_id
        })
    )

    if not existing_part:

        raise ValueError(
            "Spare part not found."
        )

    current_stock = int(
        existing_part.get(
            "stock",
            0
        )
    )

    new_stock = (
        current_stock + quantity
    )

    # ==========================================
    # PREVENT NEGATIVE STOCK
    # ==========================================

    if new_stock < 0:

        raise ValueError(
            f"Insufficient stock. "
            f"Available stock: {current_stock}"
        )

    # ==========================================
    # UPDATE STOCK
    # ==========================================

    result = spare_parts_collection.update_one(
        {
            "_id": part_id
        },
        {
            "$inc": {
                "stock": quantity
            },

            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )

    # ==========================================
    # RECORD TRANSACTION
    # ==========================================

    if result.modified_count == 1:

        if quantity > 0:

            transaction_type = (
                "Stock Added"
            )

            notes = (
                "Stock manually added."
            )

        else:

            transaction_type = (
                "Stock Removed"
            )

            notes = (
                "Stock manually removed."
            )

        create_inventory_transaction(
            part_id=part_id,
            part_name=existing_part.get(
                "name",
                "Unknown Part"
            ),
            quantity_change=quantity,
            transaction_type=transaction_type,
            reference=None,
            notes=notes
        )

    return result.modified_count


# =========================================================
# DEDUCT STOCK FOR SERVICE
# =========================================================

def deduct_stock(
    part_id,
    quantity,
    service_id=None
):
    """
    Deduct stock when a spare part is
    used in a vehicle service.

    MongoDB only performs the update
    when sufficient stock exists.
    """

    part_id = ObjectId(part_id)

    quantity = int(quantity)

    if quantity <= 0:

        raise ValueError(
            "Quantity must be greater than zero."
        )

    # ==========================================
    # GET PART
    # ==========================================

    existing_part = (
        spare_parts_collection.find_one({
            "_id": part_id
        })
    )

    if not existing_part:

        return False

    # ==========================================
    # ATOMIC STOCK DEDUCTION
    # ==========================================

    result = spare_parts_collection.update_one(
        {
            "_id": part_id,

            "stock": {
                "$gte": quantity
            }
        },
        {
            "$inc": {
                "stock": -quantity
            },

            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )

    # ==========================================
    # RECORD SERVICE TRANSACTION
    # ==========================================

    if result.modified_count == 1:

        create_inventory_transaction(
            part_id=part_id,
            part_name=existing_part.get(
                "name",
                "Unknown Part"
            ),
            quantity_change=-quantity,
            transaction_type="Service",
            reference=(
                f"SERVICE-{service_id}"
                if service_id
                else "Vehicle Service"
            ),
            notes=(
                "Stock deducted because "
                "the part was used in a service."
            ),
            service_id=service_id
        )

        return True

    return False

# =========================================================
# RESTORE STOCK AFTER FAILED SERVICE
# =========================================================

def restore_stock_after_failed_service(
    part_id,
    quantity,
    service_id=None
):
    """
    Restore stock when a service creation fails
    after stock has already been deducted.

    This creates a compensating inventory transaction
    so the inventory history remains auditable.
    """

    part_id = ObjectId(part_id)

    quantity = int(quantity)

    if quantity <= 0:
        return 0

    # ==========================================
    # GET PART
    # ==========================================

    existing_part = (
        spare_parts_collection.find_one({
            "_id": part_id
        })
    )

    if not existing_part:

        return 0

    # ==========================================
    # RESTORE STOCK
    # ==========================================

    result = spare_parts_collection.update_one(
        {
            "_id": part_id
        },
        {
            "$inc": {
                "stock": quantity
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )

    # ==========================================
    # RECORD ROLLBACK
    # ==========================================

    if result.modified_count == 1:

        create_inventory_transaction(
            part_id=part_id,
            part_name=existing_part.get(
                "name",
                "Unknown Part"
            ),
            quantity_change=quantity,
            transaction_type="Service Rollback",
            reference=(
                f"SERVICE-{service_id}"
                if service_id
                else "Failed Vehicle Service"
            ),
            notes=(
                "Stock restored because "
                "service creation failed."
            ),
            service_id=service_id
        )

    return result.modified_count