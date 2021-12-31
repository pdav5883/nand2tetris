// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@3
D=A
@numrows
M=D
@white
M=0
D=A
@status
M=D
@black
M=-1
D=A
@notstatus
M=D

(MAINLOOP)
    // check for keyboard input if none, do nothing
    @KBD
    D=M
    @MAINLOOP
    D;JEQ

    // paint everything
    @PAINT
    0;JMP
    (ENDPAINT)
    
    // flip status
    @FLIPSTATUS
    0;JMP
    (ENDFLIPSTATUS)

    @MAINLOOP
    0;JMP

// paint subroutine
(PAINT)
    @i
    M=0

    // val stores the value that we paint each row
    @notstatus
    A=M
    D=M
    @val
    M=D

    (PLOOP)
        // if i == numrows stop
        @i
        D=M
	@numrows
	D=D-M
        @ENDPAINT
        D;JEQ

        // RAM[SCREEN+i] = val
	@SCREEN
	D=A
	@i
	D=D+M
	@R0
	M=D   // address of current screen row stored in R0
	@val
	D=M
	@R0
	M=D

	// i++
	@i
	M=M+1

	@PLOOP
	0;JMP

// flip status subroutine
(FLIPSTATUS)
    @status
    D=M
    @R0
    M=D
    @notstatus
    D=M
    @status
    M=D
    @R0
    D=M
    @notstatus
    M=D
    @ENDFLIPSTATUS
    0;JMP
