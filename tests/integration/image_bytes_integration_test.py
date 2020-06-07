import os

from typing import TYPE_CHECKING

from tests.integration.base_integration_test import BaseIT
from outfit_tagging.client.params import ImageBytesParams

if TYPE_CHECKING:
    from typing import List
    from outfit_tagging.interface.service_pb2 import PredictResponse
    from outfit_tagging.client.result import PredictResult

DATA_DIR = "tests/data"


class ImageBytesIT(BaseIT):
    """
    Class to test ImageBytesParams
    """

    def test_selected_cat_selected_attr_concrete_send(self):
        self.__test_concrete_send(False, False)

    def test_selected_cat_selected_attr_generic_send(self):
        self.__test_generic_send(False, False)

    def test_all_cat_selected_attr_concrete_send(self):
        self.__test_concrete_send(True, False)

    def test_all_cat_selected_attr_generic_send(self):
        self.__test_generic_send(True, False)

    def test_selected_cat_all_attr_concrete_send(self):
        self.__test_concrete_send(False, True)

    def test_selected_cat_all_attr_generic_send(self):
        self.__test_generic_send(False, True)

    def test_all_cat_all_attr_concrete_send(self):
        self.__test_concrete_send(True, True)

    def test_all_cat_all_attr_generic_send(self):
        self.__test_generic_send(True, True)

    def __test_concrete_send(self, all_categories, all_attributes):
        print()
        print(f'Image bytes concrete send with all_categories={all_categories} and all_attributes={all_attributes}')
        for image_bytes in self.__image_bytes:
            # Predict using frontend
            image_params: 'ImageBytesParams' = ImageBytesParams(image_bytes,
                                                                all_categories=all_categories,
                                                                all_attributes=all_attributes)
            predict_results: 'List[PredictResult]' = self._send_image_bytes_params(image_params)
            grpc_response: 'PredictResponse' = self._send_grpc(image_bytes, all_categories, all_attributes)
            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    def __test_generic_send(self, all_categories, all_attributes):
        print()
        print(f'Image bytes generic send with all_categories={all_categories} and all_attributes={all_attributes}')
        for image_bytes in self.__image_bytes:
            # Prediction using frontend
            image_params: 'ImageBytesParams' = ImageBytesParams(image_bytes,
                                                                all_categories=all_categories,
                                                                all_attributes=all_attributes)
            predict_results: 'List[PredictResult]' = self._send(image_params)
            grpc_response: 'PredictResponse' = self._send_grpc(image_bytes, all_categories, all_attributes)

            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__load_image_data()

    @classmethod
    def __load_image_data(cls):
        cls.__image_bytes: 'List[bytes]' = []
        for file in os.listdir(DATA_DIR):
            with open(DATA_DIR + "/" + file, 'rb') as fp:
                cls.__image_bytes.append(fp.read())
