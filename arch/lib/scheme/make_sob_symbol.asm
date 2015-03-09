/* scheme/make_sob_integer.asm
 * Takes an bucket and place the corresponding Scheme object in R0
 * 
 * Programmer: Alon bainer, 2014
 */

 MAKE_SOB_SYMBOL:
  PUSH(FP);
  MOV(FP, SP);
  PUSH(IMM(2));
  CALL(MALLOC);
  DROP(1);
  MOV(IND(R0), T_SYMBOL);
  MOV(INDD(R0, 1), FPARG(0));
  POP(FP);
  RETURN;
