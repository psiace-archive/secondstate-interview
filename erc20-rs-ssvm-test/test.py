import ctypes
from binascii import unhexlify, hexlify
from evmc import *
from utils import *
import os
import signal
import glob
import re

handle = ctypes.cdll.LoadLibrary('./libsoll_runtime_test.so')

def evmc_vm_execute(
        calldata: bytes,
        sender: int,
        destination: int,
        wasm: bytes):
    _evmc_vm_execute = handle.evmc_vm_execute

    sender = int_to_address(sender)
    destination = int_to_address(destination)
    
    result = struct_evmc_result()
    _evmc_vm_execute(
        ctypes.cast(calldata, ctypes.c_char_p),
        len(calldata),
        ctypes.pointer(sender),
        ctypes.pointer(destination),
        ctypes.cast(wasm, ctypes.c_char_p),
        len(wasm),
        ctypes.pointer(result))

    return evmc_status_code__enumvalues[result.status_code], result


def evmc_get_storage(address: int, key: int):
    _evmc_get_storage = handle.evmc_get_storage

    address = int_to_address(address)
    key = int_to_bytes32(key)
    result = int_to_bytes32(0)
    

    _evmc_get_storage(
        ctypes.pointer(address),
        ctypes.pointer(key),
        ctypes.pointer(result))
    
    
    return bytes(result.raw)

def evmc_vm_deploy(deploy_wasm: bytes):
    sender = 0x7fffffff
    destination = 0
    return evmc_vm_execute(deploy_wasm, sender, destination, deploy_wasm)

def erc20_test(hexstr, sender, fins):
    status, result = evmc_vm_execute(
            unhexlify(hexstr),
            sender,
            0,
            erc20_rs
    )

    print(status, result.output_size)
    if result.output_size > 0:
        output = ctypes.cast(result.output_data, ctypes.POINTER(ctypes.c_char * result.output_size))
        print((bytes_to_long(bytes(output.contents))))
        return (status == 'EVMC_SUCCESS') and (fins == bytes_to_long(bytes(output.contents)))
    return (status == 'EVMC_SUCCESS')



erc20_tests = [
# // 0x06fdde03 name() ABI signature
    ("name", 
      b'06fdde03',
      0x7fffffff,
      bytes_to_long(b'ERC20TokenDemo')
    ),
# // 0x95d89b41 symbol() ABI signature
    ("symbol", 
      b'95d89b41',
      0x7fffffff,
      bytes_to_long(b'ETD')
    ),
# // 0x313ce567 decimals() ABI signature
    ("decimals", 
      b'313ce567',
      0x7fffffff,
      0
    ),
# // 0x18160ddd totalSupply() ABI signature
    ("total_supply", 
      b'18160ddd',
      0x7fffffff,
      100000000
    ),
# // 0x18160ddd mint() ABI signature
    ("mint", 
      b'aa174ccb' 
         + b'00000000000000000000000000000000DEADBEEF'
         + b'00000000000000FF',
      0x7fffffff,
      0
    ),
# // 0x9993021a do_balance(address) ABI signature
    ("do_balance_0xDEADBEEF", 
      b'9993021a' 
         + b'00000000000000000000000000000000DEADBEEF',
      0xDEADBEEF,
      0xff
    ),
# // 0x5d359fbd do_transfer() ABI signature
    ("do_transfer_0xDEADBEEF_0xFACEB00C", 
      b'5d359fbd' 
         + b'00000000000000000000000000000000FACEB00C'
         + b'0000000000000003',
      0xDEADBEEF,
      0xff
    ),     
# // 0x9993021a do_balance(address) ABI signature
    ("do_balance_0xDEADBEEF", 
      b'9993021a' 
         + b'00000000000000000000000000000000DEADBEEF',
      0xDEADBEEF,
      0xfc
    ),
# // 0x9993021a do_balance(address) ABI signature
    ("do_balance_0xFACEB00C", 
      b'9993021a' 
         + b'00000000000000000000000000000000FACEB00C',
      0xDEADBEEF,
      0x03
    ),
]

erc20_rs = open('erc20_rs.wasm', 'rb').read()
evmc_vm_deploy(erc20_rs)

for test, hexstr, sender, result in erc20_tests:
    print(test, erc20_test(hexstr, sender, result))
    print('---------------------')
