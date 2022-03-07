from secrets import token_urlsafe


def generate_new_token(*, size_in_bytes: int = 100) -> str:
    return token_urlsafe(nbytes=size_in_bytes)
