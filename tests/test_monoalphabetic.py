"""Unit tests for Monoalphabetic Substitution Cipher."""

import unittest
from cryptotoolkit.ciphers.monoalphabetic import MonoalphabeticCipher
from cryptotoolkit.utils.validation import ValidationError


class TestMonoalphabeticCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = MonoalphabeticCipher()
        self.sample_key = "QWERTYUIOPASDFGHJKLZXCVBNM"

    def test_key_generator_validity(self):
        rand_key = MonoalphabeticCipher.generate_key()
        self.assertEqual(len(rand_key), 26)
        self.assertEqual(len(set(rand_key)), 26)
        self.assertTrue(rand_key.isalpha())

    def test_round_trip_encryption_decryption(self):
        plain = "The Quick Brown Fox Jumps Over 13 Lazy Dogs!"
        enc = self.cipher.encrypt(plain, self.sample_key)
        dec = self.cipher.decrypt(enc.text, self.sample_key)
        self.assertEqual(dec.text, plain)
        self.assertNotEqual(enc.text, plain)
        # Numbers and punctuation must be preserved
        self.assertIn("13", enc.text)
        self.assertTrue(enc.text.endswith("!"))

    def test_invalid_key_length(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("TEST", "SHORTKEY")

    def test_duplicate_letter_key(self):
        # 26 chars but with duplicate 'A' and missing 'Z'
        dup_key = "QWERTYUIOPASDFGHJKLAXCVBNM"
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("TEST", dup_key)

    def test_mapping_table_structure(self):
        table = MonoalphabeticCipher.format_mapping_table(self.sample_key)
        self.assertIn("Plain:", table)
        self.assertIn("Cipher:", table)


if __name__ == "__main__":
    unittest.main()
