// r0 = max(r1,r2)
// if r1 > r2 then r0 = r1
// else r0 = r2

// D = r1
// D = r1 - M
// D > 0, jump to selr1
// (selr2)
// D = r2
// r0 = D
// jump to end
// (selr1)
// D = r1
// r0 = D
// (end)
// jump to end
@R1
D=M
@R2
D=D-M
@SELR1
D;JGT
(SELR2)
@R2
D=M
@R0
M=D
@END
0;JMP
(SELR1)
@R1
D=M
@R0
M=D
(END)
@END
0;JMP
