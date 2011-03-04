.PHONY: all clean

all: stupidos.img

stupidos.img: stupidos.asm
	nasm -f bin -o stupidos.bin $^
	dd if=stupidos.bin of=stupidos.img conv=notrunc

clean:
	-$(RM) stupidos.img stupidos.bin

qemu-test: stupidos.img
	qemu-kvm -fda stupidos.img
