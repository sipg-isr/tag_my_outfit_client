import os

from typing import TYPE_CHECKING

from fashion_frontend.params import ImageBytesParams
from tests.integration.base_integration_test import BaseIT

if TYPE_CHECKING:
    from typing import List
    from fashion_contract.service_pb2 import PredictResponse
    from fashion_frontend.result import PredictResult

DATA_DIR = "tests/data"


class ImageBytesIT(BaseIT):
    """
    Class to test ImageBytesParams
    """

    @classmethod
    def __load_image_data(cls):
        cls.__image_bytes: 'List[bytes]' = []
        for file in os.listdir(DATA_DIR):
            with open(DATA_DIR + "/" + file, 'rb') as fp:
                cls.__image_bytes.append(fp.read())

    def test_selected_cat_selected_attr_concrete_send(self):
        print()
        print("Selected categories and selected attributes for image bytes with concrete send")
        for image_bytes in self.__image_bytes:
            # Predict using frontend
            image_params: ImageBytesParams = ImageBytesParams(image_bytes, all_categories=False, all_attributes=False)
            predict_results: 'List[PredictResult]' = self._send_image_bytes_params(image_params)
            grpc_response: 'PredictResponse' = self._send_grpc(image_bytes, False, False)
            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    def test_selected_cat_selected_attr_generic_send(self):
        print()
        print("Selected categories and selected attributes for image bytes with generic send")
        for image_bytes in self.__image_bytes:
            # Prediction using frontend
            image_params: ImageBytesParams = ImageBytesParams(image_bytes, all_categories=False, all_attributes=False)
            predict_results: List[PredictResult] = self._send(image_params)
            grpc_response: 'PredictResponse' = self._send_grpc(image_bytes, False, False)
            self.assertEqual(len(predict_results), 1)
            self._assert_equal_single_prediction(predict_results[0], grpc_response)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.__load_image_data()
