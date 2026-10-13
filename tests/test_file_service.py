"""Unit tests for File Service and Envelope Service."""

import os
import tempfile
import unittest
from pathlib import Path

from cryptotoolkit.services.file_service import FileService
from cryptotoolkit.services.envelope_service import parse_envelope, EnvelopeError


class TestFileService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

        # Create sample plaintext file
        self.sample_file = self.dir_path / "sample.txt"
        self.sample_content = "NETWORK SECURITY 2026-27 FINAL YEAR ECM MINI-PROJECT TEST FILE."
        self.sample_file.write_text(self.sample_content, encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_file_encrypt_and_decrypt_round_trip(self):
        enc_file = self.dir_path / "sample.enc.txt"
        dec_file = self.dir_path / "recovered.txt"

        # Encrypt with Caesar shift 7
        res_enc = FileService.encrypt_file(
            input_path=str(self.sample_file),
            output_path=str(enc_file),
            cipher_id="caesar",
            key=7,
            overwrite=True,
        )
        self.assertTrue(res_enc.success)
        self.assertTrue(enc_file.exists())

        # Inspect envelope
        env_data = FileService.inspect_encrypted_file(str(enc_file))
        self.assertEqual(env_data["algorithm"], "caesar")
        self.assertEqual(env_data["version"], "1.0")
        # Ensure secret key is strictly omitted from envelope
        self.assertNotIn("7", str(env_data.get("parameters")))
        self.assertNotIn("key", env_data)

        # Decrypt with key 7
        res_dec = FileService.decrypt_file(
            input_path=str(enc_file),
            output_path=str(dec_file),
            key=7,
            overwrite=True,
        )
        self.assertTrue(res_dec.success)
        self.assertTrue(dec_file.exists())
        self.assertEqual(dec_file.read_text(encoding="utf-8"), self.sample_content)

    def test_prevent_same_input_and_output_path(self):
        with self.assertRaises(ValueError):
            FileService.encrypt_file(
                input_path=str(self.sample_file),
                output_path=str(self.sample_file),
                cipher_id="caesar",
                key=5,
            )

    def test_corrupted_envelope_handling(self):
        corrupt_file = self.dir_path / "corrupt.txt"
        corrupt_file.write_text("THIS IS NOT A VALID JSON ENVELOPE", encoding="utf-8")

        with self.assertRaises(ValueError):
            FileService.decrypt_file(
                input_path=str(corrupt_file),
                output_path=str(self.dir_path / "out.txt"),
                key="any",
            )

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            FileService.read_text_file(str(self.dir_path / "missing.txt"))


if __name__ == "__main__":
    unittest.main()
