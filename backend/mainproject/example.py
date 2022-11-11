import time
import binascii
from iroha import  Iroha, IrohaGrpc, IrohaCrypto
import os
import sys
import time


if sys.version_info[0] < 3:
    raise Exception('Python 3 or more updated version is required.')


# Iroha peer 1
IROHA_HOST_ADDR_1 = os.getenv('IROHA_HOST_ADDR_1', '0.0.0.0')
IROHA_PORT_1 = os.getenv('IROHA_PORT_1', '50051')
# Iroha peer 2
IROHA_HOST_ADDR_2 = os.getenv('IROHA_HOST_ADDR_2', '0.0.0.0')
IROHA_PORT_2 = os.getenv('IROHA_PORT_2', '50052')
# Iroha peer 3
IROHA_HOST_ADDR_3 = os.getenv('IROHA_HOST_ADDR_2', '0.0.0.0')
IROHA_PORT_3 = os.getenv('IROHA_PORT_3', '50053')

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


# # Satoshi's crypto material generation
habin_private_key ='3fc57dabe8b6ba959fbfd496a1d5390c8d335804f067eb0b41fece05f6cc76fb'
habin_public_key = '36d9f034299830ebd2687d514b0b871af9f1efc23b098a3e5069bb6384593c01'
iroha_habin = Iroha('habin@test')


# # Satoshi's account
SATOSHI_ACCOUNT_ID = os.getenv('SATOSHI_ACCOUNT_ID', 'satoshi@test')
iroha_satoshi = Iroha(SATOSHI_ACCOUNT_ID)
iroha_test = Iroha('test@test')



# # Nakamoto's crypto material generation
# nakamoto_private_key = IrohaCrypto.private_key()
# nakamoto_public_key = IrohaCrypto.derive_public_key(nakamoto_private_key)
# # Nakamoto's account
# NAKAMOTO_ACCOUNT_ID = os.getenv('NAKAMOTO_ACCOUNT_ID', 'nakamoto@test')
# iroha_nakamoto = Iroha(NAKAMOTO_ACCOUNT_ID)


# print("""
# Please ensure about MST in iroha config file.
# """)
elonpub='a0df360d257a2cd03594cfe46b10d83c2db032868a268a610f1d490a1c56211e'
elonpriv='43cf3533e7517833fe47a593c9e601ac8fc4ddee62cf8af83daf648342dd0b9c'

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


@trace
def send_transaction_and_print_status(transaction):
    """
    Send transaction and print status
    """
    global net_1
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net_1.send_tx(transaction)
    # for status in net_1.tx_status_stream(transaction):
    #     print(status)

    for i, status in enumerate(net_1.tx_status_stream(transaction)):
        status_name, status_code, error_code = status
        print(f"{i}: status_name={status_name}, status_code={status_code}, "
              f"error_code={error_code}")
        if status_name in ('STATEFUL_VALIDATION_FAILED', 'STATELESS_VALIDATION_FAILED', 'REJECTED'):
            raise RuntimeError(f"{status_name} failed on tx: "
                               f"{transaction} due to reason {error_code}: ")

def get_commands_from_tx(transaction):
    commands_from_tx = []
    for command in transaction.payload.reduced_payload.__getattribute__("commands"):
        listed_fields = command.ListFields()
        commands_from_tx.append(listed_fields[0][0].name)
    return commands_from_tx


def print_transaction_status(transaction):
    commands = get_commands_from_tx(transaction)
    for i, status in enumerate(net_1.tx_status_stream(transaction)):
        status_name, status_code, error_code = status
        print(f"{i}: status_name={status_name}, status_code={status_code}, "
              f"error_code={error_code}")
        print(transaction)
        if status_name in ('STATEFUL_VALIDATION_FAILED', 'STATELESS_VALIDATION_FAILED', 'REJECTED'):
            raise RuntimeError(f"{status_name} failed on tx: "
                               f"{transaction} due to reason {error_code}: "
                               )

@trace
def send_batch_and_print_status(transactions):
    net_1.send_txs(transactions)
    for tx in transactions:
        hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
        print('\t' + '-' * 20)
        creator = tx.payload.reduced_payload.creator_account_id
        print(f'Transaction hash = {hex_hash}, creator = {creator}')
        print_transaction_status(tx)




@trace
def set_detail_to_account(account_id: str,value:str):
    ms = int(time.time())
    print('ms : ',ms,type(ms))
    tx = iroha_admin.transaction([
        iroha_admin.command('SetAccountDetail',
                      account_id=account_id, key=f'{ms}', value=value)
    ],creator_account='admin@test')
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

# set_detail_to_account('jk_1@test')

@trace
def get_account_detail(user_id):    
    query = iroha_admin.query('GetAccountDetail',  creator_account='admin@test', account_id=user_id )
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net_3.send_query(query)
    print(response.account_detail_response.detail)
    return response

