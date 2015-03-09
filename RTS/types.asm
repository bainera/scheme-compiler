/* 
* run-time support types functions
*/

/***********************************/
/********  MAKE_SOB_FRAC  **********/
/***********************************/


 MAKE_SOB_FRAC:
  PUSH(FP);
  MOV(FP, SP);

  PUSH(IMM(3));
  CALL(MALLOC);
  DROP(1);
  MOV(IND(R0), T_FRAC);
  MOV(INDD(R0, 1), FPARG(0)); //numerator
  MOV(INDD(R0, 2), FPARG(1));//denomerator


  POP(FP);
  RETURN;



 INT_TO_FRAC:
  PUSH(FP);
  MOV(FP, SP);
  PUSH(R1);
  PUSH(IMM(3));
  CALL(MALLOC);
  DROP(1);
  MOV(R1,FPARG(0));
  MOV(R1,INDD(R1,1));
  MOV(IND(R0), T_FRAC);
  MOV(INDD(R0, 1), R1); //numerator
  MOV(INDD(R0, 2), IMM(1));//denomerator
  POP(R1);
  POP(FP);
  RETURN;

FRAC_TO_INT:   //return numerator/denomerator without remaining
  PUSH(FP);
  MOV(FP, SP);
  PUSH(R1);
  MOV(R1,FPARG(0));
  MOV(R0,INDD(R1,1));
  MOV(R1,INDD(R1,2));
  DIV(R0,R1);
  PUSH(R0);
  CALL(MAKE_SOB_INTEGER);
  DROP(1);
  POP(R1);
  POP(FP);
  RETURN;
 
/***********************************/
/********       PAIR?     **********/
/***********************************/

