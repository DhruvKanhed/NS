"""Algorithm Comparison and Benchmarking GUI View."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

from .theme import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BG_INPUT,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_HOVER,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_WARNING,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_MONO,
    FONT_SMALL,
)
from ..ciphers import CIPHER_REGISTRY
from ..services.comparison_service import ComparisonService, ComparisonRow


class ComparisonView(ttk.Frame):
    """Side-by-side performance benchmark and cryptanalysis comparison view."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, style="Dark.TFrame")
        self._build_header()
        self._build_controls()
        self._build_table()
        self._build_details_footer()
        # Run default comparison
        self._run_benchmarks()

    def _build_header(self) -> None:
        header_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(
            header_frame,
            text="ALGORITHM COMPARISON & BENCHMARK",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Empirical micro-timing and cryptanalytic weakness comparison under identical inputs.",
            font=FONT_SUBTITLE,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(2, 0))

    def _build_controls(self) -> None:
        ctrl_card = tk.Frame(self, bg=COLOR_BG_CARD, padx=14, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        ctrl_card.pack(fill="x", padx=20, pady=(0, 10))

        # Sample text row
        txt_row = tk.Frame(ctrl_card, bg=COLOR_BG_CARD)
        txt_row.pack(fill="x", pady=(0, 8))

        tk.Label(txt_row, text="Test Message:", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(side="left")

        self.entry_message = tk.Entry(
            txt_row,
            font=FONT_MONO,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_ACCENT_CYAN,
            relief="flat",
        )
        self.entry_message.pack(side="left", fill="x", expand=True, padx=8, ipady=3)
        self.entry_message.insert(0, "NETWORK SECURITY FINAL YEAR ECM 2026")

        btn_run = tk.Button(
            txt_row,
            text="⚡ Run Benchmark",
            font=FONT_BODY_BOLD,
            bg=COLOR_ACCENT_CYAN,
            fg=COLOR_BG_DARK,
            activebackground=COLOR_ACCENT_HOVER,
            relief="flat",
            padx=14,
            pady=4,
            command=self._run_benchmarks,
            cursor="hand2",
        )
        btn_run.pack(side="right")

        # Ciphers selection checkboxes
        cb_row = tk.Frame(ctrl_card, bg=COLOR_BG_CARD)
        cb_row.pack(fill="x")

        tk.Label(cb_row, text="Included Ciphers: ", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_CARD).pack(side="left")

        self.cipher_vars: Dict[str, tk.BooleanVar] = {}
        for cid in CIPHER_REGISTRY.keys():
            var = tk.BooleanVar(value=True)
            self.cipher_vars[cid] = var
            short_label = cid.replace("_", " ").title()
            cb = tk.Checkbutton(
                cb_row,
                text=short_label,
                variable=var,
                bg=COLOR_BG_CARD,
                fg=COLOR_TEXT_PRIMARY,
                selectcolor=COLOR_BG_INPUT,
                activebackground=COLOR_BG_CARD,
                activeforeground=COLOR_ACCENT_CYAN,
                font=FONT_SMALL,
            )
            cb.pack(side="left", padx=4)

    def _build_table(self) -> None:
        table_frame = tk.Frame(self, bg=COLOR_BG_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        columns = ("algorithm", "category", "key_type", "enc_time", "dec_time", "roundtrip", "ciphertext")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("algorithm", text="Algorithm Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("key_type", text="Key Type")
        self.tree.heading("enc_time", text="Enc (µs)")
        self.tree.heading("dec_time", text="Dec (µs)")
        self.tree.heading("roundtrip", text="Roundtrip")
        self.tree.heading("ciphertext", text="Sample Ciphertext")

        self.tree.column("algorithm", width=180, anchor="w")
        self.tree.column("category", width=110, anchor="center")
        self.tree.column("key_type", width=150, anchor="w")
        self.tree.column("enc_time", width=80, anchor="e")
        self.tree.column("dec_time", width=80, anchor="e")
        self.tree.column("roundtrip", width=80, anchor="center")
        self.tree.column("ciphertext", width=220, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _build_details_footer(self) -> None:
        footer = tk.Frame(self, bg=COLOR_BG_CARD, padx=12, pady=8, highlightbackground=COLOR_BORDER, highlightthickness=1)
        footer.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(footer, text="SELECTED CIPHER CRYPTANALYSIS & LIMITATIONS:", font=FONT_HEADING, fg=COLOR_ACCENT_CYAN, bg=COLOR_BG_CARD).pack(anchor="w")

        self.lbl_details = tk.Label(
            footer,
            text="Click any row above to inspect mathematical vulnerability details.",
            font=FONT_SMALL,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_CARD,
            wraplength=880,
            justify="left",
        )
        self.lbl_details.pack(anchor="w", pady=(4, 0))

    def _run_benchmarks(self) -> None:
        msg = self.entry_message.get().strip()
        if not msg:
            messagebox.showwarning("Empty Message", "Please enter a test message to run benchmarks.")
            return

        selected = [cid for cid, var in self.cipher_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("No Ciphers Selected", "Please select at least one cipher to compare.")
            return

        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.latest_rows = ComparisonService.run_comparison(msg, selected_cipher_ids=selected)

        for r in self.latest_rows:
            rt_str = "✓ PASS" if r.round_trip_success else "⚠ NORM"
            short_ct = r.ciphertext if len(r.ciphertext) <= 28 else r.ciphertext[:25] + "..."
            self.tree.insert(
                "",
                "end",
                iid=r.cipher_id,
                values=(
                    r.cipher_name,
                    r.category,
                    r.key_type,
                    f"{r.enc_time_us:.2f}",
                    f"{r.dec_time_us:.2f}",
                    rt_str,
                    short_ct,
                ),
            )

    def _on_row_select(self, event) -> None:
        selected_items = self.tree.selection()
        if not selected_items:
            return
        cid = selected_items[0]
        for r in self.latest_rows:
            if r.cipher_id == cid:
                text = (
                    f"Algorithm: {r.cipher_name} [{r.category}]\n"
                    f"Security Status: {r.security_verdict}\n"
                    f"Weakness & Limitations: {r.limitations}\n"
                    f"Roundtrip Recovery: {'Recovered successfully' if r.round_trip_success else 'Normalized or padded (Playfair/Hill filler rules)'}"
                )
                self.lbl_details.config(text=text)
                break
