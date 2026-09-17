import customtkinter as ctk
from tkinter import messagebox

from models.user import authenticate_user
from views.dashboard import DashboardWindow


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Garage Management System")
        self.geometry("900x600")
        self.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_ui()

    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=20
        )

        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=40
        )

        # Application title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="GARAGE MANAGEMENT SYSTEM",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.title_label.pack(pady=(60, 10))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Vehicle Service & Garage Management",
            font=ctk.CTkFont(size=15)
        )

        self.subtitle_label.pack(pady=(0, 40))

        # Email
        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            width=350,
            height=45,
            placeholder_text="Email"
        )

        self.email_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            width=350,
            height=45,
            placeholder_text="Password",
            show="*"
        )

        self.password_entry.pack(pady=10)

        # Login button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="LOGIN",
            width=350,
            height=45,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            command=self.login
        )

        self.login_button.pack(pady=(25, 10))

        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            text_color="red"
        )

        self.status_label.pack(pady=10)

        # Enter key
        self.bind("<Return>", lambda event: self.login())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        # Basic validation
        if not email:
            self.show_error("Please enter your email.")
            return

        if not password:
            self.show_error("Please enter your password.")
            return

        # Authenticate
        user = authenticate_user(email, password)

        if user:
            self.status_label.configure(
                text="Login successful!",
                text_color="green"
            )

            self.open_dashboard(user)

        else:
            self.show_error(
                "Invalid email or password."
            )

    def show_error(self, message):
        self.status_label.configure(
            text=message,
            text_color="red"
        )

    def open_dashboard(self, user):
        self.destroy()

        dashboard = DashboardWindow(user)
        dashboard.mainloop()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()