import matplotlib.pyplot as plt


def show_revenue_chart(monthly_data):

    if not monthly_data:
        return

    labels = []
    values = []

    for item in monthly_data:

        year = item["_id"]["year"]
        month = item["_id"]["month"]

        labels.append(
            f"{year}-{month:02d}"
        )

        values.append(
            item["revenue"]
        )

    plt.figure(figsize=(8, 4))

    plt.plot(
        labels,
        values,
        marker="o"
    )

    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def show_service_type_chart(service_data):

    if not service_data:
        return

    labels = []
    values = []

    for item in service_data:
        labels.append(
            item.get("_id", "Unknown")
        )

        values.append(
            item.get("count", 0)
        )

    plt.figure(figsize=(8, 4))

    plt.bar(
        labels,
        values
    )

    plt.title("Services by Type")
    plt.xlabel("Service Type")
    plt.ylabel("Number of Services")

    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()


def show_service_status_chart(status_data):

    if not status_data:
        return

    labels = []
    values = []

    for item in status_data:
        labels.append(
            item.get("_id", "Unknown")
        )

        values.append(
            item.get("count", 0)
        )

    plt.figure(figsize=(7, 7))

    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Service Status")

    plt.tight_layout()
    plt.show()


def show_most_used_parts_chart(parts_data):

    if not parts_data:
        return

    labels = []
    values = []

    for item in parts_data:
        labels.append(
            item.get("_id", "Unknown")
        )

        values.append(
            item.get("quantity", 0)
        )

    plt.figure(figsize=(9, 5))

    plt.bar(
        labels,
        values
    )

    plt.title("Most Used Spare Parts")
    plt.xlabel("Spare Part")
    plt.ylabel("Quantity Used")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()