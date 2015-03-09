/* 
* run-time support logic functions
*/

 // IND(3)=False , IND(4)= True
 
/***********************************/
/********      EQUAL      **********/
/***********************************/
EQUAL_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);

MOV(R1,FPARG(1));  //R1 = num of args
MOV(R0,IMM(5)); //R0 = #t

EQUAL_LOOP_START:
CMP(R1,IMM(2)); // while num of args >=2
JUMP_LT(EQUAL_BODY_END);
INCR(R1);
PUSH(FPARG(R1));
PUSH(FPARG(2));
CALL(BINARY_EQUAL);
DROP(2);
CMP(R0,IMM(3)); //if R0= #f
JUMP_EQ(EQUAL_BODY_END);
SUB(R1,2);
JUMP(EQUAL_LOOP_START);

EQUAL_BODY_END:
POP(R1);
POP(FP);
RETURN;

//******************
BINARY_EQUAL:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R1,FPARG(0));
PUSH(FPARG(0));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(EQUAL_FIRST_IS_FRAC);
PUSH(FPARG(0));
CALL(INT_TO_FRAC);
DROP(1);
MOV(R1,R0);

EQUAL_FIRST_IS_FRAC:
MOV(R2,FPARG(1));
PUSH(FPARG(1));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(EQUAL_BOTH_FRAC);
PUSH(FPARG(1));
CALL(INT_TO_FRAC);
MOV(R2,R0);
DROP(1);

EQUAL_BOTH_FRAC:

MUL(INDD(R1,1),INDD(R2,2));
MUL(INDD(R2,1),INDD(R1,2));
MOV(R1,INDD(R1,1));
MOV(R2,INDD(R2,1));
MOV(R0,IMM(5)); //R0 = #t
CMP(R1,R2);
JUMP_EQ(BINARY_EQUAL_END);
MOV(R0,IMM(3)); //R0 = #f

BINARY_EQUAL_END:
POP(R2);
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********  GRETAER_THAN   **********/
/***********************************/
GREATER_THAN_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);

MOV(R1,FPARG(1));  //R1 = num of args
MOV(R0,IMM(5)); //R0 = #t

GREATER_THAN_LOOP_START:
CMP(R1,IMM(2)); // while num of args >=2
JUMP_LT(GREATER_THAN_BODY_END);
INCR(R1);
PUSH(FPARG(R1));
DECR(R1);
PUSH(FPARG(R1));
CALL(BINARY_GREATER_THAN);
DROP(2);
CMP(R0,IMM(3)); //if R0= #f
JUMP_EQ(GREATER_THAN_BODY_END);
SUB(R1,1);
JUMP(GREATER_THAN_LOOP_START);

GREATER_THAN_BODY_END:
POP(R1);
POP(FP);
RETURN;

//******************
BINARY_GREATER_THAN:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R1,FPARG(0));
PUSH(FPARG(0));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(GREATER_THAN_FIRST_IS_FRAC);
PUSH(FPARG(0));
CALL(INT_TO_FRAC);
DROP(1);
MOV(R1,R0);

GREATER_THAN_FIRST_IS_FRAC:
MOV(R2,FPARG(1));
PUSH(FPARG(1));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(GREATER_THAN_BOTH_FRAC);
PUSH(FPARG(1));
CALL(INT_TO_FRAC);
MOV(R2,R0);
DROP(1);

GREATER_THAN_BOTH_FRAC:

MUL(INDD(R1,1),INDD(R2,2));
MUL(INDD(R2,1),INDD(R1,2));
MOV(R1,INDD(R1,1));
MOV(R2,INDD(R2,1));
MOV(R0,IMM(5)); //R0 = #t
CMP(R1,R2);
JUMP_GT(BINARY_GREATER_THAN_END);
MOV(R0,IMM(3)); //R0 = #f

BINARY_GREATER_THAN_END:
POP(R2);
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********  LESS_THAN   **********/
/***********************************/
LESS_THAN_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);

MOV(R1,FPARG(1));  //R1 = num of args
MOV(R0,IMM(5)); //R0 = #t

LESS_THAN_LOOP_START:
CMP(R1,IMM(2)); // while num of args >=2
JUMP_LT(LESS_THAN_BODY_END);
INCR(R1);
PUSH(FPARG(R1));
DECR(R1);
PUSH(FPARG(R1));
CALL(BINARY_LESS_THAN);
DROP(2);
CMP(R0,IMM(3)); //if R0= #f
JUMP_EQ(LESS_THAN_BODY_END);
SUB(R1,1);
JUMP(LESS_THAN_LOOP_START);

LESS_THAN_BODY_END:
POP(R1);
POP(FP);
RETURN;

//******************
BINARY_LESS_THAN:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R1,FPARG(0));
PUSH(FPARG(0));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(LESS_THAN_FIRST_IS_FRAC);
PUSH(FPARG(0));
CALL(INT_TO_FRAC);
DROP(1);
MOV(R1,R0);

LESS_THAN_FIRST_IS_FRAC:
MOV(R2,FPARG(1));
PUSH(FPARG(1));
PUSH(IMM(1)); //number of args
PUSH(IMM(999)); //FAKE ENV
CALL(INTEGER_BODY);
DROP(3);
JUMP_NE(LESS_THAN_BOTH_FRAC);
PUSH(FPARG(1));
CALL(INT_TO_FRAC);
MOV(R2,R0);
DROP(1);

LESS_THAN_BOTH_FRAC:

MUL(INDD(R1,1),INDD(R2,2));
MUL(INDD(R2,1),INDD(R1,2));
MOV(R1,INDD(R1,1));
MOV(R2,INDD(R2,1));
MOV(R0,IMM(5)); //R0 = #t
CMP(R1,R2);
JUMP_LT(BINARY_LESS_THAN_END);
MOV(R0,IMM(3)); //R0 = #f

BINARY_LESS_THAN_END:
POP(R2);
POP(R1);
POP(FP);
RETURN;
