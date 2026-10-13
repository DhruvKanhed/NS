# COMPREHENSIVE TEST CASES SPECIFICATION & MATRIX

This document records the automated verification test matrix for the **Classical Cryptography Toolkit**.

---

## 1. Test Summary

* **Testing Framework:** Python standard library `unittest` (compatible with `pytest`)
* **Total Executed Tests:** 48
* **Passed:** 48
* **Failed:** 0
* **Execution Time:** ~12 ms

---

## 2. Test Cases Matrix

### A. Caesar Cipher (`test_caesar.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-CAE-01 | `test_required_specification_vector` | Input: `"NETWORK SECURITY"`, Key: `5` | `"SJYBTWP XJHZWNYD"` & Decrypt to `"NETWORK SECURITY"` | PASS |
| TC-CAE-02 | `test_case_and_punctuation_preservation` | Mixed case, numbers, commas, exclamation mark | Exact preservation of non-alpha characters & case | PASS |
| TC-CAE-03 | `test_key_normalization` | Shift keys `5`, `31` ($5+26$), and `-21` | Identical ciphertexts generated | PASS |
| TC-CAE-04 | `test_empty_input` | Empty string `""` or whitespace `"   "` | `ValidationError` raised with descriptive message | PASS |
| TC-CAE-05 | `test_invalid_key` | Non-integer string `"abc"` or empty key | `ValidationError` raised | PASS |

### B. Monoalphabetic Substitution Cipher (`test_monoalphabetic.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-MON-01 | `test_key_generator_validity` | Call `generate_key()` via `secrets` PRNG | 26 uppercase letters, no duplicates | PASS |
| TC-MON-02 | `test_round_trip_encryption_decryption` | 26-letter key with pangram and symbols | Complete lossless decryption | PASS |
| TC-MON-03 | `test_invalid_key_length` | Key with fewer than 26 characters | `ValidationError` raised | PASS |
| TC-MON-04 | `test_duplicate_letter_key` | 26 chars containing duplicate letter 'A' | `ValidationError` identifying duplicate/missing letters | PASS |
| TC-MON-05 | `test_mapping_table_structure` | Format educational mapping table | Contains `"Plain:"` and `"Cipher:"` rows | PASS |

### C. Playfair Cipher (`test_playfair.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-PLA-01 | `test_key_matrix_generation` | Keyword `"MONARCHY"` | $5 \times 5$ matrix containing 25 unique letters (I/J merged) | PASS |
| TC-PLA-02 | `test_repeated_letters_handling` | Input: `"BALLOON"` | Digraphs: `[('B','A'), ('L','X'), ('L','O'), ('O','N')]` | PASS |
| TC-PLA-03 | `test_odd_length_padding` | Input: `"CAT"` | Digraphs: `[('C','A'), ('T','X')]` | PASS |
| TC-PLA-04 | `test_round_trip_encryption_decryption` | Plaintext: `"INSTRUMENT"` | Perfect recovery of normalized input | PASS |
| TC-PLA-05 | `test_invalid_odd_length_ciphertext_decryption` | Ciphertext with 3 letters | `ValueError` indicating invalid digraph pairing | PASS |
| TC-PLA-06 | `test_empty_keyword` | Empty keyword `""` | `ValidationError` raised | PASS |

### D. Hill Cipher (`test_hill.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-HIL-01 | `test_matrix_parsing_and_inversion` | Matrix `"3 3 2 5"`, $\det = 9$ | $\det^{-1} = 3$, $K \cdot K^{-1} \equiv I \pmod{26}$ | PASS |
| TC-HIL-02 | `test_encryption_and_decryption` | Plaintext: `"HELP"` with key `"3 3 2 5"` | Accurate round-trip recovery | PASS |
| TC-HIL-03 | `test_odd_length_padding` | Odd length: `"ACT"` (3 letters) | Padded to 4 letters (`"ACTX"`), encrypted and recovered | PASS |
| TC-HIL-04 | `test_reject_non_invertible_matrix` | Matrix with $\det = 0$ or even $\det$ | `ValidationError` stating determinant not coprime to 26 | PASS |
| TC-HIL-05 | `test_keyword_representation` | 4-letter keyword `"DDCF"` | Parsed to matrix `[[3, 3], [2, 5]]` | PASS |

