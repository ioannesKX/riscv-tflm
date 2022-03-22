# riscv-tflite-micro

You need to have a `riscv64-unknown-elf` toolchain installed and set to $PATH, along with `pk` and `spike`. 

Compiler person_detection_int8 for riscv:
```
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=mcu_riscv TARGET_ARCH=riscv32_mcu person_detection_int8
```
To use CMSIS-NN kernels:
```
make -f tensorflow/lite/micro/tools/make/Makefile TARGET=mcu_riscv TARGET_ARCH=riscv32_mcu OPTIMIZED_KERNEL_DIR=cmsis_nn person_detection_int8
```

Run with Spike:
```
spike pk tensorflow/lite/micro/tools/make/gen/mcu_riscv_riscv32_mcu_default/bin/person_detection_int8
```
