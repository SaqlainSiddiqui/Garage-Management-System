from config.database import (
    customers_collection,
    vehicles_collection,
    services_collection,
    spare_parts_collection,
    inventory_transactions_collection
)


def create_indexes():

    # ==============================
    # CUSTOMERS
    # ==============================

    customers_collection.create_index(
        "email"
    )

    customers_collection.create_index(
        "phone"
    )


    # ==============================
    # VEHICLES
    # ==============================

    vehicles_collection.create_index(
        "registration_number"
    )

    vehicles_collection.create_index(
        "customer_id"
    )


    # ==============================
    # SERVICES
    # ==============================

    services_collection.create_index(
        "vehicle_id"
    )

    services_collection.create_index(
        "service_date"
    )

    services_collection.create_index(
        "status"
    )


    # ==============================
    # SPARE PARTS
    # ==============================

    spare_parts_collection.create_index(
        "part_number"
    )

    spare_parts_collection.create_index(
        "name"
    )


    # ==============================
    # INVENTORY TRANSACTIONS
    # ==============================

    inventory_transactions_collection.create_index(
        "part_id"
    )

    inventory_transactions_collection.create_index(
        "service_id"
    )

    inventory_transactions_collection.create_index(
        "created_at"
    )


    print("MongoDB indexes created successfully.")


if __name__ == "__main__":
    create_indexes()