from .helpers import TestCase


class TestPage(TestCase):
    def test_header(self):
        rv = self.client.get("/")
        assert "Vape Survey" in str(rv.data)
