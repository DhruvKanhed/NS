"""Unit tests for Playfair Cipher."""

import unittest
from cryptotoolkit.ciphers.playfair import PlayfairCipher
from cryptotoolkit.utils.validation import ValidationError


class TestPlayfairCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = PlayfairCipher()
        self.keyword = "MONARCHY"

    def test_key_matrix_generation(self):
        matrix, pos_map = PlayfairCipher.generate_matrix(self.keyword)
        self.assertEqual(len(matrix), 5)
        self.assertEqual(len(matrix[0]), 5)
        # Should not contain J (merged with I)
        all_letters = "".join("".join(row) for row in matrix)
        self.assertNotIn("J", all_letters)
        self.assertIn("I", all_letters)
        self.assertEqual(len(set(all_letters)), 25)

    def test_repeated_letters_handling(self):
        # "BALLOON" has duplicate 'LL' and 'OO'
        digraphs, notes = PlayfairCipher.prepare_plaintext("BALLOON")
        # Expected digraphs: BA LX LO ON
        expected = [("B", "A"), ("L", "X"), ("L", "O"), ("O", "N")]
        self.assertEqual(digraphs, expected)
        self.assertTrue(any("filler" in n.lower() for n in notes))

    def test_odd_length_padding(self):
        digraphs, notes = PlayfairCipher.prepare_plaintext("CAT")
        # Expected: CA TX
        self.assertEqual(digraphs, [("C", "A"), ("T", "X")])

    def test_round_trip_encryption_decryption(self):
        plain = "INSTRUMENT"
        enc = self.cipher.encrypt(plain, self.keyword)
        dec = self.cipher.decrypt(enc.text, self.keyword)
        # Normalization: I and J merged
        self.assertEqual(dec.text, plain)

    def test_invalid_odd_length_ciphertext_decryption(self):
        with self.assertRaises(ValueError):
            self.cipher.decrypt("ABC", self.keyword)

    def test_empty_keyword(self):
        with self.assertRaises(ValidationError):
            self.cipher.encrypt("HELLO", "")


if __name__ == "__main__":
    unittest.main()
