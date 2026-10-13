"""About Project GUI view with academic metadata and placeholders."""

import tkinter as tk
from tkinter import ttk

from .theme import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BG_INPUT,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_ACCENT_CYAN,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_MONO,
    FONT_SMALL,
)


class AboutProjectView(ttk.Frame):
    """Academic mini-project metadata and specifications."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, style="Dark.TFrame")
        self._build_layout()

    def _build_layout(self) -> None:
        header_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(
            header_frame,
            text="ABOUT THE PROJECT",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Academic Mini-Project Submission | Academic Year 2026–27",
            font=FONT_SUBTITLE,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(2, 0))

        card = tk.Frame(self, bg=COLOR_BG_CARD, padx=20, pady=16, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=20, pady=(10, 14))

        metadata = [
            ("Project Title:", "Design and Development of a Classical Cryptography Toolkit"),
            ("Course / Degree:", "Final Year B.Tech / B.E. (ECM - Electronics & Computer Engineering)"),
            ("Academic Year:", "2026–2027"),
            ("Subject:", "Network Security"),
            ("Student Name:", "[STUDENT_NAME_PLACEHOLDER]"),
            ("Roll Number:", "[ROLL_NUMBER_PLACEHOLDER]"),
            ("Batch:", "[BATCH_ID_PLACEHOLDER]"),
            ("Faculty Guide:", "[FACULTY_GUIDE_NAME_PLACEHOLDER]"),
            ("Institution:", "[COLLEGE_OR_INSTITUTE_NAME_PLACEHOLDER]"),
            ("Programming Language:", "Python 3 (Standard Library + Tkinter GUI)"),
            ("File Envelope Format:", "JSON Envelope v1.0 (UTF-8, No plaintext secrets stored)"),
            ("Benchmarking Engine:", "High-Resolution Monotonic Timer (time.perf_counter_ns)"),
        ]

        for idx, (label, val) in enumerate(metadata):
            row = tk.Frame(card, bg=COLOR_BG_CARD)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=label, font=FONT_BODY_BOLD, fg=COLOR_ACCENT_CYAN, bg=COLOR_BG_CARD, width=24, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=FONT_BODY, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD, anchor="w").pack(side="left", fill="x", expand=True)

        disclaimer_box = tk.Frame(card, bg=COLOR_BG_INPUT, padx=12, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        disclaimer_box.pack(fill="x", pady=(16, 0))

        tk.Label(
            disclaimer_box,
            text="EDUCATIONAL INTEGRITY & CYBERSECURITY NOTICE",
            font=FONT_BODY_BOLD,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_INPUT,
        ).pack(anchor="w")

        tk.Label(
            disclaimer_box,
            text=(
                "This software suite was engineered strictly for academic education, algorithm demonstration, "
                "and cryptographic principle analysis in Network Security coursework. Classical ciphers do NOT provide "
                "modern confidentiality or data integrity. Do not deploy these algorithms to protect sensitive real-world records."
            ),
            font=FONT_SMALL,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_INPUT,
            wraplength=800,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))