get_account_detail('jk_1@test')
# 
@trace
def create_asset_with_account(asset,domain):
    ms = int(time.time() )
    cmds = [
        iroha_admin.command('CreateAsset', asset_name=asset,
                      domain_id=domain, precision=0),
        iroha_admin.command('AddAssetQuantity',
                      asset_id=f'{asset}#{domain}', amount='1'),
        iroha_admin.command('CreateAccount', account_name=asset, domain_id=domain,
                      public_key='a0df360d257a2cd03594cfe46b10d83c2db032868a268a610f1d490a1c56211e'),
       
        iroha_admin.command('SetAccountDetail',
                      account_id=f'{asset}@{domain}', key=f'{ms}', value='admin@test')
        
    ]
    tx = iroha_admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

# create_asset_with_account('jk_1','test')




@trace
def create_account():
    cmds = [
        # iroha_admin.command('CreateAsset', asset_name='bitcoin',
        #               domain_id='test', precision=0),
        iroha_admin.command('CreateAccount', account_name='elon', domain_id='test',
                      public_key=elonpub),
        # iroha_admin.command('TransferAsset', src_account_id='admin@test', dest_account_id='habin@test',
        #               asset_id='bitcoin#test', description='init top up', amount='9'),
    ]
    tx = iroha_admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

# create_account()


@trace
def create_and_transfer_assets():
    
    cmds = [
        #  iroha_admin.command('CreateAsset', asset_name='receipt',
        #               domain_id='test', precision=0),
        iroha_admin.command('AddAssetQuantity',
                      asset_id=f'trashcoin#gigo', amount='1000.00'),
            #    iroha_admin.command('TransferAsset', src_account_id='admin@test', dest_account_id='elon@test',asset_id='receipt#test', amount='4'),
            #    iroha_admin.command('TransferAsset', src_account_id='admin@test', dest_account_id='test@test',asset_id='receipt#test', amount='4')
       ]
    
    tx = iroha_admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)

create_and_transfer_assets()

@trace
def transfer_asset_batch():
    admin_tx = iroha_admin.transaction(
        [iroha_admin.command(
            'TransferAsset', src_account_id='admin@test', dest_account_id='elon@test',
            asset_id='jk_1#test', amount='1'
        )],
        creator_account='admin@test'
    )
    elon_tx = iroha_admin.transaction(
        [iroha_admin.command(
            'TransferAsset', src_account_id='elon@test', dest_account_id='admin@test',
            asset_id='receipt#test', amount='1'
        )],
        creator_account='elon@test'
    )
    iroha_admin.batch([admin_tx, elon_tx], atomic=True)
    # sign transactions only after batch meta creation
    IrohaCrypto.sign_transaction(admin_tx, ADMIN_PRIVATE_KEY)
    send_batch_and_print_status([admin_tx, elon_tx])
# transfer_asset_batch()

@trace
def accept_batch_bill():
    iroha_elon = Iroha('elon@test')
    q = IrohaCrypto.sign_query(
        iroha_elon.query('GetPendingTransactions'),
        elonpriv
    )
    pending_transactions = net_1.send_query(q)
    pending_data =pending_transactions.transactions_response.transactions
    print(pending_data)

    for tx in pending_data:
        if tx.payload.reduced_payload.creator_account_id == 'admin@test':
            del tx.signatures[:]
        else:
            IrohaCrypto.sign_transaction(tx, elonpriv)
    

    '''
    Finally send the atomic batch of transactions to Iroha Peer
    '''
    send_batch_and_print_status(
        pending_transactions.transactions_response.transactions)
    set_detail_to_account('jk_1@test','elon@test')
    
# accept_batch_bill()

@trace
def get_asset_query():
    query = iroha_admin.query('GetAssetInfo', asset_id='receipt#test', creator_account='admin@test')
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net_2.send_query(query)
    print(response)
    return query



# get_asset_query()




# set_detail_tx()



# 

# def create_role():
#     tx = iroha_admin.transaction([
#     iroha_admin.command('CreateRole', role_name='info', permissions=[primitive_pb2.can_get_all_acc_detail])
# ])
#     IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
#     send_transaction_and_print_status(tx)

