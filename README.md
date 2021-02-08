# Second State Interview Project

The project is to figure out how to use the Rust ewasm API to write and compile an Ethereum smart contract.

Most people write Ethereum smart contracts in a JavaScript-like language called Solidity. Here is an example: 

<https://github.com/raineorshine/solidity-by-example/blob/master/basic-token-annotated.sol>

However, to port this example to Rust requires you to figure out how to represent non-native data structures like uint256, address, and mapping in Rust. The Rust ewasm API does that.

<https://docs.rs/ewasm_api/0.10.0/ewasm_api/>

Task: create a function to implement an ERC-20 contract in Rust. Compile it into the wasi-wasm32 target, and run it in SSVM.

