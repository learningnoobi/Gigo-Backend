from iroha import  Iroha, IrohaGrpc, IrohaCrypto


node1_priv = IrohaCrypto.private_key()
print('private : ',node1_priv)
node1_pub = IrohaCrypto.derive_public_key(node1_priv)
print('public : ',node1_pub)