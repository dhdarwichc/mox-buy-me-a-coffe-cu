from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER = [boa.env.generate_address("non-owner") for _ in range(10)]

def test_price_feed_is_correct(coffe, eth_usd):
    assert coffe.PRICE_FEED() == eth_usd.address

def test_starting_values(coffe, account):
    assert coffe.MINIMUM_USD() == to_wei(5,"ether")
    assert coffe.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffe):
    with boa.reverts("You must spend more ETH!"):
        coffe.fund()

def test_fund_with_money(coffe_funded, account):
    #Arrange
    funder = coffe_funded.funders(0)
    #Assert
    assert funder == account.address
    assert coffe_funded.funder_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_cant_withdraw(coffe_funded, account):
    
    #Act
    with boa.env.prank(RANDOM_USER[3]):
        with boa.reverts("Not the contract owner!"):
            coffe_funded.withdraw()

def test_owner_can_withdraw(coffe_funded):
    #Act
    with boa.env.prank(coffe_funded.OWNER()):
        coffe_funded.withdraw()
    #Assert 
    assert boa.env.get_balance(coffe_funded.address) == 0

def test_fund_with_money_10_users(coffe):
    #Arrange
    total = 0
    balance = 0
    owner_initial_balance = boa.env.get_balance(coffe.OWNER())

    for user in RANDOM_USER:
        boa.env.set_balance(user, SEND_VALUE)
        balance = boa.env.get_balance(user)
        total = total + balance   
    contract_balance = SEND_VALUE * len(RANDOM_USER)

    #Act
    for user in RANDOM_USER:
        with boa.env.prank(user):
            coffe.fund(value=SEND_VALUE)
    #Assert
    contract_balance1 = boa.env.get_balance(coffe.address)
    funder = coffe.funders(0)

    assert funder == RANDOM_USER[0]
    assert coffe.funder_to_amount_funded(funder) == SEND_VALUE

    with boa.env.prank(coffe.OWNER()):
        coffe.withdraw()

    assert boa.env.get_balance(coffe.address) == 0
    assert boa.env.get_balance(coffe.OWNER()) == contract_balance + owner_initial_balance

def test_coverage(coffe):
    assert coffe.get_eth_to_usd_rate(SEND_VALUE) > 0

def test_coverage_default(coffe):
    #Arange
    initial_balance = boa.env.get_balance(coffe.address)
    boa.env.set_balance(RANDOM_USER[4], to_wei(10, "ether"))

    #Act
    with boa.env.prank(RANDOM_USER[4]):
       coffe.__default__(value=to_wei(1, "ether"))
  
    new_balance = boa.env.get_balance(coffe.address)

    #Assert
    assert new_balance == initial_balance + to_wei(1, 'ether')
    # Verificar el almacenamiento del financiador
    funder = coffe.funders(0)
    assert coffe.funder_to_amount_funded(funder) == to_wei(1, 'ether')

