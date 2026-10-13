"""Dashboard view displaying cards for all 8 ciphers and system statistics."""

import tkinter as tk
from tkinter import ttk
from typing import Callable

from .theme import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BG_INPUT,
    COLOR_ACCENT_CYAN,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_BORDER,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_SMALL,
    FONT_BODY_BOLD,
)
from ..ciphers import CIPHER_REGISTRY, get_cipher

CIPHER_META = [
    {
        "id": "caesar",
        "name": "1. Caesar Cipher",
        "category": "Substitution",
        "key_type": "Integer shift (0–25)",
        "desc": "Classical monoalphabetic shift cipher using modular addition.",
    },
    {
        "id": "monoalphabetic",
        "name": "2. Monoalphabetic Cipher",
        "category": "Substitution",
        "key_type": "26-letter substitution alphabet",
        "desc": "Arbitrary letter permutation; provides 26! keyspace.",
    },
    {
        "id": "playfair",
        "name": "3. Playfair Cipher",
        "category": "Substitution",
        "key_type": "Keyword (5×5 Matrix, I/J)",
        "desc": "Digraphic cipher encrypting letter pairs using geometric rules.",
    },
    {
        "id": "hill",
        "name": "4. Hill Cipher",
        "category": "Substitution",
        "key_type": "2×2 Invertible Matrix (mod 26)",
        "desc": "Polygraphic matrix multiplication with modular inversion.",
    },
    {
        "id": "vigenere",
        "name": "5. Vigenère Cipher",
        "category": "Substitution",
        "key_type": "Repeating keyword",
        "desc": "Polyalphabetic substitution masking single-letter frequencies.",
    },
    {
        "id": "one_time_pad",
        "name": "6. One-Time Pad",
        "category": "Substitution",
        "key_type": "Random string (secrets)",
        "desc": "Theoretically unbreakable Vernam cipher with perfect secrecy.",
    },
    {
        "id": "rail_fence",
        "name": "7. Rail Fence Cipher",
        "category": "Transposition",
        "key_type": "Positive integer rails (≥ 1)",
        "desc": "Zigzag transposition reading row-by-row along rail patterns.",
    },
    {
        "id": "columnar_transposition",
        "name": "8. Columnar Transposition",
        "category": "Transposition",
        "key_type": "Keyword / column order",
        "desc": "Grid permutation reading columns in alphabetical key rank.",
    },
]


class DashboardView(ttk.Frame):
    """Modern cybersecurity dashboard featuring statistics and cipher cards."""

    def __init__(self, parent: tk.Widget, on_select_cipher: Callable[[str], None], on_navigate: Callable[[str], None]):
        super().__init__(parent, style="Dark.TFrame")
        self.on_select_cipher = on_select_cipher
        self.on_navigate = on_navigate

        self._build_header()
        self._build_stats_ribbon()
        self._build_cards_grid()

    def _build_header(self) -> None:
        header_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=24, pady=(16, 8))

        lbl_title = tk.Label(
            header_frame,
            text="CLASSICAL CRYPTOGRAPHY TOOLKIT",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        )
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(
            header_frame,
            text="Academic Year 2026–27 | Final Year (ECM) | Subject: Network Security",
            font=FONT_SUBTITLE,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_DARK,
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

    def _build_stats_ribbon(self) -> None:
        ribbon = tk.Frame(self, bg=COLOR_BG_DARK)
        ribbon.pack(fill="x", padx=24, pady=8)

        stats = [
            ("8 CIPHERS", "6 Substitution + 2 Transposition"),
            ("HIGH PRECISION", "time.perf_counter_ns() timing"),
            ("JSON ENVELOPE", "Versioned File Security v1.0"),
            ("PURE PYTHON 3", "Zero external dependencies"),
        ]

        for title, subtitle in stats:
            card = tk.Frame(ribbon, bg=COLOR_BG_CARD, padx=12, pady=8, highlightbackground=COLOR_BORDER, highlightthickness=1)
            card.pack(side="left", fill="x", expand=True, padx=4)

            tk.Label(card, text=title, font=FONT_HEADING, fg=COLOR_ACCENT_CYAN, bg=COLOR_BG_CARD).pack(anchor="w")
            tk.Label(card, text=subtitle, font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_CARD).pack(anchor="w")

    def _build_cards_grid(self) -> None:
        container = tk.Frame(self, bg=COLOR_BG_DARK)
        container.pack(fill="both", expand=True, padx=24, pady=12)

        # 4 columns x 2 rows
        for idx, item in enumerate(CIPHER_META):
            row = idx // 4
            col = idx % 4

            card = tk.Frame(
                container,
                bg=COLOR_BG_CARD,
                padx=14,
                pady=12,
                highlightbackground=COLOR_BORDER,
                highlightthickness=1,
            )
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
            container.grid_columnconfigure(col, weight=1)
            container.grid_rowconfigure(row, weight=1)

            # Badge
            badge_color = "#0466c8" if item["category"] == "Substitution" else "#7b2cbf"
            badge = tk.Label(
                card,
                text=f" {item['category'].upper()} ",
                font=FONT_SMALL,
                fg="#ffffff",
                bg=badge_color,
            )
            badge.pack(anchor="w", pady=(0, 4))

            # Name
            name_lbl = tk.Label(
                card,
                text=item["name"],
                font=FONT_HEADING,
                fg=COLOR_TEXT_PRIMARY,
                bg=COLOR_BG_CARD,
                wraplength=180,
                justify="left",
            )
            name_lbl.pack(anchor="w", pady=(2, 2))

            # Desc
            desc_lbl = tk.Label(
                card,
                text=item["desc"],
                font=FONT_SMALL,
                fg=COLOR_TEXT_SECONDARY,
                bg=COLOR_BG_CARD,
                wraplength=180,
                justify="left",
            )
            desc_lbl.pack(anchor="w", pady=(2, 4))

            # Key format
            key_lbl = tk.Label(
                card,
                text=f"Key: {item['key_type']}",
                font=FONT_SMALL,
                fg=COLOR_ACCENT_CYAN,
                bg=COLOR_BG_CARD,
                wraplength=180,
                justify="left",
            )
            key_lbl.pack(anchor="w", pady=(2, 8))

            # Open Button
            cid = item["id"]
            btn = tk.Button(
                card,
                text="Open Cipher →",
                font=FONT_BODY_BOLD,
                bg=COLOR_BG_INPUT,
                fg=COLOR_ACCENT_CYAN,
                activebackground=COLOR_BORDER,
                activeforeground="#ffffff",
                relief="flat",
                command=lambda c=cid: self.on_select_cipher(c),
                cursor="hand2",
            )
            btn.pack(anchor="e", side="bottom")
