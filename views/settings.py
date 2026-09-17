import customtkinter as ctk
from tkinter import messagebox

from models.user import (
    update_user_profile,
    change_user_password
)

from config.database import client


class SettingsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        user,
        theme_callback=None
    ):

        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent"
        )

        self.user = user
        self.theme_callback = theme_callback

        self.create_ui()

    # =========================
    # MAIN UI
    # =========================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Settings",
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

        subtitle = ctk.CTkLabel(
            self,
            text="Manage your account, security and application preferences.",
            font=ctk.CTkFont(size=15)
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        # =========================
        # SCROLLABLE AREA
        # =========================

        self.settings_area = ctk.CTkScrollableFrame(
            self
        )

        self.settings_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        self.create_profile_section()

        self.create_password_section()

        self.create_appearance_section()

        self.create_database_section()

        self.create_about_section()

    # =========================
    # PROFILE
    # =========================

    def create_profile_section(self):

        frame = ctk.CTkFrame(
            self.settings_area
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Profile",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            frame,
            text="Update your account information.",
            font=ctk.CTkFont(size=13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # Name

        ctk.CTkLabel(
            frame,
            text="Name",
            anchor="w"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.name_entry = ctk.CTkEntry(
            frame,
            width=400
        )

        self.name_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        self.name_entry.insert(
            0,
            self.user.get(
                "name",
                ""
            )
        )

        # Email

        ctk.CTkLabel(
            frame,
            text="Email",
            anchor="w"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.email_entry = ctk.CTkEntry(
            frame,
            width=400
        )

        self.email_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.email_entry.insert(
            0,
            self.user.get(
                "email",
                ""
            )
        )

        # Save

        ctk.CTkButton(
            frame,
            text="Save Profile",
            width=150,
            command=self.save_profile
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # =========================
    # SAVE PROFILE
    # =========================

    def save_profile(self):

        name = self.name_entry.get().strip()

        email = self.email_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Validation",
                "Please enter your name."
            )

            return

        if not email:

            messagebox.showwarning(
                "Validation",
                "Please enter your email."
            )

            return

        success, message = update_user_profile(
            str(self.user["_id"]),
            name,
            email
        )

        if not success:

            messagebox.showerror(
                "Profile Update",
                message
            )

            return

        # Update local user object
        self.user["name"] = name
        self.user["email"] = email

        messagebox.showinfo(
            "Success",
            message
        )

    # =========================
    # PASSWORD
    # =========================

    def create_password_section(self):

        frame = ctk.CTkFrame(
            self.settings_area
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Security",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            frame,
            text="Change your account password.",
            font=ctk.CTkFont(size=13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # Current password

        ctk.CTkLabel(
            frame,
            text="Current Password"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.current_password_entry = ctk.CTkEntry(
            frame,
            width=400,
            show="*"
        )

        self.current_password_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # New password

        ctk.CTkLabel(
            frame,
            text="New Password"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.new_password_entry = ctk.CTkEntry(
            frame,
            width=400,
            show="*"
        )

        self.new_password_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        # Confirm password

        ctk.CTkLabel(
            frame,
            text="Confirm New Password"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 3)
        )

        self.confirm_password_entry = ctk.CTkEntry(
            frame,
            width=400,
            show="*"
        )

        self.confirm_password_entry.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkButton(
            frame,
            text="Change Password",
            width=170,
            command=self.change_password
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # =========================
    # CHANGE PASSWORD
    # =========================

    def change_password(self):

        current_password = (
            self.current_password_entry
            .get()
        )

        new_password = (
            self.new_password_entry
            .get()
        )

        confirm_password = (
            self.confirm_password_entry
            .get()
        )

        if not current_password:

            messagebox.showwarning(
                "Validation",
                "Enter your current password."
            )

            return

        if not new_password:

            messagebox.showwarning(
                "Validation",
                "Enter a new password."
            )

            return

        if new_password != confirm_password:

            messagebox.showwarning(
                "Validation",
                "New passwords do not match."
            )

            return

        if current_password == new_password:

            messagebox.showwarning(
                "Validation",
                "New password must be different from the current password."
            )

            return

        success, message = change_user_password(
            str(self.user["_id"]),
            current_password,
            new_password
        )

        if not success:

            messagebox.showerror(
                "Password Change",
                message
            )

            return

        self.current_password_entry.delete(
            0,
            "end"
        )

        self.new_password_entry.delete(
            0,
            "end"
        )

        self.confirm_password_entry.delete(
            0,
            "end"
        )

        messagebox.showinfo(
            "Success",
            message
        )

    # =========================
    # APPEARANCE
    # =========================

    def create_appearance_section(self):

        frame = ctk.CTkFrame(
            self.settings_area
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Appearance",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            frame,
            text="Choose how the application should appear.",
            font=ctk.CTkFont(size=13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        row = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        ctk.CTkLabel(
            row,
            text="Theme",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        self.theme_menu = ctk.CTkComboBox(
            row,
            width=180,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            command=self.change_theme
        )

        self.theme_menu.pack(
            side="right"
        )

        current_theme = self.user.get(
            "theme",
            "Dark"
        )

        self.theme_menu.set(
            current_theme
        )

    # =========================
    # CHANGE THEME
    # =========================

    # =========================
    # CHANGE THEME
    # =========================

    def change_theme(self, theme):

        self.user["theme"] = theme

        # Apply theme immediately
        if self.theme_callback:

            self.theme_callback(
                theme
            )

        else:

            ctk.set_appearance_mode(
                theme
            )

        # Save theme preference
        try:

            from config.database import (
                users_collection
            )

            from bson import ObjectId

            users_collection.update_one(
                {
                    "_id": ObjectId(
                        str(self.user["_id"])
                    )
                },
                {
                    "$set": {
                        "theme": theme
                    }
                }
            )

        except Exception as e:

            print(
                "Unable to save theme:",
                e
            )

    # =========================
    # DATABASE
    # =========================

    def create_database_section(self):

        frame = ctk.CTkFrame(
            self.settings_area
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Database",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            frame,
            text="Check the connection to the MongoDB database.",
            font=ctk.CTkFont(size=13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.database_status = ctk.CTkLabel(
            frame,
            text="Status: Not checked",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.database_status.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        ctk.CTkButton(
            frame,
            text="Test Connection",
            width=150,
            command=self.test_database
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # =========================
    # DATABASE TEST
    # =========================

    def test_database(self):

        try:

            client.admin.command(
                "ping"
            )

            self.database_status.configure(
                text="Status: Connected",
                text_color="green"
            )

        except Exception as e:

            self.database_status.configure(
                text="Status: Connection Failed",
                text_color="red"
            )

            messagebox.showerror(
                "Database Connection",
                f"MongoDB connection failed.\n\n{e}"
            )

    # =========================
    # ABOUT
    # =========================

    def create_about_section(self):

        frame = ctk.CTkFrame(
            self.settings_area
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        ctk.CTkLabel(
            frame,
            text="Application Information",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        information = [
            ("Application", "Garage Management System"),
            ("Version", "1.0"),
            ("Database", "MongoDB"),
            ("Interface", "CustomTkinter"),
            ("Purpose", "Vehicle Service & Garage Management")
        ]

        for label, value in information:

            row = ctk.CTkFrame(
                frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
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
                text=value,
                anchor="w"
            ).pack(
                side="left"
            )

        ctk.CTkLabel(
            frame,
            text="",
        ).pack(
            pady=5
        )