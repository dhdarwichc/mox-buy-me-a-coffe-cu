from src import buy_me_a_coffe
from moccasin.config import get_active_network


def withdraw():
    active_network = get_active_network()
    coffe = active_network.manifest_named("buy_me_a_coffe")
    print(f"Working with {coffe.address} in network {active_network.name}")
    coffe.withdraw()

def moccasin_main():
    return withdraw()