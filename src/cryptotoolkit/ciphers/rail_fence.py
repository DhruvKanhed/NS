"""Rail Fence (Zigzag Transposition) Cipher implementation."""

from typing import Any, List
from .base import BaseCipher, CipherResult
from ..utils.validation import validate_rail_fence_rails, validate_not_empty


class RailFenceCipher(BaseCipher):
    name = "Rail Fence Cipher"
    category = "Transposition"
    description = "Transposition cipher where characters are written in a downward and upward zigzag pattern across N rails, then read off row by row."

    @staticmethod
    def get_rail_indices(length: int, rails: int) -> List[int]:
        """Compute the rail index for each character index in the message."""
        if rails <= 1 or length <= 1:
            return [0] * length

        indices = []
        rail = 0
        direction = 1  # 1 for down, -1 for up
        for _ in range(length):
            indices.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return indices

    @staticmethod
    def generate_rail_visualization(text: str, rails: int) -> str:
        """Create an ASCII zigzag diagram of the text on the rails."""
        if rails <= 1 or len(text) <= 1:
            return text

        length = len(text)
        grid = [["·" for _ in range(length)] for _ in range(rails)]
        rail_indices = RailFenceCipher.get_rail_indices(length, rails)

        for col, (ch, r) in enumerate(zip(text, rail_indices)):
            grid[r][col] = ch

        lines = []
        for r_idx, row in enumerate(grid):
            lines.append(f"Rail {r_idx + 1}: " + "".join(row))
        return "\n".join(lines)

    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(plaintext, "Plaintext")
        rails = validate_rail_fence_rails(key)
        length = len(plaintext)

        # Edge cases: 1 rail or rails >= length
        if rails == 1 or rails >= length:
            return CipherResult(
                text=plaintext,
                key_display=f"Rails: {rails}",
                metadata={"rails": rails, "visualization": plaintext},
                notes=f"For rails={rails} and message length={length}, the text order remains unchanged."
            )

        rail_indices = self.get_rail_indices(length, rails)
        rail_buckets: List[List[str]] = [[] for _ in range(rails)]

        for ch, r in zip(plaintext, rail_indices):
            rail_buckets[r].append(ch)

        ciphertext = "".join("".join(bucket) for bucket in rail_buckets)
        viz = self.generate_rail_visualization(plaintext, rails)

        return CipherResult(
            text=ciphertext,
            key_display=f"Rails: {rails}",
            metadata={"rails": rails, "visualization": viz},
            notes=f"Zigzag pattern over {rails} rails:\n{viz}"
        )

    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        validate_not_empty(ciphertext, "Ciphertext")
        rails = validate_rail_fence_rails(key)
        length = len(ciphertext)

        if rails == 1 or rails >= length:
            return CipherResult(
                text=ciphertext,
                key_display=f"Rails: {rails}",
                metadata={"rails": rails},
                notes="Text remains unchanged."
            )

        rail_indices = self.get_rail_indices(length, rails)

        # Count how many characters land on each rail
        counts = [0] * rails
        for r in rail_indices:
            counts[r] += 1

        # Slice ciphertext into substrings corresponding to each rail
        rail_iterators = []
        ptr = 0
        for count in counts:
            segment = ciphertext[ptr : ptr + count]
            rail_iterators.append(iter(segment))
            ptr += count

        # Reconstruct plaintext by following the zigzag pattern
        plaintext_chars = []
        for r in rail_indices:
            plaintext_chars.append(next(rail_iterators[r]))

        plaintext = "".join(plaintext_chars)
        viz = self.generate_rail_visualization(plaintext, rails)

        return CipherResult(
            text=plaintext,
            key_display=f"Rails: {rails}",
            metadata={"rails": rails, "visualization": viz},
            notes=f"Reconstructed from zigzag rails:\n{viz}"
        )
