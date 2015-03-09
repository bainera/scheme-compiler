/*****************
 eq? function 
 input: two pointers for scheme objects
 output: #f for two object with diferrent types
         #f for two [chars/ints/fracs/symbols] with diferrent values
         #f for two scheme object not in a list abouve with diferrent addresses
         #t otherwise
******/ 

EQ_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R1,FPARG(2)); // FIRST POINTER
MOV(R2,FPARG(3)); //SECOND POINTER
MOV(R0,IMM(3)); // R0 = #F

CMP(IND(R1),IND(R2)); //CHECK IF THEY HAVE THE SAME TYPE
JUMP_NE(EQ_END);

CMP(IND(R1),T_INTEGER);
JUMP_EQ(EQ_CMP_VALUES);
CMP(IND(R1),T_FRAC);
JUMP_EQ(EQ_CMP_FRAC_VALUES);
CMP(IND(R1),T_CHAR);
JUMP_EQ(EQ_CMP_VALUES);
CMP(IND(R1),T_SYMBOL);
JUMP_EQ(EQ_CMP_VALUES);

//OTHERWISE COMPARE ADDRESSES:
CMP(R1,R2);
JUMP_NE(EQ_END);
MOV(R0,IMM(5)); // R0 = #T
JUMP(EQ_END);

EQ_CMP_VALUES:
CMP(INDD(R1,1),INDD(R2,1));
JUMP_NE(EQ_END);
MOV(R0,IMM(5)); // R0 = #T
JUMP(EQ_END);

EQ_CMP_FRAC_VALUES:
CMP(INDD(R1,1),INDD(R2,1));
JUMP_NE(EQ_END);
CMP(INDD(R1,2),INDD(R2,2));
JUMP_NE(EQ_END);
MOV(R0,IMM(5)); // R0 = #T
JUMP(EQ_END);

EQ_END:
POP(R2);
POP(R1);
POP(FP);
RETURN;