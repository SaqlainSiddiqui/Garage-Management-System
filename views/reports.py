import customtkinter as ctk
from tkinter import messagebox

from models.reports import (
    get_total_revenue,
    get_total_services,
    get_services_by_type,
    get_services_by_status,
    get_monthly_revenue,
    get_most_used_parts,
    get_low_stock_report,
    get_inventory_movement
)

from utils.chart import (
    show_revenue_chart,
    show_service_type_chart,
    show_service_status_chart,
    show_most_used_parts_chart
)


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.create_ui()
        self.load_reports()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Reports & Analytics",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "MongoDB-powered garage reports "
                "and business analytics."
            )
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        ctk.CTkButton(
            self,
            text="Refresh Reports",
            command=self.load_reports
        ).pack(
            anchor="e",
            padx=25,
            pady=(0, 10)
        )

        self.report_area = ctk.CTkScrollableFrame(
            self
        )

        self.report_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_reports(self):

        for widget in (
            self.report_area.winfo_children()
        ):

            widget.destroy()

    # =====================================================
    # LOAD REPORTS
    # =====================================================

    def load_reports(self):

        self.clear_reports()

        try:

            total_revenue = get_total_revenue()

            total_services = get_total_services()

            services_by_type = (
                get_services_by_type()
            )

            services_by_status = (
                get_services_by_status()
            )

            monthly_revenue = (
                get_monthly_revenue()
            )

            most_used_parts = (
                get_most_used_parts()
            )

            low_stock = (
                get_low_stock_report()
            )

            inventory_movement = (
                get_inventory_movement()
            )

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                f"Unable to load reports.\n\n{e}"
            )

            return

        # =================================================
        # SUMMARY CARDS
        # =================================================

        summary = ctk.CTkFrame(
            self.report_area
        )

        summary.pack(
            fill="x",
            pady=10
        )

        self.create_summary_card(
            summary,
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

        self.create_summary_card(
            summary,
            "Completed Services",
            str(total_services)
        )

        self.create_summary_card(
            summary,
            "Low Stock Items",
            str(len(low_stock))
        )

        # =================================================
        # SERVICE TYPES
        # =================================================

        self.create_section(
            "Services by Type"
        )

        if services_by_type:

            ctk.CTkButton(
                self.report_area,
                text="📊 View Services by Type Chart",
                command=lambda: show_service_type_chart(
                    services_by_type
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=(0, 8)
            )

            for item in services_by_type:

                self.create_report_row(
                    f"{item['_id']}",
                    str(item["count"])
                )

        else:

            self.create_empty_label()

        # =================================================
        # SERVICE STATUS
        # =================================================


        self.create_section(
            "Service Status"
        )

        if services_by_status:

            ctk.CTkButton(
                self.report_area,
                text="🥧 View Service Status Chart",
                command=lambda: show_service_status_chart(
                    services_by_status
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=(0, 8)
            )

            for item in services_by_status:

                self.create_report_row(
                    f"{item['_id']}",
                    str(item["count"])
                )

        else:

            self.create_empty_label()

        # =================================================
        # MONTHLY REVENUE
        # =================================================

                # =================================================
        # MONTHLY REVENUE
        # =================================================

        self.create_section(
            "Monthly Revenue"
        )

        if monthly_revenue:

            ctk.CTkButton(
                self.report_area,
                text="📈 View Monthly Revenue Chart",
                command=lambda: show_revenue_chart(
                    monthly_revenue
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=(0, 8)
            )

            for item in monthly_revenue:

                year = item["_id"]["year"]
                month = item["_id"]["month"]

                self.create_report_row(
                    f"{year}-{month:02d}",
                    f"₹{float(item['revenue']):,.2f}"
                )

        else:

            self.create_empty_label()

        # =================================================
        # MOST USED PARTS
        # =================================================

                # =================================================
        # MOST USED PARTS
        # =================================================

        self.create_section(
            "Most Used Spare Parts"
        )

        if most_used_parts:

            ctk.CTkButton(
                self.report_area,
                text="📊 View Most Used Parts Chart",
                command=lambda: show_most_used_parts_chart(
                    most_used_parts
                )
            ).pack(
                anchor="w",
                padx=5,
                pady=(0, 8)
            )

            for item in most_used_parts:

                self.create_report_row(
                    str(item["_id"]),
                    f"{item['quantity']} units"
                )

        else:

            self.create_empty_label()

        # =================================================
        # LOW STOCK
        # =================================================

        self.create_section(
            "Low Stock Parts"
        )

        if low_stock:

            for part in low_stock:

                self.create_report_row(
                    part.get(
                        "name",
                        "Unknown"
                    ),
                    (
                        f"Stock: "
                        f"{part.get('stock', 0)} / "
                        f"Minimum: "
                        f"{part.get('minimum_stock', 0)}"
                    )
                )

        else:

            self.create_empty_label(
                "No low-stock items."
            )

        # =================================================
        # INVENTORY MOVEMENT
        # =================================================

        self.create_section(
            "Inventory Movement"
        )

        if inventory_movement:

            for item in inventory_movement:

                self.create_report_row(
                    str(item["_id"]),
                    (
                        f"{item['quantity']} units "
                        f"({item['transactions']} "
                        f"transactions)"
                    )
                )

        else:

            self.create_empty_label()

    # =====================================================
    # SUMMARY CARD
    # =====================================================

    def create_summary_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(0, 15)
        )

    # =====================================================
    # SECTION
    # =====================================================

    def create_section(
        self,
        title
    ):

        ctk.CTkLabel(
            self.report_area,
            text=title,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            anchor="w"
        ).pack(
            fill="x",
            pady=(20, 8),
            padx=5
        )

    # =====================================================
    # REPORT ROW
    # =====================================================

    def create_report_row(
        self,
        label,
        value
    ):

        row = ctk.CTkFrame(
            self.report_area
        )

        row.pack(
            fill="x",
            pady=3,
            padx=5
        )

        ctk.CTkLabel(
            row,
            text=label,
            anchor="w"
        ).pack(
            side="left",
            padx=15,
            pady=10
        )

        ctk.CTkLabel(
            row,
            text=value,
            anchor="e",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).pack(
            side="right",
            padx=15,
            pady=10
        )

    # =====================================================
    # EMPTY
    # =====================================================

    def create_empty_label(
        self,
        text="No data available."
    ):

        ctk.CTkLabel(
            self.report_area,
            text=text
        ).pack(
            pady=10
        )
