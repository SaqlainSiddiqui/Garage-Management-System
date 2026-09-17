from datetime import datetime
from bson import ObjectId

from config.database import invoices_collection


def create_invoice(
    invoice_number,
    customer_id,
    vehicle_id,
    service_id,
    service,
    tax_rate=18,
    status="Unpaid"
):
    """Create an invoice from an existing service record."""

    if not isinstance(service, dict):
        raise TypeError("service must be a service document/dictionary.")

    labour_cost = float(service.get("labour_cost", 0) or 0)
    parts = service.get("parts", []) or []

    # Convert the service into PDF/invoice-ready line items.
    items = []

    if labour_cost > 0:
        items.append({
            "description": "Labour Charges",
            "quantity": 1,
            "price": labour_cost
        })

    for part in parts:
        quantity = float(part.get("quantity", 0) or 0)
        price = float(part.get("price", 0) or 0)
        if quantity > 0:
            items.append({
                "description": part.get("name", "Spare Part"),
                "quantity": quantity,
                "price": price
            })

    subtotal = sum(
        float(item["quantity"]) * float(item["price"])
        for item in items
    )

    tax_rate = float(tax_rate)
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative.")

    tax_amount = subtotal * tax_rate / 100
    grand_total = subtotal + tax_amount

    invoice = {
        "invoice_number": invoice_number,
        "customer_id": ObjectId(customer_id),
        "vehicle_id": ObjectId(vehicle_id),
        "service_id": ObjectId(service_id),
        "items": items,
        "service_type": service.get("service_type", ""),
        "labour_cost": labour_cost,
        "parts_total": float(service.get("parts_total", 0) or 0),
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "grand_total": grand_total,
        "status": status,
        "created_at": datetime.utcnow()
    }

    result = invoices_collection.insert_one(invoice)
    return result.inserted_id

def get_all_invoices():
    return list(
        invoices_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_invoice(invoice_id):
    return invoices_collection.find_one({
        "_id": ObjectId(invoice_id)
    })


def update_invoice_status(
    invoice_id,
    status
):
    result = invoices_collection.update_one(
        {
            "_id": ObjectId(invoice_id)
        },
        {
            "$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return result.modified_count


def delete_invoice(invoice_id):
    result = invoices_collection.delete_one({
        "_id": ObjectId(invoice_id)
    })

    return result.deleted_count


def search_invoices(search_text):
    return list(
        invoices_collection.find({
            "invoice_number": {
                "$regex": search_text,
                "$options": "i"
            }
        }).sort(
            "created_at",
            -1
        )
    )