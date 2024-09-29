import secrets
secret_key = secrets.token_urlsafe(32)  # Generates a secure random URL-safe key
print(secret_key)
