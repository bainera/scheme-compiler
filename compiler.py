from tag_parser import *
from sys import argv

def compile_scheme_file(input_path, output_path):
	
	beginText = """/* cisc.c
 * Mock-assembly programming for a CISC-like architecture
 * 
 * 
 */

#include <stdio.h>
#include <stdlib.h>

#include "arch/cisc.h"

int main()
{
  START_MACHINE;

  JUMP(CONTINUE);

#include "arch/char.lib"
#include "arch/io.lib"
#include "arch/math.lib"
#include "arch/string.lib"
#include "arch/system.lib"
#include "arch/scheme.lib"
#include "rts.lib"

CONTINUE:\n"""

	yag = """
			(define Yag
  				(lambda fs
   					 (let ((ms (map
						(lambda (fi)
		 					 (lambda ms
		    					(apply fi (map (lambda (mi)
						     (lambda args
				       			(apply (apply mi ms) args))) ms))))
						fs)))
      					(apply (car ms) ms))))
		  """
	string =  "CALL(MAKE_SOB_VOID);\n"
	string+=  "CALL(MAKE_SOB_NIL);\n"
	string+=  "PUSH (IMM(0));\n"
	string+=  "CALL(MAKE_SOB_BOOL);\n"
	string+=  "DROP(1);\n"
	string+=  "PUSH (IMM(1));\n"
	string+=  "CALL(MAKE_SOB_BOOL);\n"
	string+=  "DROP(1);\n"

	beginText += string
	
	input = open(input_path,'r')
	output = open(output_path, 'w')
	
	output.write(beginText)
	(code,r)=AbstractSchemeExpr.parse("(define list (lambda X X))")
	output.write(code)
	(code,r)=AbstractSchemeExpr.parse(yag)
	output.write(code)

	(code,r)=AbstractSchemeExpr.parse(input.read())
	
	while r != "":
		output.write(code)
		(code,r)=AbstractSchemeExpr.parse(r)
		
	output.write(code)
	output.write(AbstractSchemeExpr.generateCode())
	
	output.write("STOP_MACHINE;\n");
	output.write("return 0;}\n");

	input.close()
	output.close()
	
  
