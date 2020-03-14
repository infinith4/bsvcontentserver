import os
import flaskapp
import unittest
import tempfile
import flask

app = flask.Flask(__name__)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        print("test")

    def test_download_path():
        path = '/download/47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b'
        app.test_request_context(path)
        assert flask.request.path == path
if __name__ == '__main__':
    unittest.main()