# #     '''
#     Finally send the atomic batch of transactions to Iroha Peer
#     '''
#     send_batch_and_print_status([satoshi_tx, nakamoto_tx])
#  satoshi_tx = iroha_satoshi.transaction(
#         [iroha_satoshi.command(
#             'TransferAsset', src_account_id='satoshi@test', dest_account_id='nakamoto@test', asset_id='scoin#test',
#             amount='100'
#         )],
#         creator_account='satoshi@test'
#     )
# @trace
# def send_batch_and_print_status(transactions):
#     """
#     send batch of transactions
#     """
#     global net_1
#     net_1.send_txs(transactions)
#     for tx in transactions:
#         hex_hash = binascii.hexlify(IrohaCrypto.hash(tx))
#         print('\t' + '-' * 20)
#         print('Transaction hash = {}, creator = {}'.format(
#             hex_hash, tx.payload.reduced_payload.creator_account_id))
#         # for status in net_1.tx_status_stream(tx):
#         #     print(status)


# @trace
# def init_operation():
#     """
#     Init operation with some initialization commands
#     This operation is performed by Admin with 'admin@test' account
#     and Admin's valid credentials
#     """
#     global iroha_admin
#     '''
#     1. Admin create 'scoin' asset at 'test' domain with precision=2
#     2. Admin create 'ncoin' asset at 'test' domain with precision=2
#     3. Admin add '10000' ammount of scoin asset 
#        where asset id is 'scoin#test'
#     4. Admin add '20000' ammount of ncoin asset 
#        where asset id is 'ncoin#test'
#     5. Admin create new account where account_name='satoshi',
#        domain_id='test' with account holder public key
#     6. Admin create new account where account_name='nakamoto',
#        domain_id='test' with account holder public key
#     7. Admin transfer '10000' amount of 'scoin' from 
#        admin's account to 'satoshi' account
#     8. Admin transfer '20000' amount of 'ncoin' from 
#        admin's account to 'nakamoto' account         
#     '''
#     init_cmds = [
#         iroha_admin.command('CreateAsset', asset_name='scoin',
#                       domain_id='test', precision=2),
#         iroha_admin.command('CreateAsset', asset_name='ncoin',
#                       domain_id='test', precision=2),
#         iroha_admin.command('AddAssetQuantity',
#                       asset_id='scoin#test', amount='10000'),
#         iroha_admin.command('AddAssetQuantity',
#                       asset_id='ncoin#test', amount='20000'),
#         iroha_admin.command('CreateAccount', account_name='satoshi', domain_id='test',
#                       public_key=satoshi_public_key),
#         iroha_admin.command('CreateAccount', account_name='nakamoto', domain_id='test',
#                       public_key=nakamoto_public_key),
#         iroha_admin.command('TransferAsset', src_account_id='admin@test', dest_account_id='satoshi@test',
#                       asset_id='scoin#test', description='init top up', amount='10000'),
#         iroha_admin.command('TransferAsset', src_account_id='admin@test', dest_account_id='nakamoto@test',
#                       asset_id='ncoin#test', description='init top up', amount='20000')
#     ]
#     '''
#     Admin create transaction and sign with admin's private key
#     Finally send the transaction to Iroha Peer
#     '''
#     init_tx = iroha_admin.transaction(init_cmds)
#     IrohaCrypto.sign_transaction(init_tx, ADMIN_PRIVATE_KEY)
#     send_transaction_and_print_status(init_tx)




# @trace
# def satoshi_creates_exchange_batch():
#     """
#     Satoshi creates decentralized exchanged branch
#     """
#     global iroha_satoshi
#     global iroha_nakamoto
#     '''
#     '100' amount of 'scoin' will be transferred 
#     from 'satoshi' account to 'nakamoto' account   
#     '''
#     satoshi_tx = iroha_satoshi.transaction(
#         [iroha_satoshi.command(
#             'TransferAsset', src_account_id='satoshi@test', dest_account_id='nakamoto@test', asset_id='scoin#test',
#             amount='100'
#         )],
#         creator_account='satoshi@test'
#     )
#     '''
#     '200' amount of 'ncoin' will be transferred 
#     from 'nakamoto' account to 'satoshi' account   
#     '''
#     nakamoto_tx = iroha_nakamoto.transaction(
#         [iroha_nakamoto.command(
#             'TransferAsset', src_account_id='nakamoto@test', dest_account_id='satoshi@test', asset_id='ncoin#test',
#             amount='200'
#         )],
#         creator_account='nakamoto@test'
#     )
#     '''
#     Creating the batch of transactions for sending several transactions
#     This is atomic batch which means each and every transaction must 
#     need to pass all type of validations and after that all the transactions
#     of this batch will commit transactional changes into leger. 
#     '''
#     iroha_satoshi.batch([satoshi_tx, nakamoto_tx], atomic=True)
#     '''
#     Satoshi sign only his transaction with his private key
#     '''
#     IrohaCrypto.sign_transaction(satoshi_tx, satoshi_private_key)
#     '''
#     Finally send the atomic batch of transactions to Iroha Peer
#     '''
#     send_batch_and_print_status([satoshi_tx, nakamoto_tx])
#     time.sleep(10)


