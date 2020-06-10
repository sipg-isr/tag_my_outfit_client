"""
Example of how to classify image with the image path passed as a command line argument

Usage:

$ python predict_image_by_path.py image_path
    * image_path: path of the image to classify
"""

import sys

from typing import List
from outfit_tagging.client.frontend import Frontend
from outfit_tagging.client.params import ImagePathParams
from outfit_tagging.client.result import PredictResult

# The server is assumed to be running at localhost
_HOST = 'localhost'


def usage():
    print(f'Usage:\n\n'
          f'python predict_image_by_path.py image_path\n\n'
          f' * image_path: path of the image to classify\n')


def print_result(predict_result):
    print('Categories')
    for category in predict_result.categories:
        # print label : score
        print(f'  {category[0]} : {category[1]}')

    print()
    print('Attributes')
    for attribute in predict_result.attributes:
        # print label : score
        print(f'  {attribute[0]} : {attribute[1]}')


if len(sys.argv) != 2:
    usage()
    exit(1)

# Create frontend to communicate with server
# By default the assumed port is 50051 and the params all_categories and all_attributes are false
frontend: 'Frontend' = Frontend(_HOST)

image_path = sys.argv[1]

print()
print('Request with selected category and chosen attributes')
print()
# Create params for request
params: 'ImagePathParams' = ImagePathParams(image_path)
# Execute request
result: 'List[PredictResult]' = frontend.predict(params)
# Process results
print_result(result[0])

print()
print('Request with all categories and attributes scores')
print()
# Create params for request (the value all_categories and all_attributes with override the default server values)
params: 'ImagePathParams' = ImagePathParams(image_path, all_categories=True, all_attributes=False)
# Execute request
result: 'List[PredictResult]' = frontend.predict(params)
# Process results
print_result(result[0])
