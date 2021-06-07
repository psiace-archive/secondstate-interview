# erc20-rs-ssvm-test



## Compile libsoll_runtime_test

Required files:

+ `libssvm-evmc.so` a evmc wrapper for ssvm
+ `libsoll_runtime_test.so` a middle layer between python and `ssvm-evmc` 
+ `evmc.py` a python ctype wrapper for `libsoll_runtime_test.so`

Please clone [ssvm-evmc](https://github.com/second-state/ssvm-evmc) 
```
$ git clone git@github.com:second-state/ssvm-evmc.git
$ cd ssvm-evmc
$ git checkout master
```

Build `libsoll_runtime_test.so` and `libssvm-evmc.so `.
```
$ cd <path/to/ssvm-evmc>
$ mkdir -p build && cd build
```

Copy the libraries to `erc20-rs-ssvm-test` directory.
```
$ cd <path/to/erc20-rs-ssvm-test>
$ cp <path/to/ssvm-evmc>/build/tools/soll-runtime-test/libsoll_runtime_test.so .
$ cp <path/to/ssvm-evmc>/build/tools/tools/ssvm-evmc/libssvm-evmc.so .
```



## Testing erc20_rs.wasm

After compiling erc20_rs and soll-runtime-test. Make sure that the result files are copied into this directory:

+ `erc20_rs.wasm `
+ `libsoll_runtime_test.so`
+ `libssvm-evmc.so `

Then, execute `python test.py`. 
