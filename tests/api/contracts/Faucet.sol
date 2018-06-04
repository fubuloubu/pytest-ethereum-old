pragma solidity ^0.4.24;

contract Faucet
{
    function withdraw(uint amount) public {
        msg.sender.transfer(amount);
    }

    function () public payable { }
}
