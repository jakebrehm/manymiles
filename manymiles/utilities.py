import hashlib


def generate_hash(password: str) -> str:
    """Generates the hash of the provided password using the MD5 algorithm."""

    h = hashlib.new("SHA256")
    h.update(password.encode())
    return h.hexdigest()