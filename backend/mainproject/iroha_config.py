import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc

# Iroha peer 1
IROHA_HOST_ADDR_1 = os.getenv('IROHA_HOST_ADDR_1', '0.0.0.0')
IROHA_PORT_1 = os.getenv('IROHA_PORT_1', '50051')
# Iroha peer 2
IROHA_HOST_ADDR_2 = os.getenv('IROHA_HOST_ADDR_2', '0.0.0.0')
IROHA_PORT_2 = os.getenv('IROHA_PORT_2', '50052')
# Iroha peer 3
IROHA_HOST_ADDR_3 = os.getenv('IROHA_HOST_ADDR_2', '0.0.0.0')
IROHA_PORT_3 = os.getenv('IROHA_PORT_3', '50053')

habin_private_key ='3fc57dabe8b6ba959fbfd496a1d5390c8d335804f067eb0b41fece05f6cc76fb'
habin_public_key = '36d9f034299830ebd2687d514b0b871af9f1efc23b098a3e5069bb6384593c01'

iroha_habin = Iroha('habin@gigo')
# IrohaGrpc net for peer 1, 2, 3
net_1 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_1, IROHA_PORT_1))
net_2 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_2, IROHA_PORT_2))
net_3 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_3, IROHA_PORT_3))

# Admin Account loading with Admin's private key
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')
# Admin's account
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@gigo')
iroha_admin = Iroha(ADMIN_ACCOUNT_ID)

private_keys ={
    'habin@gigo':habin_private_key,
    'admin@gigo':ADMIN_PRIVATE_KEY,
    'pratik@gigo':'d81fbceb694bed07e25396b6daa056da810bf1189e2e30fb7151b857cbedeaac'
}

def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """

    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer

