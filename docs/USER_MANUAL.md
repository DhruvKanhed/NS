# CLASSICAL CRYPTOGRAPHY TOOLKIT — USER MANUAL

Welcome to the **Classical Cryptography Toolkit**, an educational desktop software suite developed for the Final Year (ECM) Network Security course (AY 2026–27).

---

## 1. System Requirements

* **Operating System:** macOS (10.15+), Windows (10/11), or Linux (Ubuntu, Debian, Fedora, Arch)
* **Python Version:** Python 3.8 or higher (Python 3.13 tested and verified)
* **GUI Support:** `tkinter` (included by default in standard Python installers on macOS and Windows)
* **Disk Space:** Less than 50 MB
* **Dependencies:** None! The toolkit uses 100% Python standard library modules.

---

## 2. Installation Instructions

### A. macOS & Linux
1. Open your Terminal.
2. Verify Python 3 and Tkinter are available:
   ```bash
   python3 --version
   python3 -c "import tkinter; print('Tkinter OK')"
   ```
   *(On Ubuntu/Debian, if Tkinter is missing, run: `sudo apt update && sudo apt install python3-tk`)*
3. Navigate to the project root folder:
   ```bash
   cd "/path/to/classical-cryptography-toolkit"
   ```

### B. Windows
1. Open PowerShell or Command Prompt.
2. Verify Python is installed:
   ```powershell
   python --version
   ```
3. Navigate to the project directory:
   ```powershell
   cd "C:\path\to\classical-cryptography-toolkit"
   ```

---

## 3. How to Launch the Application

### Launch Option 1: Desktop GUI (Default)
```bash
# macOS / Linux:
python3 main.py

# Windows:
python main.py
```

### Launch Option 2: Terminal Interactive Menu (CLI)
```bash
# macOS / Linux:
python3 main.py --cli

# Windows:
python main.py --cli
```

### Launch Option 3: Quick Comparative Benchmark
```bash
python3 main.py --compare "SAMPLE MESSAGE"
```

### Launch Option 4: Run Automated Tests
```bash
python3 main.py --test
```

---

## 4. Dashboard Walkthrough

When you launch the GUI, you are greeted by the **Dashboard Overview**:
* **Top Metric Ribbon:** Shows active cipher count (8 ciphers: 6 substitution + 2 transposition), high-resolution monotonic timer status, and file envelope version.
* **Cipher Grid Cards:** 8 interactive cards for all ciphers showing their category, key requirements, and mathematical summary.
* **Open Cipher Button:** Click **"Open Cipher →"** on any card to immediately navigate to that cipher's interactive workbench.

---

## 5. Step-by-Step Usage of All Eight Ciphers

### 1. Caesar Cipher
* **Navigation:** Click **"Substitution Ciphers"** in sidebar $\to$ Select **"Caesar Cipher"** from dropdown.
* **Key Input:** Enter an integer shift (e.g. `5`). Shifts $\ge 26$ or negative shifts are automatically normalized modulo 26.
* **Actions:**
  * Enter text in the **Input Text** box.
  * Click **"🔒 Encrypt"** to compute ciphertext.
  * Click **"🔓 Decrypt"** to reverse the transformation.
  * Click **"⇄ Swap In/Out"** to move output text into the input field for round-trip verification.

### 2. Monoalphabetic Substitution Cipher
* **Navigation:** Select **"Monoalphabetic Cipher"**.
* **Key Input:** Enter a 26-letter substitution alphabet (e.g., `QWERTYUIOPASDFGHJKLZXCVBNM`).
* **Random Key Generation:** Click the **"Generate Key"** button to automatically generate a cryptographically randomized 26-letter permutation.
* **Mapping Inspection:** The right-hand panel renders a full educational table showing which letter maps to which substitute.

### 3. Playfair Cipher
* **Navigation:** Select **"Playfair Cipher"**.
* **Key Input:** Enter an alphabetic keyword (e.g., `MONARCHY`).
* **Key Matrix:** The right-hand panel displays the resulting $5 \times 5$ matrix (combining letters `I` and `J`).
* **Important Note:** In classical Playfair, filler letters (`X` or `Q`) and trailing odd-length padding remain in decrypted output. This is intentional to avoid stripping valid words.

