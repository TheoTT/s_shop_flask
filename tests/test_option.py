from . import BaseTest


class TestOption(BaseTest):

    def test_options(self, client):
        resp = client.get('/api/options/')
        assert resp.status_code == 200
