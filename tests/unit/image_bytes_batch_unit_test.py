import unittest

from outfit_tagging.client.params import ImageBytesBatchParams


class ImageBytesBatchUT(unittest.TestCase):
    """
    Class to test ImageBytesBatchParams
    """

    def test_bytes(self):
        print()
        print('Image bytes batch correct arguments')
        image_batch_bytes = [bytes('img1', 'utf-8')]
        params = ImageBytesBatchParams(image_batch_bytes)
        params_bytes = params.bytes
        count = 0
        for img_bytes in params_bytes:
            self.assertEqual(image_batch_bytes[0], img_bytes)
            count += 1
        self.assertEqual(count, 1)
        self.assertFalse(params.all_categories)
        self.assertFalse(params.all_attributes)

    def test_none_iterable(self):
        print()
        print('Image bytes batch with none bytes')
        with self.assertRaises(TypeError):
            ImageBytesBatchParams(None)

    def test_none_bytes(self):
        print()
        print('Image bytes batch with none bytes')
        with self.assertRaises(TypeError):
            ImageBytesBatchParams([None])