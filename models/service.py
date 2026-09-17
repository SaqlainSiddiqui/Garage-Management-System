from datetime import datetime
from bson import ObjectId

from config.database import (
    services_collection,
    spare_parts_collection
)

from models.spare_part import(
    deduct_stock,
    restore_stock_after_failed_service
)

def create_service(
    vehicle_id,
    service_date,
    service_type,
    odometer,
    mechanic,
    labour_cost,
    parts,
    notes,
    next_service_date,
    status="Completed"
):
    """
    Create a service record and deduct
    spare parts inventory automatically.
    """

    # ==========================================
    # TRACK DEDUCTED PARTS
    # ==========================================

    service_id = ObjectId()
    deducted_parts = []

    try:

        # ======================================
        # DEDUCT INVENTORY
        # ======================================

        for part in parts:

            part_id = part.get("part_id")
            quantity = int(part["quantity"])

            if not part_id:

                raise ValueError(
                    f"Part ID missing for {part['name']}"
                )

            success = deduct_stock(
                part_id,
                quantity,
                service_id=str(service_id)
            )

            if not success:

                raise ValueError(
                    f"Insufficient stock for "
                    f"{part['name']}"
                )

            deducted_parts.append({
                "part_id": part_id,
                "quantity": quantity
            })

        # ======================================
        # CALCULATE PARTS TOTAL
        # ======================================

        parts_total = sum(
            float(part["quantity"]) *
            float(part["price"])
            for part in parts
        )

        # ======================================
        # LABOUR
        # ======================================

        labour_cost = float(
            labour_cost or 0
        )

        # ======================================
        # TOTAL COST
        # ======================================

        total_cost = (
            parts_total +
            labour_cost
        )

        # ======================================
        # SERVICE DOCUMENT
        # ======================================

        service = {

            "_id": service_id,

            "vehicle_id": ObjectId(
                vehicle_id
            ),

            "service_date": service_date,

            "service_type": service_type,

            "odometer": int(
                odometer or 0
            ),

            "mechanic": mechanic.strip(),

            "labour_cost": labour_cost,

            "parts": parts,

            "parts_total": parts_total,

            "total_cost": total_cost,

            "status": status,

            "notes": notes.strip(),

            "next_service_date": (
                next_service_date
            ),

            "created_at": datetime.utcnow()
        }

        # ======================================
        # SAVE SERVICE
        # ======================================

        result = services_collection.insert_one(
            service
        )

        return result.inserted_id

    except Exception:

        # ==========================================
        # ROLLBACK INVENTORY
        # ==========================================

        for deducted_part in deducted_parts:

            restore_stock_after_failed_service(
                part_id=deducted_part["part_id"],
                quantity=deducted_part["quantity"],
                service_id=str(service_id)
            )

        # Re-raise the original error
        raise


def get_all_services():

    return list(
        services_collection.find().sort(
            "service_date",
            -1
        )
    )


def get_services_by_vehicle(
    vehicle_id
):

    return list(
        services_collection.find({
            "vehicle_id": ObjectId(
                vehicle_id
            )
        }).sort(
            "service_date",
            -1
        )
    )


def get_service(
    service_id
):

    return services_collection.find_one({
        "_id": ObjectId(
            service_id
        )
    })


def update_service(
    service_id,
    vehicle_id,
    service_date,
    service_type,
    odometer,
    mechanic,
    labour_cost,
    parts,
    notes,
    next_service_date,
    status
):

    parts_total = sum(
        float(part["quantity"]) *
        float(part["price"])
        for part in parts
    )

    labour_cost = float(
        labour_cost or 0
    )

    total_cost = (
        parts_total +
        labour_cost
    )

    result = services_collection.update_one(
        {
            "_id": ObjectId(
                service_id
            )
        },
        {
            "$set": {

                "vehicle_id": ObjectId(
                    vehicle_id
                ),

                "service_date": service_date,

                "service_type": service_type,

                "odometer": int(
                    odometer or 0
                ),

                "mechanic": mechanic.strip(),

                "labour_cost": labour_cost,

                "parts": parts,

                "parts_total": parts_total,

                "total_cost": total_cost,

                "status": status,

                "notes": notes.strip(),

                "next_service_date": (
                    next_service_date
                ),

                "updated_at": datetime.utcnow()
            }
        }
    )

    return result.modified_count


def delete_service(
    service_id
):

    result = services_collection.delete_one({
        "_id": ObjectId(
            service_id
        )
    })

    return result.deleted_count


def get_services_by_status(
    status
):

    return list(
        services_collection.find({
            "status": status
        }).sort(
            "service_date",
            -1
        )
    )