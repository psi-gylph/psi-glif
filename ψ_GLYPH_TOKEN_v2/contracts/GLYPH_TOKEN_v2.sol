// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GLYPH_TOKEN_v2 is ERC20 {
    uint256 private constant _maxSupply = 3140000 * 10 ** 18; // 3.14 milyon token
    address private _owner;

    constructor() ERC20("GLYPH_TOKEN", "GLYPH") {
        _owner = msg.sender;
        _mint(msg.sender, 1000000 * 10 ** 18); // Başlangıç arzı: 1 milyon token
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == _owner, "Sadece sahibi mint edebilir");
        require(totalSupply() + amount <= _maxSupply, "Maksimum arz asildi");
        _mint(to, amount);
    }

    function maxSupply() external pure returns (uint256) {
        return _maxSupply;
    }
}
