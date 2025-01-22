from src import buy_me_a_coffe
from script.deploy_mocks import deploy_feed
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

def deploy_coffe(price_feed : VyperContract) -> VyperContract:

    coffe: VyperContract = buy_me_a_coffe.deploy(price_feed.address)
    
    return coffe

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name} using price feed at {price_feed.address}")
    coffe: VyperContract = deploy_coffe(price_feed)
    if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
        print("Verifying contract on explorer...")
        result = active_network.moccasin_verify(coffe)
        result.wait_for_verification()
    return coffe
