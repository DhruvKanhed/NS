"""Help, Education, and Worked Examples GUI View."""

import tkinter as tk
from tkinter import ttk

from .theme import (
    COLOR_BG_DARK,
    COLOR_BG_CARD,
    COLOR_BG_INPUT,
    COLOR_BORDER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_ACCENT_CYAN,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_HEADING,
    FONT_BODY,
    FONT_MONO,
    FONT_SMALL,
)

HELP_TOPICS = {
    "1. Overview & Fundamentals": """# CLASSICAL CRYPTOGRAPHY OVERVIEW

Classical cryptography refers to encryption methods developed and used prior to the mid-20th century (before electronic computing and modern Shannon information theory).

### Key Concepts:
1. Alphabet-centric: Operates on human-readable alphabets (A-Z) rather than binary bits (0s and 1s).
2. Symmetric: Uses the same secret key (or directly derived inverse) for both encryption and decryption.
3. Two Primary Branches:
   • Substitution Ciphers: Replace characters, pairs, or vectors with other characters.
   • Transposition Ciphers: Permute, scramble, or rearrange the positions of characters without changing their identity.

### Modern Security Reality:
Classical ciphers are strictly for pedagogical and historical study. They are completely vulnerable to:
• Frequency analysis (analyzing single-letter, digram, and trigram frequencies).
• Known-plaintext attacks (e.g. Hill cipher solved via elementary linear algebra).
• Index of Coincidence / Kasiski examination (cracking Vigenère keyword length).
• Brute-force key searches (e.g. Caesar has only 25 non-trivial keys).
NEVER use classical ciphers for confidential, real-world communication!
""",

    "2. Caesar Cipher": """# CAESAR CIPHER (SHIFT CIPHER)

### How It Works:
Replaces each letter by shifting it a fixed number of positions (k) down the alphabet.
• Mathematical Formulation:
  - Encryption: C_i = (P_i + k) mod 26
  - Decryption: P_i = (C_i - k + 26) mod 26

### Key Format:
An integer between 0 and 25 (e.g., 3, 5, 13). Shifts outside 0-25 are normalized modulo 26.

### Worked Example:
• Input: NETWORK SECURITY
• Key: 5
• Encryption:
  N (13) + 5 = 18 -> S
  E (4)  + 5 = 9  -> J
  T (19) + 5 = 24 -> Y
  W (22) + 5 = 27 = 1 -> B
  O (14) + 5 = 19 -> T
  R (17) + 5 = 22 -> W
  K (10) + 5 = 15 -> P
  ...
  Ciphertext: SJYBTWP XJHZWNYD
• Decryption:
  S (18) - 5 = 13 -> N
  J (9)  - 5 = 4  -> E
  ...
  Plaintext: NETWORK SECURITY
""",

    "3. Monoalphabetic Cipher": """# MONOALPHABETIC SUBSTITUTION CIPHER

### How It Works:
Instead of shifting by a uniform offset, each letter of the alphabet (A-Z) is mapped to an arbitrary, distinct letter in a 26-letter permutation alphabet.

### Key Format:
A 26-letter string containing every letter from A to Z exactly once.
Example: QWERTYUIOPASDFGHJKLZXCVBNM

### Worked Example:
• Alphabet:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
• Key:       Q W E R T Y U I O P A S D F G H J K L Z X C V B N M
• Plaintext: HELLO
• Mapping:
  H -> I
  E -> W
  L -> S
  L -> S
  O -> G
• Ciphertext: IWSSG
• Decryption: Invert mapping (I->H, W->E, S->L, G->O) -> HELLO

### Cryptanalysis:
Even though the keyspace is 26! ≈ 4.03 × 10^26, it is trivially broken using frequency analysis because the relative frequency of characters (E is ~12.7%, T is ~9.1%) remains unchanged.
""",

    "4. Playfair Cipher": """# PLAYFAIR CIPHER (DIGRAPHIC SUBSTITUTION)

### How It Works:
Encrypts pairs of letters (digraphs) using a 5×5 key matrix constructed from a keyword. Standard convention merges I and J into one cell.

### Key Rules:
1. Digraph Preparation:
   • If two consecutive letters in a pair are identical (e.g., LL), insert filler letter 'X' (or 'Q').
   • If odd length, append trailing padding letter 'X'.
2. Geometric Transformations:
   • Same Row: Replace with letters immediately to their right (wrap around).
   • Same Column: Replace with letters immediately below (wrap around).
   • Rectangle: Replace each letter with the letter in its own row but in the other letter's column.

### Worked Example:
• Keyword: MONARCHY
• 5×5 Matrix:
  M  O  N  A  R
  C  H  Y  B  D
  E  F  G  I  K
  L  P  Q  S  T
  U  V  W  X  Z
• Plaintext: BALLOON -> Digraphs: BA LX LO ON
• Ciphertext: IB TS MP NA
""",

    "5. Hill Cipher": """# HILL CIPHER (2×2 MODULAR MATRIX)

### How It Works:
Polygraphic substitution cipher invented by Lester S. Hill (1929) utilizing linear algebra modulo 26.
• Plaintext digraph vector P = [p1, p2]^T
• Key matrix K = [[a, b], [c, d]]
• Encryption: C = K · P (mod 26)
• Decryption: P = K^(-1) · C (mod 26)

### Invertibility Condition:
Determinant det(K) = (ad - bc) mod 26 MUST satisfy:
gcd(det(K), 26) == 1 (det must be odd and not 13).

### Worked Example:
• Matrix K: [[3, 3], [2, 5]]
• Determinant: (3·5 - 3·2) = 15 - 6 = 9.
• gcd(9, 26) = 1. Modular inverse of 9 mod 26 = 3 (since 9·3 = 27 = 1 mod 26).
• Plaintext: "HI" -> H=7, I=8
• C0 = (3·7 + 3·8) mod 26 = 45 mod 26 = 19 -> T
• C1 = (2·7 + 5·8) mod 26 = 54 mod 26 = 2  -> C
• Ciphertext: "TC"
""",

    "6. Vigenère Cipher": """# VIGENÈRE CIPHER (POLYALPHABETIC)

### How It Works:
Encrypts text using a repeating keyword, shifting each letter by the corresponding keyword character's index (A=0, B=1, ...).
• Encryption: C_i = (P_i + K_(i mod L)) mod 26
• Decryption: P_i = (C_i - K_(i mod L) + 26) mod 26
• Crucial rule: Non-alphabetic characters (spaces, punctuation) are preserved and DO NOT advance the keyword position.

### Worked Example:
• Plaintext: ATTACK AT DAWN
• Keyword:   LEMON
• Alignment:
  Plain:   A T T A C K   A T   D A W N
  Key:     L E M O N L   E M   O N L E
• Ciphertext: L X F O P V   E F   R N H R
""",

    "7. One-Time Pad": """# ONE-TIME PAD (VERNAM CIPHER)

### Perfect Secrecy (Shannon's Theorem 1949):
The One-Time Pad is the ONLY mathematically unbreakable cipher if and only if:
1. The key is generated using truly random entropy (e.g. Python secrets).
2. The key length is equal to or greater than the message length.
3. The key is NEVER reused under any circumstances.
4. The key is transmitted via an unconditionally secure channel and kept completely secret.

### Reusing Keys (The "Two-Time Pad" Vulnerability):
If key K is used twice:
C1 = P1 ⊕ K
C2 = P2 ⊕ K
Then: C1 ⊕ C2 = P1 ⊕ P2 (the key cancels out completely, allowing depth cryptanalysis).

### Toolkit Implementation:
Keys are generated using Python's secrets module and must be strictly provided for decryption. Keys are never stored in file envelopes.
""",

    "8. Rail Fence Cipher": """# RAIL FENCE CIPHER (ZIGZAG TRANSPOSITION)

### How It Works:
Characters are written diagonally down and up across N horizontal rails in a zigzag oscillation, then read off row by row from top to bottom.

### Worked Example:
• Plaintext: DEFEND THE EAST WALL (length 20)
• Rails: 3
• Zigzag Layout:
  Rail 1: D . . . N . . . E . . . S . . . A .
  Rail 2: . E . E . D . T . H . E . A . T . W . L
  Rail 3: . . F . . . H . . . A . . . T . . . L .
• Rows read:
  Row 1: D N E S A
  Row 2: E E D T H E A T W L
  Row 3: F H A T L
• Ciphertext: DNESA EEDTHEATWL FHATL
""",

    "9. Columnar Transposition": """# COLUMNAR TRANSPOSITION CIPHER

### How It Works:
Plaintext is written into a grid of width W = len(key) row by row. Columns are then read out in the alphabetical order of the keyword letters.

### Handling Ties in Repeated Letters:
When the keyword has repeated characters (e.g., "GERMAN" vs "SECRET"), ties are resolved stably from left to right.
For example, in "SECRET":
S(4), E1(1), C(0), R(3), E2(2), T(5)

### Worked Example:
• Plaintext: DEFEND THE EAST
• Key: GERMAN (Width 6) -> Alphabetical order: A(4), E(1), G(0), M(3), N(5), R(2) -> Reading Order: 4 -> 1 -> 0 -> 3 -> 5 -> 2
• Grid:
  D E F E N D
  T H E E A S
  T
• Columns are sliced and reassembled.
• Decryption reconstructs the grid exactly based on column lengths.
""",

    "10. Common Errors & Solutions": """# COMMON USER ERRORS & TROUBLESHOOTING

1. "Invalid Hill matrix: Determinant is not coprime to 26":
   • Cause: The determinant det(K) is even or divisible by 13 (gcd(det, 26) != 1).
   • Fix: Choose a matrix whose determinant is odd and not 13 (e.g., [3, 3, 2, 5], [5, 8, 17, 3]).

2. "Monoalphabetic key must contain every English letter exactly once":
   • Cause: The key contains duplicates or missing letters.
   • Fix: Use the "Generate Key" button to produce a valid 26-letter permutation.

3. "One-Time Pad key is too short":
   • Cause: The supplied key has fewer alphabetic letters than the message.
   • Fix: Generate a key using the button or supply a longer random string.

4. "Playfair filler letters in decrypted text":
   • Note: This is an intentional characteristic of classical Playfair. Filler 'X' or 'Q' cannot be safely stripped automatically because they might be part of original valid words.

5. "File Decryption Error: Envelope format unrecognized":
   • Cause: The file was not created using the toolkit's envelope format.
   • Fix: Encrypt the file using the toolkit first, or select raw decryption mode.
"""
}


