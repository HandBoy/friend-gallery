from pytest import raises
from gallery.paginator import Paginator


def test_fail_send_page_like_string():
    with raises(Exception):
        Paginator("a", 10, "https://friend-gallery.herokuapp.com/api/v1/pics")


def test_fail_send_limit_like_string():
    with raises(Exception):
        Paginator(0, "a", "https://friend-gallery.herokuapp.com/api/v1/pics")
