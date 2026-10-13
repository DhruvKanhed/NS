"""Unit tests for Vigenère Cipher."""

import unittest
from cryptotoolkit.ciphers.vigenere import VigenereCipher
from cryptotoolkit.utils.validation import ValidationError


class TestVigenereCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = VigenereCipher()
        self.keyword = "LEMON"

    def test_standard_polyalphabetic_encryption(self):
        plain = "ATTACKATDAWN"
        enc = self.cipher.encrypt(plain, self.keyword)
        self.assertEqual(enc.text, "LXFOPVEFRNHR")

        dec = self.cipher.decrypt(enc.text, self.keyword)
        self.assertEqual(dec.text, plain)

    def test_spaces_and_non_alpha_do_not_advance_key(self):
        # Plain with spaces
        plain = "ATTACK AT DAWN"
        enc = self.cipher.encrypt(plain, self.keyword)
        self.assertEqual(enc.text, "LXFOPV EF RNHR")

        dec = self.cipher.decrypt(enc.text, self.keyword)
        self.assertEqual(dec.text, plain)

    def test_mixed_case_and_punctuation(self):
        plain = "Attack at Dawn! Operation #42."
        enc = self.cipher.encrypt(plain, self.keyword)
        dec = self.cipher.decrypt(enc.text, self.keyword)
        self.assertEqual(dec.text, plain)
        self.assertTrue(enc.text.startswith("Lxfopv"))

    def test_empty_keyword(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "")


if __name__ == "__main__":
    unittest.main()
