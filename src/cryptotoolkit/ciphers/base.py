"""Base class and common data structures for classical ciphers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import time
from typing import Any, Dict, Optional


@dataclass
class CipherResult:
    """Encapsulates the output and metadata of a cipher operation."""
    text: str
    key_display: str
    execution_time_ns: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    @property
    def execution_time_ms(self) -> float:
        """Execution time in milliseconds."""
        return self.execution_time_ns / 1_000_000.0

    @property
    def execution_time_us(self) -> float:
        """Execution time in microseconds."""
        return self.execution_time_ns / 1_000.0


class BaseCipher(ABC):
    """Abstract base class for all classical ciphers."""

    name: str = "Base Cipher"
    category: str = "Classical"
    description: str = ""

    @abstractmethod
    def encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        """Encrypt plaintext using the provided key."""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        """Decrypt ciphertext using the provided key."""
        pass

    def timed_encrypt(self, plaintext: str, key: Any, **kwargs) -> CipherResult:
        """Execute encrypt and attach precise high-resolution execution time."""
        t0 = time.perf_counter_ns()
        res = self.encrypt(plaintext, key, **kwargs)
        t1 = time.perf_counter_ns()
        res.execution_time_ns = t1 - t0
        return res

    def timed_decrypt(self, ciphertext: str, key: Any, **kwargs) -> CipherResult:
        """Execute decrypt and attach precise high-resolution execution time."""
        t0 = time.perf_counter_ns()
        res = self.decrypt(ciphertext, key, **kwargs)
        t1 = time.perf_counter_ns()
        res.execution_time_ns = t1 - t0
        return res
