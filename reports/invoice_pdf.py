import os

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_invoice_pdf(
    invoice,
    customer,
    vehicle,
    output_folder="reports/generated"
):
    os.makedirs(
        output_folder,
        exist_ok=True
    )

    filename = (
        f"{invoice['invoice_number']}.pdf"
    )

    filepath = os.path.join(
        output_folder,
        filename
    )

    document = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()

    story = []

    # Header
    story.append(
        Paragraph(
            "<b>GARAGE MANAGEMENT SYSTEM</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "Vehicle Service & Repair",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # Invoice details
    story.append(
        Paragraph(
            f"<b>Invoice:</b> "
            f"{invoice['invoice_number']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> "
            f"{invoice['status']}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # Customer
    story.append(
        Paragraph(
            "<b>Customer Details</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Name: {customer.get('name', '')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Phone: {customer.get('phone', '')}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # Vehicle
    story.append(
        Paragraph(
            "<b>Vehicle Details</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Vehicle: "
            f"{vehicle.get('vehicle_number', '')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Vehicle: "
            f"{vehicle.get('brand', '')} "
            f"{vehicle.get('model', '')}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # Items
    data = [
        [
            "Description",
            "Qty",
            "Price",
            "Total"
        ]
    ]

    for item in invoice.get(
        "items",
        []
    ):

        quantity = float(
            item["quantity"]
        )

        price = float(
            item["price"]
        )

        total = quantity * price

        data.append(
            [
                item["description"],
                str(quantity),
                f"₹{price:.2f}",
                f"₹{total:.2f}"
            ]
        )

    table = Table(
        data,
        colWidths=[
            85 * mm,
            20 * mm,
            35 * mm,
            35 * mm
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "RIGHT"
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            )
        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 15)
    )

    # Totals
    story.append(
        Paragraph(
            f"<b>Subtotal:</b> "
            f"₹{invoice['subtotal']:.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Tax "
            f"({invoice['tax_rate']:.0f}%):</b> "
            f"₹{invoice['tax_amount']:.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            f"<b>Grand Total:</b> "
            f"₹{invoice['grand_total']:.2f}",
            styles["Heading2"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Thank you for choosing our garage.",
            styles["Normal"]
        )
    )

    document.build(story)

    return filepath