"""File Encryption and Decryption GUI View with Envelope Support."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

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
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_BODY_BOLD,
    FONT_MONO,
    FONT_SMALL,
)
from ..ciphers import CIPHER_DISPLAY_NAMES, get_cipher
from ..services.file_service import FileService


class FileOperationView(ttk.Frame):
    """File encryption and decryption workbench with envelope serialization."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, style="Dark.TFrame")
        self._build_header()
        self._build_notebook()

    def _build_header(self) -> None:
        header_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(
            header_frame,
            text="FILE ENCRYPTION & DECRYPTION",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Encapsulates text files into versioned JSON security envelopes with UTF-8 encoding.",
            font=FONT_SUBTITLE,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(2, 0))

    def _build_notebook(self) -> None:
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tab_enc = self._build_encrypt_tab(notebook)
        tab_dec = self._build_decrypt_tab(notebook)

        notebook.add(tab_enc, text="  🔒 Encrypt Text File  ")
        notebook.add(tab_dec, text="  🔓 Decrypt Text File  ")

    def _build_encrypt_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        tab = ttk.Frame(parent, style="Dark.TFrame")

        card = tk.Frame(tab, bg=COLOR_BG_CARD, padx=16, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=6, pady=6)

        # 1. Source file picker
        tk.Label(card, text="1. Select Input Plaintext File (.txt):", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        f_row = tk.Frame(card, bg=COLOR_BG_CARD)
        f_row.pack(fill="x", pady=(4, 10))

        self.enc_in_entry = tk.Entry(f_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.enc_in_entry.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 6))

        btn_browse_in = tk.Button(f_row, text="Browse...", font=FONT_BODY, bg=COLOR_BG_INPUT, fg=COLOR_ACCENT_CYAN, relief="flat", command=self._browse_enc_in, cursor="hand2")
        btn_browse_in.pack(side="right")

        # 2. Algorithm selection & Key
        tk.Label(card, text="2. Choose Cipher & Enter Secret Key:", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        algo_row = tk.Frame(card, bg=COLOR_BG_CARD)
        algo_row.pack(fill="x", pady=(4, 10))

        self.enc_algo_cb = ttk.Combobox(algo_row, values=[item[1] for item in CIPHER_DISPLAY_NAMES], state="readonly", width=36, style="Dark.TCombobox")
        self.enc_algo_cb.current(0)
        self.enc_algo_cb.pack(side="left", padx=(0, 8))

        tk.Label(algo_row, text="Key: ", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(side="left")
        self.enc_key_entry = tk.Entry(algo_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.enc_key_entry.pack(side="left", fill="x", expand=True, ipady=3)
        self.enc_key_entry.insert(0, "5")

        # 3. Output file destination
        tk.Label(card, text="3. Destination Output Envelope Path (.enc / .txt):", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        out_row = tk.Frame(card, bg=COLOR_BG_CARD)
        out_row.pack(fill="x", pady=(4, 14))

        self.enc_out_entry = tk.Entry(out_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.enc_out_entry.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 6))

        btn_browse_out = tk.Button(out_row, text="Choose Save Path...", font=FONT_BODY, bg=COLOR_BG_INPUT, fg=COLOR_ACCENT_CYAN, relief="flat", command=self._browse_enc_out, cursor="hand2")
        btn_browse_out.pack(side="right")

        # Encrypt Action button
        btn_do_enc = tk.Button(card, text="🔒 Execute File Encryption", font=FONT_BODY_BOLD, bg=COLOR_ACCENT_CYAN, fg=COLOR_BG_DARK, activebackground=COLOR_ACCENT_HOVER, relief="flat", padx=16, pady=8, command=self._do_encrypt, cursor="hand2")
        btn_do_enc.pack(anchor="w", pady=(0, 10))

        # Output / Log preview
        self.enc_log = tk.Text(card, height=6, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_SECONDARY, relief="flat")
        self.enc_log.pack(fill="both", expand=True)

        return tab

    def _build_decrypt_tab(self, parent: ttk.Notebook) -> ttk.Frame:
        tab = ttk.Frame(parent, style="Dark.TFrame")

        card = tk.Frame(tab, bg=COLOR_BG_CARD, padx=16, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=6, pady=6)

        # 1. Enveloped file picker
        tk.Label(card, text="1. Select Encrypted File Envelope (.enc / .txt):", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        f_row = tk.Frame(card, bg=COLOR_BG_CARD)
        f_row.pack(fill="x", pady=(4, 10))

        self.dec_in_entry = tk.Entry(f_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.dec_in_entry.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 6))

        btn_browse_in = tk.Button(f_row, text="Browse...", font=FONT_BODY, bg=COLOR_BG_INPUT, fg=COLOR_ACCENT_CYAN, relief="flat", command=self._browse_dec_in, cursor="hand2")
        btn_browse_in.pack(side="right", padx=(0, 4))

        btn_inspect = tk.Button(f_row, text="Inspect Envelope", font=FONT_BODY, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, relief="flat", command=self._inspect_envelope, cursor="hand2")
        btn_inspect.pack(side="right")

        # 2. Secret Key entry
        tk.Label(card, text="2. Enter Secret Key (Keys are NOT stored inside envelope):", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        key_row = tk.Frame(card, bg=COLOR_BG_CARD)
        key_row.pack(fill="x", pady=(4, 10))

        self.dec_key_entry = tk.Entry(key_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.dec_key_entry.pack(side="left", fill="x", expand=True, ipady=3)

        # 3. Output destination
        tk.Label(card, text="3. Destination Decrypted Plaintext File Path:", font=FONT_BODY_BOLD, fg=COLOR_TEXT_PRIMARY, bg=COLOR_BG_CARD).pack(anchor="w")
        out_row = tk.Frame(card, bg=COLOR_BG_CARD)
        out_row.pack(fill="x", pady=(4, 14))

        self.dec_out_entry = tk.Entry(out_row, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_PRIMARY, insertbackground=COLOR_ACCENT_CYAN, relief="flat")
        self.dec_out_entry.pack(side="left", fill="x", expand=True, ipady=3, padx=(0, 6))

        btn_browse_out = tk.Button(out_row, text="Choose Save Path...", font=FONT_BODY, bg=COLOR_BG_INPUT, fg=COLOR_ACCENT_CYAN, relief="flat", command=self._browse_dec_out, cursor="hand2")
        btn_browse_out.pack(side="right")

        # Decrypt Action button
        btn_do_dec = tk.Button(card, text="🔓 Execute File Decryption", font=FONT_BODY_BOLD, bg=COLOR_ACCENT_BLUE, fg="#ffffff", activebackground=COLOR_ACCENT_HOVER, relief="flat", padx=16, pady=8, command=self._do_decrypt, cursor="hand2")
        btn_do_dec.pack(anchor="w", pady=(0, 10))

        # Log preview
        self.dec_log = tk.Text(card, height=6, font=FONT_MONO, bg=COLOR_BG_INPUT, fg=COLOR_TEXT_SECONDARY, relief="flat")
        self.dec_log.pack(fill="both", expand=True)

        return tab

    def _browse_enc_in(self) -> None:
        path = filedialog.askopenfilename(title="Select Plaintext File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.enc_in_entry.delete(0, tk.END)
            self.enc_in_entry.insert(0, path)
            # Suggest output file name
            suggested = str(Path(path).with_suffix(".enc.txt"))
            self.enc_out_entry.delete(0, tk.END)
            self.enc_out_entry.insert(0, suggested)

    def _browse_enc_out(self) -> None:
        path = filedialog.asksaveasfilename(title="Save Encrypted Envelope As", filetypes=[("Text / Envelope Files", "*.txt;*.enc"), ("All Files", "*.*")])
        if path:
            self.enc_out_entry.delete(0, tk.END)
            self.enc_out_entry.insert(0, path)

    def _browse_dec_in(self) -> None:
        path = filedialog.askopenfilename(title="Select Encrypted File", filetypes=[("Envelope / Text Files", "*.txt;*.enc"), ("All Files", "*.*")])
        if path:
            self.dec_in_entry.delete(0, tk.END)
            self.dec_in_entry.insert(0, path)
            suggested = str(Path(path).with_name("decrypted_" + Path(path).name.replace(".enc", "")))
            self.dec_out_entry.delete(0, tk.END)
            self.dec_out_entry.insert(0, suggested)

    def _browse_dec_out(self) -> None:
        path = filedialog.asksaveasfilename(title="Save Decrypted Plaintext As", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.dec_out_entry.delete(0, tk.END)
            self.dec_out_entry.insert(0, path)

    def _inspect_envelope(self) -> None:
        in_path = self.dec_in_entry.get().strip()
        if not in_path:
            messagebox.showwarning("Missing Input", "Please select an encrypted envelope file first.")
            return
        try:
            env = FileService.inspect_encrypted_file(in_path)
            algo = env.get("algorithm", "unknown")
            created = env.get("created_at_utc", "unknown")
            orig_name = env.get("original_filename", "unknown")
            params = env.get("parameters", {})
            ct_len = len(env.get("ciphertext", ""))

            msg = (
                f"File Envelope Inspection:\n\n"
                f"• Algorithm: {algo.upper()}\n"
                f"• Timestamp: {created}\n"
                f"• Original Filename: {orig_name}\n"
                f"• Ciphertext Length: {ct_len} characters\n"
                f"• Parameters: {params}\n\n"
                f"Notice: The secret key is NOT stored in the file envelope. Enter the correct key to decrypt."
            )
            messagebox.showinfo("Envelope Metadata", msg)
        except Exception as exc:
            messagebox.showerror("Inspection Error", f"Failed to inspect envelope:\n{exc}")

    def _do_encrypt(self) -> None:
        in_p = self.enc_in_entry.get().strip()
        out_p = self.enc_out_entry.get().strip()
        key = self.enc_key_entry.get().strip()
        algo_idx = self.enc_algo_cb.current()
        cid = CIPHER_DISPLAY_NAMES[algo_idx][0]

        if not in_p or not out_p:
            messagebox.showerror("Missing Paths", "Please specify both input and destination file paths.")
            return

        # Check overwrite
        if Path(out_p).exists():
            if not messagebox.askyesno("File Exists", f"Destination file already exists:\n'{out_p}'\n\nOverwrite it?"):
                return

        try:
            res = FileService.encrypt_file(in_p, out_p, cid, key, overwrite=True)
            self.enc_log.delete("1.0", tk.END)
            log_text = (
                f"✓ SUCCESS: {res.message}\n"
                f"Destination: {res.output_path}\n"
                f"Input Size: {res.input_size_bytes} bytes | Output Envelope: {res.output_size_bytes} bytes\n"
                f"Execution Time: {res.execution_time_ms:.3f} ms ({res.execution_time_ns} ns)\n"
                f"Algorithm Notes: {res.details.get('notes', '')}\n"
            )
            self.enc_log.insert("1.0", log_text)
            messagebox.showinfo("Encryption Completed", f"Successfully encrypted file to:\n{res.output_path}")
        except Exception as exc:
            self.enc_log.delete("1.0", tk.END)
            self.enc_log.insert("1.0", f"✗ FAILED: {exc}\n")
            messagebox.showerror("Encryption Failed", str(exc))

    def _do_decrypt(self) -> None:
        in_p = self.dec_in_entry.get().strip()
        out_p = self.dec_out_entry.get().strip()
        key = self.dec_key_entry.get().strip()

        if not in_p or not out_p:
            messagebox.showerror("Missing Paths", "Please specify both input and destination file paths.")
            return

        if Path(out_p).exists():
            if not messagebox.askyesno("File Exists", f"Destination file already exists:\n'{out_p}'\n\nOverwrite it?"):
                return

        try:
            res = FileService.decrypt_file(in_p, out_p, key, overwrite=True)
            self.dec_log.delete("1.0", tk.END)
            log_text = (
                f"✓ SUCCESS: {res.message}\n"
                f"Destination: {res.output_path}\n"
                f"Input Envelope: {res.input_size_bytes} bytes | Decrypted File: {res.output_size_bytes} bytes\n"
                f"Execution Time: {res.execution_time_ms:.3f} ms ({res.execution_time_ns} ns)\n"
                f"Algorithm Notes: {res.details.get('notes', '')}\n"
            )
            self.dec_log.insert("1.0", log_text)
            messagebox.showinfo("Decryption Completed", f"Successfully decrypted file to:\n{res.output_path}")
        except Exception as exc:
            self.dec_log.delete("1.0", tk.END)
            self.dec_log.insert("1.0", f"✗ FAILED: {exc}\n")
            messagebox.showerror("Decryption Failed", str(exc))
