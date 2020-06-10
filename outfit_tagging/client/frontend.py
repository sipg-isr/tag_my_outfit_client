import grpc

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from outfit_tagging.interface.service_pb2 import PredictRequest
from outfit_tagging.interface.service_pb2_grpc import TagMyOutfitServiceStub
from outfit_tagging.client.result import PredictResult

if TYPE_CHECKING:
    from typing import List, Iterable
    from outfit_tagging.interface.service_pb2 import PredictResponse, StreamPredictResponse
    from outfit_tagging.client.params import (PredictParams, UnaryPredictParams,
                                              ImageBytesParams, ImagePathParams, ImageBytesBatchParams)

_DEFAULT_GRPC_PORT = 50051


class FrontendInterface(ABC):
    """
    Abstract class to handle predictions
    """

    def __init__(self, all_categories: bool = False, all_attributes: bool = False):
        """
        :param all_categories: True if the the server response should contain the values for all categories
                               and false for only the predicted one
        :param all_attributes: True if the the server response should contain the values for all attributes
                               and false for only the predicted ones
        """
        self._all_categories = all_categories
        self._all_attributes = all_attributes

    @abstractmethod
    def predict_image_bytes(self, params: 'ImageBytesParams') -> 'List[PredictResult]':
        """
        Predicts the categories and attributes for the given image bytes
        :param params: Params with the image bytes to classify. The default values for
                       all_categories and all_attributes are overridden by the values in the request if they exist
        :return: a single element list with all the prediction results
        """
        pass

    @abstractmethod
    def predict_image_path(self, params: 'ImagePathParams') -> 'List[PredictResult]':
        """
        Predicts the categories and attributes for the image in the given path
        :param params: Params with path to the image to classify. The default values for
                       all_categories and all_attributes are overridden by the values
                       in the request if they exist
        :return: a single element list with all the prediction results
        """
        pass

    @abstractmethod
    def predict_image_bytes_batch(self, params: 'ImageBytesBatchParams'):
        """
        Predicts the categories and attributes for the multiple images bytes
        :param params: Params with the multiple images bytes to classify. The default values for
                       all_categories and all_attributes are overridden by the values
                       in the request if they exist
        :return: a single element list with all the prediction results
        """
        pass


class Frontend(FrontendInterface):
    """
    Class to connect to server implementing the gRPC service interface
    specified in the fashion_contract package. Can be used as an interface for
    the provided service, handling the connection management
    """

    def __init__(self, host: str, port: str = _DEFAULT_GRPC_PORT,
                 all_categories: 'bool' = False, all_attributes: bool = False):
        """
        Connects the frontend to the server at the given host and port.
        The params all_categories and all_attributes will be used as default for the predictions
        :param host: Server host to connect (also supports DNS name resolution)
        :param port: Server port (defaults to 50051 since its gRPC default port)
        :param all_categories: True if the the server response should contain the values for all categories
                               and false for only the predicted one
        :param all_attributes: True if the the server response should contain the values for all attributes
                               and false for only the predicted ones
        """
        super().__init__(all_categories=all_categories, all_attributes=all_attributes)
        self.__host = host
        self.__port = port
        self.__channel = grpc.insecure_channel(f'{host}:{port}')
        self.__stub = TagMyOutfitServiceStub(self.__channel)

    def predict(self, params: 'PredictParams') -> 'List[PredictResult]':
        """
        Predicts the categories and attributes for the given request
        :param params: Params with the data to classify. The default values for
                       all_categories and all_attributes are overridden by the values
                       in the request if they exist
        :return: the prediction results for the given params
        """
        return params.accept_frontend_interface(self)

    def predict_image_bytes(self, params: 'ImageBytesParams') -> 'List[PredictResult]':
        return self.__predict_unary_prediction(params)

    def predict_image_path(self, params: 'ImagePathParams') -> 'List[PredictResult]':
        return self.__predict_unary_prediction(params)

    def predict_image_bytes_batch(self, params: 'ImageBytesBatchParams') -> 'List[PredictResult]':
        all_categories = params.all_categories if params.all_categories else self._all_categories
        all_attributes = params.all_attributes if params.all_attributes else self._all_attributes

        request_generator: 'Iterable[PredictRequest]' = map(lambda x: PredictRequest(image_data=x,
                                                                                     all_categories=all_categories,
                                                                                     all_attributes=all_attributes),
                                                            params.bytes)
        response: 'StreamPredictResponse' = self.__stub.stream_predict(request_generator)
        return [PredictResult(prediction) for prediction in response.predictions]

    def __predict_unary_prediction(self, params: 'UnaryPredictParams') -> 'List[PredictResult]':
        image_bytes = params.bytes
        all_categories = params.all_categories if params.all_categories else self._all_categories
        all_attributes = params.all_attributes if params.all_attributes else self._all_attributes

        request: 'PredictRequest' = PredictRequest(image_data=image_bytes,
                                                   all_categories=all_categories,
                                                   all_attributes=all_attributes)
        response: 'PredictResponse' = self.__stub.predict(request)

        return [PredictResult(response)]

    def __del__(self):
        self.__channel.close()
