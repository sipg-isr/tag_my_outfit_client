import setuptools

setuptools.setup(
    name='outfit-tagging-client',
    description='client side gRPC communication interface for the tag my outfit service',
    packages=['outfit_tagging.client'],
    version='0.0.1',
    python_requires='>=3.6',
    install_requires=['outfit-tagging-interface==0.0.1', 'grpcio>=1.16.1']
)
