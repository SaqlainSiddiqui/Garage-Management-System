import customtkinter as ctk
from tkinter import messagebox

from models.vehicle import (
    create_vehicle,
    get_all_vehicles,
    update_vehicle,
    delete_vehicle,
    search_vehicles
)

from models.customer import get_all_customers


class VehiclePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_vehicle_id = None
        self.customers = []

        self.create_ui()
        self.load_customers()
        self.load_vehicles()

    # =========================
    # UI
    # =========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Vehicle Management",
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

        # Customer
        ctk.CTkLabel(
            form,
            text="Customer"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=(15, 5)
        )

        self.customer_menu = ctk.CTkComboBox(
            form,
            width=190,
            values=["No customers"]
        )

        self.customer_menu.grid(
            row=1,
            column=0,
            padx=8,
            pady=(0, 15)
        )

        # Vehicle Number
        self.vehicle_number_entry = self.create_entry(
            form,
            "Vehicle Number",
            1
        )

        # Brand
        self.brand_entry = self.create_entry(
            form,
            "Brand",
            2
        )

        # Model
        self.model_entry = self.create_entry(
            form,
            "Model",
            3
        )

        # Year
        self.year_entry = self.create_entry(
            form,
            "Year",
            4
        )

        # Fuel type
        ctk.CTkLabel(
            form,
            text="Fuel Type"
        ).grid(
            row=0,
            column=5,
            padx=8,
            pady=(15, 5)
        )

        self.fuel_menu = ctk.CTkComboBox(
            form,
            width=150,
            values=[
                "Petrol",
                "Diesel",
                "CNG",
                "Electric",
                "Hybrid"
            ]
        )

        self.fuel_menu.grid(
            row=1,
            column=5,
            padx=8,
            pady=(0, 15)
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            pady=10
        )

        ctk.CTkButton(
            button_frame,
            text="Add Vehicle",
            command=self.add_vehicle
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_vehicle
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Delete",
            fg_color="#c0392b",
            hover_color="#962d22",
            command=self.delete_vehicle
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
            placeholder_text="Search vehicle..."
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
            command=self.load_vehicles
        ).pack(
            side="left"
        )

        # Vehicle list
        self.vehicle_list = ctk.CTkScrollableFrame(
            self
        )

        self.vehicle_list.pack(
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
            width=160,
            placeholder_text=placeholder
        )

        entry.grid(
            row=1,
            column=column,
            padx=8,
            pady=(0, 15)
        )

        ctk.CTkLabel(
            parent,
            text=placeholder
        ).grid(
            row=0,
            column=column,
            padx=8,
            pady=(15, 5)
        )

        return entry

    # =========================
    # CUSTOMER DATA
    # =========================

    def load_customers(self):

        self.customers = get_all_customers()

        customer_names = [
            f"{customer['name']} | {customer['phone']}"
            for customer in self.customers
        ]

        if customer_names:
            self.customer_menu.configure(
                values=customer_names
            )
            self.customer_menu.set(
                customer_names[0]
            )
        else:
            self.customer_menu.configure(
                values=["No customers"]
            )
            self.customer_menu.set(
                "No customers"
            )

    def get_selected_customer_id(self):

        selected = self.customer_menu.get()

        for customer in self.customers:

            customer_text = (
                f"{customer['name']} | "
                f"{customer['phone']}"
            )

            if customer_text == selected:
                return str(customer["_id"])

        return None

    # =========================
    # ADD
    # =========================

    def add_vehicle(self):

        customer_id = self.get_selected_customer_id()

        vehicle_number = (
            self.vehicle_number_entry.get()
        )

        brand = self.brand_entry.get()
        model = self.model_entry.get()
        year = self.year_entry.get()
        fuel_type = self.fuel_menu.get()

        if not customer_id:
            messagebox.showwarning(
                "Validation",
                "Please add a customer first."
            )
            return

        if not vehicle_number or not brand or not model:
            messagebox.showwarning(
                "Validation",
                "Vehicle number, brand and model are required."
            )
            return

        try:

            create_vehicle(
                customer_id,
                vehicle_number,
                brand,
                model,
                year,
                fuel_type
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Year must be a valid number."
            )
            return

        messagebox.showinfo(
            "Success",
            "Vehicle added successfully."
        )

        self.clear_form()
        self.load_vehicles()

    # =========================
    # LOAD
    # =========================

    def load_vehicles(self):

        vehicles = get_all_vehicles()

        self.display_vehicles(
            vehicles
        )

    # =========================
    # DISPLAY
    # =========================

    def display_vehicles(
        self,
        vehicles
    ):

        for widget in self.vehicle_list.winfo_children():
            widget.destroy()

        customer_map = {
            str(customer["_id"]): customer["name"]
            for customer in self.customers
        }

        for vehicle in vehicles:

            frame = ctk.CTkFrame(
                self.vehicle_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            customer_name = customer_map.get(
                str(vehicle.get("customer_id")),
                "Unknown Customer"
            )

            info = (
                f"{vehicle['vehicle_number']}   |   "
                f"{vehicle['brand']} "
                f"{vehicle['model']}   |   "
                f"{vehicle.get('year', '')}   |   "
                f"{vehicle.get('fuel_type', '')}   |   "
                f"Owner: {customer_name}"
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

            edit_button = ctk.CTkButton(
                frame,
                text="Edit",
                width=70,
                command=lambda v=vehicle:
                self.select_vehicle(v)
            )

            edit_button.pack(
                side="right",
                padx=10
            )

    # =========================
    # SELECT
    # =========================

    def select_vehicle(
        self,
        vehicle
    ):

        self.selected_vehicle_id = str(
            vehicle["_id"]
        )

        self.clear_entries_only()

        # Select customer
        customer_id = str(
            vehicle.get("customer_id")
        )

        for customer in self.customers:

            if str(customer["_id"]) == customer_id:

                text = (
                    f"{customer['name']} | "
                    f"{customer['phone']}"
                )

                self.customer_menu.set(
                    text
                )

                break

        self.vehicle_number_entry.insert(
            0,
            vehicle.get(
                "vehicle_number",
                ""
            )
        )

        self.brand_entry.insert(
            0,
            vehicle.get(
                "brand",
                ""
            )
        )

        self.model_entry.insert(
            0,
            vehicle.get(
                "model",
                ""
            )
        )

        if vehicle.get("year"):
            self.year_entry.insert(
                0,
                str(vehicle["year"])
            )

        self.fuel_menu.set(
            vehicle.get(
                "fuel_type",
                "Petrol"
            )
        )

    # =========================
    # UPDATE
    # =========================

    def update_vehicle(self):

        if not self.selected_vehicle_id:
            messagebox.showwarning(
                "Update",
                "Select a vehicle first."
            )
            return

        customer_id = self.get_selected_customer_id()

        try:

            update_vehicle(
                self.selected_vehicle_id,
                customer_id,
                self.vehicle_number_entry.get(),
                self.brand_entry.get(),
                self.model_entry.get(),
                self.year_entry.get(),
                self.fuel_menu.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Year must be a valid number."
            )
            return

        messagebox.showinfo(
            "Success",
            "Vehicle updated successfully."
        )

        self.clear_form()
        self.load_vehicles()

    # =========================
    # DELETE
    # =========================

    def delete_vehicle(self):

        if not self.selected_vehicle_id:
            messagebox.showwarning(
                "Delete",
                "Select a vehicle first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this vehicle?"
        )

        if not confirm:
            return

        delete_vehicle(
            self.selected_vehicle_id
        )

        messagebox.showinfo(
            "Success",
            "Vehicle deleted successfully."
        )

        self.clear_form()
        self.load_vehicles()

    # =========================
    # SEARCH
    # =========================

    def search(self):

        text = self.search_entry.get().strip()

        if not text:
            self.load_vehicles()
            return

        vehicles = search_vehicles(text)

        self.display_vehicles(
            vehicles
        )

    # =========================
    # CLEAR
    # =========================

    def clear_entries_only(self):

        self.vehicle_number_entry.delete(
            0,
            "end"
        )

        self.brand_entry.delete(
            0,
            "end"
        )

        self.model_entry.delete(
            0,
            "end"
        )

        self.year_entry.delete(
            0,
            "end"
        )

    def clear_form(self):

        self.selected_vehicle_id = None

        self.clear_entries_only()

        if self.customers:

            first = self.customers[0]

            self.customer_menu.set(
                f"{first['name']} | "
                f"{first['phone']}"
            )

        self.fuel_menu.set("Petrol")