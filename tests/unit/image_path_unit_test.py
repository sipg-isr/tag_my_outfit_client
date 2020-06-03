import unittest

from fashion_frontend.params import ImagePathParams


class ImagePathUT(unittest.TestCase):
    """
    Class to test ImagePathParams
    """

    def test_invalid_path_none_path(self):
        print()
        print('Image path with none path')
        with self.assertRaises(TypeError):
            ImagePathParams(None)

    def test_invalid_path_no_such_path(self):
        print()
        print('Image path with no such path')
        with self.assertRaises(ValueError):
            ImagePathParams('no_such_path')

    def test_invalid_path_no_such_file(self):
        print()
        print('Image path with no such file')
        with self.assertRaises(ValueError):
            ImagePathParams('tests/unit')
