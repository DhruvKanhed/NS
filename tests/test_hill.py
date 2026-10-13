"""Unit tests for Hill Cipher (2×2)."""

import unittest
from cryptotoolkit.ciphers.hill import HillCipher
from cryptotoolkit.utils.validation import ValidationError, parse_hill_2x2_matrix


class TestHillCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = HillCipher()
        # Matrix [[3, 3], [2, 5]], det = 15 - 6 = 9. gcd(9, 26) = 1. Invertible!
        self.valid_key = "3 3 2 5"

    def test_matrix_parsing_and_inversion(self):
        matrix, det, det_inv = parse_hill_2x2_matrix(self.valid_key)
        self.assertEqual(matrix, [[3, 3], [2, 5]])
        self.assertEqual(det, 9)
        self.assertEqual(det_inv, 3)  # (9 * 3) % 26 = 27 % 26 = 1

        inv_matrix = HillCipher.get_inverse_matrix(matrix, det_inv)
        # Verify inv_matrix * matrix mod 26 = Identity [[1, 0], [0, 1]]
        prod_00 = (matrix[0][0] * inv_matrix[0][0] + matrix[0][1] * inv_matrix[1][0]) % 26
        prod_01 = (matrix[0][0] * inv_matrix[0][1] + matrix[0][1] * inv_matrix[1][1]) % 26
        prod_10 = (matrix[1][0] * inv_matrix[0][0] + matrix[1][1] * inv_matrix[1][0]) % 26
        prod_11 = (matrix[1][0] * inv_matrix[0][1] + matrix[1][1] * inv_matrix[1][1]) % 26
        self.assertEqual([[prod_00, prod_01], [prod_10, prod_11]], [[1, 0], [0, 1]])

    def test_encryption_and_decryption(self):
        plain = "HELP"
        enc = self.cipher.encrypt(plain, self.valid_key)
        dec = self.cipher.decrypt(enc.text, self.valid_key)
        self.assertEqual(dec.text, plain)

    def test_odd_length_padding(self):
        plain = "ACT"  # Length 3, odd
        enc = self.cipher.encrypt(plain, self.valid_key)
        self.assertEqual(len(enc.text), 4)  # Padded to 4
        dec = self.cipher.decrypt(enc.text, self.valid_key)
        self.assertEqual(dec.text, "ACTX")

    def test_reject_non_invertible_matrix(self):
        # Matrix [[2, 4], [1, 2]], det = 4 - 4 = 0 (gcd = 26)
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("TEST", "2 4 1 2")

        # Matrix [[2, 1], [4, 6]], det = 12 - 4 = 8 (even, gcd(8, 26) = 2)
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("TEST", "2 1 4 6")

    def test_keyword_representation(self):
        # Letters "DDCF" -> D=3, D=3, C=2, F=5
        matrix, det, det_inv = parse_hill_2x2_matrix("DDCF")
        self.assertEqual(matrix, [[3, 3], [2, 5]])


if __name__ == "__main__":
    unittest.main()
