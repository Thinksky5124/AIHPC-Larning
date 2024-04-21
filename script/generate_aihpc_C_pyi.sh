#!/bin/bash
###
 # @Author       : Thinksky5124
 # @Date         : 2024-04-21 18:59:16
 # @LastEditors  : Thinksky5124
 # @LastEditTime : 2024-04-21 20:57:27
 # @Description  : file content
 # @FilePath     : /AIHPC-Larning/script/generate_aihpc_C_pyi.sh
### 
mkdir build
cd build
cmake .. -DBUILD_STUB_FILES=ON
make
cp aihpc/_C.cpython-310-x86_64-linux-gnu.so ../aihpc/
