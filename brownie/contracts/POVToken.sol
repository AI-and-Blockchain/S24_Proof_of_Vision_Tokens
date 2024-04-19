// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/token/ERC1155/ERC1155.sol";
import "OpenZeppelin/openzeppelin-contracts@4.8.3/contracts/access/Ownable.sol";

contract POVToken is ERC1155, Ownable {

    constructor() ERC1155("") Ownable() {
    }

    // Owner must be set to TokenManager
    function setOwner(address owner) public onlyOwner {
        transferOwnership(owner);
    }
    
    function setURI(string memory newuri) public onlyOwner {
        _setURI(newuri);
    }

    // Function to mint new token. add is a worker
    function mint(address add, uint256 id, uint256 amount, bytes memory data) public returns(uint){
        _mint(add, id, amount, data);
    }
}
