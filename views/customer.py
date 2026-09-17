import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from models.customer import (
    create_customer,
    get_all_customers,
    update_customer,
    delete_customer,
    search_customers
)

from models.vehicle import get_vehicles_by_customer
from models.service import get_services_by_vehicle


class CustomerPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_customer_id = None

        self.create_ui()
        self.load_customers()

    # =========================
    # UI
    # =========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Customer Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        # Form
        form = ctk.CTkFrame(self)

        form.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.name_entry = self.create_entry(
            form,
            "Customer Name",
            0
        )

        self.phone_entry = self.create_entry(
            form,
            "Phone Number",
            1
        )

        self.email_entry = self.create_entry(
            form,
            "Email",
            2
        )

        self.address_entry = self.create_entry(
            form,
            "Address",
            3
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="Add Customer",
            command=self.add_customer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_customer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Delete",
            fg_color="#c0392b",
            hover_color="#962d22",
            command=self.delete_customer
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        # Search
        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Search customer..."
        )

        self.search_entry.pack(
            side="left"
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            search_frame,
            text="Show All",
            command=self.load_customers
        ).pack(
            side="left"
        )

        # Customer list
        self.customer_list = ctk.CTkScrollableFrame(
            self
        )

        self.customer_list.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 25)
        )

    # =========================
    # ENTRY
    # =========================

    def create_entry(
        self,
        parent,
        placeholder,
        column
    ):

        entry = ctk.CTkEntry(
            parent,
            width=200,
            placeholder_text=placeholder
        )

        entry.grid(
            row=0,
            column=column,
            padx=8,
            pady=15
        )

        return entry

    # =========================
    # ADD
    # =========================

    def add_customer(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not name or not phone:
            messagebox.showwarning(
                "Validation",
                "Name and phone are required."
            )
            return

        create_customer(
            name,
            phone,
            email,
            address
        )

        messagebox.showinfo(
            "Success",
            "Customer added successfully."
        )

        self.clear_form()
        self.load_customers()

    # =========================
    # LOAD
    # =========================

    def load_customers(self):

        customers = get_all_customers()

        self.display_customers(customers)

    # =========================
    # DISPLAY
    # =========================

    def display_customers(
        self,
        customers
    ):

        for widget in self.customer_list.winfo_children():
            widget.destroy()

        for customer in customers:

            frame = ctk.CTkFrame(
                self.customer_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            info = (
                f"{customer['name']}   |   "
                f"{customer['phone']}   |   "
                f"{customer['email']}"
            )

            label = ctk.CTkLabel(
                frame,
                text=info,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=15,
                pady=12
            )

            view_button = ctk.CTkButton(
                frame,
                text="View Vehicles",
                width=110,
                command=lambda c=customer:
                self.show_customer_vehicles(c)
            )

            view_button.pack(
                side="right",
                padx=5
            )

            edit_button = ctk.CTkButton(
                frame,
                text="Edit",
                width=70,
                command=lambda c=customer:
                self.select_customer(c)
            )

            edit_button.pack(
                side="right",
                padx=5
            )

    # =========================
    # SELECT
    # =========================

    def select_customer(
        self,
        customer
    ):

        self.selected_customer_id = str(
            customer["_id"]
        )

        self.clear_entries_only()

        self.name_entry.insert(
            0,
            customer.get("name", "")
        )

        self.phone_entry.insert(
            0,
            customer.get("phone", "")
        )

        self.email_entry.insert(
            0,
            customer.get("email", "")
        )

        self.address_entry.insert(
            0,
            customer.get("address", "")
        )

    # =========================
    # UPDATE
    # =========================

    def update_customer(self):

        if not self.selected_customer_id:
            messagebox.showwarning(
                "Update",
                "Select a customer first."
            )
            return

        update_customer(
            self.selected_customer_id,
            self.name_entry.get(),
            self.phone_entry.get(),
            self.email_entry.get(),
            self.address_entry.get()
        )

        messagebox.showinfo(
            "Success",
            "Customer updated successfully."
        )

        self.clear_form()
        self.load_customers()

    # =========================
    # DELETE
    # =========================

    def delete_customer(self):

        if not self.selected_customer_id:
            messagebox.showwarning(
                "Delete",
                "Select a customer first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this customer?"
        )

        if not confirm:
            return

        delete_customer(
            self.selected_customer_id
        )

        messagebox.showinfo(
            "Success",
            "Customer deleted successfully."
        )

        self.clear_form()
        self.load_customers()

    # =========================
    # SEARCH
    # =========================

    def search(self):

        text = self.search_entry.get().strip()

        if not text:
            self.load_customers()
            return

        customers = search_customers(text)

        self.display_customers(customers)

    # =========================
    # CLEAR
    # =========================

    def clear_entries_only(self):

        self.name_entry.delete(
            0,
            "end"
        )

        self.phone_entry.delete(
            0,
            "end"
        )

        self.email_entry.delete(
            0,
            "end"
        )

        self.address_entry.delete(
            0,
            "end"
        )

    def clear_form(self):

        self.selected_customer_id = None

        self.clear_entries_only()

        # =========================
    # CUSTOMER VEHICLES
    # =========================

    def show_customer_vehicles(self, customer):

        customer_id = str(customer["_id"])

        try:
            vehicles = get_vehicles_by_customer(customer_id)
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load customer vehicles.\n\n{e}"
            )
            return

        vehicle_window = ctk.CTkToplevel(self)
        vehicle_window.title("Customer Vehicles")
        vehicle_window.geometry("800x600")
        vehicle_window.minsize(650, 450)
        vehicle_window.transient(self.winfo_toplevel())

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(vehicle_window)
        header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            header,
            text="Customer Vehicles",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            header,
            text=(
                f"{customer.get('name', '')}  |  "
                f"{customer.get('phone', '')}"
            ),
            font=ctk.CTkFont(size=15)
        ).pack(pady=(0, 15))

        # =========================
        # Vehicle Count
        # =========================

        ctk.CTkLabel(
            vehicle_window,
            text=f"Total Vehicles: {len(vehicles)}",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # =========================
        # Vehicle List
        # =========================

        vehicle_list = ctk.CTkScrollableFrame(
            vehicle_window
        )

        vehicle_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        if not vehicles:

            ctk.CTkLabel(
                vehicle_list,
                text="No vehicles registered for this customer.",
                font=ctk.CTkFont(size=16)
            ).pack(pady=50)

            return

        # =========================
        # Display Vehicles
        # =========================

        for index, vehicle in enumerate(
            vehicles,
            start=1
        ):

            card = ctk.CTkFrame(vehicle_list)

            card.pack(
                fill="x",
                padx=5,
                pady=8
            )

            vehicle_number = vehicle.get(
                "vehicle_number",
                "Unknown"
            )

            brand = vehicle.get(
                "brand",
                ""
            )

            model = vehicle.get(
                "model",
                ""
            )

            year = vehicle.get(
                "year",
                ""
            )

            fuel_type = vehicle.get(
                "fuel_type",
                ""
            )

            # Vehicle number

            ctk.CTkLabel(
                card,
                text=f"{index}. {vehicle_number}",
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            # Vehicle details

            ctk.CTkLabel(
                card,
                text=(
                    f"Vehicle: {brand} {model}    |    "
                    f"Year: {year}    |    "
                    f"Fuel: {fuel_type}"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(0, 10)
            )

            # =========================
            # Vehicle Actions
            # =========================

            button_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            button_frame.pack(
                fill="x",
                padx=15,
                pady=(0, 12)
            )

            # Service History
            ctk.CTkButton(
                button_frame,
                text="Service History",
                width=140,
                command=lambda v=vehicle:
                self.show_vehicle_service_history(v)
            ).pack(
                side="right",
                padx=(5, 0)
            )

            # Vehicle Summary
            ctk.CTkButton(
                button_frame,
                text="Vehicle Summary",
                width=140,
                command=lambda v=vehicle:
                self.show_vehicle_summary(v)
            ).pack(
                side="right",
                padx=(0, 5)
            )

    def show_vehicle_summary(self, vehicle):

        vehicle_id = str(vehicle["_id"])

        try:
            services = get_services_by_vehicle(vehicle_id)
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load vehicle summary.\n\n{e}"
            )
            return

        # =========================
        # Vehicle Information
        # =========================

        vehicle_number = vehicle.get(
            "vehicle_number",
            "Unknown"
        )

        brand = vehicle.get(
            "brand",
            ""
        )

        model = vehicle.get(
            "model",
            ""
        )

        year = vehicle.get(
            "year",
            ""
        )

        fuel_type = vehicle.get(
            "fuel_type",
            ""
        )

        # =========================
        # Calculate Summary
        # =========================

        total_services = len(services)

        total_spent = 0

        last_service_date = None

         # =========================
        # Calculate Summary
        # =========================

        total_services = len(services)

        total_spent = 0

        last_service_date = None

        next_service_date = None

        # Today's date
        today = datetime.today().date()

        for service in services:

            # -------------------------
            # Total Amount Spent
            # -------------------------

            total_spent += float(
                service.get(
                    "total_cost",
                    0
                ) or 0
            )

            # -------------------------
            # Last Service Date
            # -------------------------

            service_date = service.get(
                "service_date"
            )

            if service_date:

                try:

                    service_date_obj = datetime.strptime(
                        str(service_date),
                        "%Y-%m-%d"
                    ).date()

                    if (
                        last_service_date is None
                        or service_date_obj >
                        last_service_date
                    ):
                        last_service_date = service_date_obj

                except (ValueError, TypeError):

                    pass

            # -------------------------
            # Next Service Date
            # -------------------------

            upcoming_date = service.get(
                "next_service_date"
            )

            if upcoming_date:

                try:

                    upcoming_date_obj = datetime.strptime(
                        str(upcoming_date),
                        "%Y-%m-%d"
                    ).date()

                    # Only consider future dates
                    if upcoming_date_obj >= today:

                        if (
                            next_service_date is None
                            or upcoming_date_obj <
                            next_service_date
                        ):
                            next_service_date = upcoming_date_obj

                except (ValueError, TypeError):

                    pass

        # =========================
        # Create Window
        # =========================

        summary_window = ctk.CTkToplevel(
            self
        )

        summary_window.title(
            "Vehicle Summary"
        )

        summary_window.geometry(
            "800x600"
        )

        summary_window.minsize(
            650,
            500
        )

        summary_window.transient(
            self.winfo_toplevel()
        )

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(
            summary_window
        )

        header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            header,
            text="Vehicle Summary",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            header,
            text=(
                f"{vehicle_number}  |  "
                f"{brand} {model}"
            ),
            font=ctk.CTkFont(
                size=17
            )
        ).pack(
            pady=(0, 5)
        )

        ctk.CTkLabel(
            header,
            text=(
                f"Year: {year}    |    "
                f"Fuel: {fuel_type}"
            ),
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=(0, 15)
        )

        # =========================
        # Summary Cards
        # =========================

        cards_frame = ctk.CTkFrame(
            summary_window,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Total Services

        services_card = ctk.CTkFrame(
            cards_frame
        )

        services_card.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            services_card,
            text="Total Services",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            services_card,
            text=str(total_services),
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).pack(
            pady=(0, 15)
        )

        # Total Spent

        spent_card = ctk.CTkFrame(
            cards_frame
        )

        spent_card.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            spent_card,
            text="Total Amount Spent",
            font=ctk.CTkFont(
                size=14
            )
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            spent_card,
            text=f"₹{total_spent:,.2f}",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(0, 15)
        )

        cards_frame.grid_columnconfigure(
            0,
            weight=1
        )

        cards_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =========================
        # Service Dates
        # =========================

        dates_frame = ctk.CTkFrame(
            summary_window
        )

        dates_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        ctk.CTkLabel(
            dates_frame,
            text="Service Schedule",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            dates_frame,
            text=(
                "Last Service: "
                f"{last_service_date.strftime('%Y-%m-%d') if last_service_date else 'No service recorded'}"
            ),
            font=ctk.CTkFont(
                size=15
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=5
        )

        ctk.CTkLabel(
            dates_frame,
            text=(
                "Next Service: "
                f"{next_service_date.strftime('%Y-%m-%d') if next_service_date else 'Not scheduled'}"
            ),
            font=ctk.CTkFont(
                size=15
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=(5, 15)
        )

        # =========================
        # View History Button
        # =========================

        ctk.CTkButton(
            summary_window,
            text="View Complete Service History",
            width=240,
            height=40,
            command=lambda:
            self.show_vehicle_service_history(
                vehicle
            )
        ).pack(
            pady=15
        )

    def show_vehicle_service_history(self, vehicle):

        vehicle_id = str(vehicle["_id"])

        try:
            services = get_services_by_vehicle(vehicle_id)
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to load service history.\n\n{e}"
            )
            return

        service_window = ctk.CTkToplevel(self)

        service_window.title(
            "Vehicle Service History"
        )

        service_window.geometry(
            "900x650"
        )

        service_window.minsize(
            700,
            500
        )

        service_window.transient(
            self.winfo_toplevel()
        )

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(
            service_window
        )

        header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            header,
            text="Vehicle Service History",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(15, 5)
        )

        vehicle_number = vehicle.get(
            "vehicle_number",
            "Unknown"
        )

        brand = vehicle.get(
            "brand",
            ""
        )

        model = vehicle.get(
            "model",
            ""
        )

        ctk.CTkLabel(
            header,
            text=f"{vehicle_number}  |  {brand} {model}",
            font=ctk.CTkFont(size=15)
        ).pack(
            pady=(0, 15)
        )

        # =========================
        # Service Count
        # =========================

        ctk.CTkLabel(
            service_window,
            text=f"Total Services: {len(services)}",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # =========================
        # Service List
        # =========================

        service_list = ctk.CTkScrollableFrame(
            service_window
        )

        service_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        if not services:

            ctk.CTkLabel(
                service_list,
                text="No service history found for this vehicle.",
                font=ctk.CTkFont(size=16)
            ).pack(
                pady=50
            )

            return

        # =========================
        # Display Services
        # =========================

        for index, service in enumerate(
            services,
            start=1
        ):

            card = ctk.CTkFrame(
                service_list
            )

            card.pack(
                fill="x",
                padx=5,
                pady=8
            )

            service_type = service.get(
                "service_type",
                "Unknown"
            )

            service_date = service.get(
                "service_date",
                ""
            )

            mechanic = service.get(
                "mechanic",
                ""
            )

            status = service.get(
                "status",
                ""
            )

            total_cost = service.get(
                "total_cost",
                0
            )

            # =========================
            # Service Title
            # =========================

            ctk.CTkLabel(
                card,
                text=f"{index}. {service_type}",
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(12, 5)
            )

            # =========================
            # Service Information
            # =========================

            ctk.CTkLabel(
                card,
                text=(
                    f"Date: {service_date}    |    "
                    f"Mechanic: {mechanic}    |    "
                    f"Status: {status}"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=3
            )

            # =========================
            # Parts Used
            # =========================

            parts = service.get(
                "parts",
                []
            )

            ctk.CTkLabel(
                card,
                text="Parts Used:",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(8, 3)
            )

            if parts:

                for part in parts:

                    part_name = part.get(
                        "name",
                        "Unknown Part"
                    )

                    quantity = part.get(
                        "quantity",
                        0
                    )

                    price = part.get(
                        "price",
                        0
                    )

                    part_total = (
                        quantity * price
                    )

                    ctk.CTkLabel(
                        card,
                        text=(
                            f"• {part_name}  |  "
                            f"Qty: {quantity}  |  "
                            f"₹{price:,.2f} each  |  "
                            f"₹{part_total:,.2f}"
                        ),
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=25,
                        pady=2
                    )

            else:

                ctk.CTkLabel(
                    card,
                    text="• No spare parts used.",
                    anchor="w"
                ).pack(
                    fill="x",
                    padx=25,
                    pady=2
                )

            # =========================
            # Total Cost
            # =========================

            # =========================
            # Bottom Row
            # =========================

            bottom_frame = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            bottom_frame.pack(
                fill="x",
                padx=15,
                pady=(8, 12)
            )

            # Total cost
            ctk.CTkLabel(
                bottom_frame,
                text=f"Total Cost: ₹{total_cost:,.2f}",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                side="left"
            )

            # View details button
            ctk.CTkButton(
                bottom_frame,
                text="View Details",
                width=120,
                command=lambda s=service:
                self.show_service_details(s)
            ).pack(
                side="right"
            )

    def show_service_details(self, service):

        # =========================
        # Get Service Information
        # =========================

        service_type = service.get(
            "service_type",
            "Unknown"
        )

        service_date = service.get(
            "service_date",
            ""
        )

        status = service.get(
            "status",
            ""
        )

        mechanic = service.get(
            "mechanic",
            ""
        )

        odometer = service.get(
            "odometer",
            ""
        )

        labour_cost = service.get(
            "labour_cost",
            0
        )

        parts_total = service.get(
            "parts_total",
            0
        )

        total_cost = service.get(
            "total_cost",
            0
        )

        notes = service.get(
            "notes",
            ""
        )

        next_service_date = service.get(
            "next_service_date",
            ""
        )

        parts = service.get(
            "parts",
            []
        )

        # =========================
        # Create Window
        # =========================

        detail_window = ctk.CTkToplevel(self)

        detail_window.title(
            "Service Details"
        )

        detail_window.geometry(
            "850x700"
        )

        detail_window.minsize(
            700,
            550
        )

        detail_window.transient(
            self.winfo_toplevel()
        )

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(
            detail_window
        )

        header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            header,
            text="Service Details",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            pady=(15, 5)
        )

        ctk.CTkLabel(
            header,
            text=service_type,
            font=ctk.CTkFont(
                size=17
            )
        ).pack(
            pady=(0, 15)
        )

        # =========================
        # Scrollable Content
        # =========================

        content = ctk.CTkScrollableFrame(
            detail_window
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =========================
        # Service Information
        # =========================

        info_frame = ctk.CTkFrame(
            content
        )

        info_frame.pack(
            fill="x",
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            info_frame,
            text="Service Information",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        details = [
            ("Service Type", service_type),
            ("Service Date", service_date),
            ("Status", status),
            ("Mechanic", mechanic),
            ("Odometer", odometer),
            ("Next Service Date", next_service_date)
        ]

        for label, value in details:

            row = ctk.CTkFrame(
                info_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=15,
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=f"{label}:",
                width=150,
                anchor="w",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row,
                text=str(value) if value else "N/A",
                anchor="w"
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        # =========================
        # Parts Used
        # =========================

        parts_frame = ctk.CTkFrame(
            content
        )

        parts_frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            parts_frame,
            text="Spare Parts Used",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        if parts:

            for part in parts:

                part_name = part.get(
                    "name",
                    "Unknown Part"
                )

                quantity = part.get(
                    "quantity",
                    0
                )

                price = part.get(
                    "price",
                    0
                )

                part_total = (
                    quantity * price
                )

                row = ctk.CTkFrame(
                    parts_frame,
                    fg_color="transparent"
                )

                row.pack(
                    fill="x",
                    padx=15,
                    pady=3
                )

                ctk.CTkLabel(
                    row,
                    text=part_name,
                    anchor="w"
                ).pack(
                    side="left",
                    fill="x",
                    expand=True
                )

                ctk.CTkLabel(
                    row,
                    text=(
                        f"Qty: {quantity}   |   "
                        f"₹{price:,.2f}   |   "
                        f"₹{part_total:,.2f}"
                    ),
                    anchor="e"
                ).pack(
                    side="right"
                )

        else:

            ctk.CTkLabel(
                parts_frame,
                text="No spare parts were used.",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 15)
            )

        # Parts total

        ctk.CTkLabel(
            parts_frame,
            text=f"Parts Total: ₹{parts_total:,.2f}",
            font=ctk.CTkFont(
                weight="bold"
            ),
            anchor="e"
        ).pack(
            fill="x",
            padx=15,
            pady=(8, 15)
        )

        # =========================
        # Cost Summary
        # =========================

        cost_frame = ctk.CTkFrame(
            content
        )

        cost_frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            cost_frame,
            text="Cost Summary",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            cost_frame,
            text=f"Labour Cost: ₹{labour_cost:,.2f}",
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=4
        )

        ctk.CTkLabel(
            cost_frame,
            text=f"Parts Cost: ₹{parts_total:,.2f}",
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=4
        )

        ctk.CTkLabel(
            cost_frame,
            text=f"Total Service Cost: ₹{total_cost:,.2f}",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=(6, 15)
        )

        # =========================
        # Notes
        # =========================

        notes_frame = ctk.CTkFrame(
            content
        )

        notes_frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            notes_frame,
            text="Service Notes",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 8)
        )

        ctk.CTkLabel(
            notes_frame,
            text=notes if notes else "No notes available.",
            anchor="w",
            justify="left",
            wraplength=750
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )