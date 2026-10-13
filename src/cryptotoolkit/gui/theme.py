"""Cybersecurity Dark Theme colors, fonts, and ttk styles."""

import tkinter as tk
from tkinter import ttk

# Cohesive Cybersecurity Palette (Dark Navy & Neon Cyan / Ice Blue)
COLOR_BG_DARK = "#0a1128"        # Deep midnight navy
COLOR_BG_SIDEBAR = "#001233"     # Darker sidebar navy
COLOR_BG_CARD = "#031d44"        # Surface card navy
COLOR_BG_INPUT = "#062854"       # Input box navy
COLOR_BORDER = "#1b3b6f"         # Subtle border blue

COLOR_TEXT_PRIMARY = "#ffffff"   # Clean white
COLOR_TEXT_SECONDARY = "#8da9c4" # Muted cyan-gray
COLOR_TEXT_MUTED = "#5c799a"     # Darker muted

COLOR_ACCENT_CYAN = "#00e5ff"    # Vibrant neon cyan
COLOR_ACCENT_HOVER = "#33ebff"   # Lighter cyan
COLOR_ACCENT_BLUE = "#0466c8"    # Classic cyber blue

COLOR_SUCCESS = "#00f5d4"        # Cyber emerald / mint
COLOR_WARNING = "#ffb703"        # Amber
COLOR_DANGER = "#ff4d6d"         # Coral red

FONT_FAMILY = "Helvetica" if tk.TkVersion >= 8.6 else "Arial"
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13, "bold")
FONT_HEADING = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 10, "normal")
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_MONO = ("Courier", 10, "normal")
FONT_MONO_BOLD = ("Courier", 10, "bold")
FONT_SMALL = (FONT_FAMILY, 9, "normal")


def apply_theme(root: tk.Tk) -> ttk.Style:
    """Configure ttk widgets to match cybersecurity dark aesthetic."""
    style = ttk.Style(root)

    # Use 'clam' as base theme for highest customization consistency across OSes
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Root background
    root.configure(bg=COLOR_BG_DARK)

    # Frame styles
    style.configure("Dark.TFrame", background=COLOR_BG_DARK)
    style.configure("Sidebar.TFrame", background=COLOR_BG_SIDEBAR)
    style.configure("Card.TFrame", background=COLOR_BG_CARD, relief="flat")
    style.configure("InputCard.TFrame", background=COLOR_BG_CARD)

    # Label styles
    style.configure(
        "Dark.TLabel",
        background=COLOR_BG_DARK,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_BODY,
    )
    style.configure(
        "Title.TLabel",
        background=COLOR_BG_DARK,
        foreground=COLOR_ACCENT_CYAN,
        font=FONT_TITLE,
    )
    style.configure(
        "Subtitle.TLabel",
        background=COLOR_BG_DARK,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_SUBTITLE,
    )
    style.configure(
        "Heading.TLabel",
        background=COLOR_BG_CARD,
        foreground=COLOR_ACCENT_CYAN,
        font=FONT_HEADING,
    )
    style.configure(
        "CardText.TLabel",
        background=COLOR_BG_CARD,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_BODY,
    )

    # Buttons
    style.configure(
        "Accent.TButton",
        background=COLOR_ACCENT_CYAN,
        foreground=COLOR_BG_DARK,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(12, 6),
    )
    style.map(
        "Accent.TButton",
        background=[("active", COLOR_ACCENT_HOVER), ("disabled", COLOR_BG_INPUT)],
        foreground=[("active", COLOR_BG_DARK), ("disabled", COLOR_TEXT_MUTED)],
    )

    style.configure(
        "Secondary.TButton",
        background=COLOR_BG_INPUT,
        foreground=COLOR_TEXT_PRIMARY,
        font=FONT_BODY,
        borderwidth=1,
        relief="flat",
        padding=(10, 5),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLOR_BORDER)],
        foreground=[("active", COLOR_ACCENT_CYAN)],
    )

    style.configure(
        "Nav.TButton",
        background=COLOR_BG_SIDEBAR,
        foreground=COLOR_TEXT_SECONDARY,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        anchor="w",
        padding=(16, 8),
    )
    style.map(
        "Nav.TButton",
        background=[("active", COLOR_BG_CARD)],
        foreground=[("active", COLOR_ACCENT_CYAN)],
    )

    style.configure(
        "NavActive.TButton",
        background=COLOR_BG_CARD,
        foreground=COLOR_ACCENT_CYAN,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        anchor="w",
        padding=(16, 8),
    )

    # Entry and Combobox
    style.configure(
        "Dark.TEntry",
        fieldbackground=COLOR_BG_INPUT,
        foreground=COLOR_TEXT_PRIMARY,
        insertcolor=COLOR_ACCENT_CYAN,
        padding=6,
    )

    style.configure(
        "Dark.TCombobox",
        fieldbackground=COLOR_BG_INPUT,
        background=COLOR_BG_CARD,
        foreground=COLOR_TEXT_PRIMARY,
        arrowcolor=COLOR_ACCENT_CYAN,
        padding=4,
    )

    # Treeview (Comparison table)
    style.configure(
        "Treeview",
        background=COLOR_BG_CARD,
        foreground=COLOR_TEXT_PRIMARY,
        fieldbackground=COLOR_BG_CARD,
        font=FONT_BODY,
        rowheight=26,
    )
    style.configure(
        "Treeview.Heading",
        background=COLOR_BG_SIDEBAR,
        foreground=COLOR_ACCENT_CYAN,
        font=FONT_BODY_BOLD,
        relief="flat",
        padding=5,
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_ACCENT_BLUE)],
        foreground=[("selected", COLOR_TEXT_PRIMARY)],
    )

    return style
