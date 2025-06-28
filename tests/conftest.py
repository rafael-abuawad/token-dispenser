import pytest


@pytest.fixture(scope="module")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def sender(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def user1(accounts):
    return accounts[1]


@pytest.fixture(scope="module")
def user2(accounts):
    return accounts[2]


@pytest.fixture(scope="module")
def user3(accounts):
    return accounts[3]


@pytest.fixture(scope="function")
def token_dispenser(project, sender):
    return project.TokenDispenser.deploy(sender=sender)


@pytest.fixture(scope="module")
def token(project, owner):
    return project.Token.deploy("Test Token", "TEST", owner, sender=owner)
