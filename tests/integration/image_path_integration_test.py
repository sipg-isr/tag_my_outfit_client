import os

from typing import TYPE_CHECKING

from tests.integration.base_integration_test import BaseIT
from outfit_tagging.client.params import ImagePathParams

if TYPE_CHECKING:
    from typing import List
    from outfit_tagging.interface.service_pb2 import PredictResponse
    from outfit_tagging.client.result import PredictResult

DATA_DIR = "tests/data"


class ImagePathIT(BaseIT):
    """
    Class to test ImagePathParams
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
        print(f'Image path concrete send with all_categories={all_categories} and all_attributes={all_attributes}')
        for image_path in self.__image_paths:
            # Predict using frontend
            image_params: 'ImagePathParams' = ImagePathParams(image_path,
                                                              all_categories=all_categories,
                                                              all_attributes=all_attributes)
            predict_results: 'List[PredictResult]' = self._send_image_path_params(image_params)
            # Predict without frontend
            with open(image_path, 'rb') as fp:
                image_bytes = fp.read()
            grpc_response: 'PredictResponse' = self._send_grpc_unary(image_bytes, all_categories, all_attributes)
            # Assert results
            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    def __test_generic_send(self, all_categories, all_attributes):
        print()
        print(f'Image path generic send with all_categories={all_categories} and all_attributes={all_attributes}')
        for image_path in self.__image_paths:
            # Predict using frontend
            image_params: 'ImagePathParams' = ImagePathParams(image_path,
                                                              all_categories=all_categories,
                                                              all_attributes=all_attributes)
            predict_results: 'List[PredictResult]' = self._send(image_params)
            # Predict without frontend
            with open(image_path, 'rb') as fp:
                image_bytes = fp.read()
            grpc_response: 'PredictResponse' = self._send_grpc_unary(image_bytes, all_categories, all_attributes)
            # Assert results
            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__load_image_paths()

    @classmethod
    def __load_image_paths(cls) -> None:
        cls.__image_paths: 'List[str]' = list(map(lambda path: DATA_DIR + "/" + path, os.listdir(DATA_DIR)))