/* cisc.c
 * Mock-assembly programming for a CISC-like architecture
 * 
 * Programmer: Mayer Goldberg, 2010
 */

#include <stdio.h>
#include <stdlib.h>

#include "cisc.h"

/* change to 0 for no debug info to be printed: */
#define DO_SHOW 1

/* for debugging only, use SHOW("<some message>, <arg> */
#if DO_SHOW
#define SHOW(msg, x) { printf("%s %s = %ld\n", (msg), (#x), (x)); }
#else
#define SHOW(msg, x) 
 
#endif

int main()
{
  START_MACHINE;

  JUMP(CONTINUE);

#include "char.lib"
#include "io.lib"
#include "math.lib"
#include "string.lib"
#include "system.lib"

 CONTINUE:

  MAKE_SOB_VOID ();
  MOV (IND(0),R0);
  MAKE_SOB_NIL ();
  MOV (IND(1),R0);  
  MAKE_SOB_BOOL (IMM(0));
  MOV (IND(2),R0);
  MAKE_SOB_BOOL (IMM (1));
  MOV (IND(3),R0);


  OUT(IMM(2), IMM('?'));
  OUT(IMM(2), IMM(' '));
  CALL(READLINE);
  PUSH(R0);
  CALL(STRING_TO_UC);
  CALL(WRITELN);
  POP(R1);

  STOP_MACHINE;

  return 0;
}
