from ape import project, accounts


def main():
    cuenta_brave = accounts.load("brave")
    project.TokenDispenser.deploy(sender=cuenta_brave, publish=True)
