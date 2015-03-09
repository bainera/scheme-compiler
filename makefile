.SUFFIXES: .asm
	-Iarch
%: %.asm
	gcc -x c -o $@ $<
#With warnings gcc -x c -o $@ $<s 
