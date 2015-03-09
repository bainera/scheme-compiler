/* scheme/write_sob_string.asm
 * Take a pointer to a Scheme string object, and 
 * prints (to stdout) the character representation
 * of that object.
 * 
 * Programmer: Mayer Goldberg, 2010
 */

 WRITE_SOB_STRING_SYMBOL:
  PUSH(FP);
  MOV(FP, SP);
  PUSH(R1);
  PUSH(R2);
  PUSH(R3);
  PUSH(R4);
  MOV(R0, FPARG(0));
  MOV(R1, INDD(R0, 1));
  MOV(R2, R0);
  ADD(R2, IMM(2));
 L_WSS_LOOP_SYMBOL:
  CMP(R1, IMM(0));
  JUMP_EQ(L_WSS_EXIT_SYMBOL);
  CMP(IND(R2), '\n');
  JUMP_EQ(L_WSS_NEWLINE_SYMBOL);
  CMP(IND(R2), '\t');
  JUMP_EQ(L_WSS_TAB_SYMBOL);
  CMP(IND(R2), '\f');
  JUMP_EQ(L_WSS_PAGE_SYMBOL);
  CMP(IND(R2), '\r');
  JUMP_EQ(L_WSS_RETURN_SYMBOL);
  CMP(IND(R2), '\\');
  JUMP_EQ(L_WSS_BACKSLASH_SYMBOL);
  CMP(IND(R2), '\"');
  JUMP_EQ(L_WSS_DQUOTE_SYMBOL);
  CMP(IND(R2), ' ');
  JUMP_LT(L_WSS_OCT_CHAR_SYMBOL);
  MOV (R4,IND(R2));
  //ADD(R4,IMM(32));
  PUSH(R4);
  CALL(PUTCHAR);
  DROP(1);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_DQUOTE_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('\"'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_BACKSLASH_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_RETURN_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('r'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_PAGE_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('f'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_TAB_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('t'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);  
 L_WSS_NEWLINE_SYMBOL:
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  PUSH(IMM('n'));
  CALL(PUTCHAR);
  DROP(2);
  JUMP(L_WSS_LOOP_CONT_SYMBOL);
 L_WSS_OCT_CHAR_SYMBOL:
  MOV(R0, IND(R2));
  MOV(R3, R0);
  REM(R3, IMM(8));
  PUSH(R3);
  DIV(R0, IMM(8));
  MOV(R3, R0);
  REM(R3, IMM(8));
  PUSH(R3);
  DIV(R0, IMM(8));
  REM(R0, IMM(8));
  PUSH(R0);
  PUSH(IMM('\\'));
  CALL(PUTCHAR);
  DROP(1);
  CALL(WRITE_INTEGER);
  DROP(1);
  CALL(WRITE_INTEGER);
  DROP(1);
  CALL(WRITE_INTEGER);
  DROP(1);
 L_WSS_LOOP_CONT_SYMBOL:
  INCR(R2);
  DECR(R1);
  JUMP(L_WSS_LOOP_SYMBOL);
 L_WSS_EXIT_SYMBOL:
  POP(R4);
  POP(R3);
  POP(R2);
  POP(R1);
  POP(FP);
  RETURN;

 
