import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from models.invoice import (
    create_invoice,
    get_all_invoices,
    update_invoice_status,
    delete_invoice,
    search_invoices
)

from models.customer import get_all_customers
from models.vehicle import get_all_vehicles
from models.service import get_all_services

from reports.invoice_pdf import generate_invoice_pdf


class BillingPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.customers = []
        self.vehicles = []
        self.services = []

        self.create_ui()

        self.load_data()
        self.load_invoices()

    # =========================
    # UI
    # =========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Billing & Invoices",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        form = ctk.CTkFrame(self)

        form.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # =========================
        # CUSTOMER
        # =========================

        ctk.CTkLabel(
            form,
            text="Customer"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        self.customer_menu = ctk.CTkComboBox(
            form,
            width=220,
            values=["No customers"],
            command=lambda _: self.on_customer_selected()
        )

        self.customer_menu.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        # =========================
        # VEHICLE
        # =========================

        ctk.CTkLabel(
            form,
            text="Vehicle"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.vehicle_menu = ctk.CTkComboBox(
            form,
            width=220,
            values=["No vehicles"],
            command=lambda _: self.on_vehicle_selected()
        )

        self.vehicle_menu.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # =========================
        # SERVICE
        # =========================

        ctk.CTkLabel(
            form,
            text="Service"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        self.service_menu = ctk.CTkComboBox(
            form,
            width=250,
            values=["No services"],
            command=lambda _: self.update_service_amount()
        )

        self.service_menu.grid(
            row=1,
            column=2,
            padx=10,
            pady=5
        )

        # =========================
        # TAX
        # =========================

        ctk.CTkLabel(
            form,
            text="Tax %"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=5
        )

        self.tax_entry = ctk.CTkEntry(
            form,
            width=100,
            placeholder_text="18"
        )

        self.tax_entry.insert(
            0,
            "18"
        )

        self.tax_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        self.tax_entry.bind(
            "<KeyRelease>",
            lambda event: self.update_service_amount()
        )

        # =========================
        # SERVICE AMOUNT
        # =========================

        ctk.CTkLabel(
            form,
            text="Service Amount"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=(20, 5)
        )

        self.service_amount_label = ctk.CTkLabel(
            form,
            text="₹0.00",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.service_amount_label.grid(
            row=2,
            column=1,
            padx=10,
            pady=(20, 5)
        )

        # =========================
        # TAX AMOUNT
        # =========================

        ctk.CTkLabel(
            form,
            text="Tax Amount"
        ).grid(
            row=2,
            column=2,
            padx=10,
            pady=(20, 5)
        )

        self.tax_amount_label = ctk.CTkLabel(
            form,
            text="₹0.00",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.tax_amount_label.grid(
            row=2,
            column=3,
            padx=10,
            pady=(20, 5)
        )

        # =========================
        # GRAND TOTAL
        # =========================

        ctk.CTkLabel(
            form,
            text="Grand Total"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10
        )

        self.grand_total_label = ctk.CTkLabel(
            form,
            text="₹0.00",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.grand_total_label.grid(
            row=3,
            column=1,
            columnspan=2,
            sticky="w",
            padx=10,
            pady=10
        )

        # =========================
        # CREATE INVOICE
        # =========================

        ctk.CTkButton(
            form,
            text="Create Invoice",
            height=40,
            command=self.create_invoice
        ).grid(
            row=4,
            column=0,
            columnspan=4,
            pady=20
        )

        # =========================
        # SEARCH
        # =========================

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
            placeholder_text="Search invoice number..."
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
            command=self.load_invoices
        ).pack(
            side="left"
        )

        # =========================
        # INVOICE LIST
        # =========================

        self.invoice_list = ctk.CTkScrollableFrame(
            self
        )

        self.invoice_list.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 25)
        )

        # =========================
    # LOAD DATA
    # =========================

    def load_data(self):

        try:

            self.customers = get_all_customers()
            self.vehicles = get_all_vehicles()
            self.services = get_all_services()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load billing data.\n\n{e}"
            )

            return

        customer_values = [
            f"{c['name']} | {c['phone']}"
            for c in self.customers
        ]

        self.customer_menu.configure(
            values=customer_values or ["No customers"]
        )

        if customer_values:

            self.customer_menu.set(
                customer_values[0]
            )

            # Automatically load vehicles
            # belonging to the first customer.
            self.on_customer_selected()

        else:

            self.customer_menu.set(
                "No customers"
            )

            self.vehicle_menu.configure(
                values=["No vehicles"]
            )

            self.vehicle_menu.set(
                "No vehicles"
            )

            self.service_menu.configure(
                values=["No services"]
            )

            self.service_menu.set(
                "No services"
            )

            self.update_service_amount()

    # =========================
    # CUSTOMER SELECTED
    # =========================

    def on_customer_selected(self):

        customer_id = self.get_customer_id()

        if not customer_id:

            self.vehicle_menu.configure(
                values=["No vehicles"]
            )

            self.vehicle_menu.set(
                "No vehicles"
            )

            self.service_menu.configure(
                values=["No services"]
            )

            self.service_menu.set(
                "No services"
            )

            self.update_service_amount()

            return

        # Find vehicles belonging
        # to selected customer.

        customer_vehicles = [
            vehicle
            for vehicle in self.vehicles
            if str(
                vehicle.get("customer_id")
            ) == customer_id
        ]

        vehicle_values = [
            f"{v['vehicle_number']} | "
            f"{v['brand']} {v['model']}"
            for v in customer_vehicles
        ]

        self.vehicle_menu.configure(
            values=vehicle_values or ["No vehicles"]
        )

        if vehicle_values:

            self.vehicle_menu.set(
                vehicle_values[0]
            )

            self.on_vehicle_selected()

        else:

            self.vehicle_menu.set(
                "No vehicles"
            )

            self.service_menu.configure(
                values=["No services"]
            )

            self.service_menu.set(
                "No services"
            )

            self.update_service_amount()


    # =========================
    # VEHICLE SELECTED
    # =========================

    def on_vehicle_selected(self):

        vehicle_id = self.get_vehicle_id()

        if not vehicle_id:

            self.service_menu.configure(
                values=["No services"]
            )

            self.service_menu.set(
                "No services"
            )

            self.update_service_amount()

            return

        # Find services belonging
        # to selected vehicle.

        vehicle_services = [
            service
            for service in self.services
            if str(
                service.get("vehicle_id")
            ) == vehicle_id
        ]

        service_values = [
            f"{s['service_date']} | "
            f"{s['service_type']} | "
            f"₹{float(s.get('total_cost', 0) or 0):.2f}"
            for s in vehicle_services
        ]

        self.service_menu.configure(
            values=service_values or ["No services"]
        )

        if service_values:

            self.service_menu.set(
                service_values[0]
            )

        else:

            self.service_menu.set(
                "No services"
            )

        self.update_service_amount()


    # =========================
    # SERVICE AMOUNT PREVIEW
    # =========================

    def update_service_amount(self):

        service_id = self.get_service_id()

        if not service_id:

            self.service_amount_label.configure(
                text="₹0.00"
            )

            self.tax_amount_label.configure(
                text="₹0.00"
            )

            self.grand_total_label.configure(
                text="₹0.00"
            )

            return

        service = next(
            (
                s for s in self.services
                if str(s["_id"]) == service_id
            ),
            None
        )

        if not service:

            return

        service_amount = float(
            service.get(
                "total_cost",
                0
            ) or 0
        )

        try:

            tax_rate = float(
                self.tax_entry.get()
            )

        except ValueError:

            tax_rate = 0

        tax_amount = (
            service_amount *
            tax_rate /
            100
        )

        grand_total = (
            service_amount +
            tax_amount
        )

        self.service_amount_label.configure(
            text=f"₹{service_amount:,.2f}"
        )

        self.tax_amount_label.configure(
            text=f"₹{tax_amount:,.2f}"
        )

        self.grand_total_label.configure(
            text=f"₹{grand_total:,.2f}"
        )

    # =========================
    # SELECT CUSTOMER
    # =========================

    def get_customer_id(self):

        selected = self.customer_menu.get()

        for customer in self.customers:

            text = (
                f"{customer.get('name', '')} | "
                f"{customer.get('phone', '')}"
            )

            if text == selected:

                return str(
                    customer["_id"]
                )

        return None

    # =========================
    # SELECT VEHICLE
    # =========================

    def get_vehicle_id(self):

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

    # =========================
    # SELECT SERVICE
    # =========================

    def get_service_id(self):

        selected = self.service_menu.get()

        for service in self.services:

            total_cost = float(
                service.get(
                    "total_cost",
                    0
                ) or 0
            )

            text = (
                f"{service.get('service_date', '')} | "
                f"{service.get('service_type', 'Service')} | "
                f"₹{total_cost:.2f}"
            )

            if text == selected:

                return str(
                    service["_id"]
                )

        return None

    # =========================
    # CREATE AUTOMATIC ITEMS
    # =========================

    def build_invoice_items(self, service):

        items = []

        # -------------------------
        # Labour
        # -------------------------

        labour_cost = float(
            service.get(
                "labour_cost",
                0
            ) or 0
        )

        if labour_cost > 0:

            items.append({
                "description": "Labour Charges",
                "quantity": 1,
                "price": labour_cost
            })

        # -------------------------
        # Spare Parts
        # -------------------------

        parts = service.get(
            "parts",
            []
        )

        for part in parts:

            quantity = float(
                part.get(
                    "quantity",
                    0
                ) or 0
            )

            price = float(
                part.get(
                    "price",
                    0
                ) or 0
            )

            name = (
                part.get(
                    "name",
                    "Spare Part"
                )
            )

            if quantity > 0:

                items.append({
                    "description": name,
                    "quantity": quantity,
                    "price": price
                })

        return items

    # =========================
    # CREATE INVOICE
    # =========================

    def create_invoice(self):

        customer_id = self.get_customer_id()
        vehicle_id = self.get_vehicle_id()
        service_id = self.get_service_id()

        # -------------------------
        # Validation
        # -------------------------

        if not customer_id:

            messagebox.showwarning(
                "Validation",
                "Select a customer."
            )

            return

        if not vehicle_id:

            messagebox.showwarning(
                "Validation",
                "Select a vehicle."
            )

            return

        if not service_id:

            messagebox.showwarning(
                "Validation",
                "Select a service."
            )

            return

        # -------------------------
        # Find selected service
        # -------------------------

        service = next(
            (
                s for s in self.services
                if str(s["_id"]) == service_id
            ),
            None
        )

        if not service:

            messagebox.showerror(
                "Error",
                "Selected service could not be found."
            )

            return

        # -------------------------
        # Make sure service belongs
        # to selected vehicle
        # -------------------------

        service_vehicle_id = service.get(
            "vehicle_id"
        )

        if service_vehicle_id:

            if str(service_vehicle_id) != vehicle_id:

                messagebox.showwarning(
                    "Validation",
                    "The selected service does not "
                    "belong to the selected vehicle."
                )

                return

        # -------------------------
        # Tax
        # -------------------------

        try:

            tax_rate = float(
                self.tax_entry.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Tax must be a number."
            )

            return

        if tax_rate < 0:

            messagebox.showwarning(
                "Validation",
                "Tax cannot be negative."
            )

            return

        # -------------------------
        # Service amount
        # -------------------------

        service_total = float(
            service.get(
                "total_cost",
                0
            ) or 0
        )

        if service_total <= 0:

            messagebox.showwarning(
                "Validation",
                "The selected service has no billable amount."
            )

            return

        # -------------------------
        # Automatically create
        # invoice items from service
        # -------------------------

        items = self.build_invoice_items(
            service
        )

        if not items:

            messagebox.showwarning(
                "Validation",
                "The selected service has no "
                "labour or spare-part charges."
            )

            return

        # -------------------------
        # Invoice number
        # -------------------------

        invoice_number = (
            "INV-"
            + datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

        # -------------------------
        # Create invoice
        # -------------------------

        try:

            # models.invoice.create_invoice() expects the full
            # service document and builds invoice line items from it.
            invoice_id = create_invoice(
                invoice_number,
                customer_id,
                vehicle_id,
                service_id,
                service,
                tax_rate
            )

        except Exception as e:

            messagebox.showerror(
                "Invoice Error",
                f"Unable to create invoice.\n\n{e}"
            )

            return

        # -------------------------
        # Calculate totals
        # -------------------------

        subtotal = sum(
            float(item["quantity"]) *
            float(item["price"])
            for item in items
        )

        tax_amount = (
            subtotal *
            tax_rate /
            100
        )

        grand_total = (
            subtotal +
            tax_amount
        )

        # -------------------------
        # Invoice object for PDF
        # -------------------------

        invoice = {
            "_id": invoice_id,
            "invoice_number": invoice_number,

            "customer_id": customer_id,
            "vehicle_id": vehicle_id,
            "service_id": service_id,

            "items": items,

            "service_type": service.get(
                "service_type",
                "Service"
            ),

            "labour_cost": float(
                service.get(
                    "labour_cost",
                    0
                ) or 0
            ),

            "parts_total": float(
                service.get(
                    "parts_total",
                    0
                ) or 0
            ),

            "subtotal": subtotal,

            "tax_rate": tax_rate,

            "tax_amount": tax_amount,

            "grand_total": grand_total,

            "status": "Unpaid"
        }

        # -------------------------
        # Find customer
        # -------------------------

        customer = next(
            (
                c for c in self.customers
                if str(c["_id"]) == customer_id
            ),
            None
        )

        # -------------------------
        # Find vehicle
        # -------------------------

        vehicle = next(
            (
                v for v in self.vehicles
                if str(v["_id"]) == vehicle_id
            ),
            None
        )

        if not customer:

            messagebox.showerror(
                "Error",
                "Customer information not found."
            )

            return

        if not vehicle:

            messagebox.showerror(
                "Error",
                "Vehicle information not found."
            )

            return

        # -------------------------
        # Generate PDF
        # -------------------------

        try:

            filepath = generate_invoice_pdf(
                invoice,
                customer,
                vehicle
            )

        except Exception as e:

            messagebox.showwarning(
                "PDF Warning",
                "Invoice was created, but the PDF "
                f"could not be generated.\n\n{e}"
            )

            filepath = "PDF generation failed."

        # -------------------------
        # Success
        # -------------------------

        messagebox.showinfo(
            "Success",
            f"Invoice created successfully.\n\n"
            f"Invoice: {invoice_number}\n"
            f"Subtotal: ₹{subtotal:,.2f}\n"
            f"Tax ({tax_rate:g}%): "
            f"₹{tax_amount:,.2f}\n"
            f"Grand Total: ₹{grand_total:,.2f}\n\n"
            f"PDF: {filepath}"
        )

        # -------------------------
        # Refresh
        # -------------------------

        self.load_invoices()

        self.update_service_amount()

    # =========================
    # LOAD INVOICES
    # =========================

    def load_invoices(self):

        try:

            invoices = get_all_invoices()

            self.display_invoices(
                invoices
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load invoices.\n\n{e}"
            )

    # =========================
    # DISPLAY INVOICES
    # =========================

    def display_invoices(
        self,
        invoices
    ):

        for widget in self.invoice_list.winfo_children():

            widget.destroy()

        if not invoices:

            ctk.CTkLabel(
                self.invoice_list,
                text="No invoices found.",
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                pady=40
            )

            return

        for invoice in invoices:

            frame = ctk.CTkFrame(
                self.invoice_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            grand_total = float(
                invoice.get(
                    "grand_total",
                    0
                ) or 0
            )

            text = (
                f"{invoice.get('invoice_number', '')} | "
                f"₹{grand_total:.2f} | "
                f"{invoice.get('status', 'Unpaid')}"
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

            # -------------------------
            # Mark Paid
            # -------------------------

            if invoice.get("status") != "Paid":

                status_button = ctk.CTkButton(
                    frame,
                    text="Mark Paid",
                    width=100,
                    command=lambda i=invoice:
                    self.mark_paid(i)
                )

                status_button.pack(
                    side="right",
                    padx=5
                )

            # -------------------------
            # Delete
            # -------------------------

            delete_button = ctk.CTkButton(
                frame,
                text="Delete",
                width=70,
                fg_color="#c0392b",
                hover_color="#962d22",
                command=lambda i=invoice:
                self.delete_invoice(i)
            )

            delete_button.pack(
                side="right",
                padx=5
            )

    # =========================
    # MARK PAID
    # =========================

    def mark_paid(
        self,
        invoice
    ):

        try:

            update_invoice_status(
                str(invoice["_id"]),
                "Paid"
            )

            self.load_invoices()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to mark invoice as paid.\n\n{e}"
            )

    # =========================
    # DELETE
    # =========================

    def delete_invoice(
        self,
        invoice
    ):

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this invoice?"
        )

        if not confirm:

            return

        try:

            delete_invoice(
                str(invoice["_id"])
            )

            self.load_invoices()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to delete invoice.\n\n{e}"
            )

    # =========================
    # SEARCH
    # =========================

    def search(self):

        text = (
            self.search_entry
            .get()
            .strip()
        )

        if not text:

            self.load_invoices()

            return

        try:

            invoices = search_invoices(
                text
            )

            self.display_invoices(
                invoices
            )

        except Exception as e:

            messagebox.showerror(
                "Search Error",
                f"Unable to search invoices.\n\n{e}"
            )