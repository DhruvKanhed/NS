"""File encryption and decryption operations service."""

from dataclasses import dataclass
import os
from pathlib import Path
import time
from typing import Any, Dict, Optional, Tuple

from ..ciphers import get_cipher
from .envelope_service import create_envelope, parse_envelope, EnvelopeError


@dataclass
class FileOperationResult:
    """Result of file encryption or decryption."""
    success: bool
    operation: str  # "encrypt" or "decrypt"
    algorithm: str
    input_path: str
    output_path: str
    input_size_bytes: int
    output_size_bytes: int
    execution_time_ns: int
    message: str
    details: Dict[str, Any]

    @property
    def execution_time_ms(self) -> float:
        return self.execution_time_ns / 1_000_000.0


class FileService:
    """Handles secure, validated file encryption and decryption."""

    @staticmethod
    def read_text_file(filepath: str) -> str:
        """Safely read UTF-8 text file with informative errors."""
        p = Path(filepath)
        if not p.exists():
            raise FileNotFoundError(f"Input file does not exist: '{filepath}'")
        if not p.is_file():
            raise IsADirectoryError(f"Target is a directory, not a file: '{filepath}'")
        try:
            return p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Fallback with error
            raise ValueError(
                f"File '{p.name}' is not a valid UTF-8 text file. "
                "Only UTF-8 encoded text files are supported for classical cipher operations."
            )
        except PermissionError:
            raise PermissionError(f"Permission denied when attempting to read '{filepath}'.")

    @staticmethod
    def write_text_file(filepath: str, content: str, overwrite: bool = False) -> None:
        """Safely write UTF-8 text file with overwrite guard."""
        p = Path(filepath)
        if p.exists() and not overwrite:
            raise FileExistsError(f"Output file already exists: '{filepath}'")
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        except PermissionError:
            raise PermissionError(f"Permission denied when attempting to write to '{filepath}'.")

    @classmethod
    def encrypt_file(
        cls,
        input_path: str,
        output_path: str,
        cipher_id: str,
        key: Any,
        overwrite: bool = False
    ) -> FileOperationResult:
        """Encrypt a text file and package into a versioned envelope."""
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()

        if in_p == out_p:
            raise ValueError(
                "Input and output file paths cannot be the same. "
                "Specify a distinct destination to avoid overwriting your original file."
            )

        t0 = time.perf_counter_ns()
        content = cls.read_text_file(str(in_p))
        cipher = get_cipher(cipher_id)

        # Nonsecret parameters to record in envelope
        public_params = {
            "category": cipher.category,
            "original_char_count": len(content),
        }

        # Perform encryption
        res = cipher.timed_encrypt(content, key)

        # Store envelope without secret key
        envelope_str = create_envelope(
            cipher_id=cipher_id,
            ciphertext=res.text,
            public_params=public_params,
            original_filename=in_p.name,
        )

        cls.write_text_file(str(out_p), envelope_str, overwrite=overwrite)
        t1 = time.perf_counter_ns()

        in_size = in_p.stat().st_size
        out_size = out_p.stat().st_size

        return FileOperationResult(
            success=True,
            operation="encrypt",
            algorithm=cipher.name,
            input_path=str(in_p),
            output_path=str(out_p),
            input_size_bytes=in_size,
            output_size_bytes=out_size,
            execution_time_ns=t1 - t0,
            message=f"Successfully encrypted '{in_p.name}' using {cipher.name}.",
            details={
                "notes": res.notes,
                "key_display": res.key_display,
                "metadata": res.metadata,
            }
        )

    @classmethod
    def inspect_encrypted_file(cls, input_path: str) -> Dict[str, Any]:
        """Read and inspect an encrypted envelope file without decrypting yet."""
        content = cls.read_text_file(input_path)
        return parse_envelope(content)

    @classmethod
    def decrypt_file(
        cls,
        input_path: str,
        output_path: str,
        key: Any,
        cipher_id_override: Optional[str] = None,
        overwrite: bool = False
    ) -> FileOperationResult:
        """Decrypt an enveloped text file using the provided key."""
        in_p = Path(input_path).resolve()
        out_p = Path(output_path).resolve()

        if in_p == out_p:
            raise ValueError(
                "Input and output file paths cannot be the same. "
                "Specify a distinct destination file."
            )

        t0 = time.perf_counter_ns()
        raw_content = cls.read_text_file(str(in_p))

        # Check if wrapped in standard envelope or raw text
        try:
            envelope = parse_envelope(raw_content)
            cipher_id = envelope.get("algorithm", cipher_id_override or "caesar")
            ciphertext = envelope.get("ciphertext", "")
        except EnvelopeError:
            # Fall back to using user-supplied cipher_id_override on raw text
            if not cipher_id_override:
                raise ValueError(
                    "The file is not a standard classical cipher envelope. "
                    "Please explicitly select the cipher algorithm to decrypt raw text."
                )
            cipher_id = cipher_id_override
            ciphertext = raw_content

        cipher = get_cipher(cipher_id)
        res = cipher.timed_decrypt(ciphertext, key)

        cls.write_text_file(str(out_p), res.text, overwrite=overwrite)
        t1 = time.perf_counter_ns()

        in_size = in_p.stat().st_size
        out_size = out_p.stat().st_size

        return FileOperationResult(
            success=True,
            operation="decrypt",
            algorithm=cipher.name,
            input_path=str(in_p),
            output_path=str(out_p),
            input_size_bytes=in_size,
            output_size_bytes=out_size,
            execution_time_ns=t1 - t0,
            message=f"Successfully decrypted '{in_p.name}' using {cipher.name}.",
            details={"notes": res.notes, "metadata": res.metadata}
        )
