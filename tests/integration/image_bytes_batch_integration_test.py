import os

from typing import TYPE_CHECKING

from tests.integration.base_integration_test import BaseIT
from outfit_tagging.client.params import ImageBytesBatchParams

if TYPE_CHECKING:
    from typing import List
    from outfit_tagging.interface.service_pb2 import StreamPredictResponse, Prediction
    from outfit_tagging.client.result import PredictResult

DATA_DIR = "tests/data"


class ImageBytesBatchIT(BaseIT):
    """
    Class to test ImageBytesBatchParams
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
        print(f'Image bytes batch concrete send with '
              f'all_categories={all_categories} and all_attributes={all_attributes}')
        # Predict with frontend
        image_params: 'ImageBytesBatchParams' = ImageBytesBatchParams(self.__image_bytes,
                                                                      all_categories=all_categories,
                                                                      all_attributes=all_attributes)
        predict_results: 'List[PredictResult]' = self._send_image_bytes_batch_params(image_params)
        # Compare with grpc result
        self.__cmp_result_with_grpc(predict_results, all_categories, all_attributes)

    def __test_generic_send(self, all_categories, all_attributes):
        print()
        print(f'Image bytes batch generic send with '
              f'all_categories={all_categories} and all_attributes={all_attributes}')
        # Predict with frontend
        image_params: 'ImageBytesBatchParams' = ImageBytesBatchParams(self.__image_bytes,
                                                                      all_categories=all_categories,
                                                                      all_attributes=all_attributes)
        predict_results: 'List[PredictResult]' = self._send(image_params)
        # Compare with grpc result
        self.__cmp_result_with_grpc(predict_results, all_categories, all_attributes)

    def __cmp_result_with_grpc(self, predict_results, all_categories, all_attributes):
        # Predict without frontend
        grpc_response: 'StreamPredictResponse' = self._send_grpc_stream(self.__image_bytes,
                                                                        all_categories,
                                                                        all_attributes)
        grpc_predictions: 'List[Prediction]' = list(grpc_response.predictions)
        # Assert results
        self.assertEqual(len(predict_results), len(grpc_predictions))
        for predict_result, grpc_prediction in zip(predict_results, grpc_predictions):
            self._assert_equal_single_prediction(predict_result, grpc_prediction)

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
