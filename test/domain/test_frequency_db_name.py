from src.domain import FrequencyDbName

if __name__ == "__main__":
    n = FrequencyDbName.DAILY
    assert n == "daily"
    print(n)
    print(repr(n))
    x = FrequencyDbName("todo")
