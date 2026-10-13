"""Interactive Cipher views supporting all 8 classical ciphers."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional

from .theme import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BG_INPUT,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_ACCENT_CYAN,
    COLOR_ACCENT_HOVER,
    COLOR_ACCENT_BLUE,
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
from ..ciphers import get_cipher, CIPHER_REGISTRY, CIPHER_DISPLAY_NAMES
from ..ciphers.monoalphabetic import MonoalphabeticCipher
from ..ciphers.one_time_pad import OneTimePadCipher


CIPHER_DEFAULTS = {
    "caesar": ("NETWORK SECURITY", "5", "Integer shift (0–25)"),
    "monoalphabetic": ("HELLO WORLD", "QWERTYUIOPASDFGHJKLZXCVBNM", "26-letter substitution alphabet"),
    "playfair": ("BALLOON ATTACK", "MONARCHY", "Keyword for 5×5 matrix (I/J combined)"),
    "hill": ("ACT", "3 3 2 5", "4 integers (a b c d) or 4 letters e.g. 'DDCF'"),
    "vigenere": ("ATTACK AT DAWN", "LEMON", "Repeating alphabetic keyword"),
    "one_time_pad": ("SECRET MESSAGE", "", "Leave empty to auto-generate or enter key"),
    "rail_fence": ("DEFEND THE EAST WALL", "3", "Positive integer rails count (≥ 1)"),
    "columnar_transposition": ("DEFEND THE EAST WALL", "GERMAN", "Keyword or numeric order"),
}


class CipherWorkbenchView(ttk.Frame):
    """Unified, interactive cipher workbench supporting all eight ciphers."""

    def __init__(self, parent: tk.Widget, default_cipher_id: str = "caesar", filter_category: Optional[str] = None):
        super().__init__(parent, style="Dark.TFrame")
        self.current_cipher_id = default_cipher_id
        self.filter_category = filter_category

        self._build_header_and_selector()
        self._build_workbench()
        self.switch_cipher(default_cipher_id)

    def _build_header_and_selector(self) -> None:
        top_bar = tk.Frame(self, bg=COLOR_BG_DARK)
        top_bar.pack(fill="x", padx=20, pady=(14, 8))

        lbl_title = tk.Label(
            top_bar,
            text="CIPHER WORKBENCH",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        )
        lbl_title.pack(side="left")

        # Cipher selector combobox
        sel_frame = tk.Frame(top_bar, bg=COLOR_BG_DARK)
        sel_frame.pack(side="right")

        tk.Label(
            sel_frame,
            text="Select Algorithm: ",
            font=FONT_BODY_BOLD,
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG_DARK,
        ).pack(side="left", padx=4)

        self.ciphers_list = []
        for cid, display in CIPHER_DISPLAY_NAMES:
            cipher = get_cipher(cid)
            if self.filter_category is None or cipher.category == self.filter_category:
                self.ciphers_list.append((cid, display))

        self.cipher_combobox = ttk.Combobox(
            sel_frame,
            values=[item[1] for item in self.ciphers_list],
            state="readonly",
            width=36,
            style="Dark.TCombobox",
        )
        self.cipher_combobox.pack(side="left", padx=4)
        self.cipher_combobox.bind("<<ComboboxSelected>>", self._on_combobox_select)

    def switch_cipher(self, cipher_id: str) -> None:
        """Switch current workbench view to a specific cipher."""
        self.current_cipher_id = cipher_id
        # Sync combobox
        for idx, (cid, display) in enumerate(self.ciphers_list):
            if cid == cipher_id:
                self.cipher_combobox.current(idx)
                break

        cipher = get_cipher(cipher_id)
        self.lbl_cipher_name.config(text=f"{cipher.name.upper()} ({cipher.category.upper()})")
        self.lbl_cipher_desc.config(text=cipher.description)

        # Set sensible default inputs and hints
        default_in, default_k, hint = CIPHER_DEFAULTS.get(cipher_id, ("SAMPLE TEXT", "1", "Key"))
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.insert("1.0", default_in)
        self.entry_key.delete(0, tk.END)
        self.entry_key.insert(0, default_k)
        self.lbl_key_hint.config(text=f"Format: {hint}")

        # Show/hide key generator button for Monoalphabetic & OTP
        if cipher_id in ("monoalphabetic", "one_time_pad"):
            self.btn_gen_key.pack(side="left", padx=6)
        else:
            self.btn_gen_key.pack_forget()

        self._clear_output()
        self._update_counts()

    def _on_combobox_select(self, event) -> None:
        sel_idx = self.cipher_combobox.current()
        if 0 <= sel_idx < len(self.ciphers_list):
            cid = self.ciphers_list[sel_idx][0]
            self.switch_cipher(cid)

    def _build_workbench(self) -> None:
        # Description banner
        desc_card = tk.Frame(self, bg=COLOR_BG_CARD, padx=16, pady=10, highlightbackground=COLOR_BORDER, highlightthickness=1)
        desc_card.pack(fill="x", padx=20, pady=(0, 10))

        self.lbl_cipher_name = tk.Label(desc_card, text="", font=FONT_HEADING, fg=COLOR_ACCENT_CYAN, bg=COLOR_BG_CARD)
        self.lbl_cipher_name.pack(anchor="w")

        self.lbl_cipher_desc = tk.Label(desc_card, text="", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_CARD)
        self.lbl_cipher_desc.pack(anchor="w", pady=(2, 0))

        # Main Split Content: Left = Inputs/Outputs, Right = Educational Matrix/Notes Panel
        content_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        left_pane = tk.Frame(content_frame, bg=COLOR_BG_DARK)
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_pane = tk.Frame(content_frame, bg=COLOR_BG_CARD, width=320, padx=12, pady=12, highlightbackground=COLOR_BORDER, highlightthickness=1)
        right_pane.pack(side="right", fill="both", padx=(0, 0))

        # Key Input Row
        key_card = tk.Frame(left_pane, bg=COLOR_BG_CARD, padx=12, pady=8, highlightbackground=COLOR_BORDER, highlightthickness=1)
        key_card.pack(fill="x", pady=(0, 8))

        key_top_row = tk.Frame(key_card, bg=COLOR_BG_CARD)
        key_top_row.pack(fill="x")

        tk.Label(key_top_row, text="Secret / Shift Key:", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(side="left")
        self.lbl_key_hint = tk.Label(key_top_row, text="", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_CARD)
        self.lbl_key_hint.pack(side="left", padx=10)

        key_input_row = tk.Frame(key_card, bg=COLOR_BG_CARD)
        key_input_row.pack(fill="x", pady=(4, 0))

        self.entry_key = tk.Entry(
            key_input_row,
            font=FONT_MONO,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_ACCENT_CYAN,
            relief="flat",
        )
        self.entry_key.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 6))

        self.btn_gen_key = tk.Button(
            key_input_row,
            text="Generate Key",
            font=FONT_SMALL,
            bg=COLOR_BG_DARK,
            fg=COLOR_ACCENT_CYAN,
            activebackground=COLOR_BORDER,
            activeforeground="#ffffff",
            relief="flat",
            command=self._generate_random_key,
            cursor="hand2",
        )

        # Input Text Section
        in_header = tk.Frame(left_pane, bg=COLOR_BG_DARK)
        in_header.pack(fill="x", pady=(2, 2))

        tk.Label(in_header, text="Input Text", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_DARK).pack(side="left")
        self.lbl_in_count = tk.Label(in_header, text="Length: 0 chars", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_DARK)
        self.lbl_in_count.pack(side="right")

        self.txt_input = tk.Text(
            left_pane,
            height=4,
            font=FONT_MONO,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_ACCENT_CYAN,
            relief="flat",
            wrap="word",
        )
        self.txt_input.pack(fill="x", pady=(0, 6))
        self.txt_input.bind("<KeyRelease>", lambda e: self._update_counts())

        # Action Buttons Row
        actions_bar = tk.Frame(left_pane, bg=COLOR_BG_DARK)
        actions_bar.pack(fill="x", pady=4)

        btn_enc = tk.Button(
            actions_bar,
            text="🔒 Encrypt",
            font=FONT_BODY_BOLD,
            bg=COLOR_ACCENT_CYAN,
            fg=COLOR_BG_DARK,
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_BG_DARK,
            relief="flat",
            padx=16,
            pady=6,
            command=self._handle_encrypt,
            cursor="hand2",
        )
        btn_enc.pack(side="left", padx=(0, 6))

        btn_dec = tk.Button(
            actions_bar,
            text="🔓 Decrypt",
            font=FONT_BODY_BOLD,
            bg=COLOR_ACCENT_BLUE,
            fg="#ffffff",
            activebackground=COLOR_ACCENT_HOVER,
            activeforeground=COLOR_BG_DARK,
            relief="flat",
            padx=16,
            pady=6,
            command=self._handle_decrypt,
            cursor="hand2",
        )
        btn_dec.pack(side="left", padx=6)

        btn_swap = tk.Button(
            actions_bar,
            text="⇄ Swap In/Out",
            font=FONT_BODY,
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_PRIMARY,
            activebackground=COLOR_BORDER,
            activeforeground=COLOR_ACCENT_CYAN,
            relief="flat",
            padx=10,
            pady=6,
            command=self._swap_texts,
            cursor="hand2",
        )
        btn_swap.pack(side="left", padx=6)

        btn_clear = tk.Button(
            actions_bar,
            text="Clear",
            font=FONT_BODY,
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_SECONDARY,
            activebackground=COLOR_BORDER,
            activeforeground=COLOR_DANGER,
            relief="flat",
            padx=10,
            pady=6,
            command=self._clear_all,
            cursor="hand2",
        )
        btn_clear.pack(side="left", padx=6)

        self.lbl_exec_time = tk.Label(
            actions_bar,
            text="Execution Time: --",
            font=FONT_SMALL,
            fg=COLOR_SUCCESS,
            bg=COLOR_BG_DARK,
        )
        self.lbl_exec_time.pack(side="right")

        # Output Text Section
        out_header = tk.Frame(left_pane, bg=COLOR_BG_DARK)
        out_header.pack(fill="x", pady=(6, 2))

        tk.Label(out_header, text="Result / Output Text", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_DARK).pack(side="left")
        self.lbl_out_count = tk.Label(out_header, text="Length: 0 chars", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_DARK)
        self.lbl_out_count.pack(side="right")

        self.txt_output = tk.Text(
            left_pane,
            height=4,
            font=FONT_MONO,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_ACCENT_CYAN,
            relief="flat",
            wrap="word",
        )
        self.txt_output.pack(fill="x", pady=(0, 6))

        out_actions = tk.Frame(left_pane, bg=COLOR_BG_DARK)
        out_actions.pack(fill="x")

        btn_copy = tk.Button(
            out_actions,
            text="📋 Copy Output to Clipboard",
            font=FONT_BODY,
            bg=COLOR_BG_CARD,
            fg=COLOR_ACCENT_CYAN,
            activebackground=COLOR_BORDER,
            activeforeground="#ffffff",
            relief="flat",
            padx=12,
            pady=4,
            command=self._copy_output,
            cursor="hand2",
        )
        btn_copy.pack(side="left")

        self.lbl_status = tk.Label(out_actions, text="Ready", font=FONT_SMALL, fg=COLOR_TEXT_SECONDARY, bg=COLOR_BG_DARK)
        self.lbl_status.pack(side="right")

        # Right Educational / Matrix / Notes Panel
        tk.Label(
            right_pane,
            text="ALGORITHM ARTIFACTS & DETAILS",
            font=FONT_HEADING,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_CARD,
        ).pack(anchor="w", pady=(0, 6))

        self.txt_details = tk.Text(
            right_pane,
            font=FONT_MONO,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_SECONDARY,
            relief="flat",
            wrap="word",
        )
        self.txt_details.pack(fill="both", expand=True)

    def _update_counts(self) -> None:
        in_text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        out_text = self.txt_output.get("1.0", tk.END).rstrip("\n")
        self.lbl_in_count.config(text=f"Length: {len(in_text)} chars")
        self.lbl_out_count.config(text=f"Length: {len(out_text)} chars")

    def _clear_output(self) -> None:
        self.txt_output.delete("1.0", tk.END)
        self.lbl_exec_time.config(text="Execution Time: --")
        self.lbl_status.config(text="Ready", fg=COLOR_TEXT_SECONDARY)
        self.txt_details.delete("1.0", tk.END)
        self.txt_details.insert("1.0", "Execute encryption or decryption to inspect matrix transformations, grids, and notes.")

    def _clear_all(self) -> None:
        self.txt_input.delete("1.0", tk.END)
        self._clear_output()
        self._update_counts()

    def _swap_texts(self) -> None:
        out_text = self.txt_output.get("1.0", tk.END).rstrip("\n")
        if not out_text:
            return
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.insert("1.0", out_text)
        self._clear_output()
        self._update_counts()

    def _copy_output(self) -> None:
        out_text = self.txt_output.get("1.0", tk.END).rstrip("\n")
        if not out_text:
            return
        self.clipboard_clear()
        self.clipboard_append(out_text)
        self.lbl_status.config(text="✓ Copied to clipboard!", fg=COLOR_SUCCESS)

    def _generate_random_key(self) -> None:
        if self.current_cipher_id == "monoalphabetic":
            rand_key = MonoalphabeticCipher.generate_key()
            self.entry_key.delete(0, tk.END)
            self.entry_key.insert(0, rand_key)
            self.lbl_status.config(text="Generated random 26-letter substitution alphabet.", fg=COLOR_SUCCESS)
        elif self.current_cipher_id == "one_time_pad":
            in_text = self.txt_input.get("1.0", tk.END).rstrip("\n")
            alpha_len = sum(1 for ch in in_text if ch.isalpha())
            rand_key = OneTimePadCipher.generate_random_key(max(alpha_len, 16))
            self.entry_key.delete(0, tk.END)
            self.entry_key.insert(0, rand_key)
            self.lbl_status.config(text=f"Generated {len(rand_key)}-character cryptographic key via secrets.", fg=COLOR_SUCCESS)

    def _handle_encrypt(self) -> None:
        cipher = get_cipher(self.current_cipher_id)
        in_text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        key_val = self.entry_key.get().strip()

        try:
            res = cipher.timed_encrypt(in_text, key_val)
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert("1.0", res.text)

            us = res.execution_time_us
            ms = res.execution_time_ms
            self.lbl_exec_time.config(text=f"Time: {us:.2f} µs ({ms:.4f} ms)")
            self.lbl_status.config(text="✓ Encryption Successful", fg=COLOR_SUCCESS)

            # Update details panel
            self.txt_details.delete("1.0", tk.END)
            details_content = f"Operation: Encryption\nAlgorithm: {cipher.name}\nKey Display: {res.key_display}\n\n"
            if res.notes:
                details_content += f"Notes:\n{res.notes}\n\n"
            if "matrix_display" in res.metadata:
                details_content += f"Matrix:\n{res.metadata['matrix_display']}\n\n"
            if "grid_viz" in res.metadata:
                details_content += f"Transposition Grid:\n{res.metadata['grid_viz']}\n\n"
            self.txt_details.insert("1.0", details_content)

            # In case OTP auto-generated a key
            if self.current_cipher_id == "one_time_pad" and not key_val:
                self.entry_key.delete(0, tk.END)
                self.entry_key.insert(0, res.key_display)

            self._update_counts()

        except Exception as exc:
            self.lbl_status.config(text=f"✗ Error: {exc}", fg=COLOR_DANGER)
            messagebox.showerror("Cipher Error", str(exc))

    def _handle_decrypt(self) -> None:
        cipher = get_cipher(self.current_cipher_id)
        in_text = self.txt_input.get("1.0", tk.END).rstrip("\n")
        key_val = self.entry_key.get().strip()

        try:
            res = cipher.timed_decrypt(in_text, key_val)
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert("1.0", res.text)

            us = res.execution_time_us
            ms = res.execution_time_ms
            self.lbl_exec_time.config(text=f"Time: {us:.2f} µs ({ms:.4f} ms)")
            self.lbl_status.config(text="✓ Decryption Successful", fg=COLOR_SUCCESS)

            # Update details panel
            self.txt_details.delete("1.0", tk.END)
            details_content = f"Operation: Decryption\nAlgorithm: {cipher.name}\nKey Display: {res.key_display}\n\n"
            if res.notes:
                details_content += f"Notes:\n{res.notes}\n\n"
            if "matrix_display" in res.metadata:
                details_content += f"Matrix:\n{res.metadata['matrix_display']}\n\n"
            self.txt_details.insert("1.0", details_content)

            self._update_counts()

        except Exception as exc:
            self.lbl_status.config(text=f"✗ Error: {exc}", fg=COLOR_DANGER)
            messagebox.showerror("Cipher Error", str(exc))
