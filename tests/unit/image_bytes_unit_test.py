import unittest

from outfit_tagging.client.params import ImageBytesParams


class ImageBytesUT(unittest.TestCase):
    """
    Class to test ImageBytesParams
    """

    def test_invalid_path_none_bytes(self):
        print()
        print('Image bytes with none bytes')
        with self.assertRaises(TypeError):
            ImageBytesParams(None)
