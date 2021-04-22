use hex_slice::AsHex;
use sha3::{Digest, Keccak256};
use std::env;
use std::convert::AsMut;

pub fn copy_into_array<A, T>(slice: &[T]) -> A
where
    A: Default + AsMut<[T]>,
    T: Copy,
{
    let mut a = A::default();
    <A as AsMut<[T]>>::as_mut(&mut a).copy_from_slice(slice);
    a
}


fn main() {
    let args: Vec<String> = env::args().collect();
	
    let mut hasher = Keccak256::new();
	hasher.update(&args[1].as_bytes());
	let result = hasher.finalize();

    let result_front: [u8; 4] = copy_into_array(&result[0..4]);
	println!("{:x}", result_front.as_hex());
}
