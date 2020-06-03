import grpc
import unittest

from typing import TYPE_CHECKING

from fashion_contract.service_pb2 import PredictRequest
from fashion_contract.service_pb2_grpc import PredictionServiceStub
from fashion_frontend.frontend import Frontend

if TYPE_CHECKING:
    from typing import List
    from fashion_contract.service_pb2 import PredictResponse
    from fashion_frontend.params import PredictParams, ImageBytesParams
    from fashion_frontend.result import PredictResult


class BaseIT(unittest.TestCase):
    """
    Base class to define tests for the frontend
    """

    __frontend: Frontend = None
    __grpc_channel: grpc.Channel = None
    __grpc_stub: PredictionServiceStub = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.__frontend = Frontend('localhost')
        cls.__grpc_channel = grpc.insecure_channel('localhost:50051')
        cls.__grpc_stub = PredictionServiceStub(cls.__grpc_channel)

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.__frontend
        cls.__grpc_channel.close()

    @classmethod
    def _send_image_bytes_params(cls, image_bytes_params: 'ImageBytesParams') -> 'List[PredictResult]':
        return cls.__frontend.predict_image_bytes(image_bytes_params)

    @classmethod
    def _send(cls, request_params: 'PredictParams') -> 'List[PredictResult]':
        return cls.__frontend.predict(request_params)

    @classmethod
    def _send_grpc(cls, image_bytes: bytes, all_categories: bool, all_attributes: bool) -> 'PredictResponse':
        predict_request: PredictRequest = PredictRequest(image_data=image_bytes,
                                                         all_categories=all_categories,
                                                         all_attributes=all_attributes)
        return cls.__grpc_stub.predict(predict_request)

    def _assert_equal_single_prediction(self, predict_result: 'PredictResult', grpc_response: 'PredictResponse') -> None:
        result_categories = predict_result.categories
        result_attributes = predict_result.attributes

        grpc_categories = grpc_response.predicted_categories
        grpc_attributes = grpc_response.predicted_attributes

        self.assertEqual(len(result_categories), len(grpc_categories))
        for result_cat, grpc_cat in zip(result_categories, grpc_categories):
            self.assertEqual(result_cat[0], grpc_cat.label)
            self.assertEqual(result_cat[1], grpc_cat.value)

        self.assertEqual(len(result_attributes), len(grpc_attributes))
        for result_attr, grpc_attr in zip(result_attributes, grpc_attributes):
            self.assertEqual(result_attr[0], grpc_attr.label)
            self.assertEqual(result_attr[1], grpc_attr.value)
