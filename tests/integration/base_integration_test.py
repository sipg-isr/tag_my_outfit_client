import grpc
import unittest

from typing import TYPE_CHECKING

from outfit_tagging.interface.service_pb2_grpc import TagMyOutfitServiceStub
from outfit_tagging.interface.service_pb2 import PredictRequest
from outfit_tagging.client.frontend import Frontend

if TYPE_CHECKING:
    from typing import List, Iterator
    from outfit_tagging.interface.service_pb2 import PredictResponse, StreamPredictResponse
    from outfit_tagging.client.params import PredictParams, ImageBytesParams, ImagePathParams, ImageBytesBatchParams
    from outfit_tagging.client.result import PredictResult


class BaseIT(unittest.TestCase):
    """
    Base class to define tests for the frontend
    """

    __frontend: 'Frontend' = None
    __grpc_channel: 'grpc.Channel' = None
    __grpc_stub: 'TagMyOutfitServiceStub' = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.__frontend = Frontend('localhost')
        cls.__grpc_channel = grpc.insecure_channel('localhost:50051')
        cls.__grpc_stub = TagMyOutfitServiceStub(cls.__grpc_channel)

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.__frontend
        cls.__grpc_channel.close()

    @classmethod
    def _send_image_bytes_params(cls, image_bytes_params: 'ImageBytesParams') -> 'List[PredictResult]':
        return cls.__frontend.predict_image_bytes(image_bytes_params)

    @classmethod
    def _send_image_path_params(cls, image_path_params: 'ImagePathParams') -> 'List[PredictResult]':
        return cls.__frontend.predict_image_path(image_path_params)

    @classmethod
    def _send_image_bytes_batch_params(cls, image_bytes_batch_params: 'ImageBytesBatchParams') -> 'List[PredictResult]':
        return cls.__frontend.predict_image_bytes_batch(image_bytes_batch_params)

    @classmethod
    def _send(cls, request_params: 'PredictParams') -> 'List[PredictResult]':
        return cls.__frontend.predict(request_params)

    @classmethod
    def _send_grpc_unary(cls, image_bytes: bytes, all_categories: bool, all_attributes: bool) -> 'PredictResponse':
        predict_request: 'PredictRequest' = PredictRequest(image_data=image_bytes,
                                                           all_categories=all_categories,
                                                           all_attributes=all_attributes)
        return cls.__grpc_stub.predict(predict_request)

    @classmethod
    def _send_grpc_stream(cls, image_bytes_batch: 'List[bytes]', all_categories: bool, all_attributes: bool) \
            -> 'StreamPredictResponse':
        request_iterator: 'Iterator[PredictRequest]' = map(lambda x: PredictRequest(image_data=x,
                                                                                    all_categories=all_categories,
                                                                                    all_attributes=all_attributes),
                                                           image_bytes_batch)
        return cls.__grpc_stub.stream_predict(request_iterator)

    def _assert_equal_single_prediction(self,
                                        predict_result: 'PredictResult',
                                        grpc_response: 'PredictResponse') -> None:
        result_categories = predict_result.categories
        result_attributes = predict_result.attributes

        grpc_categories = grpc_response.categories
        grpc_attributes = grpc_response.attributes

        self.assertEqual(len(result_categories), len(grpc_categories))
        for result_cat, grpc_cat in zip(result_categories, grpc_categories):
            self.assertEqual(result_cat[0], grpc_cat.label)
            self.assertEqual(result_cat[1], grpc_cat.value)

        self.assertEqual(len(result_attributes), len(grpc_attributes))
        for result_attr, grpc_attr in zip(result_attributes, grpc_attributes):
            self.assertEqual(result_attr[0], grpc_attr.label)
            self.assertEqual(result_attr[1], grpc_attr.value)
