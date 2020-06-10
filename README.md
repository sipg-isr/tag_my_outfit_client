# Tag My Outfit - Client Interface

## Overview

This project defines a client package to facilitate the communication with a server that implements this [gRPC interface](https://github.com/sipg-isr/tag_my_outfit_interface).
It aims to provide a object oriented interface which hides the client side gRPC communication details. 

The code was developed and tested in coordination with the [Tag My Outfit server](https://github.com/sipg-isr/tag_my_outfit_server), which implements the server side of the previously mentioned interface.

## Technologies

 * [Python](https://www.python.org)
 
 * [gRPC](https://grpc.io)

## Usage

### Requirements

 * [Python 3.6+](https://www.python.org)
 
 * [gRPC 1.16.1+](https://grpc.io) *(Automatically installed if missing)*
 
 * [gRPC interface 0.0.1](https://github.com/sipg-isr/tag_my_outfit_interface)

### Install

The project can be locally installed as a python package by following the next steps:

 * Clone the github repository, *(use tags for specific versions)*:
 
 ```
 $ git clone https://github.com/sipg-isr/tag_my_outfit_client.git
 ```

 * Inside the project folder, install the package:
 
 ```
 $ make
 ```

### Examples

Code examples are available in the [examples](examples) directory.
To execute any example, the server should also be running.
The [developed server](https://github.com/sipg-isr/tag_my_outfit_server) can be used with the provided examples.

### Uninstall

To uninstall the python package execute one of these commands:

 * Pip:
 
 ```
 $ pip uninstall -y outfit-tagging-client
 ```

 * Make *(Inside the project folder)*:
 
 ```
 $ make uninstall 
 ```

## License

This project is released under the [MIT License](LICENSE.md).