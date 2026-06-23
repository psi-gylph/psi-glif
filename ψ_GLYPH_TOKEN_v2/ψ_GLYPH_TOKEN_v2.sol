// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract GLYPH_TOKEN_V2 is ERC20 {
    constructor() ERC20("GlyphToken", "GLYPH") {
        _mint(msg.sender, 3140000 * 10 ** decimals());
    }
}
