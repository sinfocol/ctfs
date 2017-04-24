# PlaidCTF 2017 - Down the Reversing Hole

| Category | Points | Solves |
| -------- |--------| -------|
| Misc     | 50     | 76     |

> Don't forget. This is a MISC challenge. 
> 
> [Download](reversing-hole_c344571f488311a2553d2cbac6fa0d35.exe)

## Solution

This is a misc challenge with some reversing. First we noticed the DOS code section of the binary was not an standard one, so we load the binary as an MS-DOS executable on the disassembler and we see two strings being xored, that would be a good indicator of an incoming flag:

```
seg000:0000                 public start
seg000:0000 start           proc near
seg000:0000                 mov     ax, seg dseg
seg000:0003                 mov     ds, ax
seg000:0005                 assume ds:dseg
seg000:0005                 lea     dx, unk_10030   ; "This program cannot be..."
seg000:0009                 mov     ah, 9
seg000:000B                 int     21h             ; DOS - PRINT STRING
seg000:000B                                         ; DS:DX -> string terminated by "$"
seg000:000D                 mov     cx, 0
seg000:0010
seg000:0010 loc_10010:
seg000:0010                 cmp     cx, 39h ; '9'
seg000:0013                 jz      short loc_1002C
seg000:0015                 lea     bx, unk_1005B   ; "WWE3>...\x0c\x00..." first string
seg000:0019                 add     bx, cx
seg000:001B                 mov     dl, [bx]
seg000:001D                 lea     bx, unk_10094   ; "\x15"1\x13VirQy..." second string
seg000:0021                 add     bx, cx
seg000:0023                 xor     dl, [bx]
seg000:0025                 mov     ah, 2
seg000:0027                 int     21h             ; DOS - DISPLAY OUTPUT
seg000:0027                                         ; DL = character to send to standard output
seg000:0029                 inc     cx
seg000:002A                 jmp     short loc_10010
seg000:002C ; ---------------------------------------------------------------------------
seg000:002C
seg000:002C loc_1002C:
seg000:002C                 mov     ah, 4Ch
seg000:002E                 int     21h             ; DOS - 2+ - QUIT WITH EXIT CODE (EXIT)
seg000:002E start           endp                    ; AL = exit code
seg000:002E
seg000:002E seg000          ends
seg000:002E
```

The answer is the XOR of the two strings:

```
57 57 45 33 3E 0C 00 34 5E 61 62 55 37 65 6E 64 76 02 57
20 65 52 62 79 30 27 0A 76 32 16 72 67 66 49 05 10 57 20
0B 51 19 25 3B 6D 03 64 60 07 30 36 72 6D 48 55 73 3A 0F 
^
15 22 31 13 56 69 72 51 79 12 42 34 17 03 02 05 11 22 07
63 31 14 19 18 44 78 66 45 53 23 06 38 12 21 36 62 64 53
54 35 29 15 56 32 73 54 12 73 43 69 42 03 17 31 43 49 72
=
But here's a flag PCTF{at_l3a5t_th3r3s_d00m_p0rts_0n_d0s}
```

## Flag
> PCTF{at_l3a5t_th3r3s_d00m_p0rts_0n_d0s}
