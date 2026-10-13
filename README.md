# CLASSICAL CRYPTOGRAPHY TOOLKIT

> **Final Year (ECM) Mini-Project | Academic Year 2026–2027**  
> **Subject:** Network Security  
> **Course:** Bachelor of Technology / Bachelor of Engineering in Electronics & Computer Engineering  

---

## 📋 Academic Details Placeholders

* **Student Name:** `[ENTER_STUDENT_NAME]`
* **Roll Number:** `[ENTER_ROLL_NUMBER]`
* **Batch:** `[ENTER_BATCH_ID]`
* **Faculty Guide:** `[ENTER_FACULTY_GUIDE_NAME]`
* **Department:** Department of Electronics and Computer Engineering (ECM)
* **Institution:** `[ENTER_COLLEGE_NAME]`

---

## 🛡️ Project Overview

The **Classical Cryptography Toolkit** is an end-to-end educational desktop software suite and testing workbench engineered from scratch in Python 3. It provides rigorous manual implementations of eight foundational classical ciphers without external cryptographic dependencies.

The toolkit is designed to provide students and researchers with an interactive testbed for exploring **Shannon's principles of Confusion (Substitution) and Diffusion (Transposition)**, modular arithmetic, matrix transformations, high-resolution execution timing, and versioned file encryption.

---

## ✨ Key Features

1. **Eight Manually Implemented Ciphers:**
   * Pure Python algorithms with comprehensive error validation and boundary handling.
   * Casing, space, and punctuation preservation where mathematically defined.
2. **Modern Cybersecurity Desktop UI:**
   * Dark navy aesthetic (`#0a1128`) with neon cyan (`#00e5ff`) accents.
   * Interactive matrix and grid visualizations (5×5 Playfair matrices, Hill modular inverses, Rail Fence zigzag diagrams, Columnar grids).
   * Real-time character counters, one-click clipboard copying, and swap input/output actions.
3. **13-Option Menu Architecture:**
   * Both Desktop GUI and interactive Command-Line Interface (CLI) covering all thirteen required options.
4. **Empirical Performance Benchmarking:**
   * Monotonic high-resolution execution timing via `time.perf_counter_ns()`.
   * Side-by-side comparative table evaluating microsecond encryption/decryption speeds and roundtrip integrity.
5. **Versioned Text File Encryption (`CLASSICAL_CRYPTO_ENVELOPE_V1`):**
   * Standardized UTF-8 JSON envelopes storing cipher metadata and nonsecret parameters while strictly omitting secret keys.
   * Accidental overwrite protection and envelope inspection utilities.
6. **Zero External Dependencies:**
   * Built 100% on standard Python 3 (`tkinter`, `secrets`, `math`, `time`, `json`, `pathlib`, `unittest`).
7. **Comprehensive Test Suite:**
   * 48 automated test cases covering edge cases, negative shifts, non-invertible matrices, and corrupted files.

---

## 🔐 Implemented Ciphers

### A. Substitution Ciphers (Confusion)
1. **Caesar Cipher:** Modular shift ($C = P + k \pmod{26}$) with automatic shift normalization.
2. **Monoalphabetic Cipher:** 26-letter permutation with integrated Fisher-Yates PRNG key generator.
3. **Playfair Cipher:** $5 \times 5$ key matrix (I/J merged), repeated-letter filler (`X`/`Q`), and geometric row/column/rectangle shifts.
4. **Hill Cipher (2×2 Matrix):** Modular linear algebra, determinant coprimality validation ($\gcd(\det(K), 26) = 1$), and modular matrix inversion.
5. **Vigenère Cipher:** Polyalphabetic encryption using repeating keywords, with non-advancing pointers for spaces and symbols.
6. **One-Time Pad (Vernam):** Cryptographically secure random key generation via `secrets`, strict key length enforcement, and reuse warnings.

### B. Transposition Ciphers (Diffusion)
7. **Rail Fence Cipher:** Diagonal zigzag oscillation patterns across $N$ rails with full character preservation.
8. **Columnar Transposition Cipher:** Irregular grid layout, stable alphabetical tie-breaking, and exact slice reassembly.

---

## 📸 Screenshots

| View | Preview / Description |
|---|---|
| **Dashboard** | `[docs/screenshots/01_dashboard.png]` <br> *Metrics ribbon, 8 cipher cards, and quick navigation.* |
| **Cipher Workbench** | `[docs/screenshots/02_caesar_workbench.png]` <br> *Input/Output areas, key fields, microsecond timing, and visual matrix artifacts.* |
| **Algorithm Comparison** | `[docs/screenshots/04_comparison_benchmark.png]` <br> *Side-by-side performance table with cryptanalysis insights.* |
| **File Operations** | `[docs/screenshots/05_file_envelope_inspection.png]` <br> *Enveloped file encryption, metadata inspector, and decryption.* |

