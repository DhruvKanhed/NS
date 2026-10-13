# ALGORITHMS SPECIFICATION & MATHEMATICAL FOUNDATIONS

This document provides exhaustive mathematical explanations, formal notation, pseudocode, and cryptanalytic properties for all eight algorithms implemented in the **Classical Cryptography Toolkit**.

---

## 1. Caesar Cipher (Shift Cipher)

### 1.1 Mathematical Formulation
Let the alphabet be $\Sigma = \{A, B, \dots, Z\}$ indexed as $\mathbb{Z}_{26} = \{0, 1, \dots, 25\}$.
Given shift key $k \in \mathbb{Z}$:

$$\text{Normalize: } k' = k \pmod{26}$$

**Encryption Function:**
$$E(p, k') = (p + k') \pmod{26}$$

**Decryption Function:**
$$D(c, k') = (c - k' + 26) \pmod{26}$$

### 1.2 Complexity & Keyspace
* **Time Complexity:** $O(n)$ where $n$ is text length.
* **Space Complexity:** $O(n)$
* **Keyspace Size:** $|\mathcal{K}| = 26$ (25 non-trivial shifts).
* **Cryptanalysis:** Exhaustive brute-force key search in $O(1)$ operations or unigram frequency analysis.

---

## 2. Monoalphabetic Substitution Cipher

### 2.1 Mathematical Formulation
Let $\pi: \Sigma \to \Sigma$ be a bijective permutation function defined by key string $K \in \Sigma^{26}$ such that:

$$\pi(i) = K[i], \quad \forall i \in \{0, \dots, 25\}$$

**Encryption:**
$$c_i = \pi(p_i)$$

**Decryption:**
$$p_i = \pi^{-1}(c_i)$$

### 2.2 Complexity & Keyspace
* **Time Complexity:** $O(n)$ using hash map or direct array indexing.
* **Space Complexity:** $O(|\Sigma|) = O(1)$ auxiliary space.
* **Keyspace Size:** $|\mathcal{K}| = 26! \approx 4.0329 \times 10^{26}$ ($88.4$ bits).
* **Cryptanalysis:** Although brute-force is infeasible, unigram frequency matching (comparing character frequencies with standard English frequencies: E $\approx 12.7\%$, T $\approx 9.1\%$, A $\approx 8.2\%$) solves the cipher within seconds.

---

## 3. Playfair Cipher (Digraphic Substitution)

### 3.1 Key Matrix Construction
1. Keyword string $W$ is sanitized: uppercase letters only, replace `J` with `I`.
2. Construct set $S = \text{Unique}(W) \cup (\Sigma \setminus \{'J'\})$.
3. Populate $5 \times 5$ matrix $M$:
   $$M[r][c] \in \Sigma \setminus \{'J'\}, \quad r, c \in \{0, 1, 2, 3, 4\}$$

### 3.2 Digraph Generation & Geometric Rules
Pair adjacent letters $(p_1, p_2)$:
* If $p_1 == p_2$: insert filler 'X' (or 'Q' if $p_1 == 'X'$).
* If odd length trailing letter: append 'X'.

Let coordinates be $(r_1, c_1) = \text{pos}(p_1)$ and $(r_2, c_2) = \text{pos}(p_2)$:
* **Same Row ($r_1 == r_2$):**
  $$c_1' = (c_1 \pm 1) \pmod 5, \quad c_2' = (c_2 \pm 1) \pmod 5$$
* **Same Column ($c_1 == c_2$):**
  $$r_1' = (r_1 \pm 1) \pmod 5, \quad r_2' = (r_2 \pm 1) \pmod 5$$
* **Rectangle ($r_1 \neq r_2, c_1 \neq c_2$):**
  $$(r_1, c_2) \quad \text{and} \quad (r_2, c_1)$$

---

## 4. Hill Cipher (2×2 Matrix)

### 4.1 Modular Linear Algebra
Key matrix:
$$K = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in \mathcal{M}_{2 \times 2}(\mathbb{Z}_{26})$$

$$\det(K) = (ad - bc) \pmod{26}$$

**Invertibility Criterion:**
Matrix $K$ is invertible over $\mathbb{Z}_{26}$ if and only if:
$$\gcd(\det(K), 26) = 1$$
(i.e., $\det(K)$ must be coprime to 2 and 13).

**Modular Multiplicative Inverse:**
$$\det(K)^{-1} \cdot \det(K) \equiv 1 \pmod{26}$$
Computed via the Extended Euclidean Algorithm:
$$\gcd(a, m) = a \cdot x + m \cdot y$$

**Inverse Matrix:**
$$K^{-1} = \det(K)^{-1} \cdot \begin{pmatrix} d & -b \\ -c & a \end{pmatrix} \pmod{26}$$

**Vector Transformations:**
$$C = K \cdot P \pmod{26}, \quad P = K^{-1} \cdot C \pmod{26}$$

---

## 5. Vigenère Cipher (Polyalphabetic)

### 5.1 Formulation
Given key string $K$ of length $L$:
$$C_i = (P_i + K_{j \pmod L}) \pmod{26}$$
$$P_i = (C_i - K_{j \pmod L} + 26) \pmod{26}$$

Where $j$ is incremented strictly on alphabetic characters.

### 5.2 Cryptanalysis
* **Kasiski Examination:** Identifies repeating substrings in ciphertext to determine factors of key length $L$.
* **Friedman Test (Index of Coincidence):**
  $$IC = \frac{\sum f_i(f_i - 1)}{N(N - 1)}$$
  Estimates key length $L \approx \frac{0.027 N}{(N - 1) IC - 0.038 N + 0.065}$.

---

## 6. One-Time Pad (Vernam Cipher)

### 6.1 Shannon's Perfect Secrecy
$$H(M | C) = H(M)$$
The ciphertext provides zero mutual information regarding the plaintext:
$$I(M; C) = 0$$

### 6.2 Strict Prerequisites
1. $K$ is generated via a cryptographically secure random number generator (CSPRNG).
2. $|K| \ge |M|$.
3. $K$ is strictly single-use (never reused).
4. $K$ is transmitted over a secure out-of-band channel.

---

## 7. Rail Fence Cipher (Zigzag Transposition)

### 7.1 Oscillation Sequence
Given $r$ rails, the rail assignment function for character index $t \in \{0, \dots, n-1\}$ follows periodic triangular wave:
$$\text{period} = 2(r - 1)$$
$$\text{rail}(t) = r - 1 - |(t \bmod \text{period}) - (r - 1)|$$

---

## 8. Columnar Transposition Cipher

### 8.1 Grid Mapping
Width $W = |K|$. Length $n = |P|$.
$$\text{num\_rows} = \lceil n / W \rceil, \quad \text{rem} = n \pmod W$$

Columns $c \in \{0, \dots, W-1\}$ have lengths:
$$\text{length}(c) = \begin{cases} \lfloor n/W \rfloor + 1 & \text{if } c < \text{rem} \\ \lfloor n/W \rfloor & \text{otherwise} \end{cases}$$

Reading order is determined by sorting key characters with stable left-to-right indexing.
Decryption reverses the slicing operation and reads row-by-row.
