from ape import networks


ADDRESS = "0xcec60Cbd4d90DA8e6cE5cc4969C67B74af06b9cd"


def main():
    etherscan = networks.provider.network.explorer
    etherscan.publish_contract(ADDRESS)
