# 实现 fib 函数

这里是测试如何使用 Rust 生成 SSVM 可用的 wsam 文件，目标是简单的 fibonacci 计算，希望达到上文中的等价效果。

## 添加 wasm 工具链

这里添加 `wasm32-unknown-unknown` 作为目标。当然 ssvm 也支持 wasi ，所以可以添加 `wasm32-wasi` 并使用 rust 标准库。

```
rustup target add wasm32-unknown-unknown
```

## 编写 fib 示例

新建 fib-wasm 库，`cargo new --lib fib-wasm` 。相关文件内容如下：

**Cargo.toml**：编译类型指定为 `cdylib` 。

```
[package]
name = "fib-wasm"
version = "0.1.0"
authors = ["Chojan Shang <psiace@outlook.com>"]
edition = "2018"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]


[lib]
crate-type = ["cdylib"]

[profile.release]
incremental = false
panic = "abort"
lto = true
opt-level = "z"
```

**src/lib.rs**：编写 fib 函数，ssvm 调用需要加 `#[export_name = "fib"]`，需要自定义 `#[panic_handler]` 。

```
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
```

**.cargo/config**：指定编译目标为 `wasm32-unknown-unknown` 。

```
[build]
target = "wasm32-unknown-unknown"
rustflags = ["-Clink-arg=--export-table"]
```

## 使用 ssvm 验证

编译、运行需要遵循以下的方式：

```
# target 已经指定好，不需要额外处理
$ cargo build
# 编译好的文件位于 target/wasm32-unknown-unknown/release
$ ssvm --reactor fib_wasm.wasm fib 10
89
```

验证成功。
