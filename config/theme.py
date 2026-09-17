import customtkinter as ctk


DARK = {
    "background": "#0F172A",
    "sidebar": "#111827",
    "surface": "#1E293B",
    "surface_hover": "#26354A",
    "input": "#273449",
    "border": "#334155",

    "primary": "#3B82F6",
    "primary_hover": "#2563EB",

    "danger": "#EF4444",
    "danger_hover": "#DC2626",

    "warning": "#F59E0B",
    "success": "#22C55E",

    "text": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "text_on_primary": "#FFFFFF"
}


LIGHT = {
    "background": "#F8FAFC",
    "sidebar": "#FFFFFF",
    "surface": "#FFFFFF",
    "surface_hover": "#F1F5F9",
    "input": "#F1F5F9",
    "border": "#CBD5E1",

    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",

    "danger": "#DC2626",
    "danger_hover": "#B91C1C",

    "warning": "#D97706",
    "success": "#16A34A",

    "text": "#0F172A",
    "text_secondary": "#475569",
    "text_on_primary": "#FFFFFF"
}


def get_theme_colors(mode=None):
    """Return colors for Dark, Light, or System appearance mode."""

    if mode is None or str(mode).lower() == "system":
        mode = ctk.get_appearance_mode()

    if str(mode).lower() == "light":
        return LIGHT

    return DARK
