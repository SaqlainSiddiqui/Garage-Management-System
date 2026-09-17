from config.database import (
    services_collection,
    inventory_transactions_collection,
    spare_parts_collection
)


# =========================================================
# TOTAL REVENUE
# =========================================================

def get_total_revenue():

    result = list(
        services_collection.aggregate([
            {
                "$match": {
                    "status": "Completed"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$total_cost"
                    }
                }
            }
        ])
    )

    if not result:
        return 0

    return float(
        result[0].get("total", 0)
    )


# =========================================================
# SERVICE COUNT
# =========================================================

def get_total_services():

    return services_collection.count_documents({
        "status": "Completed"
    })


# =========================================================
# SERVICE TYPE REPORT
# =========================================================

def get_services_by_type():

    return list(
        services_collection.aggregate([
            {
                "$group": {
                    "_id": "$service_type",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ])
    )


# =========================================================
# SERVICE STATUS REPORT
# =========================================================

def get_services_by_status():

    return list(
        services_collection.aggregate([
            {
                "$group": {
                    "_id": "$status",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ])
    )


# =========================================================
# MONTHLY REVENUE
# =========================================================

def get_monthly_revenue():

    return list(
        services_collection.aggregate([
            {
                "$match": {
                    "status": "Completed"
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {
                            "$year": {
                                "$dateFromString": {
                                    "dateString":
                                        "$service_date"
                                }
                            }
                        },
                        "month": {
                            "$month": {
                                "$dateFromString": {
                                    "dateString":
                                        "$service_date"
                                }
                            }
                        }
                    },
                    "revenue": {
                        "$sum": "$total_cost"
                    },
                    "services": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1
                }
            }
        ])
    )


# =========================================================
# MOST USED SPARE PARTS
# =========================================================

def get_most_used_parts():

    return list(
        services_collection.aggregate([
            {
                "$unwind": "$parts"
            },
            {
                "$group": {
                    "_id": "$parts.name",
                    "quantity": {
                        "$sum": {
                            "$toInt":
                                "$parts.quantity"
                        }
                    }
                }
            },
            {
                "$sort": {
                    "quantity": -1
                }
            },
            {
                "$limit": 10
            }
        ])
    )


# =========================================================
# LOW STOCK PARTS
# =========================================================

def get_low_stock_report():

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
# INVENTORY MOVEMENT
# =========================================================

def get_inventory_movement():

    return list(
        inventory_transactions_collection.aggregate([
            {
                "$group": {
                    "_id": "$transaction_type",
                    "quantity": {
                        "$sum": "$quantity_change"
                    },
                    "transactions": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "transactions": -1
                }
            }
        ])
    )