# 5-MINUTE PROJECT DEMONSTRATION VIDEO SCRIPT

**Project:** Design and Development of a Classical Cryptography Toolkit  
**Duration:** Under 5 minutes (300 seconds)  
**Target Audience:** Network Security Evaluators & Academic Faculty  

---

## Video Timeline & Spoken Script

### 0:00 – 0:45 | Scene 1: Introduction & Dashboard Overview
* **Action on Screen:**
  1. Open terminal and run: `python3 main.py`
  2. The window opens displaying the Cybersecurity Dark Navy & Cyan interface.
  3. Mouse hovers over the Dashboard cards and top metrics ribbon.
* **Narrator:**
  > "Hello everyone. Welcome to the demonstration of our Final Year ECM Network Security mini-project: The Classical Cryptography Toolkit.
  > Built using pure standard Python 3 and Tkinter, the application provides an educational environment for classical ciphers.
  > On the main dashboard, you can see all eight ciphers categorized into Substitution and Transposition, along with key requirements and system metrics."

---

### 0:45 – 1:45 | Scene 2: Interactive Cipher Workbenches
* **Action on Screen:**
  1. Click on **"Caesar Cipher"** card $\to$ opens workbench.
  2. Plaintext: `NETWORK SECURITY`, Key: `5`. Click **"🔒 Encrypt"**.
  3. Output shows: `SJYBTWP XJHZWNYD`, execution time ~17 µs.
  4. Click **"⇄ Swap In/Out"**, then click **"🔓 Decrypt"** $\to$ recovers `NETWORK SECURITY`.
  5. Switch to **"Playfair Cipher"**. Enter keyword `MONARCHY` and text `BALLOON`. Click **"🔒 Encrypt"**.
  6. Point out the $5 \times 5$ matrix generated on the right and filler `'X'` explanation.
  7. Switch to **"Hill Cipher"**. Key: `3 3 2 5`. Show the computed determinant (9) and inverse matrix mod 26.
* **Narrator:**
  > "Let's demonstrate our Caesar Cipher with key 5. Notice that encryption produces the exact expected vector: 'SJYBTWP XJHZWNYD'.
  > Clicking 'Swap' and 'Decrypt' verifies perfect round-trip recovery with microsecond timing.
  > Moving to the Playfair Cipher with keyword 'MONARCHY', the system constructs the 5x5 key matrix combining I and J, handles repeated letters with filler 'X', and displays the geometric transformations.
  > In the Hill Cipher, entering 3 3 2 5 calculates determinant 9, validates coprimality to 26, and calculates the modular inverse matrix."

---

### 1:45 – 2:30 | Scene 3: One-Time Pad & Transposition Ciphers
* **Action on Screen:**
  1. Switch to **"One-Time Pad"**. Enter message `SECRET TRANSMISSION`. Click **"Generate Key"** (random key generated via `secrets`). Click **"🔒 Encrypt"**. Highlight security warning notes.
  2. Switch to **"Transposition Ciphers"** $\to$ **"Rail Fence Cipher"**. Enter 3 rails. Click **"🔒 Encrypt"**.
  3. Point out the ASCII zigzag diagram on the right panel.
  4. Switch to **"Columnar Transposition"**. Enter keyword `GERMAN`. Show the grid visualization and column order.
* **Narrator:**
  > "The One-Time Pad utilizes Python's cryptographically secure secrets module. The system enforces matching key length and explicitly warns against key reuse.
  > In Transposition, the Rail Fence workbench visualizes the diagonal zigzag oscillations across three rails.
  > Columnar Transposition renders the irregular grid layout and illustrates reading columns according to alphabetical key ranks."

---

### 2:30 – 3:30 | Scene 4: Algorithm Comparison Benchmark
* **Action on Screen:**
  1. Click **"⚡ Algorithm Comparison"** in the sidebar.
  2. Input: `NETWORK SECURITY FINAL YEAR ECM 2026`.
  3. Click **"⚡ Run Benchmark"**.
  4. The Treeview table populates with encryption/decryption times in microseconds, roundtrip status, and ciphertext.
  5. Click on different rows to inspect the cryptanalytic vulnerabilities and limitations box at the bottom.
* **Narrator:**
  > "The Algorithm Comparison module runs a side-by-side benchmark using Python's monotonic high-resolution timer.
  > All algorithms are evaluated under the same message.
  > Selecting any cipher reveals its cryptanalytic weaknesses—such as unigram frequency vulnerability in Caesar and Monoalphabetic, or known-plaintext vulnerability in Hill cipher."

---

### 3:30 – 4:30 | Scene 5: File Operations & Envelope Security
* **Action on Screen:**
  1. Click **"📁 File Encrypt & Decrypt"** in the sidebar.
  2. Select `examples/sample_plaintext.txt`.
  3. Choose cipher: `Caesar Cipher`, Key: `5`. Destination: `sample_demo.enc.txt`. Click **"🔒 Execute File Encryption"**.
  4. Switch to **"Decrypt Text File"** tab. Select `sample_demo.enc.txt`. Click **"Inspect Envelope"** $\to$ modal shows JSON format, timestamp, algorithm, and no stored secret key.
  5. Enter key `5`, set output to `demo_recovered.txt`. Click **"🔓 Execute File Decryption"**. Show success dialog.
* **Narrator:**
  > "Our file service packages encrypted files in a versioned JSON security envelope.
  > The envelope stores algorithm metadata and UTF-8 encoding parameters, but strictly excludes secret keys to prevent credential leakage.
  > The inspect feature lets users verify the file envelope before entering their key to decrypt."

---

### 4:30 – 5:00 | Scene 6: Automated Testing & Conclusion
* **Action on Screen:**
  1. Switch back to terminal.
  2. Run `python3 main.py --test`.
  3. Terminal displays all 48 test cases running and passing with `OK`.
  4. Concluding slide / window view.
* **Narrator:**
  > "Finally, our automated test suite executes 48 comprehensive unit and integration tests, verifying boundary conditions, negative shifts, non-invertible matrices, and file envelopes in just 12 milliseconds.
  > Thank you for watching our demonstration of the Classical Cryptography Toolkit."

---

## Instructions for Capturing Screenshots for Report / Presentation

To capture high-quality screenshots for your submission:

1. **Dashboard Overview:**
   * Run `python3 main.py`. Ensure the window is sized to `1180x760`.
   * On macOS: Press `Command + Shift + 4`, then press `Spacebar` and click the application window to capture a clean window screenshot with drop-shadow.
   * On Windows: Press `Alt + PrintScreen` to capture the active window.
   * Save as `docs/screenshots/01_dashboard.png`.

2. **Caesar & Playfair Workbenches:**
   * Enter input and click Encrypt to populate the result and the right-hand matrix grid.
   * Capture and save as `docs/screenshots/02_caesar_workbench.png` and `docs/screenshots/03_playfair_matrix.png`.

3. **Algorithm Comparison Table:**
   * Navigate to Algorithm Comparison, click "Run Benchmark".
   * Capture the populated table and save as `docs/screenshots/04_comparison_benchmark.png`.

4. **File Encryption & Envelope Inspection:**
   * Click "Inspect Envelope" in the File Decryption tab so the metadata popup is visible.
   * Capture and save as `docs/screenshots/05_file_envelope_inspection.png`.

5. **Terminal Test Run:**
   * In terminal, run: `python3 main.py --test`.
   * Capture the terminal showing all 48 tests passing and save as `docs/screenshots/06_unit_tests.png`.
