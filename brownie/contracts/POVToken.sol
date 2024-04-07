// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/token/ERC1155/ERC1155.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/access/Ownable.sol";

contract POVToken is ERC1155, Ownable {
    constructor(address initialOwner) ERC1155("") Ownable() {
        transferOwnership(initialOwner);
    }

    function setURI(string memory newuri) public onlyOwner {
        _setURI(newuri);
    }
}
