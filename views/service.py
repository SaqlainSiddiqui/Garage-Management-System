import customtkinter as ctk
from tkinter import messagebox

from models.service import (
    create_service,
    get_all_services,
    delete_service,
    get_services_by_vehicle,
)

from models.vehicle import get_all_vehicles
from models.spare_part import get_all_spare_parts

from tkcalendar import DateEntry


class ServicePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        # =========================
        # DATA
        # =========================

        self.vehicles = []
        self.inventory_parts = []
        self.parts = []

        # =========================
        # CREATE UI
        # =========================

        self.create_ui()

        # =========================
        # LOAD DATA
        # =========================

        self.load_vehicles()
        self.load_inventory_parts()
        self.load_services()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        # =========================
        # TITLE
        # =========================

        title = ctk.CTkLabel(
            self,
            text="Service Management",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        # =========================
        # FORM AREA
        # =========================

        self.form_area = ctk.CTkScrollableFrame(
            self,
            height=450
        )

        self.form_area.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # =====================================================
        # VEHICLE
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Vehicle"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        self.vehicle_menu = ctk.CTkComboBox(
            self.form_area,
            width=250,
            values=["No vehicles"]
        )

        self.vehicle_menu.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        # =====================================================
        # SERVICE TYPE
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Service Type"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.service_type_menu = ctk.CTkComboBox(
            self.form_area,
            width=200,
            values=[
                "General Service",
                "Oil Change",
                "Full Service",
                "Brake Service",
                "Engine Repair",
                "AC Service",
                "Tyre Service",
                "Other"
            ]
        )

        self.service_type_menu.set(
            "General Service"
        )

        self.service_type_menu.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # =====================================================
        # MECHANIC
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Mechanic"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        self.mechanic_entry = ctk.CTkEntry(
            self.form_area,
            width=200,
            placeholder_text="Mechanic name"
        )

        self.mechanic_entry.grid(
            row=1,
            column=2,
            padx=10,
            pady=5
        )

        # =====================================================
        # ODOMETER
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Odometer (KM)"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        self.odometer_entry = ctk.CTkEntry(
            self.form_area,
            width=150,
            placeholder_text="35000"
        )

        self.odometer_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        # =====================================================
        # SERVICE DATE
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Service Date"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=(20, 5)
        )

        self.service_date = DateEntry(
            self.form_area,
            width=18,
            date_pattern="yyyy-mm-dd"
        )

        self.service_date.grid(
            row=3,
            column=0,
            padx=10,
            pady=5
        )

        # =====================================================
        # NEXT SERVICE DATE
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Next Service Date"
        ).grid(
            row=2,
            column=1,
            padx=10,
            pady=(20, 5)
        )

        self.next_service_date = DateEntry(
            self.form_area,
            width=18,
            date_pattern="yyyy-mm-dd"
        )

        self.next_service_date.grid(
            row=3,
            column=1,
            padx=10,
            pady=5
        )

        # =====================================================
        # STATUS
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Status"
        ).grid(
            row=2,
            column=2,
            padx=10,
            pady=(20, 5)
        )

        self.status_menu = ctk.CTkComboBox(
            self.form_area,
            width=180,
            values=[
                "Pending",
                "In Progress",
                "Completed",
                "Cancelled"
            ]
        )

        self.status_menu.set(
            "Completed"
        )

        self.status_menu.grid(
            row=3,
            column=2,
            padx=10,
            pady=5
        )

        # =====================================================
        # LABOUR COST
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Labour Cost"
        ).grid(
            row=2,
            column=3,
            padx=10,
            pady=(20, 5)
        )

        self.labour_entry = ctk.CTkEntry(
            self.form_area,
            width=150,
            placeholder_text="1500"
        )

        self.labour_entry.grid(
            row=3,
            column=3,
            padx=10,
            pady=5
        )

        # =====================================================
        # PARTS SECTION
        # =====================================================

        parts_title = ctk.CTkLabel(
            self.form_area,
            text="Spare Parts Used",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        parts_title.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=(25, 10)
        )

        # Part dropdown

        self.part_menu = ctk.CTkComboBox(
            self.form_area,
            width=300,
            values=["No parts"]
        )

        self.part_menu.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        # Quantity

        self.part_quantity_entry = ctk.CTkEntry(
            self.form_area,
            width=100,
            placeholder_text="Qty"
        )

        self.part_quantity_entry.grid(
            row=5,
            column=2,
            padx=10,
            pady=5
        )

        # Add part button

        ctk.CTkButton(
            self.form_area,
            text="Add Part",
            command=self.add_part
        ).grid(
            row=5,
            column=3,
            padx=10,
            pady=5
        )

        # =====================================================
        # PARTS LIST
        # =====================================================

        self.parts_list = ctk.CTkLabel(
            self.form_area,
            text="No parts added.",
            anchor="w",
            justify="left"
        )

        self.parts_list.grid(
            row=6,
            column=0,
            columnspan=4,
            sticky="w",
            padx=10,
            pady=10
        )

        # =====================================================
        # NOTES
        # =====================================================

        ctk.CTkLabel(
            self.form_area,
            text="Notes"
        ).grid(
            row=7,
            column=0,
            padx=10,
            pady=10
        )

        self.notes_entry = ctk.CTkTextbox(
            self.form_area,
            width=600,
            height=80
        )

        self.notes_entry.grid(
            row=7,
            column=1,
            columnspan=3,
            padx=10,
            pady=10
        )

        # =====================================================
        # CREATE SERVICE BUTTON
        # =====================================================

        ctk.CTkButton(
            self.form_area,
            text="Create Service Record",
            height=40,
            command=self.add_service
        ).grid(
            row=8,
            column=0,
            columnspan=4,
            pady=20
        )

        ctk.CTkButton(
            self.form_area,
            text="View Vehicle Service History",
            height=40,
            command=self.show_service_history
        ).grid(
            row=9,
            column=0,
            columnspan=4,
            pady=(0, 20)
        )


        # =====================================================
        # SERVICE SEARCH & FILTER
        # =====================================================

        filter_frame = ctk.CTkFrame(self)

        filter_frame.pack(
            fill="x",
            padx=25,
            pady=(10, 5)
        )

        # Search
        ctk.CTkLabel(
            filter_frame,
            text="Search:"
        ).pack(
            side="left",
            padx=(10, 5)
        )

        self.service_search_entry = ctk.CTkEntry(
            filter_frame,
            width=250,
            placeholder_text="Vehicle, service type, mechanic..."
        )

        self.service_search_entry.pack(
            side="left",
            padx=5
        )

        # Status filter
        ctk.CTkLabel(
            filter_frame,
            text="Status:"
        ).pack(
            side="left",
            padx=(15, 5)
        )

        self.service_status_filter = ctk.CTkComboBox(
            filter_frame,
            width=160,
            values=[
                "All",
                "Pending",
                "In Progress",
                "Completed",
                "Cancelled"
            ]
        )

        self.service_status_filter.set("All")

        self.service_status_filter.pack(
            side="left",
            padx=5
        )

        # Search button
        ctk.CTkButton(
            filter_frame,
            text="Search",
            width=100,
            command=self.filter_services
        ).pack(
            side="left",
            padx=5
        )

        # Show all button
        ctk.CTkButton(
            filter_frame,
            text="Show All",
            width=100,
            command=self.show_all_services
        ).pack(
            side="left",
            padx=5
        )

        # Service list
        self.service_list = ctk.CTkScrollableFrame(
            self
        )

        self.service_list.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

    # =========================================================
    # VEHICLES
    # =========================================================

    def load_vehicles(self):

        try:

            self.vehicles = get_all_vehicles()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load vehicles.\n\n{e}"
            )

            self.vehicles = []

        values = []

        for vehicle in self.vehicles:

            values.append(
                f"{vehicle.get('vehicle_number', '')} | "
                f"{vehicle.get('brand', '')} "
                f"{vehicle.get('model', '')}"
            )

        if values:

            self.vehicle_menu.configure(
                values=values
            )

            self.vehicle_menu.set(
                values[0]
            )

        else:

            self.vehicle_menu.configure(
                values=["No vehicles"]
            )

            self.vehicle_menu.set(
                "No vehicles"
            )

    # =========================================================
    # GET SELECTED VEHICLE
    # =========================================================

    def get_selected_vehicle_id(self):

        selected = self.vehicle_menu.get()

        for vehicle in self.vehicles:

            text = (
                f"{vehicle.get('vehicle_number', '')} | "
                f"{vehicle.get('brand', '')} "
                f"{vehicle.get('model', '')}"
            )

            if text == selected:

                return str(
                    vehicle["_id"]
                )

        return None

    # =========================================================
    # INVENTORY PARTS
    # =========================================================

    def load_inventory_parts(self):

        try:

            self.inventory_parts = (
                get_all_spare_parts()
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load spare parts.\n\n{e}"
            )

            self.inventory_parts = []

        values = []

        for part in self.inventory_parts:

            values.append(
                f"{part.get('name', '')} | "
                f"{part.get('part_number', '')} | "
                f"Stock: {part.get('stock', 0)} | "
                f"₹{float(part.get('selling_price', 0)):.2f}"
            )

        if values:

            self.part_menu.configure(
                values=values
            )

            self.part_menu.set(
                values[0]
            )

        else:

            self.part_menu.configure(
                values=["No parts"]
            )

            self.part_menu.set(
                "No parts"
            )

    # =========================================================
    # GET SELECTED INVENTORY PART
    # =========================================================

    def get_selected_inventory_part(self):

        selected = self.part_menu.get()

        for part in self.inventory_parts:

            text = (
                f"{part.get('name', '')} | "
                f"{part.get('part_number', '')} | "
                f"Stock: {part.get('stock', 0)} | "
                f"₹{float(part.get('selling_price', 0)):.2f}"
            )

            if text == selected:

                return part

        return None

    # =========================================================
    # ADD PART TO SERVICE
    # =========================================================

    def add_part(self):

        selected_part = (
            self.get_selected_inventory_part()
        )

        if not selected_part:

            messagebox.showwarning(
                "Validation",
                "Please select a spare part."
            )

            return

        quantity_text = (
            self.part_quantity_entry
            .get()
            .strip()
        )

        if not quantity_text:

            messagebox.showwarning(
                "Validation",
                "Please enter the quantity."
            )

            return

        try:

            quantity = int(
                quantity_text
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a whole number."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero."
            )

            return

        stock = int(
            selected_part.get(
                "stock",
                0
            )
        )

        # ==========================================
        # CHECK AVAILABLE STOCK
        # ==========================================

        if quantity > stock:

            messagebox.showerror(
                "Insufficient Stock",
                f"Only {stock} unit(s) of "
                f"{selected_part.get('name', '')} "
                f"are available."
            )

            return

        # ==========================================
        # CHECK IF SAME PART ALREADY EXISTS
        # ==========================================

        selected_part_id = str(
            selected_part["_id"]
        )

        for existing_part in self.parts:

            if (
                existing_part["part_id"]
                == selected_part_id
            ):

                new_quantity = (
                    existing_part["quantity"]
                    + quantity
                )

                if new_quantity > stock:

                    messagebox.showerror(
                        "Insufficient Stock",
                        f"You already added "
                        f"{existing_part['quantity']} "
                        f"unit(s).\n\n"
                        f"Available stock: {stock}"
                    )

                    return

                existing_part["quantity"] = (
                    new_quantity
                )

                self.update_parts_display()

                self.part_quantity_entry.delete(
                    0,
                    "end"
                )

                return

        # ==========================================
        # ADD NEW PART
        # ==========================================

        self.parts.append({
            "part_id": selected_part_id,
            "name": selected_part.get(
                "name",
                ""
            ),
            "quantity": quantity,
            "price": float(
                selected_part.get(
                    "selling_price",
                    0
                )
            )
        })

        self.update_parts_display()

        self.part_quantity_entry.delete(
            0,
            "end"
        )

    # =========================================================
    # DISPLAY PARTS
    # =========================================================

    def update_parts_display(self):

        if not self.parts:

            self.parts_list.configure(
                text="No parts added."
            )

            return

        lines = []

        total_parts_cost = 0

        for index, part in enumerate(
            self.parts,
            start=1
        ):

            quantity = float(
                part["quantity"]
            )

            price = float(
                part["price"]
            )

            total = (
                quantity * price
            )

            total_parts_cost += total

            lines.append(
                f"{index}. "
                f"{part['name']} | "
                f"Qty: {part['quantity']} | "
                f"Price: ₹{price:.2f} | "
                f"Total: ₹{total:.2f}"
            )

        lines.append("")
        lines.append(
            f"Parts Total: "
            f"₹{total_parts_cost:.2f}"
        )

        self.parts_list.configure(
            text="\n".join(lines)
        )

    # =========================================================
    # CREATE SERVICE
    # =========================================================

    def add_service(self):

        # ==========================================
        # VEHICLE
        # ==========================================

        vehicle_id = (
            self.get_selected_vehicle_id()
        )

        if not vehicle_id:

            messagebox.showwarning(
                "Validation",
                "Please select a vehicle."
            )

            return

        # ==========================================
        # MECHANIC
        # ==========================================

        mechanic = (
            self.mechanic_entry
            .get()
            .strip()
        )

        if not mechanic:

            messagebox.showwarning(
                "Validation",
                "Please enter mechanic name."
            )

            return

        # ==========================================
        # ODOMETER
        # ==========================================

        odometer_text = (
            self.odometer_entry
            .get()
            .strip()
        )

        if not odometer_text:

            odometer_text = "0"

        try:

            odometer = int(
                odometer_text
            )

            if odometer < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Odometer",
                "Odometer must be a valid positive number."
            )

            return

        # ==========================================
        # LABOUR
        # ==========================================

        labour_text = (
            self.labour_entry
            .get()
            .strip()
        )

        if not labour_text:

            labour_text = "0"

        try:

            labour = float(
                labour_text
            )

            if labour < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Labour Cost",
                "Labour cost must be a valid number."
            )

            return

        # ==========================================
        # DATES
        # ==========================================

        service_date = (
            self.service_date
            .get_date()
            .strftime("%Y-%m-%d")
        )

        next_service_date = (
            self.next_service_date
            .get_date()
            .strftime("%Y-%m-%d")
        )

        # ==========================================
        # NOTES
        # ==========================================

        notes = (
            self.notes_entry
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        # ==========================================
        # CREATE SERVICE
        # ==========================================

        try:

            service_id = create_service(
                vehicle_id=vehicle_id,
                service_date=service_date,
                service_type=(
                    self.service_type_menu.get()
                ),
                odometer=odometer,
                mechanic=mechanic,
                labour_cost=labour,
                parts=self.parts,
                notes=notes,
                next_service_date=(
                    next_service_date
                ),
                status=self.status_menu.get()
            )

        except ValueError as e:

            messagebox.showerror(
                "Unable to Create Service",
                str(e)
            )

            # Refresh inventory because
            # another operation may have
            # changed stock.

            self.load_inventory_parts()

            return

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to create service.\n\n{e}"
            )

            return

        # ==========================================
        # SUCCESS
        # ==========================================

        messagebox.showinfo(
            "Success",
            "Service record created successfully.\n\n"
            "Inventory stock has been updated."
        )

        self.clear_form()

        # Refresh inventory so the
        # new stock values appear.

        self.load_inventory_parts()

        self.load_services()

    # =========================================================
    # LOAD SERVICES
    # =========================================================

    def load_services(self):

        try:

            services = get_all_services()
            

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load services.\n\n{e}"
            )

            return

        self.display_services(
            services
        )
        # Clear previous records

        for widget in (
            self.service_list.winfo_children()
        ):

            widget.destroy()

        # Create vehicle lookup

        vehicle_map = {}

        for vehicle in self.vehicles:

            vehicle_map[
                str(vehicle["_id"])
            ] = (
                f"{vehicle.get('vehicle_number', '')} "
                f"{vehicle.get('brand', '')} "
                f"{vehicle.get('model', '')}"
            )

        # ==========================================
        # DISPLAY SERVICES
        # ==========================================

        if not services:

            label = ctk.CTkLabel(
                self.service_list,
                text="No service records found."
            )

            label.pack(
                pady=30
            )

            return

        for service in services:

            frame = ctk.CTkFrame(
                self.service_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            vehicle_name = vehicle_map.get(
                str(
                    service.get(
                        "vehicle_id",
                        ""
                    )
                ),
                "Unknown Vehicle"
            )

            total_cost = float(
                service.get(
                    "total_cost",
                    0
                )
            )

            text = (
                f"{vehicle_name} | "
                f"{service.get('service_type', '')} | "
                f"{service.get('service_date', '')} | "
                f"₹{total_cost:.2f} | "
                f"{service.get('status', '')}"
            )

            label = ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=15,
                pady=12
            )

            delete_button = ctk.CTkButton(
                frame,
                text="Delete",
                width=70,
                fg_color="#c0392b",
                hover_color="#962d22",
                command=lambda s=service:
                self.delete_service(s)
            )

            delete_button.pack(
                side="right",
                padx=10
            )

    # =========================================================
    # DELETE SERVICE
    # =========================================================

    def delete_service(self, service):

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this service record?"
        )

        if not confirm:
            return

        try:

            deleted = delete_service(
                str(
                    service["_id"]
                )
            )

            if deleted:

                messagebox.showinfo(
                    "Success",
                    "Service deleted successfully."
                )

            else:

                messagebox.showwarning(
                    "Not Found",
                    "Service record was not found."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to delete service.\n\n{e}"
            )

            return

        self.load_services()

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        # Clear selected parts

        self.parts = []

        self.update_parts_display()

        # Mechanic

        self.mechanic_entry.delete(
            0,
            "end"
        )

        # Odometer

        self.odometer_entry.delete(
            0,
            "end"
        )

        # Labour

        self.labour_entry.delete(
            0,
            "end"
        )

        # Notes

        self.notes_entry.delete(
            "1.0",
            "end"
        )

        # Dropdown defaults

        self.service_type_menu.set(
            "General Service"
        )

        self.status_menu.set(
            "Completed"
        )

        # Vehicle

        if self.vehicles:

            first_vehicle = self.vehicles[0]

            self.vehicle_menu.set(
                f"{first_vehicle.get('vehicle_number', '')} | "
                f"{first_vehicle.get('brand', '')} "
                f"{first_vehicle.get('model', '')}"
            )

        # Part quantity

        self.part_quantity_entry.delete(
            0,
            "end"
        )

        # First inventory part

        if self.inventory_parts:

            first_part = self.inventory_parts[0]

            self.part_menu.set(
                f"{first_part.get('name', '')} | "
                f"{first_part.get('part_number', '')} | "
                f"Stock: {first_part.get('stock', 0)} | "
                f"₹{float(first_part.get('selling_price', 0)):.2f}"
            )

        else:

            self.part_menu.set(
                "No parts"
            )

    def show_service_history(self):

    # ==========================================
    # GET SELECTED VEHICLE
    # ==========================================

        vehicle_id = self.get_selected_vehicle_id()

        if not vehicle_id:

            messagebox.showwarning(
                "No Vehicle",
                "Please select a vehicle first."
            )

            return

        # ==========================================
        # GET VEHICLE INFORMATION
        # ==========================================

        selected_vehicle = None

        for vehicle in self.vehicles:

            if str(vehicle["_id"]) == vehicle_id:

                selected_vehicle = vehicle
                break

        if not selected_vehicle:

            messagebox.showerror(
                "Error",
                "Unable to find selected vehicle."
            )

            return

        # ==========================================
        # GET SERVICE HISTORY
        # ==========================================

        try:

            services = get_services_by_vehicle(
                vehicle_id
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load service history.\n\n{e}"
            )

            return

        # ==========================================
        # HISTORY WINDOW
        # ==========================================

        history_window = ctk.CTkToplevel(
            self
        )

        history_window.title(
            "Vehicle Service History"
        )

        history_window.geometry(
            "850x650"
        )

        history_window.minsize(
            700,
            500
        )

        # Keep window above main application

        history_window.transient(
            self.winfo_toplevel()
        )

        # ==========================================
        # HEADER
        # ==========================================

        vehicle_number = selected_vehicle.get(
            "vehicle_number",
            "Unknown"
        )

        brand = selected_vehicle.get(
            "brand",
            ""
        )

        model = selected_vehicle.get(
            "model",
            ""
        )

        header = ctk.CTkFrame(
            history_window
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

        ctk.CTkLabel(
            header,
            text=(
                f"{vehicle_number}  |  "
                f"{brand} {model}"
            ),
            font=ctk.CTkFont(
                size=16
            )
        ).pack(
            pady=(0, 15)
        )

        # ==========================================
        # TOTAL SERVICES
        # ==========================================

        ctk.CTkLabel(
            history_window,
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

        # ==========================================
        # SCROLLABLE HISTORY
        # ==========================================

        history_frame = ctk.CTkScrollableFrame(
            history_window
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # ==========================================
        # NO HISTORY
        # ==========================================

        if not services:

            ctk.CTkLabel(
                history_frame,
                text=(
                    "No service history found "
                    "for this vehicle."
                ),
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                pady=50
            )

            return

        # ==========================================
        # DISPLAY SERVICES
        # ==========================================

        for index, service in enumerate(
            services,
            start=1
        ):

            service_card = ctk.CTkFrame(
                history_frame
            )

            service_card.pack(
                fill="x",
                padx=5,
                pady=8
            )

            # --------------------------------------
            # SERVICE HEADER
            # --------------------------------------

            service_type = service.get(
                "service_type",
                "Service"
            )

            service_date = service.get(
                "service_date",
                ""
            )

            status = service.get(
                "status",
                "Unknown"
            )

            total_cost = float(
                service.get(
                    "total_cost",
                    0
                )
            )

            ctk.CTkLabel(
                service_card,
                text=(
                    f"{index}. {service_type}"
                ),
                font=ctk.CTkFont(
                    size=17,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=(12, 3)
            )

            ctk.CTkLabel(
                service_card,
                text=(
                    f"Date: {service_date}    |    "
                    f"Status: {status}"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=3
            )

            # --------------------------------------
            # ODOMETER / MECHANIC
            # --------------------------------------

            odometer = service.get(
                "odometer",
                0
            )

            mechanic = service.get(
                "mechanic",
                ""
            )

            ctk.CTkLabel(
                service_card,
                text=(
                    f"Odometer: {odometer} KM    |    "
                    f"Mechanic: {mechanic}"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=3
            )

            # --------------------------------------
            # LABOUR / PARTS / TOTAL
            # --------------------------------------

            labour_cost = float(
                service.get(
                    "labour_cost",
                    0
                )
            )

            parts_total = float(
                service.get(
                    "parts_total",
                    0
                )
            )

            ctk.CTkLabel(
                service_card,
                text=(
                    f"Labour: ₹{labour_cost:.2f}    |    "
                    f"Parts: ₹{parts_total:.2f}    |    "
                    f"Total: ₹{total_cost:.2f}"
                ),
                anchor="w",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(
                fill="x",
                padx=15,
                pady=5
            )

            # --------------------------------------
            # PARTS USED
            # --------------------------------------

            parts = service.get(
                "parts",
                []
            )

            if parts:

                ctk.CTkLabel(
                    service_card,
                    text="Parts Used:",
                    anchor="w",
                    font=ctk.CTkFont(
                        weight="bold"
                    )
                ).pack(
                    fill="x",
                    padx=15,
                    pady=(8, 2)
                )

                for part in parts:

                    part_name = part.get(
                        "name",
                        "Unknown Part"
                    )

                    quantity = part.get(
                        "quantity",
                        0
                    )

                    price = float(
                        part.get(
                            "price",
                            0
                        )
                    )

                    part_total = (
                        float(quantity) *
                        price
                    )

                    ctk.CTkLabel(
                        service_card,
                        text=(
                            f"• {part_name}  |  "
                            f"Qty: {quantity}  |  "
                            f"₹{part_total:.2f}"
                        ),
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=25,
                        pady=2
                    )

            # --------------------------------------
            # NOTES
            # --------------------------------------

            notes = service.get(
                "notes",
                ""
            )

            if notes:

                ctk.CTkLabel(
                    service_card,
                    text=f"Notes: {notes}",
                    anchor="w",
                    justify="left"
                ).pack(
                    fill="x",
                    padx=15,
                    pady=(8, 12)
                )

            else:

                ctk.CTkLabel(
                    service_card,
                    text=""
                ).pack(
                    pady=5
                )

    # =========================================================
# FILTER SERVICES
# =========================================================

        # =========================================================
    # FILTER SERVICES
    # =========================================================

    def filter_services(self):

        search_text = (
            self.service_search_entry
            .get()
            .strip()
            .lower()
        )

        selected_status = (
            self.service_status_filter
            .get()
        )

        try:

            services = get_all_services()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to search services.\n\n{e}"
            )

            return

        # ==========================================
        # VEHICLE SEARCH
        # ==========================================

        matching_vehicle_ids = set()

        if search_text:

            for vehicle in self.vehicles:

                vehicle_number = str(
                    vehicle.get(
                        "vehicle_number",
                        ""
                    )
                ).lower()

                brand = str(
                    vehicle.get(
                        "brand",
                        ""
                    )
                ).lower()

                model = str(
                    vehicle.get(
                        "model",
                        ""
                    )
                ).lower()

                if (
                    search_text in vehicle_number
                    or search_text in brand
                    or search_text in model
                ):

                    matching_vehicle_ids.add(
                        str(vehicle["_id"])
                    )

        # ==========================================
        # FILTER SERVICES
        # ==========================================

        filtered_services = []

        for service in services:

            service_type = str(
                service.get(
                    "service_type",
                    ""
                )
            ).lower()

            mechanic = str(
                service.get(
                    "mechanic",
                    ""
                )
            ).lower()

            service_date = str(
                service.get(
                    "service_date",
                    ""
                )
            ).lower()

            status = str(
                service.get(
                    "status",
                    ""
                )
            )

            service_vehicle_id = str(
                service.get(
                    "vehicle_id",
                    ""
                )
            )

            # Text search
            search_match = (
                not search_text
                or search_text in service_type
                or search_text in mechanic
                or search_text in service_date
                or service_vehicle_id in matching_vehicle_ids
            )

            # Status filter
            status_match = (
                selected_status == "All"
                or status == selected_status
            )

            if search_match and status_match:

                filtered_services.append(
                    service
                )

        self.display_services(
            filtered_services
        )


    # =========================================================
    # SHOW ALL SERVICES
    # =========================================================

    def show_all_services(self):

        self.service_search_entry.delete(
            0,
            "end"
        )

        self.service_status_filter.set(
            "All"
        )

        self.load_services()


    # =========================================================
    # DISPLAY SERVICES
    # =========================================================

    def display_services(self, services):

        # Clear existing list

        for widget in (
            self.service_list.winfo_children()
        ):

            widget.destroy()

        # Vehicle lookup

        vehicle_map = {}

        for vehicle in self.vehicles:

            vehicle_map[
                str(vehicle["_id"])
            ] = (
                f"{vehicle.get('vehicle_number', '')} "
                f"{vehicle.get('brand', '')} "
                f"{vehicle.get('model', '')}"
            )

        # No results

        if not services:

            ctk.CTkLabel(
                self.service_list,
                text="No matching service records found."
            ).pack(
                pady=30
            )

            return

        # Display services

        for service in services:

            frame = ctk.CTkFrame(
                self.service_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            vehicle_name = vehicle_map.get(
                str(
                    service.get(
                        "vehicle_id",
                        ""
                    )
                ),
                "Unknown Vehicle"
            )

            total_cost = float(
                service.get(
                    "total_cost",
                    0
                )
            )

            text = (
                f"{vehicle_name} | "
                f"{service.get('service_type', '')} | "
                f"{service.get('service_date', '')} | "
                f"₹{total_cost:.2f} | "
                f"{service.get('status', '')}"
            )

            label = ctk.CTkLabel(
                frame,
                text=text,
                anchor="w"
            )

            label.pack(
                side="left",
                padx=15,
                pady=12
            )

            delete_button = ctk.CTkButton(
                frame,
                text="Delete",
                width=70,
                fg_color="#c0392b",
                hover_color="#962d22",
                command=lambda s=service:
                self.delete_service(s)
            )

            delete_button.pack(
                side="right",
                padx=10
            )