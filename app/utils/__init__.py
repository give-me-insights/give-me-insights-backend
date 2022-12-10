import string
import random


def generate_key(max_length: int, chars: str = string.ascii_uppercase) -> str:
    return "".join(random.choice(chars) for _ in range(max_length))


__all__ = [
    "generate_key",
]
