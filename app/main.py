def get_greeting(name: str | None = None) -> str:
    if name is None:
        name = "World"
    if not isinstance(name, str):
        raise TypeError("name must be a string or None")
    cleaned_name = name.strip() or "World"
    return f"Hello, {cleaned_name}!"


def main() -> None:
    print(get_greeting())


if __name__ == "__main__":
    main()