# @trace
# def nakamoto_accepts_exchange_request():
#     """
#     Nakomoto accepts  the atomic batch of transactions
#     """
#     global net_1
#     '''
#     Nakamoto can find pending transactions from peer 
#     or Satoshi may pass that via a messaging channel
#     (Like the example of multi signature)
#     Nakamoto is querying pending transactions from peer
#     with his valid credentials
#     '''
#     q = IrohaCrypto.sign_query(
#         iroha_nakamoto.query('GetPendingTransactions'),
#         nakamoto_private_key
#     )
#     '''
#     The atomic batch of transactions, which was previously created by 
#     Satoshi are now in pending state as those got Satoshi's signature for 
#     transferring of '100' amount of 'scoin'  from 'satoshi' account to 
#     'nakamoto' account but do not get Nakamoto's signature for transferring 
#     of '200' amount of 'ncoin' from  'nakamoto' account to 'satoshi' account
#     '''
#     pending_transactions = net_1.send_query(q)
#     '''
#     This atomic batch of pending transactions, already 
#     got Satoshi's signature and only need Nakamoto's signature
#     Nakamoto will delete Satoshi's signature and will sign 
#     only his transaction with his private key
#     '''
#     for tx in pending_transactions.transactions_response.transactions:
#         if tx.payload.reduced_payload.creator_account_id == 'satoshi@test':
#             del tx.signatures[:]
#         else:
#             IrohaCrypto.sign_transaction(tx, nakamoto_private_key)
#     '''
#     Finally send the atomic batch of transactions to Iroha Peer
#     '''
#     send_batch_and_print_status(
#         pending_transactions.transactions_response.transactions)
#     time.sleep(10)


# @trace
# def check_no_pending_txs():
#     """
#     The atomic batch of transactions got all the necessary
#     signatures and all the transactional changes are committed
#     into the ledger. So there will be no pending transactions
#     """
#     global net_1
#     print(' ~~~ No pending txs expected:')
#     print(
#         net_1.send_query(
#             IrohaCrypto.sign_query(
#                 iroha_nakamoto.query('GetPendingTransactions',
#                             creator_account='nakamoto@test'),
#                 nakamoto_private_key
#             )
#         )
#     )
#     print(' ~~~')


# @trace
# def get_nakamoto_account_assets_from_peer_1():
#     """
#     Nakamoto get account assets by querying
#     from peer 1 with valid credentials
#     """
#     global net_1
#     query = iroha_nakamoto.query('GetAccountAssets', account_id='nakamoto@test')
#     IrohaCrypto.sign_query(query, nakamoto_private_key)

#     response = net_1.send_query(query)
#     data = response.account_assets_response.account_assets
#     for asset in data:
#         print('Asset id = {}, balance = {}'.format(
#             asset.asset_id, asset.balance))


# @trace
# def get_nakamoto_account_assets_from_peer_2():
#     """
#     Nakamoto get account assets by querying
#     from peer 2 with valid credentials
#     """
#     global net_2
#     query = iroha_nakamoto.query('GetAccountAssets', account_id='nakamoto@test')
#     IrohaCrypto.sign_query(query, nakamoto_private_key)

#     response = net_2.send_query(query)
#     data = response.account_assets_response.account_assets
#     for asset in data:
#         print('Asset id = {}, balance = {}'.format(
#             asset.asset_id, asset.balance))


# @trace
# def get_nakamoto_account_assets_from_peer_3():
#     """
#     Nakamoto get account assets by querying
#     from peer 3 with valid credentials
#     """
#     global net_3
#     query = iroha_nakamoto.query('GetAccountAssets', account_id='nakamoto@test')
#     IrohaCrypto.sign_query(query, nakamoto_private_key)

#     response = net_3.send_query(query)
#     data = response.account_assets_response.account_assets
#     for asset in data:
#         print('Asset id = {}, balance = {}'.format(
#             asset.asset_id, asset.balance))


# @trace
# def get_satoshi_account_assets_from_peer_3():
#     """
#     Satoshi get account assets by querying
#     from peer 3 with valid credentials
#     """
#     global net_3
#     query = iroha_satoshi.query('GetAccountAssets', account_id='satoshi@test')
#     IrohaCrypto.sign_query(query, satoshi_private_key)

#     response = net_3.send_query(query)
#     data = response.account_assets_response.account_assets
#     for asset in data:
#         print('Asset id = {}, balance = {}'.format(
#             asset.asset_id, asset.balance))


# init_operation()
# satoshi_creates_exchange_batch()
# nakamoto_accepts_exchange_request()
# check_no_pending_txs()
# get_nakamoto_account_assets_from_peer_1()
# get_nakamoto_account_assets_from_peer_2()
# get_nakamoto_account_assets_from_peer_3()
# get_satoshi_account_assets_from_peer_3()


#