PAIR_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(PAIR_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

PAIR_NOT_SYMBOL:
CMP(IND(R1),T_PAIR);
JUMP_NE(PAIR_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
PAIR_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      BOOLEAN?     **********/
/***********************************/
BOOLEAN_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(BOOLEAN_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

BOOLEAN_NOT_SYMBOL:
CMP(IND(R1),T_BOOL);
JUMP_NE(BOOLEAN_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
BOOLEAN_BODY_END:
POP(R1);
POP(FP);
RETURN;


/***********************************/
/********      CHAR?     **********/
/***********************************/
CHAR_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(CHAR_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

CHAR_NOT_SYMBOL:

CMP(IND(R1),T_CHAR);
JUMP_NE(CHAR_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
CHAR_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      ZERO?     **********/
/***********************************/
ZERO_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(ZERO_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

ZERO_NOT_SYMBOL:
PUSH(R1);
PUSH(IMM(1)); //number of args
PUSH(IMM(444)); //fake env
CALL(NUMBER_BODY);
DROP(3);
CMP(R0,IMM(5));
JUMP_NE(ZERO_BODY_END);
MOV(R0,IMM(3)); //R0 = False
CMP(INDD(R1,1),IMM(0));
JUMP_NE(ZERO_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
ZERO_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      INTEGER?     **********/
/***********************************/

INTEGER_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(INTEGER_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

INTEGER_NOT_SYMBOL:
CMP(IND(R1),T_INTEGER);
JUMP_NE(INTEGER_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
INTEGER_BODY_END:
POP(R1);
POP(FP);
RETURN;


/***********************************/
/********      SYMBOL?     **********/
/***********************************/

SYMBOL_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));

SYMBOL_CHECK:
CMP(IND(R1),T_SYMBOL);
JUMP_NE(SYMBOL_BODY_END);
MOV(R1,INDD(R1,1));
CMP(R1,IMM(0));
JUMP_EQ(SYMBOL_IS_TRUE);
MOV(R1,INDD(R1,1));
JUMP(SYMBOL_CHECK)

SYMBOL_IS_TRUE:
MOV(R0,IMM(5)); //R0 = TRUE

SYMBOL_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      STRING?     **********/
/***********************************/

STRING_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(STRING_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

STRING_NOT_SYMBOL:
CMP(IND(R1),T_STRING);
JUMP_NE(STRING_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
STRING_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      VECTOR?     **********/
/***********************************/

VECTOR_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2))
CMP(IND(R1),T_SYMBOL);
JUMP_NE(VECTOR_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

VECTOR_NOT_SYMBOL:
CMP(IND(R1),T_VECTOR);
JUMP_NE(VECTOR_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
VECTOR_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      PROCEDURE?  **********/
/***********************************/

PROCEDURE_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(PROCEDURE_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

PROCEDURE_NOT_SYMBOL:
CMP(IND(R1),T_CLOSURE);
JUMP_NE(PROCEDURE_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
PROCEDURE_BODY_END:
POP(R1);
POP(FP);
RETURN;


/***********************************/
/********      NULL?     **********/
/***********************************/

NULL_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(3)); //R0 = False
MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(NULL_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

NULL_NOT_SYMBOL:
CMP(IND(R1),T_NIL);
JUMP_NE(NULL_BODY_END);
MOV(R0,IMM(5)); //R0 = TRUE
NULL_BODY_END:
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********      NUMBER?     **********/
/***********************************/

NUMBER_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R0,IMM(5)); //R0 = True

MOV(R1,FPARG(2));
CMP(IND(R1),T_SYMBOL);
JUMP_NE(NUMBER_NOT_SYMBOL);
MOV(R1,INDD(R1,1));
MOV(R1,INDD(R1,1));

NUMBER_NOT_SYMBOL:
CMP(IND(R1),T_INTEGER);
JUMP_EQ(NUMBER_BODY_END);
CMP(IND(R1),T_FRAC);
JUMP_EQ(NUMBER_BODY_END);
MOV(R0,IMM(3)); //R0 = False
NUMBER_BODY_END:
POP(R1);
POP(FP);
RETURN;


/***********************************/
/********      CAR     **********/
/***********************************/

CAR_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0,FPARG(2));
MOV(R0,INDD(R0,1));
POP(FP);
RETURN;

/***********************************/
/********      CDR        **********/
/***********************************/

//__label__ CDR_BODY;
CDR_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0,FPARG(2));
MOV(R0,INDD(R0,2));
POP(FP);
RETURN;

/***********************************/
/********      CONS     **********/
/***********************************/

CONS_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(FPARG(3));
PUSH(FPARG(2));
CALL(MAKE_SOB_PAIR);
DROP(2);
POP(FP);
RETURN;

/***********************************/
/********  CHAR->INTEGER    **********/
/***********************************/

CHAR_TO_INTEGER_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0, FPARG(2));
MOV (R0, INDD(R0,1));
PUSH (R0);
CALL(MAKE_SOB_INTEGER);
DROP(1);
POP(FP);
RETURN;

/***********************************/
/********   INTEGER->CHAR   **********/
/***********************************/

INTEGER_TO_CHAR_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0, FPARG(2));
MOV (R0, INDD(R0,1));
PUSH(R0);
CALL(MAKE_SOB_CHAR);
DROP(1);
POP(FP);
RETURN;

/***********************************/
/******** STRING_LENGTH   **********/
/***********************************/

STRING_LENGTH_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0, FPARG(2));
MOV(R0,INDD(R0,1));

PUSH(R0);
CALL(MAKE_SOB_INTEGER);
DROP(1)
POP(FP);
RETURN;

/***********************************/
/******** STRING-REF   **********/
/***********************************/

STRING_REF_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);

MOV(R1,FPARG(2)); //r1 = string
MOV(R0,FPARG(3)); //r0 = index

MOV(R0,INDD(R0,1));
ADD(R0,2);

MOV(R1,INDD(R1,R0));

PUSH(R1);
CALL(MAKE_SOB_CHAR);
DROP(1);

POP(R1);
POP(FP);
RETURN;
/***********************************/
/******** VECTOR_LENGTH   **********/
/***********************************/

VECTOR_LENGTH_BODY:
PUSH(FP);
MOV(FP,SP);
MOV(R0, FPARG(2));
MOV(R0,INDD(R0,1));
PUSH(R0);
CALL(MAKE_SOB_INTEGER);
DROP(1);
POP(FP);
RETURN;

/***********************************/
/********  VECTOR_REF   **********/
/***********************************/

VECTOR_REF_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
MOV(R1,FPARG(2));
MOV(R0,FPARG(3));
MOV(R0,INDD(R0,1));
ADD(R0,2);
MOV(R0,INDD(R1,R0));
POP(R1);
POP(FP);
RETURN;

/***********************************/
/******** MAKE-VECTOR    **********/
/***********************************/

MAKE_VECTOR_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R2,FPARG(1)); //num of args
MOV(R0,FPARG(3)); 
CMP(R2,IMM(2));
JUMP_EQ(MAKE_VECTOR_BEGIN);

PUSH(IMM(0));
CALL(MAKE_SOB_INTEGER);
DROP(1);

MAKE_VECTOR_BEGIN:
MOV(R1,FPARG(2));
MOV(R1,INDD(R1,1)); //r1 = number of elemnt left
MOV(R2,R1); //r2 = number of elemnt in vercotr

MAKE_VECTOR_LOOP:
CMP(R1,IMM(0));
JUMP_EQ(MAKE_VECTOR_LOOP_END);
PUSH(R0);
SUB(R1,IMM(1));
JUMP(MAKE_VECTOR_LOOP);

MAKE_VECTOR_LOOP_END:
PUSH(R2);
CALL(MAKE_SOB_VECTOR);
DROP(R2);
DROP(1);

POP(R2);
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********  MAKE-STRING    **********/
/***********************************/

MAKE_STRING_BODY:
PUSH(FP);
MOV(FP,SP);
PUSH(R1);
PUSH(R2);

MOV(R2,FPARG(1));              // holds the number of args
CMP(R2,IMM(1));                  //check if only one 
JUMP_EQ(MAKE_STRING_ONE_ARG);
MOV(R0,FPARG(3));               // holds the char
JUMP(MAKE_STRING_TWO_ARGS);

MAKE_STRING_ONE_ARG:
  MOV(R0,IMM(0));
  MOV(R1,FPARG(2)); 
  MOV(R1,INDD(R1,1));
  MOV(R2,R1);
  JUMP(MAKE_STRING_LOOP);

MAKE_STRING_TWO_ARGS:

MOV(R1,FPARG(2));        //holds t_int
MOV(R1,INDD(R1,1));       //holds the number of copyes
MOV(R2,R1);
MOV(R0,INDD(R0,1));     //put in R0 the number of  the char on hasci

MAKE_STRING_LOOP:
CMP(R1,IMM(0));
JUMP_EQ(MAKE_STRING_LOOP_END);

PUSH(R0);
SUB(R1,IMM(1));
JUMP(MAKE_STRING_LOOP);
MAKE_STRING_LOOP_END:
PUSH(R2);
CALL(MAKE_SOB_STRING);
DROP(R2);
DROP(1);
POP(R2);
POP(R1);
POP(FP);
RETURN;

/***********************************/
/********  SYMBOL->STRING **********/
/***********************************/
SYMBOL_TO_STRING_BODY:
 PUSH(FP);
 MOV(FP,SP);
 PUSH(R1);
 PUSH(R2);
 PUSH(R3);

 MOV(R1,FPARG(2));
 MOV(R3,R1);

 CMP (INDD(R1,1),IMM(0));
 JUMP_EQ(HAVE_NO_BUCKET_SYMBOL_TO_STRING);

 MOV(R1,INDD(R1,1));
 MOV(R2,IND(R1));
 MOV(R0,R2);
 JUMP (BYOOSH);

 HAVE_NO_BUCKET_SYMBOL_TO_STRING:

 STARTING_LABEL: 
 CMP(IND(R3),T_STRING) ; // r3 holds the pointer to the symbol
 JUMP_EQ(ENDING_LABEL) ;
 DECR(R3) ;
 JUMP(STARTING_LABEL) ;
 ENDING_LABEL:

  MOV(R0,R3);

BYOOSH:
  POP(R3);
 POP(R2);
 POP(R1);
 POP(FP);
  RETURN;
