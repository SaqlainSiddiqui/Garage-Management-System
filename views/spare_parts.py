import customtkinter as ctk
from tkinter import messagebox

from models.spare_part import (
    create_spare_part,
    get_all_spare_parts,
    update_spare_part,
    delete_spare_part,
    search_spare_parts,
    get_low_stock_parts
)

from views.inventory_history import (
    InventoryHistoryPage
)


class SparePartsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.selected_part_id = None

        self.create_ui()
        self.load_parts()

    # =========================
    # UI
    # =========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Spare Parts & Inventory",
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

        # Form
        form = ctk.CTkFrame(self)

        form.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.name_entry = self.create_entry(
            form,
            "Part Name",
            0
        )

        self.part_number_entry = self.create_entry(
            form,
            "Part Number",
            1
        )

        self.category_entry = self.create_entry(
            form,
            "Category",
            2
        )

        self.supplier_entry = self.create_entry(
            form,
            "Supplier",
            3
        )

        self.purchase_entry = self.create_entry(
            form,
            "Purchase Price",
            4
        )

        self.selling_entry = self.create_entry(
            form,
            "Selling Price",
            5
        )

        self.stock_entry = self.create_entry(
            form,
            "Stock",
            6
        )

        self.minimum_stock_entry = self.create_entry(
            form,
            "Minimum Stock",
            7
        )

        self.location_entry = self.create_entry(
            form,
            "Location",
            8
        )

        # Buttons
        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=9,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="Add Part",
            command=self.add_part
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_part
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Delete",
            fg_color="#c0392b",
            hover_color="#962d22",
            command=self.delete_part
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

        ctk.CTkButton(
            button_frame,
            text="Low Stock",
            fg_color="#d68910",
            hover_color="#a9690b",
            command=self.show_low_stock
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            button_frame,
            text="Inventory History",
            command=self.show_inventory_history
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
            placeholder_text="Search part..."
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
            command=self.load_parts
        ).pack(
            side="left"
        )

        # List
        self.parts_list = ctk.CTkScrollableFrame(
            self
        )

        self.parts_list.pack(
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
            width=135,
            placeholder_text=placeholder
        )

        entry.grid(
            row=1,
            column=column,
            padx=5,
            pady=5
        )

        ctk.CTkLabel(
            parent,
            text=placeholder
        ).grid(
            row=0,
            column=column,
            padx=5,
            pady=(10, 3)
        )

        return entry

    # =========================
    # ADD
    # =========================

    def add_part(self):

        try:

            create_spare_part(
                self.name_entry.get(),
                self.part_number_entry.get(),
                self.category_entry.get(),
                self.supplier_entry.get(),
                self.purchase_entry.get(),
                self.selling_entry.get(),
                self.stock_entry.get(),
                self.minimum_stock_entry.get(),
                self.location_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Data",
                "Prices and stock values must be valid numbers."
            )

            return

        messagebox.showinfo(
            "Success",
            "Spare part added successfully."
        )

        self.clear_form()
        self.load_parts()

    # =========================
    # LOAD
    # =========================

    def load_parts(self):

        parts = get_all_spare_parts()

        self.display_parts(parts)

    # =========================
    # DISPLAY
    # =========================

    def display_parts(self, parts):

        for widget in self.parts_list.winfo_children():
            widget.destroy()

        for part in parts:

            frame = ctk.CTkFrame(
                self.parts_list
            )

            frame.pack(
                fill="x",
                pady=5
            )

            stock = part.get(
                "stock",
                0
            )

            minimum = part.get(
                "minimum_stock",
                0
            )

            if stock <= minimum:

                stock_text = (
                    f"⚠ LOW STOCK: {stock}"
                )

            else:

                stock_text = (
                    f"Stock: {stock}"
                )

            text = (
                f"{part['name']} | "
                f"{part['part_number']} | "
                f"{part['category']} | "
                f"₹{part['selling_price']:.2f} | "
                f"{stock_text}"
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

            edit_button = ctk.CTkButton(
                frame,
                text="Edit",
                width=70,
                command=lambda p=part:
                self.select_part(p)
            )

            edit_button.pack(
                side="right",
                padx=5
            )

    # =========================
    # SELECT
    # =========================

    def select_part(self, part):

        self.selected_part_id = str(
            part["_id"]
        )

        self.clear_entries_only()

        self.name_entry.insert(
            0,
            part.get("name", "")
        )

        self.part_number_entry.insert(
            0,
            part.get("part_number", "")
        )

        self.category_entry.insert(
            0,
            part.get("category", "")
        )

        self.supplier_entry.insert(
            0,
            part.get("supplier", "")
        )

        self.purchase_entry.insert(
            0,
            str(part.get("purchase_price", ""))
        )

        self.selling_entry.insert(
            0,
            str(part.get("selling_price", ""))
        )

        self.stock_entry.insert(
            0,
            str(part.get("stock", ""))
        )

        self.minimum_stock_entry.insert(
            0,
            str(part.get("minimum_stock", ""))
        )

        self.location_entry.insert(
            0,
            part.get("location", "")
        )

    # =========================
    # UPDATE
    # =========================

    def update_part(self):

        if not self.selected_part_id:

            messagebox.showwarning(
                "Update",
                "Select a part first."
            )

            return

        try:

            update_spare_part(
                self.selected_part_id,
                self.name_entry.get(),
                self.part_number_entry.get(),
                self.category_entry.get(),
                self.supplier_entry.get(),
                self.purchase_entry.get(),
                self.selling_entry.get(),
                self.stock_entry.get(),
                self.minimum_stock_entry.get(),
                self.location_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Data",
                "Prices and stock values must be numbers."
            )

            return

        messagebox.showinfo(
            "Success",
            "Spare part updated successfully."
        )

        self.clear_form()
        self.load_parts()

    # =========================
    # DELETE
    # =========================

    def delete_part(self):

        if not self.selected_part_id:

            messagebox.showwarning(
                "Delete",
                "Select a part first."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this spare part?"
        )

        if not confirm:
            return

        delete_spare_part(
            self.selected_part_id
        )

        messagebox.showinfo(
            "Success",
            "Spare part deleted successfully."
        )

        self.clear_form()
        self.load_parts()

    # =========================
    # SEARCH
    # =========================

    def search(self):

        text = self.search_entry.get().strip()

        if not text:

            self.load_parts()

            return

        parts = search_spare_parts(text)

        self.display_parts(parts)

    # =========================
    # LOW STOCK
    # =========================

    def show_low_stock(self):

        parts = get_low_stock_parts()

        self.display_parts(parts)

        if not parts:

            messagebox.showinfo(
                "Low Stock",
                "No low-stock items found."
            )

    # =========================
    # CLEAR
    # =========================

    def clear_entries_only(self):

        entries = [
            self.name_entry,
            self.part_number_entry,
            self.category_entry,
            self.supplier_entry,
            self.purchase_entry,
            self.selling_entry,
            self.stock_entry,
            self.minimum_stock_entry,
            self.location_entry
        ]

        for entry in entries:

            entry.delete(
                0,
                "end"
            )

    def clear_form(self):

        self.selected_part_id = None

        self.clear_entries_only()

        # =========================
    # INVENTORY HISTORY
    # =========================

    def show_inventory_history(self):

        history_window = ctk.CTkToplevel(
            self
        )

        history_window.title(
            "Inventory Transaction History"
        )

        history_window.geometry(
            "900x650"
        )

        history_window.minsize(
            750,
            500
        )

        # Keep window above the main application
        history_window.transient(
            self.winfo_toplevel()
        )

        # Create Inventory History page
        history_page = InventoryHistoryPage(
            history_window
        )

        history_page.pack(
            fill="both",
            expand=True
        )