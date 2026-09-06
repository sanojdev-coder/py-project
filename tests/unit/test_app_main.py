from app.main import get_greeting, main


def test_get_greeting_returns_name():
    assert get_greeting("Alice") == "Hello, Alice!"


def test_main_prints_default_greeting(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"


def test_get_greeting_handles_blank_name():
    assert get_greeting("   ") == "Hello, World!"
