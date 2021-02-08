#![no_std]

#[panic_handler]
fn self_panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[export_name = "fib"]
pub extern "C" fn fib(n: u32) -> u32 {
    if n == 0 {
        return 1;
    } else if n == 1 {
        return 1;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}
