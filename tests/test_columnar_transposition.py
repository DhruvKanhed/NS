"""Unit tests for Columnar Transposition Cipher."""

import unittest
from cryptotoolkit.ciphers.columnar_transposition import ColumnarTranspositionCipher
from cryptotoolkit.utils.validation import ValidationError, validate_columnar_key


class TestColumnarTranspositionCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = ColumnarTranspositionCipher()

    def test_key_ordering_with_repeated_letters(self):
        # Key "SECRET" has repeated 'E's
        key_str, order = validate_columnar_key("SECRET")
        self.assertEqual(key_str, "SECRET")
        self.assertEqual(len(order), 6)
        # S E C R E T
        # C (idx 2) is rank 0
        # First E (idx 1) is rank 1
        # Second E (idx 4) is rank 2
        # R (idx 3) is rank 3
        # S (idx 0) is rank 4
        # T (idx 5) is rank 5
        self.assertEqual(order, [2, 1, 4, 3, 0, 5])

    def test_numeric_order_key(self):
        key_str, order = validate_columnar_key("3 1 4 2")
        self.assertEqual(order, [2, 0, 3, 1])

    def test_irregular_grid_round_trip(self):
        # Incomplete final row: 14 chars with width 5
        plain = "ATTACK AT DAWN"
        key = "ZEBRA"
        enc = self.cipher.encrypt(plain, key)
        self.assertNotEqual(enc.text, plain)
        self.assertEqual(len(enc.text), len(plain))

        dec = self.cipher.decrypt(enc.text, key)
        self.assertEqual(dec.text, plain)

    def test_long_message_with_spaces_and_punct(self):
        plain = "The meeting is at 2300 hours near Bridge #7. Confirm receipt!"
        key = "MISSION"
        enc = self.cipher.encrypt(plain, key)
        dec = self.cipher.decrypt(enc.text, key)
        self.assertEqual(dec.text, plain)

    def test_empty_or_invalid_key(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "")
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "!@#$%")


if __name__ == "__main__":
    unittest.main()
