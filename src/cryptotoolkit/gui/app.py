"""Main Application Window for Classical Cryptography Toolkit."""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

from .theme import (
    apply_theme,
    COLOR_BG_DARK,
    COLOR_BG_SIDEBAR,
    COLOR_BG_CARD,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_BLUE,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_SMALL,
)
from .dashboard import DashboardView
from .cipher_views import CipherWorkbenchView
from .comparison_view import ComparisonView
from .file_view import FileOperationView
from .help_view import HelpDocumentationView
from .about_view import AboutProjectView


class CryptoToolkitApp(tk.Tk):
    """Main Desktop Window with Sidebar Navigation."""

    def __init__(self):
        super().__init__()
        self.title("CLASSICAL CRYPTOGRAPHY TOOLKIT")
        self.geometry("1180x760")
        self.minsize(980, 640)

        # Apply dark theme
        apply_theme(self)

        self._build_sidebar()
        self._build_main_container()
        self._build_status_bar()

        # Initialize views
        self.views: Dict[str, tk.Widget] = {}
        self._init_views()

        # Default to Dashboard
        self.show_view("dashboard")

    def _build_sidebar(self) -> None:
        self.sidebar = tk.Frame(
            self,
            bg=COLOR_BG_SIDEBAR,
            width=230,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand header
        brand_frame = tk.Frame(self.sidebar, bg=COLOR_BG_SIDEBAR, padx=16, pady=20)
        brand_frame.pack(fill="x")

        tk.Label(
            brand_frame,
            text="CRYPTOTOOLKIT",
            font=FONT_HEADING,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_SIDEBAR,
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            brand_frame,
            text="Final Year ECM (2026-27)",
            font=FONT_SMALL,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_SIDEBAR,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        # Divider
        tk.Frame(self.sidebar, bg=COLOR_BORDER, height=1).pack(fill="x", padx=12, pady=(0, 10))

        # Nav Buttons list
        self.nav_buttons: Dict[str, tk.Button] = {}
        nav_items = [
            ("dashboard", "📊 Dashboard"),
            ("substitution", "🔤 Substitution Ciphers"),
            ("transposition", "🔀 Transposition Ciphers"),
            ("comparison", "⚡ Algorithm Comparison"),
            ("file_ops", "📁 File Encrypt & Decrypt"),
            ("help", "📖 Help & Documentation"),
            ("about", "ℹ️ About Project"),
        ]

        for view_id, label in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=label,
                font=FONT_BODY_BOLD,
                bg=COLOR_BG_SIDEBAR,
                fg=COLOR_TEXT_SECONDARY,
                activebackground=COLOR_BG_CARD,
                activeforeground=COLOR_ACCENT_CYAN,
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                command=lambda v=view_id: self.show_view(v),
                cursor="hand2",
            )
            btn.pack(fill="x")
            self.nav_buttons[view_id] = btn

        # Spacer to push bottom action down
        spacer = tk.Frame(self.sidebar, bg=COLOR_BG_SIDEBAR)
        spacer.pack(fill="both", expand=True)

        # Quit Button
        btn_quit = tk.Button(
            self.sidebar,
            text="🚪 Exit Toolkit",
            font=FONT_BODY,
            bg=COLOR_BG_SIDEBAR,
            fg=COLOR_TEXT_SECONDARY,
            activebackground=COLOR_BORDER,
            activeforeground="#ff4d6d",
            relief="flat",
            anchor="w",
            padx=16,
            pady=12,
            command=self._on_exit,
            cursor="hand2",
        )
        btn_quit.pack(fill="x", side="bottom")

    def _build_main_container(self) -> None:
        self.main_container = tk.Frame(self, bg=COLOR_BG_DARK)
        self.main_container.pack(side="left", fill="both", expand=True)

    def _build_status_bar(self) -> None:
        self.status_bar = tk.Frame(self, bg=COLOR_BG_SIDEBAR, height=26, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.status_bar.pack(side="bottom", fill="x")

        self.lbl_status_msg = tk.Label(
            self.status_bar,
            text="System Ready | Python 3 Standard Library | High-Resolution Monotonic Timer Active",
            font=FONT_SMALL,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_SIDEBAR,
            padx=12,
        )
        self.lbl_status_msg.pack(side="left")

        lbl_academic = tk.Label(
            self.status_bar,
            text="Network Security Mini-Project (ECM)",
            font=FONT_SMALL,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_SIDEBAR,
            padx=12,
        )
        lbl_academic.pack(side="right")

    def _init_views(self) -> None:
        """Instantiate views lazily or on demand."""
        self.views["dashboard"] = DashboardView(
            self.main_container,
            on_select_cipher=self.open_cipher,
            on_navigate=self.show_view,
        )
        self.views["substitution"] = CipherWorkbenchView(
            self.main_container,
            default_cipher_id="caesar",
            filter_category="Substitution",
        )
        self.views["transposition"] = CipherWorkbenchView(
            self.main_container,
            default_cipher_id="rail_fence",
            filter_category="Transposition",
        )
        self.views["comparison"] = ComparisonView(self.main_container)
        self.views["file_ops"] = FileOperationView(self.main_container)
        self.views["help"] = HelpDocumentationView(self.main_container)
        self.views["about"] = AboutProjectView(self.main_container)

    def show_view(self, view_id: str) -> None:
        """Switch current view."""
        if view_id not in self.views:
            return

        # Update button visual styling
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                btn.config(bg=COLOR_BG_CARD, fg=COLOR_ACCENT_CYAN)
            else:
                btn.config(bg=COLOR_BG_SIDEBAR, fg=COLOR_TEXT_SECONDARY)

        # Hide all, show selected
        for vid, view_widget in self.views.items():
            view_widget.pack_forget()

        self.views[view_id].pack(fill="both", expand=True)
        self.lbl_status_msg.config(text=f"Active Section: {view_id.replace('_', ' ').title()}")

    def open_cipher(self, cipher_id: str) -> None:
        """Direct jump from dashboard card to specific cipher."""
        from ..ciphers import get_cipher
        cipher = get_cipher(cipher_id)
        target_view = "substitution" if cipher.category == "Substitution" else "transposition"
        self.show_view(target_view)
        # Select cipher in workbench
        workbench: CipherWorkbenchView = self.views[target_view]
        workbench.switch_cipher(cipher_id)

    def _on_exit(self) -> None:
        if messagebox.askyesno("Exit Toolkit", "Are you sure you want to exit the Classical Cryptography Toolkit?"):
            self.destroy()


def run_app():
    """Launch Desktop GUI application."""
    app = CryptoToolkitApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
