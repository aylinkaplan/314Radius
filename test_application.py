import unittest
import json
import io
import application as app


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_list(self):
        sent = '["John", "Smith", "1985-12-04", "Back to the Future"]'
        response = app.app.test_client().post(
            '/list',
            data=sent,
            content_type='application/json',)
        self.assertEqual(200, response.status_code)

    def test_csv(self):
        client = app.app.test_client()
        response = client.post(
            '/csv',
            data={
                'data_file': (io.BytesIO(b'109;122\n14;2\n206;23\n24;25\n27;28\n35;44\n46;54\n57;67\n68;95\n99;78'), 'input.csv'),
            }
        )
        self.assertEqual(200, response.status_code)

    def test_json(self):
        response = app.app.test_client().post(
            '/json',
            data=json.dumps({
                             "first_name": "John",
                             "last_name": "Smith",
                             "d_o_b": "1985-12-04",
                             "favorite_film": "Back to the Future"}),
            content_type='application/json',)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(200, response.status_code)
        assert len(data) == 6
        assert len(data['password']) > 6


if __name__ == '__main__':
    unittest.main()
