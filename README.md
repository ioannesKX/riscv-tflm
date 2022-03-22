# riscv-tflite-micro

You need to have a `riscv64-unknown-elf` toolchain installed and set to $PATH, along with `pk` and `spike`. See guide below. 

Compile person_detection_int8 for RISC-V:
```
git clone https://github.com/ioannesKX/riscv-tflm.git
cd riscv-tflm
```
then:
```
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=mcu_riscv TARGET_ARCH=riscv32_mcu person_detection_int8
```
or to use CMSIS-NN kernels:
```
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=mcu_riscv TARGET_ARCH=riscv32_mcu OPTIMIZED_KERNEL_DIR=cmsis_nn person_detection_int8
```

Run with Spike:
```
spike pk tensorflow/lite/micro/tools/make/gen/mcu_riscv_riscv32_mcu_default/bin/person_detection_int8
```

## RISC-V toolchain
This will install the RISC-V toolchain under /opt/riscv which requires sudo. You can use a different directory.

### RISC-V GCC
```
sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git
cd riscv-gnu-toolchain
./configure --prefix=/opt/riscv --with-arch=rv64gc --with-abi=lp64d
sudo make
```

then add /opt/riscv/bin to $PATH and restart (pk requires a RISC-V compiler)

### pk
```
cd ..
git clone https://github.com/riscv-software-src/riscv-pk.git
cd riscv-pk
mkdir build
cd build
../configure --prefix=/opt/riscv --host=riscv64-unknown-elf
make
sudo make install
```

### Spike
```
cd ..
sudo apt-get install device-tree-compiler
git clone https://github.com/riscv-software-src/riscv-isa-sim
cd riscv-isa-sim
mkdir build
cd build
../configure --prefix=/opt/riscv
make
sudo make install
```
