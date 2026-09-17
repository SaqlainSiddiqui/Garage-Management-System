import customtkinter as ctk
from tkinter import messagebox

from models.inventory_transaction import (
    get_all_inventory_transactions
)


class InventoryHistoryPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.create_ui()
        self.load_transactions()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        # ================================================
        # TITLE
        # ================================================

        title = ctk.CTkLabel(
            self,
            text="Inventory Transaction History",
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
                "Track every stock addition, "
                "deduction and adjustment."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        # ================================================
        # REFRESH BUTTON
        # ================================================

        ctk.CTkButton(
            self,
            text="Refresh",
            width=100,
            command=self.load_transactions
        ).pack(
            anchor="e",
            padx=25,
            pady=(0, 10)
        )

        # ================================================
        # TRANSACTION AREA
        # ================================================

        self.transaction_list = ctk.CTkScrollableFrame(
            self
        )

        self.transaction_list.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    # =====================================================
    # LOAD TRANSACTIONS
    # =====================================================

    def load_transactions(self):

        # ================================================
        # CLEAR OLD DATA
        # ================================================

        for widget in (
            self.transaction_list.winfo_children()
        ):

            widget.destroy()

        # ================================================
        # GET TRANSACTIONS
        # ================================================

        try:

            transactions = (
                get_all_inventory_transactions()
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load inventory history.\n\n{e}"
            )

            return

        # ================================================
        # NO DATA
        # ================================================

        if not transactions:

            ctk.CTkLabel(
                self.transaction_list,
                text="No inventory transactions found.",
                font=ctk.CTkFont(
                    size=16
                )
            ).pack(
                pady=40
            )

            return

        # ================================================
        # DISPLAY TRANSACTIONS
        # ================================================

        for transaction in transactions:

            self.create_transaction_card(
                transaction
            )

    # =====================================================
    # TRANSACTION CARD
    # =====================================================

    def create_transaction_card(
        self,
        transaction
    ):

        card = ctk.CTkFrame(
            self.transaction_list
        )

        card.pack(
            fill="x",
            pady=5,
            padx=5
        )

        # ================================================
        # DATA
        # ================================================

        part_name = transaction.get(
            "part_name",
            "Unknown Part"
        )

        quantity = int(
            transaction.get(
                "quantity_change",
                0
            )
        )

        transaction_type = transaction.get(
            "transaction_type",
            "Unknown"
        )

        reference = transaction.get(
            "reference"
        )

        notes = transaction.get(
            "notes",
            ""
        )

        created_at = transaction.get(
            "created_at"
        )

        # ================================================
        # DATE
        # ================================================

        if created_at:

            try:

                date_text = created_at.strftime(
                    "%d-%m-%Y %H:%M"
                )

            except AttributeError:

                date_text = str(
                    created_at
                )

        else:

            date_text = "Unknown"

        # ================================================
        # QUANTITY DISPLAY
        # ================================================

        if quantity > 0:

            quantity_text = (
                f"+{quantity}"
            )

        else:

            quantity_text = str(
                quantity
            )

        # ================================================
        # HEADER
        # ================================================

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            header,
            text=part_name,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header,
            text=quantity_text,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).pack(
            side="right"
        )

        # ================================================
        # TRANSACTION TYPE
        # ================================================

        ctk.CTkLabel(
            card,
            text=(
                f"Type: {transaction_type}"
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=2
        )

        # ================================================
        # DATE
        # ================================================

        ctk.CTkLabel(
            card,
            text=(
                f"Date: {date_text}"
            ),
            anchor="w"
        ).pack(
            fill="x",
            padx=15,
            pady=2
        )

        # ================================================
        # REFERENCE
        # ================================================

        if reference:

            ctk.CTkLabel(
                card,
                text=(
                    f"Reference: {reference}"
                ),
                anchor="w"
            ).pack(
                fill="x",
                padx=15,
                pady=2
            )

        # ================================================
        # NOTES
        # ================================================

        if notes:

            ctk.CTkLabel(
                card,
                text=(
                    f"Notes: {notes}"
                ),
                anchor="w",
                justify="left"
            ).pack(
                fill="x",
                padx=15,
                pady=(2, 10)
            )

