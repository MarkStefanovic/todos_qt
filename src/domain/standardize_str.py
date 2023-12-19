__all__ = ("standardize_str",)


def standardize_str(s: str) -> str:
    return s.replace("\xa0", " ").replace("\r", "\n").strip("\xef\xbb\xbf ")