class HelpDocumentationView(ttk.Frame):
    """Searchable help and interactive educational guide."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, style="Dark.TFrame")
        self._build_layout()

    def _build_layout(self) -> None:
        header_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        header_frame.pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(
            header_frame,
            text="HELP & CRYPTOGRAPHY EDUCATION",
            font=FONT_TITLE,
            fg=COLOR_ACCENT_CYAN,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Comprehensive theory, mathematical formulas, worked examples, and security advisories.",
            font=FONT_SUBTITLE,
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_DARK,
        ).pack(anchor="w", pady=(2, 0))

        content_frame = tk.Frame(self, bg=COLOR_BG_DARK)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Left list of topics
        left_list = tk.Frame(content_frame, bg=COLOR_BG_CARD, width=240, padx=8, pady=8, highlightbackground=COLOR_BORDER, highlightthickness=1)
        left_list.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(left_list, text="SELECT TOPIC", font=FONT_HEADING, fg=COLOR_ACCENT_CYAN, bg=COLOR_BG_CARD).pack(anchor="w", pady=(0, 6))

        self.topic_listbox = tk.Listbox(
            left_list,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            selectbackground=COLOR_ACCENT_CYAN,
            selectforeground=COLOR_BG_DARK,
            font=FONT_BODY,
            relief="flat",
            highlightthickness=0,
            width=26,
        )
        self.topic_listbox.pack(fill="both", expand=True)
        self.topic_listbox.bind("<<ListboxSelect>>", self._on_topic_select)

        self.topics = list(HELP_TOPICS.keys())
        for t in self.topics:
            self.topic_listbox.insert(tk.END, t)

        # Right text view
        right_view = tk.Frame(content_frame, bg=COLOR_BG_CARD, padx=12, pady=12, highlightbackground=COLOR_BORDER, highlightthickness=1)
        right_view.pack(side="right", fill="both", expand=True)

        self.txt_content = tk.Text(
            right_view,
            font=FONT_BODY,
            bg=COLOR_BG_INPUT,
            fg=COLOR_TEXT_PRIMARY,
            relief="flat",
            wrap="word",
        )
        scrollbar = ttk.Scrollbar(right_view, orient="vertical", command=self.txt_content.yview)
        self.txt_content.configure(yscrollcommand=scrollbar.set)

        self.txt_content.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Select first topic by default
        self.topic_listbox.select_set(0)
        self._display_topic(self.topics[0])

    def _on_topic_select(self, event) -> None:
        sel = self.topic_listbox.curselection()
        if sel:
            idx = sel[0]
            self._display_topic(self.topics[idx])

    def _display_topic(self, topic_key: str) -> None:
        content = HELP_TOPICS.get(topic_key, "Topic not found.")
        self.txt_content.delete("1.0", tk.END)
        self.txt_content.insert("1.0", content)