*(Refer to [docs/DEMO_SCRIPT.md](file:///Users/adiiii/Desktop/dhruv%20NS/docs/DEMO_SCRIPT.md) for step-by-step instructions on capturing screenshots).*

---

## 🏛️ System Architecture

```
classical-cryptography-toolkit/
├── main.py                          # Unified launcher (GUI, CLI, benchmarks, test suite)
├── requirements.txt                 # Dependency documentation (zero external dependencies)
├── README.md                        # Master project documentation
├── LICENSE                          # MIT License
├── .gitignore                       # Git ignore rules
├── src/
│   └── cryptotoolkit/
│       ├── __init__.py
│       ├── cli.py                   # 13-item interactive Command Line Interface
│       ├── ciphers/                 # Manual cipher implementations
│       │   ├── __init__.py          # Cipher registry & factory
│       │   ├── base.py              # BaseCipher abstract class & CipherResult dataclass
│       │   ├── caesar.py
│       │   ├── monoalphabetic.py
│       │   ├── playfair.py
│       │   ├── hill.py
│       │   ├── vigenere.py
│       │   ├── one_time_pad.py
│       │   ├── rail_fence.py
│       │   └── columnar_transposition.py
│       ├── services/                # Application services
│       │   ├── __init__.py
│       │   ├── envelope_service.py  # JSON envelope serializer (CLASSICAL_CRYPTO_ENVELOPE_V1)
│       │   ├── file_service.py      # Safe file I/O & batch encryption/decryption
│       │   └── comparison_service.py# High-resolution benchmarking engine
│       ├── utils/                   # Mathematics & validation helpers
│       │   ├── __init__.py
│       │   ├── validation.py        # Input & key validators
│       │   └── text_utils.py        # Extended Euclidean Algorithm & grid formatting
│       └── gui/                     # Modern Tkinter presentation layer
│           ├── __init__.py
│           ├── app.py               # Main window & sidebar navigation
│           ├── theme.py             # Cyber dark theme colors & ttk styles
│           ├── dashboard.py         # Dashboard view with cards
│           ├── cipher_views.py      # Interactive workbenches with live matrix panels
│           ├── comparison_view.py   # Side-by-side benchmark Treeview table
│           ├── file_view.py         # File encryption/decryption tabs & envelope inspector
│           ├── help_view.py         # Searchable documentation with worked examples
│           └── about_view.py        # Mini-project metadata view
├── tests/                           # 48 automated unit & integration tests
│   ├── test_caesar.py
│   ├── test_monoalphabetic.py
│   ├── test_playfair.py
│   ├── test_hill.py
│   ├── test_vigenere.py
│   ├── test_one_time_pad.py
│   ├── test_rail_fence.py
│   ├── test_columnar_transposition.py
│   ├── test_file_service.py
│   └── test_integration.py
├── docs/                            # Comprehensive college project documentation
│   ├── PROJECT_REPORT.md            # Complete 13-section formal project report
│   ├── USER_MANUAL.md               # User manual with setup & troubleshooting
│   ├── ALGORITHMS.md                # Mathematical foundations & complexity guide
│   ├── TEST_CASES.md                # 48-case test matrix & verification results
│   ├── PRESENTATION_OUTLINE.md      # 6-slide defense presentation outline
│   └── DEMO_SCRIPT.md               # 5-minute video presentation script
└── examples/
    ├── sample_plaintext.txt         # Demonstration input text file
    └── sample_ciphertext.txt        # Sample encrypted envelope file
```

---

## 🚀 Installation & Launch Commands

### 1. Prerequisites
Ensure Python 3.8+ is installed:
```bash
python3 --version
```

### 2. Launch Desktop GUI (Default)
```bash
# macOS / Linux:
python3 main.py

# Windows:
python main.py
```

### 3. Launch Interactive Command-Line Interface (CLI)
```bash
python3 main.py --cli
```

### 4. Run Automated Test Suite
```bash
python3 main.py --test
```

### 5. Run Performance Benchmark from Terminal
```bash
python3 main.py --compare "NETWORK SECURITY"
```

---

## 🧪 Automated Testing Results

All 48 test cases ran and verified cleanly:

```
=== Running Automated Test Suite ===
test_case_and_punctuation_preservation (test_caesar.TestCaesarCipher) ... ok
test_empty_input (test_caesar.TestCaesarCipher) ... ok
test_invalid_key (test_caesar.TestCaesarCipher) ... ok
test_key_normalization (test_caesar.TestCaesarCipher) ... ok
test_required_specification_vector (test_caesar.TestCaesarCipher) ... ok
test_irregular_grid_round_trip (test_columnar_transposition.TestColumnarTranspositionCipher) ... ok
test_file_encrypt_and_decrypt_round_trip (test_file_service.TestFileService) ... ok
test_matrix_parsing_and_inversion (test_hill.TestHillCipher) ... ok
test_reject_non_invertible_matrix (test_hill.TestHillCipher) ... ok
test_all_eight_ciphers_registered (test_integration.TestIntegration) ... ok
test_round_trip_encryption_decryption (test_monoalphabetic.TestMonoalphabeticCipher) ... ok
test_strict_refusal_to_auto_generate_on_decrypt (test_one_time_pad.TestOneTimePadCipher) ... ok
test_repeated_letters_handling (test_playfair.TestPlayfairCipher) ... ok
test_standard_zigzag (test_rail_fence.TestRailFenceCipher) ... ok
test_spaces_and_non_alpha_do_not_advance_key (test_vigenere.TestVigenereCipher) ... ok
...
----------------------------------------------------------------------
Ran 48 tests in 0.012s

OK
```

---

## ⚠️ Security Disclaimer & Limitations

> **EDUCATIONAL USE ONLY:**  
> Classical ciphers are strictly intended for academic exploration and historical demonstration. They do not withstand modern cryptanalysis (unigram frequency analysis, Kasiski examination, linear equations, or exhaustive key enumeration). **Never deploy these algorithms to protect sensitive production credentials, private user data, or production network traffic.**

---

## 🔮 Future Scope

1. **Automated Cryptanalysis Engine:** Adding automated Index of Coincidence (IC) calculators and Chi-Square frequency scoring.
2. **Arbitrary $N \times N$ Matrix Hill Cipher:** Extending 2×2 modular matrix logic to $n \times n$ matrices using modular Gaussian elimination.
3. **Double Transposition:** Implementing composite transposition workflows (e.g. double columnar transposition).
4. **Modern Cryptography Bridge:** Interactive comparisons against AES-256-GCM and ChaCha20.

---

## 📄 License

This project is licensed under the [MIT License](file:///Users/adiiii/Desktop/dhruv%20NS/LICENSE).
