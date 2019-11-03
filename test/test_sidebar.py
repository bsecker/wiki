from sidebar_generator import exclude_directories


def test_exclude_some():
    a = list("abcdef")
    exclude = ["a", "b", "c"]

    assert exclude_directories(a, exclude) == ["d", "e", "f"]


def test_exclude_none():
    a = list("abcdef")
    exclude = [""]

    assert exclude_directories(a, exclude) == list("abcdef")


def test_exclude_all():
    a = list("abcdef")
    exclude = list("abcdef")

    assert exclude_directories(a, exclude) == []
