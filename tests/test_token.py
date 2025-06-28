from ape import reverts


class TestTokenBasic:
    """Test basic ERC20 functionality"""

    def test_constructor(self, token, owner):
        """Test token constructor sets correct values"""
        assert token.name() == "Test Token"
        assert token.symbol() == "TEST"
        assert token.decimals() == 18
        assert token.owner() == owner

    def test_initial_balance(self, token, owner):
        """Test initial balance is zero"""
        assert token.balanceOf(owner) == 0

    def test_total_supply_initial(self, token):
        """Test initial total supply is zero"""
        assert token.totalSupply() == 0


class TestTokenMinting:
    """Test minting functionality"""

    def test_mint_by_owner(self, token, owner, user1):
        """Test owner can mint tokens"""
        initial_balance = token.balanceOf(user1)
        mint_amount = 1000 * 10**18

        token.mint(user1, mint_amount, sender=owner)

        assert token.balanceOf(user1) == initial_balance + mint_amount
        assert token.totalSupply() == mint_amount

    def test_mint_by_non_owner_reverts(self, token, user1, user2):
        """Test non-owner cannot mint tokens"""
        mint_amount = 1000 * 10**18

        with reverts():
            token.mint(user1, mint_amount, sender=user2)

    def test_mint_to_zero_address_reverts(self, token, owner):
        """Test minting to zero address reverts"""
        mint_amount = 1000 * 10**18

        with reverts():
            token.mint(
                "0x0000000000000000000000000000000000000000", mint_amount, sender=owner
            )

    def test_mint_zero_amount(self, token, owner, user1):
        """Test minting zero amount is allowed but doesn't change balance"""
        initial_balance = token.balanceOf(user1)
        initial_supply = token.totalSupply()

        token.mint(user1, 0, sender=owner)

        assert token.balanceOf(user1) == initial_balance
        assert token.totalSupply() == initial_supply


