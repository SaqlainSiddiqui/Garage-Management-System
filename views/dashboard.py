import customtkinter as ctk

from models.dashboard import (
    get_dashboard_statistics,
    get_recent_services,
    get_monthly_revenue
)

from utils.chart import show_revenue_chart

from config.theme import (
    DARK,
    LIGHT,
    get_theme_colors
)

class DashboardWindow(ctk.CTk):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title("Garage Management System")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        theme = self.user.get(
            "theme",
            "Dark"
        )

        ctk.set_appearance_mode(
            theme
        )

        ctk.set_default_color_theme(
            "blue"
        )

        self.colors = get_theme_colors(
            theme
        )

        # Build the widgets immediately. Without this call,
        # main_area/sidebar do not exist and theme switching
        # raises attribute/Tkinter errors.
        self.create_layout()

    def create_layout(self):
        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=self.colors["sidebar"]
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo / title
        logo = ctk.CTkLabel(
            self.sidebar,
            text="🚗 GARAGE\nMANAGEMENT",
            text_color=self.colors["text"],
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        logo.pack(
            pady=(35, 40)
        )

        # Navigation buttons
        self.create_sidebar_button(
            "Dashboard",
            self.show_dashboard
        )

        self.create_sidebar_button(
            "Customers",
            self.show_customers
        )

        self.create_sidebar_button(
            "Vehicles",
            self.show_vehicles
        )

        self.create_sidebar_button(
            "Services",
            self.show_services
        )

        self.create_sidebar_button(
            "Spare Parts",
            self.show_spare_parts
        )

        self.create_sidebar_button(
            "Billing",
            self.show_billing
        )

        self.create_sidebar_button(
            "Reports",
            self.show_reports
        )

        self.create_sidebar_button(
            "Revenue Analytics",
            self.show_revenue_analytics
        )

        self.create_sidebar_button(
            "Settings",
            self.show_settings
        )

        # Logout
        logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            height=42,
            corner_radius=8,

            fg_color=self.colors[
                "danger"
            ],

            hover_color=self.colors[
                "danger_hover"
            ],

            text_color="#FFFFFF",

            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),

            command=self.logout
        )

        logout_button.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25
        )

        # =========================
        # MAIN AREA
        # =========================

        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.colors["background"]
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard()

    # =========================
    # SIDEBAR BUTTON
    # =========================

    # =========================
    # APPLY THEME
    # =========================

    def apply_theme(self, theme):

        ctk.set_appearance_mode(
            theme
        )

        self.user["theme"] = theme

        self.colors = get_theme_colors(
            theme
        )

        # Main background
        self.main_area.configure(
            fg_color=self.colors[
                "background"
            ]
        )

        # Sidebar
        self.sidebar.configure(
            fg_color=self.colors[
                "sidebar"
            ]
        )

        # Update sidebar buttons
        for widget in self.sidebar.winfo_children():

            if isinstance(
                widget,
                ctk.CTkButton
            ):

                # Logout
                if widget.cget(
                    "text"
                ) == "Logout":

                    widget.configure(
                        fg_color=self.colors[
                            "danger"
                        ],

                        hover_color=self.colors[
                            "danger_hover"
                        ],

                        text_color="#FFFFFF"
                    )

                else:

                    widget.configure(
                        fg_color="transparent",

                        hover_color=self.colors[
                            "surface_hover"
                        ],

                        text_color=self.colors[
                            "text"
                        ]
                    )

            elif isinstance(
                widget,
                ctk.CTkLabel
            ):

                widget.configure(
                    text_color=self.colors[
                        "text"
                    ]
                )

    def show_revenue_analytics(self):

        monthly_data = get_monthly_revenue()

        if not monthly_data:

            from tkinter import messagebox

            messagebox.showinfo(
                "Revenue Analytics",
                "No paid invoice data available yet."
            )

            return

        show_revenue_chart(
            monthly_data
        )


    def create_sidebar_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,

            text=text,

            height=42,

            corner_radius=8,

            fg_color="transparent",

            hover_color=self.colors[
                "surface_hover"
            ],

            text_color=self.colors[
                "text"
            ],

            anchor="w",

            font=ctk.CTkFont(
                size=14
            ),

            command=command
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4
        )

        return button

    # =========================
    # CLEAR MAIN AREA
    # =========================

    def clear_main_area(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):

        self.clear_main_area()

        # =========================
        # GET STATISTICS
        # =========================

        stats = get_dashboard_statistics()

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self.main_area,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        welcome = ctk.CTkLabel(
            self.main_area,
            text=f"Welcome, {self.user['name']}",
            font=ctk.CTkFont(size=15)
        )

        welcome.pack(
            anchor="w",
            padx=35,
            pady=(0, 25)
        )

        # =========================
        # STATISTICS
        # =========================

        stats_frame = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            padx=25
        )

        self.create_stat_card(
            stats_frame,
            "Customers",
            str(stats["total_customers"]),
            0
        )

        self.create_stat_card(
            stats_frame,
            "Vehicles",
            str(stats["total_vehicles"]),
            1
        )

        self.create_stat_card(
            stats_frame,
            "Services",
            str(stats["total_services"]),
            2
        )

        self.create_stat_card(
            stats_frame,
            "Revenue",
            f"₹{stats['total_revenue']:.2f}",
            3
        )

        # =========================
        # SECONDARY STATS
        # =========================

        secondary_frame = ctk.CTkFrame(
            self.main_area,
            fg_color="transparent"
        )

        secondary_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.create_stat_card(
            secondary_frame,
            "Today's Services",
            str(stats["today_services"]),
            0
        )

        self.create_stat_card(
            secondary_frame,
            "Pending Services",
            str(stats["pending_services"]),
            1
        )

        self.create_stat_card(
            secondary_frame,
            "Low Stock Items",
            str(stats["low_stock_parts"]),
            2
        )

        self.create_stat_card(
            secondary_frame,
            "Pending Revenue",
            f"₹{stats['pending_revenue']:.2f}",
            3
        )

        # =========================
        # RECENT SERVICES
        # =========================

        recent_frame = ctk.CTkFrame(
            self.main_area
        )

        recent_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        recent_title = ctk.CTkLabel(
            recent_frame,
            text="Recent Service Activity",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        recent_title.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        recent_services = get_recent_services()

        if not recent_services:

            no_data = ctk.CTkLabel(
                recent_frame,
                text="No service records available yet."
            )

            no_data.pack(
                pady=30
            )

        else:

            for service in recent_services:

                text = (
                    f"{service.get('service_date', '')} | "
                    f"{service.get('service_type', '')} | "
                    f"₹{service.get('total_cost', 0):.2f} | "
                    f"{service.get('status', '')}"
                )

                label = ctk.CTkLabel(
                    recent_frame,
                    text=text,
                    anchor="w"
                )

                label.pack(
                    fill="x",
                    padx=20,
                    pady=5
                )

    # =========================
    # STAT CARD
    # =========================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            height=120,
            corner_radius=15
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            pady=10,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13)
        )

        title_label.pack(
            pady=(25, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        value_label.pack()

    # =========================
    # PLACEHOLDER PAGES
    # =========================

    def show_page(self, page_name):

        self.clear_main_area()

        label = ctk.CTkLabel(
            self.main_area,
            text=f"{page_name} Module",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        label.pack(
            pady=50
        )

        coming = ctk.CTkLabel(
            self.main_area,
            text="This module will be implemented next.",
            font=ctk.CTkFont(size=15)
        )

        coming.pack()

    def show_customers(self):

        self.clear_main_area()

        from views.customer import CustomerPage

        customer_page = CustomerPage(
            self.main_area
        )

        customer_page.pack(
            fill="both",
            expand=True
        )

    def show_vehicles(self):

        self.clear_main_area()

        from views.vehicle import VehiclePage

        vehicle_page = VehiclePage(
            self.main_area
        )

        vehicle_page.pack(
            fill="both",
            expand=True
        )

    def show_services(self):

        self.clear_main_area()

        from views.service import ServicePage

        service_page = ServicePage(
            self.main_area
        )

        service_page.pack(
            fill="both",
            expand=True
        )

    def show_spare_parts(self):

        self.clear_main_area()

        from views.spare_parts import SparePartsPage

        spare_parts_page = SparePartsPage(
            self.main_area
        )

        spare_parts_page.pack(
            fill="both",
            expand=True
        )

    def show_billing(self):

        self.clear_main_area()

        from views.billing import BillingPage

        billing_page = BillingPage(
            self.main_area
        )

        billing_page.pack(
            fill="both",
            expand=True
        )

    def show_reports(self):

        self.clear_main_area()

        from views.reports import ReportsPage

        reports_page = ReportsPage(
            self.main_area
        )

        reports_page.pack(
            fill="both",
            expand=True
        )

    def show_settings(self):

        self.clear_main_area()

        from views.settings import SettingsPage

        settings_page = SettingsPage(
            self.main_area,
            self.user,
            theme_callback=self.apply_theme
        )

        settings_page.pack(
            fill="both",
            expand=True
        )

    # =========================
    # LOGOUT
    # =========================

    def logout(self):

        self.destroy()

        # Login will be connected here later.


if __name__ == "__main__":

    test_user = {
        "name": "System Administrator",
        "email": "admin@garage.com",
        "role": "admin"
    }

    app = DashboardWindow(test_user)
    app.mainloop()