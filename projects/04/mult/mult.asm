@i
M=1
@ans
M=0

(LOOP)
@i
D=M
@R1
D=D-M
@END1
D;JGT
@R0
D=M
@ans
M=M+D
@i
M=M+1
@LOOP
0;JMP

(END1)
@ans
D=M
@R2
M=D

(END)
@END
0;JMP