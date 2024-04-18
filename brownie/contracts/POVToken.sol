// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/token/ERC1155/ERC1155.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/access/Ownable.sol";

contract POVToken is ERC1155, Ownable {

    event MintingAttempt(address account, uint256 id, uint256 amount, bytes data);
    event MintingSuccess(address account, uint256 id, uint256 amount, bytes data);
    uint public test = 1234;
    constructor() ERC1155("") Ownable() {
    }

    function setOwner(address owner) public onlyOwner {
        transferOwnership(owner);
    }

    function setURI(string memory newuri) public onlyOwner {
        _setURI(newuri);
    }

    function mint(address to, uint256 id, uint256 amount, bytes memory data) public returns(uint){
        _mint(to, id, amount, data);
    }
}
