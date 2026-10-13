"""Unit tests for Caesar Cipher."""

import unittest
from cryptotoolkit.ciphers.caesar import CaesarCipher
from cryptotoolkit.utils.validation import ValidationError


class TestCaesarCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = CaesarCipher()

    def test_required_specification_vector(self):
        """Test exact expected encryption and decryption from prompt."""
        plain = "NETWORK SECURITY"
        key = 5
        res = self.cipher.encrypt(plain, key)
        self.assertEqual(res.text, "SJYBTWP XJHZWNYD")

        dec = self.cipher.decrypt(res.text, key)
        self.assertEqual(dec.text, "NETWORK SECURITY")

    def test_case_and_punctuation_preservation(self):
        plain = "Network Security, 2026-27! Final Year."
        key = 3
        enc = self.cipher.encrypt(plain, key)
        dec = self.cipher.decrypt(enc.text, key)
        self.assertEqual(dec.text, plain)
        self.assertTrue(enc.text.startswith("Qhwzrun"))

    def test_key_normalization(self):
        plain = "HELLO"
        # Key 5, key 31 (5 + 26), and key -21 should all produce identical shift
        enc1 = self.cipher.encrypt(plain, 5)
        enc2 = self.cipher.encrypt(plain, 31)
        enc3 = self.cipher.encrypt(plain, -21)
        self.assertEqual(enc1.text, enc2.text)
        self.assertEqual(enc1.text, enc3.text)

    def test_empty_input(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("", 5)
        with self.assertRaises(ValidationError):
            self.cipher.decrypt("   ", 5)

    def test_invalid_key(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "abc")
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "")


if __name__ == "__main__":
    unittest.main()
