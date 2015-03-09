 
APPLY_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R1,FPARG(1)); // R1 = NUM OF ARGS
INCR(R1);
MOV(R2,FPARG(R1));
DECR(R1); 
PUSH(R2);//R2 = LIST
CALL(REVERSE);
DROP(1);
MOV(R2,R0); //R2 = REVERSED LIST 
MOV(R0,0); // R0 = COUNTER OF ARGS IN LIST 


PUSH(IMM(2)); //push magic!
APPLY_LOOP:
CMP(R2,IMM(2)); // IF R2 = NIL
JUMP_EQ(APPLY_LOOP_2);
PUSH(INDD(R2,1));  //push car
MOV(R2,INDD(R2,2)); // move to cdr
INCR(R0);
JUMP(APPLY_LOOP);

APPLY_LOOP_2:
CMP(R1, IMM(2)); //WHILE NUM OF ARGS >2
JUMP_EQ(APPLY_LOOP_END);
PUSH(FPARG(R1));
DECR(R1);
INCR(R0);
JUMP(APPLY_LOOP_2);

APPLY_LOOP_END:
MOV(R1,R0); //NUM OF ARGS
PUSH(R1);
MOV(R0,FPARG(2)); //FUNCTION
PUSH(INDD(R0,1)); //ENV
CALLA(INDD(R0,2));
DROP(1); // drop env
POP(R1); // r1 = num of args
DROP(R1); // drop args
DROP(1); //drop magic

POP(R2);
POP(R1);
POP(FP);
RETURN;


REVERSE:
PUSH(FP);
MOV(FP,SP);
PUSH(R2);

MOV(R2,FPARG(0)); //POINTER TO LIST
MOV(R0,IMM(2)); //R0= NIL

REVERSE_LOOP:
CMP(R2, IMM(2)); //WHILE R0 IS NOT NIL
JUMP_EQ(REVERSE_END);
PUSH(R0);
PUSH(INDD(R2,1)); //PUSH (CAR R0)
CALL(MAKE_SOB_PAIR);
DROP(2);
MOV(R2, INDD(R2,2)); //R0 = CDR R0
JUMP(REVERSE_LOOP);

REVERSE_END:
POP(R2);
POP(FP);
RETURN;