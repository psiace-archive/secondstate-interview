# 


wat2wasm sqlite_host.wat -o sqlite_host.wasm

gcc sqlite_host.c -lwasmedge_c -lsqlite3 -o sqlite_host.out

./sqlite_host.out