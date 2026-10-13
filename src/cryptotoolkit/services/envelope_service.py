"""File envelope serialization and verification for encrypted text files."""

from datetime import datetime, timezone
import json
from typing import Any, Dict, Tuple

ENVELOPE_MAGIC = "CLASSICAL_CRYPTO_ENVELOPE_V1"
ENVELOPE_VERSION = "1.0"


class EnvelopeError(ValueError):
    """Raised when file envelope parsing or validation fails."""
    pass


def create_envelope(
    cipher_id: str,
    ciphertext: str,
    public_params: Dict[str, Any] = None,
    original_filename: str = ""
) -> str:
    """Create a standardized, versioned JSON envelope for encrypted content.
    Notice: Secret keys are strictly omitted from the envelope.
    """
    if public_params is None:
        public_params = {}

    envelope_data = {
        "format": ENVELOPE_MAGIC,
        "version": ENVELOPE_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": cipher_id.lower(),
        "original_filename": original_filename,
        "encoding": "utf-8",
        "parameters": public_params,
        "security_notice": "Educational classical cryptography envelope. Key is NOT stored.",
        "ciphertext": ciphertext,
    }

    return json.dumps(envelope_data, indent=2, ensure_ascii=False)


def parse_envelope(envelope_content: str) -> Dict[str, Any]:
    """Parse and validate a file envelope string.
    Returns the parsed dictionary.
    """
    if not envelope_content or not envelope_content.strip():
        raise EnvelopeError("File is empty or contains no valid envelope content.")

    try:
        data = json.loads(envelope_content)
    except json.JSONDecodeError as exc:
        raise EnvelopeError(
            f"Corrupted or invalid file format. Expected JSON envelope.\nDetails: {exc}"
        )

    if not isinstance(data, dict):
        raise EnvelopeError("Malformed envelope structure. Expected root JSON object.")

    if data.get("format") != ENVELOPE_MAGIC:
        raise EnvelopeError(
            f"Unsupported or unrecognized file envelope format: '{data.get('format')}'. "
            f"Expected '{ENVELOPE_MAGIC}'."
        )

    if "algorithm" not in data or "ciphertext" not in data:
        raise EnvelopeError("Envelope is missing required fields ('algorithm' or 'ciphertext').")

    return data
