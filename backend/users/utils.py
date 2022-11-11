from mainproject.iroha_config import *

@trace
def send_transaction_and_print_status(transaction):
    """
    Send transaction and print status
    """
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net_1.send_tx(transaction)
    for status in net_1.tx_status_stream(transaction):
        print(status)


def give_me_keys():
    private_key = IrohaCrypto.private_key()
    print('private : ',private_key)
    public_key = IrohaCrypto.derive_public_key(private_key)
    print('public : ',public_key)
    return {
        'public_key':public_key,
        'private_key':private_key
    }


def create_iroha_account(username):
    keys = give_me_keys()
    cmds = [
        iroha_admin.command('CreateAccount',
         account_name=f'{username}', domain_id='gigo',
                      public_key=keys['public_key'])
        
    ]
    tx = iroha_admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)
    return keys['private_key']


def get_asset_of_user(account_id,private_key='f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'):
    iroha_user = Iroha(account_id)
    print('account_id',account_id ,private_key)
    query = iroha_user.query('GetAccountAssets',creator_account='admin@gigo', account_id=account_id)
    IrohaCrypto.sign_query(query, private_key)
    response = net_3.send_query(query)
    data = response.account_assets_response
    return data