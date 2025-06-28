// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Token} from "./Token.sol";

contract TokenDispenser {
    uint256 public constant fee = 0.1 * 10 ** 18;
    Token[] public tokens;
    mapping (address => address) public owners;
    // uint256 public constant FEE = 0.1 ether;

    function mint(
        string memory _name,
        string memory _symbol
    ) payable public returns (address) {
        require(msg.value == fee, "fee insufficient");
        Token t = new Token(_name, _symbol, msg.sender);
        
        address token_address = address(t); 
        owners[token_address] = msg.sender;
        tokens.push(t);
        return token_address;
    }
}