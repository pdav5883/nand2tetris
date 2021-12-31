// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// R2 = 0
// R3 = R1
// (LOOP)
// if R3 <= 0 jump to ENDLOOP
// R2 += R0
// R3--
// jump to loop
// (ENDLOOP)
// jump to ENDLOOP
    
    @R2
    M=0
    @R1
    D=M
    @R3
    M=D

(LOOP)
    // condition
    @R3
    D=M
    @END
    D;JLE

    // action
    @R0
    D=M
    @R2
    M=M+D

    @R3
    M=M-1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP
