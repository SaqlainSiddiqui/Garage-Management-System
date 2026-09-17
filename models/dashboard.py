from datetime import datetime

from config.database import (
    customers_collection,
    vehicles_collection,
    services_collection,
    spare_parts_collection,
    invoices_collection
)


def get_dashboard_statistics():

    total_customers = customers_collection.count_documents({})

    total_vehicles = vehicles_collection.count_documents({})

    total_services = services_collection.count_documents({})

    today = datetime.now().strftime("%Y-%m-%d")

    today_services = services_collection.count_documents({
        "service_date": today
    })

    pending_services = services_collection.count_documents({
        "status": {
            "$in": [
                "Pending",
                "In Progress"
            ]
        }
    })

    low_stock_parts = spare_parts_collection.count_documents({
        "$expr": {
            "$lte": [
                "$stock",
                "$minimum_stock"
            ]
        }
    })

    paid_invoice_data = list(
        invoices_collection.aggregate([
            {
                "$match": {
                    "status": "Paid"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$grand_total"
                    }
                }
            }
        ])
    )

    total_revenue = 0

    if paid_invoice_data:
        total_revenue = paid_invoice_data[0]["total"]

    unpaid_invoice_data = list(
        invoices_collection.aggregate([
            {
                "$match": {
                    "status": "Unpaid"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {
                        "$sum": "$grand_total"
                    }
                }
            }
        ])
    )

    pending_revenue = 0

    if unpaid_invoice_data:
        pending_revenue = unpaid_invoice_data[0]["total"]

    return {
        "total_customers": total_customers,
        "total_vehicles": total_vehicles,
        "total_services": total_services,
        "today_services": today_services,
        "pending_services": pending_services,
        "low_stock_parts": low_stock_parts,
        "total_revenue": total_revenue,
        "pending_revenue": pending_revenue
    }


def get_recent_services(limit=5):

    return list(
        services_collection.find()
        .sort("created_at", -1)
        .limit(limit)
    )


def get_monthly_revenue():

    result = list(
        invoices_collection.aggregate([
            {
                "$match": {
                    "status": "Paid"
                }
            },
            {
                "$group": {
                    "_id": {
                        "year": {
                            "$year": "$created_at"
                        },
                        "month": {
                            "$month": "$created_at"
                        }
                    },
                    "revenue": {
                        "$sum": "$grand_total"
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

    return result