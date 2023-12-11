class Unspecified:
    pass

    def __repr__(self) -> str:
        return "Unspecified"


if __name__ == "__main__":
    u = Unspecified()
    print(u)
