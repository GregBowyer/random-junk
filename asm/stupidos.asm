; Compile with nasm -f bin -o stupidos.bin stupidos.asm
; Then build the disk image dd if=stupidos.bin of=flop.img conv=notrunc
; Then you can run under qemu -fda flop.img
BITS 16
[ORG 0x7C00]

start:
    call clear_screen    ; Blank out the screen (lots of fiddly int10h work :S)
    call print_message
    jmp halt
    ;jmp $                ; Weeeeeee (infinate loop)

print_message:
    mov bx, 0
    mov bh, 00h
    mov bl, 07h
    mov al, 1
    mov bh, 0 
    mov bl, 02h
    mov cx, text_string_end - text_string
    mov dl, 10
    mov dh, 7
    push cs
    pop es
    mov bp, text_string
    mov ah, 13h
    int 10h
    ret

; Stolen from http://www.emu8086.com/assembler_source_code/micro-os_kernel.asm.html
clear_screen:
    
    ; Save the registers in case, I dunno in case we might need them again :P
    push ax
    push ds
    push bx
    push cx
    push di

    mov ax, 40h
    mov ds, ax           ; The screen params
    mov ah, 06h          ; 06h -> scroll screen up / clear screen AL - lines to scroll (0 for clea)
    mov al, 0            ; 0 all the lines !
    mov bh, 0h ; 1001_1111b   ; Wot new lines look like
    mov ch, 0            ; select the upper row (cursor pos)
    mov cl, 0            ; .... and the upper col (cursor pos)
    mov di, 84h          ; rows on screen - 1
    mov dh, [di]         ; lower row (from byte val)
    mov di, 4ah          ; cols on screen
    mov dl, [di]         ; ditto :40
    dec dl               ; lower col
    int 10h              ; inter on 10 -> call bios video services

    ; Rig up the cursor pos at the top of the screen
    mov bh, 0            ; page ?!?! 0 (think like VT but odder)
    mov dl, 0            ; col 0
    mov dh, 0            ; row 0
    mov ah, 02
    int 10h

    ; restore the registers from the stack
    pop ax
    pop ds
    pop bx
    pop cx
    pop di

    ret

halt:
    hlt                  ; Halt the cpu, dont burn it
    jmp halt             ; Spin round on int

print_string:            ; Routine: output string in SI to the screen
    mov ah, 0Eh          ; int 10h write teletype char
;    mov ah, 0Ah          ; int 10h write char
    mov bh, 0            ; 0 page
  .repeat:
    lodsb                ; Comsume a char from the string
    cmp al, 0
    je .done             ; Did we get a 0 (C styled EOS?)
    int 10h
    jmp .repeat
  .done:
    ret

; String table is here
text_string DB 'Why do you forsake me ?', 0
text_string_end:

times 510-($-$$) DB 0   ; Pad remainder of the boot sector with 0
dw 0xAA55               ; PC bios magic number for the boot sector