### E. Vigenère Cipher (`test_vigenere.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-VIG-01 | `test_standard_polyalphabetic_encryption` | Input: `"ATTACKATDAWN"`, Key: `"LEMON"` | Ciphertext: `"LXFOPVEFRNHR"` & round-trip pass | PASS |
| TC-VIG-02 | `test_spaces_and_non_alpha_do_not_advance_key` | Input: `"ATTACK AT DAWN"` | Ciphertext: `"LXFOPV EF RNHR"` | PASS |
| TC-VIG-03 | `test_mixed_case_and_punctuation` | Mixed case, numbers, `#42.` | Exact casing & symbol preservation | PASS |
| TC-VIG-04 | `test_empty_keyword` | Empty keyword `""` | `ValidationError` raised | PASS |

### F. One-Time Pad (`test_one_time_pad.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-OTP-01 | `test_random_key_generation` | Generate 20-character key via `secrets` | Truly random 20-char uppercase key | PASS |
| TC-OTP-02 | `test_encryption_and_decryption_with_same_key` | Length-matched key encryption | Lossless decryption | PASS |
| TC-OTP-03 | `test_auto_key_generation_during_encryption` | Empty key on encrypt | Auto-generates key of sufficient length | PASS |
| TC-OTP-04 | `test_strict_refusal_to_auto_generate_on_decrypt` | Empty key on decrypt | Strict refusal (`ValueError`) | PASS |
| TC-OTP-05 | `test_key_too_short` | Key shorter than alphabetic count | `ValidationError` detailing length mismatch | PASS |

### G. Rail Fence Cipher (`test_rail_fence.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-RF-01 | `test_standard_zigzag` | 3 rails with `"WE ARE DISCOVERED FLEE AT ONCE"` | Clean zigzag recovery | PASS |
| TC-RF-02 | `test_all_characters_preserved` | Spaces, punctuation, digits | All preserved identically | PASS |
| TC-RF-03 | `test_edge_case_one_rail` | Key: 1 rail | Message unchanged | PASS |
| TC-RF-04 | `test_edge_case_rails_greater_than_length` | Rails > length | Message unchanged | PASS |
| TC-RF-05 | `test_edge_case_single_character` | Single character `"A"` | Unchanged round trip | PASS |
| TC-RF-06 | `test_invalid_rails` | Rails $\le 0$ or non-integer | `ValidationError` raised | PASS |

### H. Columnar Transposition Cipher (`test_columnar_transposition.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-COL-01 | `test_key_ordering_with_repeated_letters` | Key: `"SECRET"` (repeated 'E') | Stable left-to-right tie resolution | PASS |
| TC-COL-02 | `test_numeric_order_key` | Permutation `"3 1 4 2"` | Parsed to column order `[2, 0, 3, 1]` | PASS |
| TC-COL-03 | `test_irregular_grid_round_trip` | Incomplete final row (14 chars / 5 cols) | Perfect round-trip recovery | PASS |
| TC-COL-04 | `test_long_message_with_spaces_and_punct` | Multi-word sentence with numbers and symbols | Exact character preservation | PASS |
| TC-COL-05 | `test_empty_or_invalid_key` | Empty or symbol-only key | `ValidationError` raised | PASS |

### I. File Operations & Integration (`test_file_service.py`, `test_integration.py`)

| Test ID | Test Method | Test Description & Inputs | Expected Output | Status |
|---|---|---|---|---|
| TC-FIL-01 | `test_file_encrypt_and_decrypt_round_trip` | Read `.txt`, wrap envelope, decrypt back | Exact match, secret key absent from envelope | PASS |
| TC-FIL-02 | `test_prevent_same_input_and_output_path` | Input path == Output path | `ValueError` preventing accidental file destruction | PASS |
| TC-FIL-03 | `test_corrupted_envelope_handling` | Invalid JSON envelope content | `ValueError` with clear corrupted notice | PASS |
| TC-FIL-04 | `test_nonexistent_file` | Missing file path | `FileNotFoundError` raised | PASS |
| TC-INT-01 | `test_all_eight_ciphers_registered` | Verify cipher registry | Exactly 8 ciphers present | PASS |
| TC-INT-02 | `test_extended_gcd_and_modular_inverse` | Modular inverse of 9 mod 26 | Inverse is 3; non-coprime raises error | PASS |
| TC-INT-03 | `test_comparison_service_all_ciphers` | Batch benchmark execution | All 8 ciphers benchmarked successfully | PASS |
