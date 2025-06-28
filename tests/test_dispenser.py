from ape import reverts


def get_tokens(sc_token_dispenser):
    tokens = []
    i = 0
    while True:
        try:
            tokens.append(sc_token_dispenser.tokens(i))
            i += 1
        except Exception:
            break
    return tokens


def test_fee_equals_0_1(token_dispenser):
    assert token_dispenser.fee() == int(0.1e18)  # 0.1 ETH


def test_mint_success(token_dispenser, user1, project):
    name = "MyToken"
    symbol = "MTK"
    fee = token_dispenser.fee()
    token_dispenser.mint(name, symbol, sender=user1, value=fee)

    id = 0
    token = project.Token.at(token_dispenser.tokens(id))
    tokens = get_tokens(token_dispenser)
    assert token in tokens
    assert token.name() == name
    assert token.symbol() == symbol
    assert token.owner() == user1


def test_mint_wrong_fee_reverts(token_dispenser, user2):
    name = "FailToken"
    symbol = "FAIL"
    wrong_fee = token_dispenser.fee() - 1
    with reverts():
        token_dispenser.mint(name, symbol, sender=user2, value=wrong_fee)


def test_multiple_tokens(token_dispenser, user1, user2, project):
    fee = token_dispenser.fee()
    token_dispenser.mint("TokenA", "TKA", sender=user1, value=fee)
    token_dispenser.mint("TokenB", "TKB", sender=user2, value=fee)
    tokens = get_tokens(token_dispenser)
    token1 = project.Token.at(tokens[0])
    token2 = project.Token.at(tokens[1])
    assert token1.symbol() == "TKA"
    assert token2.symbol() == "TKB"


def test_token_contract_properties(token_dispenser, user1, project):
    fee = token_dispenser.fee()
    name = "SpecialToken"
    symbol = "SPC"
    token_dispenser.mint(name, symbol, sender=user1, value=fee)
    id = 0
    token = project.Token.at(token_dispenser.tokens(id))
    assert token.name() == name
    assert token.symbol() == symbol
    assert token.owner() == user1


def test_tokens_array_length(token_dispenser, user1):
    fee = token_dispenser.fee()
    tokens_before = get_tokens(token_dispenser)
    token_dispenser.mint("NewToken", "NEW", sender=user1, value=fee)
    tokens_after = get_tokens(token_dispenser)
    assert len(tokens_after) == len(tokens_before) + 1
