import hashlib

def hash_password(password):
    """Hashes a password using SHA256.
    For a production application, consider using stronger hashing libraries
    like bcrypt or scrypt.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, user_password):
    """Checks if a user-provided password matches the hashed password."""
    return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()