### 4. Hill Cipher (2×2 Matrix)
* **Key Input:** Enter 4 space-separated numbers (e.g., `3 3 2 5`) or a 4-letter keyword (e.g. `DDCF`).
* **Matrix Validation:** The toolkit computes $\det(K) \pmod{26}$ and validates that $\gcd(\det(K), 26) = 1$. If the matrix is non-invertible, an error advisory is displayed.
* **Visual Output:** The right panel displays the key matrix, determinant, determinant inverse, and modular inverse matrix $K^{-1} \pmod{26}$.

### 5. Vigenère Cipher
* **Key Input:** Enter an alphabetic keyword (e.g., `LEMON`).
* **Feature:** Non-alphabetic symbols (spaces, punctuation, digits) are preserved and **do not** advance the keyword index.

### 6. One-Time Pad (Vernam)
* **Key Input:** Enter an alphabetic string whose length $\ge$ the message's alphabetic characters, or leave blank during encryption.
* **Auto-Generation:** If left blank during encryption, the toolkit generates a cryptographically secure key via Python's `secrets` module.
* **Decryption Safety:** Decryption **strictly requires** the original key. The system will never silently substitute a random key during decryption.

### 7. Rail Fence Cipher
* **Key Input:** Enter an integer number of rails $\ge 1$ (e.g., `3`).
* **Visualization:** The right-hand panel renders the exact zigzag pattern across the rails.

### 8. Columnar Transposition Cipher
* **Key Input:** Enter a keyword (e.g., `GERMAN` or `SECRET`) or a numeric permutation (`3 1 4 2`).
* **Grid Visualization:** The right panel renders the irregular transposition grid and indicates column reading orders.

---

## 6. File Encryption and Decryption Instructions

The toolkit features a robust **File Operations** module that wraps ciphertexts in a versioned JSON security envelope (`CLASSICAL_CRYPTO_ENVELOPE_V1`).

### To Encrypt a Text File:
1. Click **"📁 File Encrypt & Decrypt"** in the sidebar.
2. In the **Encrypt Text File** tab, click **"Browse..."** to select an input `.txt` file.
3. Select your desired cipher and enter the secret key.
4. Choose the destination output file path (e.g., `sample.enc.txt`).
5. Click **"🔒 Execute File Encryption"**.
6. The file is encrypted and saved in UTF-8 format.

### To Decrypt an Encrypted File:
1. Open the **Decrypt Text File** tab.
2. Click **"Browse..."** and choose the encrypted envelope file.
3. Click **"Inspect Envelope"** to preview the algorithm used, original filename, and timestamp.
4. Enter the secret key (remember: secret keys are **never** stored inside the envelope!).
5. Choose your output destination path (e.g., `recovered.txt`).
6. Click **"🔓 Execute File Decryption"**.

---

## 7. How to Run Automated Tests

To run the complete automated test suite (48 unit and integration tests):

```bash
python3 main.py --test
```

Expected output:
```
=== Running Automated Test Suite ===
... [48 test executions] ...
Ran 48 tests in 0.012s
OK
```

---

## 8. Troubleshooting & FAQ

| Issue / Error | Cause | Recommended Solution |
|---|---|---|
| `ModuleNotFoundError: No module named '_tkinter'` | Python environment lacks Tkinter graphics library. | On Ubuntu/Debian: `sudo apt install python3-tk`. On macOS: Install official Python 3 from python.org. |
| `Invalid Hill matrix: Determinant is not coprime to 26` | Determinant is even or divisible by 13. | Choose a matrix with an odd determinant that is not 13 (e.g., `3 3 2 5` or `5 8 17 3`). |
| `Monoalphabetic key must contain every English letter exactly once` | Key has fewer than 26 letters or has duplicates. | Click the "Generate Key" button to produce a valid 26-letter substitution alphabet. |
| `One-Time Pad key is too short` | Supplied key has fewer letters than the plaintext message. | Generate a fresh key using the "Generate Key" button or supply a longer random string. |

---

## 9. Security Disclaimer

> **IMPORTANT CYBERSECURITY ADVISORY:**  
> The ciphers implemented in this toolkit are classical algorithms developed prior to modern computational cryptography. They are susceptible to frequency analysis, linear cryptanalysis, and brute-force attacks. **They must never be used to protect sensitive passwords, financial data, or real-world confidential communications.**
