"""Unit tests for One-Time Pad (Vernam) Cipher."""

import unittest
from cryptotoolkit.ciphers.one_time_pad import OneTimePadCipher
from cryptotoolkit.utils.validation import ValidationError


class TestOneTimePadCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = OneTimePadCipher()

    def test_random_key_generation(self):
        key = OneTimePadCipher.generate_random_key(20)
        self.assertEqual(len(key), 20)
        self.assertTrue(key.isalpha())
        self.assertTrue(key.isupper())

    def test_encryption_and_decryption_with_same_key(self):
        plain = "CONFIDENTIAL TRANSMISSION"
        alpha_count = sum(1 for c in plain if c.isalpha())
        key = OneTimePadCipher.generate_random_key(alpha_count)

        enc = self.cipher.encrypt(plain, key)
        self.assertNotEqual(enc.text, plain)
        self.assertIn(" ", enc.text)  # Space preserved

        dec = self.cipher.decrypt(enc.text, key)
        self.assertEqual(dec.text, plain)

    def test_auto_key_generation_during_encryption(self):
        plain = "TOP SECRET"
        # Key left blank -> auto-generates key of sufficient length
        enc = self.cipher.encrypt(plain, "")
        self.assertIsNotNone(enc.key_display)
        self.assertGreaterEqual(len(enc.key_display), 9)

        # Decrypt using generated key
        dec = self.cipher.decrypt(enc.text, enc.key_display)
        self.assertEqual(dec.text, plain)

    def test_strict_refusal_to_auto_generate_on_decrypt(self):
        """Never silently generate a replacement key when decrypting."""
        with self.assertRaises(ValueError) as ctx:
            self.cipher.decrypt("ENCRYPTED TEXT", "")
        self.assertIn("original One-Time Pad key", str(ctx.exception))

    def test_key_too_short(self):
        plain = "VERY LONG SECRET MESSAGE"
        short_key = "ABC"
        with self.assertRaises(ValidationError) as ctx:
            self.cipher.encrypt(plain, short_key)
        self.assertIn("too short", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