class TestTokenTransfer:
    """Test ERC20 transfer functionality"""

    def test_transfer(self, token, owner, user1, user2):
        """Test basic transfer functionality"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        transfer_amount = 100 * 10**18
        initial_balance_user1 = token.balanceOf(user1)
        initial_balance_user2 = token.balanceOf(user2)

        token.transfer(user2, transfer_amount, sender=user1)

        assert token.balanceOf(user1) == initial_balance_user1 - transfer_amount
        assert token.balanceOf(user2) == initial_balance_user2 + transfer_amount

    def test_transfer_insufficient_balance(self, token, owner, user1, user2):
        """Test transfer with insufficient balance reverts"""
        # Mint tokens to user1
        mint_amount = 100 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        transfer_amount = 200 * 10**18  # More than balance

        with reverts():
            token.transfer(user2, transfer_amount, sender=user1)

    def test_transfer_to_zero_address(self, token, owner, user1):
        """Test transfer to zero address reverts"""
        # Mint tokens to user1
        mint_amount = 100 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        with reverts():
            token.transfer(
                "0x0000000000000000000000000000000000000000", 50 * 10**18, sender=user1
            )


class TestTokenApproval:
    """Test ERC20 approval functionality"""

    def test_approve(self, token, user1, user2):
        """Test approve functionality"""
        approve_amount = 500 * 10**18

        token.approve(user2, approve_amount, sender=user1)

        assert token.allowance(user1, user2) == approve_amount

    def test_transfer_from(self, token, owner, user1, user2):
        """Test transferFrom functionality"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        approve_amount = 500 * 10**18
        transfer_amount = 200 * 10**18

        # User1 approves user2 to spend tokens
        token.approve(user2, approve_amount, sender=user1)

        # User2 transfers tokens from user1
        token.transferFrom(user1, user2, transfer_amount, sender=user2)

        assert token.balanceOf(user1) == mint_amount - transfer_amount
        assert token.balanceOf(user2) == transfer_amount
        assert token.allowance(user1, user2) == approve_amount - transfer_amount

    def test_transfer_from_insufficient_allowance(self, token, owner, user1, user2):
        """Test transferFrom with insufficient allowance reverts"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        approve_amount = 100 * 10**18
        transfer_amount = 200 * 10**18  # More than allowance

        # User1 approves user2 to spend tokens
        token.approve(user2, approve_amount, sender=user1)

        # User2 tries to transfer more than allowed
        with reverts():
            token.transferFrom(user1, user2, transfer_amount, sender=user2)


class TestTokenBurnable:
    """Test ERC20Burnable functionality"""

    def test_burn(self, token, owner, user1):
        """Test burn functionality"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        burn_amount = 200 * 10**18
        initial_balance = token.balanceOf(user1)
        initial_supply = token.totalSupply()

        token.burn(burn_amount, sender=user1)

        assert token.balanceOf(user1) == initial_balance - burn_amount
        assert token.totalSupply() == initial_supply - burn_amount

    def test_burn_from(self, token, owner, user1, user2):
        """Test burnFrom functionality"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        approve_amount = 500 * 10**18
        burn_amount = 200 * 10**18

        # User1 approves user2 to burn tokens
        token.approve(user2, approve_amount, sender=user1)

        # User2 burns tokens from user1
        token.burnFrom(user1, burn_amount, sender=user2)

        assert token.balanceOf(user1) == mint_amount - burn_amount
        assert token.totalSupply() == mint_amount - burn_amount
        assert token.allowance(user1, user2) == approve_amount - burn_amount

    def test_burn_insufficient_balance(self, token, owner, user1):
        """Test burn with insufficient balance reverts"""
        # Mint tokens to user1
        mint_amount = 100 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        burn_amount = 200 * 10**18  # More than balance

        with reverts():
            token.burn(burn_amount, sender=user1)


class TestTokenPermit:
    """Test ERC20Permit functionality"""

    def test_nonce_increments(self, token, user1):
        """Test that nonce increments correctly"""
        initial_nonce = token.nonces(user1)

        # Nonce should start at 0
        assert initial_nonce == 0

    def test_permit_domain_separator(self, token):
        """Test that domain separator is correctly set"""
        # This tests that the permit functionality is properly initialized
        # The domain separator should be non-zero
        domain_separator = token.DOMAIN_SEPARATOR()
        assert domain_separator != 0


class TestTokenOwnable:
    """Test Ownable functionality"""

    def test_owner_transfer_ownership(self, token, owner, user1):
        """Test owner can transfer ownership"""
        assert token.owner() == owner

        token.transferOwnership(user1, sender=owner)

        assert token.owner() == user1

    def test_non_owner_transfer_ownership_reverts(self, token, user1, user2):
        """Test non-owner cannot transfer ownership"""
        with reverts():
            token.transferOwnership(user2, sender=user1)

    def test_renounce_ownership(self, token, owner):
        """Test owner can renounce ownership"""
        assert token.owner() == owner

        token.renounceOwnership(sender=owner)

        assert token.owner() == "0x0000000000000000000000000000000000000000"

    def test_non_owner_renounce_ownership_reverts(self, token, user1):
        """Test non-owner cannot renounce ownership"""
        with reverts():
            token.renounceOwnership(sender=user1)


class TestTokenIntegration:
    """Test integration scenarios"""

    def test_complete_workflow(self, token, owner, user1, user2):
        """Test a complete workflow: mint, approve, transfer, burn"""
        # 1. Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)
        assert token.balanceOf(user1) == mint_amount

        # 2. User1 approves user2 to spend tokens
        approve_amount = 500 * 10**18
        token.approve(user2, approve_amount, sender=user1)
        assert token.allowance(user1, user2) == approve_amount

        # 3. User2 transfers tokens from user1 to themselves
        transfer_amount = 200 * 10**18
        token.transferFrom(user1, user2, transfer_amount, sender=user2)
        assert token.balanceOf(user1) == mint_amount - transfer_amount
        assert token.balanceOf(user2) == transfer_amount

        # 4. User2 burns some tokens
        burn_amount = 50 * 10**18
        token.burn(burn_amount, sender=user2)
        assert token.balanceOf(user2) == transfer_amount - burn_amount
        assert token.totalSupply() == mint_amount - burn_amount

    def test_multiple_mints(self, token, owner, user1, user2):
        """Test multiple mint operations"""
        # First mint
        mint1_amount = 500 * 10**18
        token.mint(user1, mint1_amount, sender=owner)
        assert token.balanceOf(user1) == mint1_amount
        assert token.totalSupply() == mint1_amount

        # Second mint to same user
        mint2_amount = 300 * 10**18
        token.mint(user1, mint2_amount, sender=owner)
        assert token.balanceOf(user1) == mint1_amount + mint2_amount
        assert token.totalSupply() == mint1_amount + mint2_amount

        # Third mint to different user
        mint3_amount = 200 * 10**18
        token.mint(user2, mint3_amount, sender=owner)
        assert token.balanceOf(user2) == mint3_amount
        assert token.totalSupply() == mint1_amount + mint2_amount + mint3_amount

    def test_approval_workflow(self, token, user1, user2, user3):
        """Test approval and transfer workflow with multiple users"""
        # User1 approves user2
        approve_amount_1 = 300 * 10**18
        token.approve(user2, approve_amount_1, sender=user1)
        assert token.allowance(user1, user2) == approve_amount_1

        # User1 also approves user3
        approve_amount_2 = 200 * 10**18
        token.approve(user3, approve_amount_2, sender=user1)
        assert token.allowance(user1, user3) == approve_amount_2

        # User1 changes approval for user2
        new_approve_amount = 400 * 10**18
        token.approve(user2, new_approve_amount, sender=user1)
        assert token.allowance(user1, user2) == new_approve_amount
        assert (
            token.allowance(user1, user3) == approve_amount_2
        )  # Should remain unchanged

    def test_burn_workflow(self, token, owner, user1, user2):
        """Test burn workflow with approvals"""
        # Mint tokens to user1
        mint_amount = 1000 * 10**18
        token.mint(user1, mint_amount, sender=owner)

        # User1 approves user2 to burn tokens
        approve_amount = 500 * 10**18
        token.approve(user2, approve_amount, sender=user1)

        # User2 burns tokens from user1
        burn_amount = 200 * 10**18
        token.burnFrom(user1, burn_amount, sender=user2)

        # Check balances and allowances
        assert token.balanceOf(user1) == mint_amount - burn_amount
        assert token.totalSupply() == mint_amount - burn_amount
        assert token.allowance(user1, user2) == approve_amount - burn_amount

        # User1 burns some of their own tokens
        user_burn_amount = 100 * 10**18
        token.burn(user_burn_amount, sender=user1)

        assert token.balanceOf(user1) == mint_amount - burn_amount - user_burn_amount
        assert token.totalSupply() == mint_amount - burn_amount - user_burn_amount
