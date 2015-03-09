import pc
import sexprs
import tag_parser

class SexprParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(Pskip())\
                        .parser(NumberParser())\
                        .parser(CharParser())\
                        .parser(StringParser())\
                        .parser(BoolanParser())\
                        .parser(NilParser())\
                        .delayed_parser(lambda: PairParser())\
                        .delayed_parser(lambda: VectorParser())\
                        .delayed_parser(lambda: QuotelikeParser())\
                        .parser(SymbolParser())\
                        .disjs(9)\
                        .parser(Pskip())\
                        .catens(3)\
                        .pack(lambda m: m[1])\
                        .done()

    def match(self,s):
        return self.parser.match(s)
##########################################################

class SignPosNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='+')\
                        .parser(Dig0Parser())\
                        .plus()\
                        .caten()\
                        .pack(lambda m: sexprs.Integer(m[0],10,"".join(m[1])))\
                        .done()
        
    def match(self,s):
        return self.parser.match(s)
##########################################################
class SignPosNotZeroNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='+')\
                        .const(lambda ch: ch==0)\
                        .star()\
                        .parser(DigParser())\
                        .plus()\
                        .catens(3)\
                        .pack(lambda m: sexprs.Integer("".join(m[0]),10,"".join(m[2])))\
                        .done()
 
        
    def match(self,s):
        return self.parser.match(s)
##########################################################
class NegNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='-')\
                        .parser(Dig0Parser())\
                        .plus()\
                        .caten()\
                        .pack(lambda m: sexprs.Integer(m[0],10,"".join(m[1])))\
                        .done()
        
    def match(self,s):
        return self.parser.match(s)     
##########################################################

class NegNotZeroNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='-')\
                        .const(lambda a: a=='0')\
                        .star()\
                        .parser(DigParser())\
                        .plus()\
                        .catens(3)\
                        .pack(lambda m: sexprs.Integer(m[0],10,"".join(m[2])))\
                        .done()
        
    def match(self,s):
        return self.parser.match(s)     
##########################################################   
class NoSignPosNotZeroNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda ch: ch==0)\
                        .star()\
                        .parser(DigParser())\
                        .plus()\
                        .caten()\
                        .pack(lambda m: sexprs.Integer('no',10,"".join(m[1])))\
                        .done()
        
    def match(self,s):
        return self.parser.match(s)    
##########################################################
class NoSignPosNatParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(Dig0Parser())\
                        .plus()\
                        .pack(lambda m: sexprs.Integer("",10,"".join(m)))\
                        .done()
        
    def match(self,s):
        return self.parser.match(s)   
##########################################################
   
class PosNumber (pc.AbstractParsingCombinator):  
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(SignPosNatParser())\
                        .parser(NoSignPosNatParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s) 
##########################################################
class PosNotZeroNumber (pc.AbstractParsingCombinator):  
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(NoSignPosNotZeroNatParser())\
                        .parser(SignPosNotZeroNatParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s)   
###########################################
     
class DigParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.pcRange('1','9')
    
    def match(self,s):
        return self.parser.match(s)
################################################
class Dig0Parser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.pcRange('0','9')
    
    def match(self,s):
        return self.parser.match(s)
################################################
##************######_____ I  N T E G E R _________###############
################################################
class IntegerParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(HexaNumberParser())\
                        .parser(NegNatParser())\
                        .parser(PosNumber())\
                        .disjs(3)\
                        .done()

    def match(self,s):
        return self.parser.match(s)  
######################################################



class HexaInitParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='0')\
                        .const(lambda m: m=='x')\
                        .caten()\
                        .const(lambda m: m=='0')\
                        .const(lambda m: m=='X')\
                        .caten()\
                        .const(lambda m: m=='0')\
                        .const(lambda m: m=='h')\
                        .caten()\
                        .const(lambda m: m=='0')\
                        .const(lambda m: m=='H')\
                        .caten()\
                        .disjs(4)\
                        .done()

    def match(self,s):
        return self.parser.match(s) 
######################################################
class HexaCharsParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcRange('a','z'))\
                        .parser(pc.pcRange('A','Z'))\
                        .parser(Dig0Parser())\
                        .disjs(3)\
                        .star()\
                        .done()               

    def match(self,s):
        return self.parser.match(s) 
######################################################
class HexaParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(HexaInitParser())\
                        .parser(HexaCharsParser())\
                        .caten()\
                        .pack(lambda m: sexprs.Integer('no',16,"".join(m[1])))\
                        .done()

    def match(self,s):
        return self.parser.match(s)    

######################################################
class PosSignHexaNumberParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='+')\
                        .parser(HexaInitParser())\
                        .parser(HexaCharsParser())\
                        .catens(3)\
                        .pack(lambda m: sexprs.Integer(m[0],16,"".join(m[2])))\
                        .done()

    def match(self,s):
        return self.parser.match(s)
    ######################################################
class NegSignHexaNumberParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='-')\
                        .parser(HexaInitParser())\
                        .parser(HexaCharsParser())\
                        .catens(3)\
                        .pack(lambda m: sexprs.Integer(m[0],16,"".join(m[2])))\
                        .done()
    def match(self,s):
        return self.parser.match(s)
######################################################
class HexaNumberParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(PosSignHexaNumberParser())\
                        .parser(NegSignHexaNumberParser())\
                        .parser(HexaParser())\
                        .disjs(3)\
                        .done()

    def match(self,s):
        return self.parser.match(s)  
        
class ZeroHexaNumberParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(HexaInitParser())\
                        .const(lambda m: m=='0')\
                        .plus()\
                        .caten()\
                        .done()

    def match(self,s):
        return self.parser.match(s)  
######################################################
class FractionsParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(IntegerParser())\
                        .const(lambda m: m=='/')\
                        .parser(PosNotZeroNumber())\
                        .parser(NegNotZeroNatParser())\
                        .parser(HexaNumberParser())\
                        .parser(ZeroHexaNumberParser())\
                        .butNot()\
                        .disjs(3)\
                        .catens(3)\
                        .pack(lambda m: sexprs.Fraction(m[0],m[2]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)     

######################################################    .parser(const(lambda ch: ord(ch)==92))\

class LineCommentParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m==';')\
                        .const(lambda ch: ch!='\n' and ch!='\r')\
                        .star()\
                        .caten()\
                        .pack(lambda m: m[0]+"".join(m[1]))  \
                        .done()

    def match(self,s):
        return self.parser.match(s)  
######################################################   

class SexprCommentParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcWord('#;'))\
                        .delayed_parser(lambda: SexprParser())\
                        .caten()\
                        .done()

    def match(self,s):
        return self.parser.match(s)          

######################################################   

class Pskip(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(SexprCommentParser())\
                        .const(lambda ch: ch <= ' ')\
                        .parser(LineCommentParser())\
                        .disjs(3)\
                        .star()\
                        .pack(lambda m: '')\
                        .done()

    def match(self,s):
        return self.parser.match(s)  
######################################################   

class TrueParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda k: k=='#')\
                        .parser(pc.pcCharCI('t'))\
                        .caten()\
                        .done()
        self.pack= pc.pack(self.parser,lambda m: sexprs.Boolean(m[0]+"".join(m[1]).lower()))

    def match(self,s):
        return self.pack.match(s)     
##########################################################
class FalseParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda k: k=='#')\
                        .parser(pc.pcCharCI('f'))\
                        .caten()\
                        .done()
        self.pack= pc.pack(self.parser,lambda m: sexprs.Boolean(m[0]+"".join(m[1]).lower()))

    def match(self,s):
        return self.pack.match(s)     
##########################################################
class BoolanParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(FalseParser())\
                        .parser(TrueParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s)     

##########################################################
class NumberParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(FractionsParser())\
                        .parser(IntegerParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s)    
    
##########################################################
class SymbolParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcRange('a','z'))\
                        .parser(pc.pcRange('A','Z'))\
                        .parser(Dig0Parser())\
                        .const(lambda ch: ch=='#')\
                        .const(lambda ch: ch=='!')\
                        .const(lambda ch: ch=='$')\
                        .const(lambda ch: ch=='^')\
                        .const(lambda ch: ch=='*')\
                        .const(lambda ch: ch=='-')\
                        .const(lambda ch: ch=='_')\
                        .const(lambda ch: ch=='=')\
                        .const(lambda ch: ch=='+')\
                        .const(lambda ch: ch=='<')\
                        .const(lambda ch: ch=='>')\
                        .const(lambda ch: ch=='/')\
                        .const(lambda ch: ch=='?')\
                        .disjs(16)\
                        .plus()\
                        .pack(lambda m: sexprs.Symbol("".join(m)))\
                        .done()
######################################_____ S T O R E ____ I N   BIG    LETTERS ####################333
    def match(self,s):
        return self.parser.match(s)     
    
################################################
class NamedCharParsers(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='#')\
                        .const(lambda m: ord(m)==92)\
                        .caten()\
                        .parser(pc.pcWordCI('newline'))\
                        .pack(lambda m: chr(10))\
                        .parser(pc.pcWordCI('return'))\
                        .pack(lambda m: chr(13))\
                        .parser(pc.pcWordCI('tab'))\
                        .pack(lambda m: chr(9))\
                        .parser(pc.pcWordCI('page'))\
                        .pack(lambda m: chr(12))\
                        .parser(pc.pcWordCI('lambda'))\
                        .pack(lambda m: chr(0x03bb))\
                        .disjs(5)\
                        .caten()\
                        .pack(lambda ch: sexprs.Char('named',"".join(ch[1])))\
                        .done()


    def match(self,s):
        return self.parser.match(s)       
################################################
####################___STRING___#####################
class QuotedStringParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: ord(m)==34)\
                        .parser(MetaCharsStringParser())\
                        .const(lambda ch: ord(ch)!=34)\
                        .disj()\
                        .star()\
                        .const(lambda m: ord(m)==34)\
                        .catens(3)\
                       .pack(lambda m: sexprs.String('quoted',"".join(m[1])))\
                        .done()

    def match(self,s):
        return self.parser.match(s)       
        
#####################################################                        .pack(lambda m: sexprs.String("".join(m[1])))\

################################################
class MetaCharsStringParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: ord(m)==92)\
                        .parser(pc.pcChar('n'))\
                        .pack(lambda m: chr(10))\
                        .parser(pc.pcChar('f'))\
                        .pack(lambda m: chr(12))\
                        .parser(pc.pcChar('r'))\
                        .pack(lambda m: chr(13))\
                        .parser(pc.pcChar('t'))\
                        .pack(lambda m: chr(9))\
                        .const(lambda m: ord(m)==92)\
                        .pack(lambda m: chr(93))\
                        .parser(pc.pcChar('"'))\
                        .pack(lambda m: chr(34))\
                        .parser(pc.pcChar('l'))\
                        .pack(lambda m: chr(0x03bb))\
                        .disjs(7)\
                        .caten()\
                        .pack(lambda m: "".join(m[1]))\
                        .done()
                        
    def match(self,s):
        return self.parser.match(s)       
        
###################################################################
class StringParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(QuotedStringParser())\
                        .parser(MetaCharsStringParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s)   


################################################################3

class HexBytesParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcRange('a', 'z'))\
                        .parser(pc.pcRange('A', 'Z'))\
                        .parser(pc.pcRange('0', '9'))\
                        .disjs(3)\
                        .done()

    def match(self,s):
        return self.parser.match(s)   

################################################################3

class TwoBytesParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(HexBytesParser())\
                        .parser(HexBytesParser())\
                        .parser(HexBytesParser())\
                        .parser(HexBytesParser())\
                        .catens(4)\
                        .pack(lambda m: "".join(m))\
                        .done()

    def match(self,s):
        return self.parser.match(s)   
                                              
################################################################3

class OneBytesParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(HexBytesParser())\
                        .parser(HexBytesParser())\
                        .caten()\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
                       
################################################################3
class CharHexParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='#')\
                        .const(lambda m: ord(m)==92)\
                        .const(lambda m: m=='x')\
                        .catens(3)\
                        .parser(TwoBytesParser())\
                        .parser(OneBytesParser())\
                        .disj()\
                        .caten()\
                        .pack(lambda m: sexprs.Char('hexadecimal',chr(int("".join(m[1]),16))))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      

##########################################################
class CharParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(CharHexParser())\
                        .parser(NamedCharParsers())\
                        .parser(VisibleCharParser())\
                        .disjs(3)\
                        .done()

    def match(self,s):
        return self.parser.match(s)      

##########################################################
################################################################3

class VisibleCharParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='#')\
                        .const(lambda m: ord(m)==92)\
                        .const(lambda m: ord(m)>32)\
                        .catens(3)\
                        .pack(lambda m: sexprs.Char('visible',"".join(m[2])))\
                        .done()

    def match(self,s):
        return self.parser.match(s)     
################################################################3

class NilParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(Pskip())\
                        .const(lambda k: k=='(')\
                        .parser(Pskip())\
                        .const(lambda k: k==')')\
                        .parser(Pskip())\
                        .catens(5)\
                        .pack(lambda m: sexprs.Nil())\
                        .done()

    def match(self,s):
        return self.parser.match(s)  
 ################################################################
#############################____P A I R___############################
class PairParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(ProperListParser())\
                        .parser(ImProperListParser())\
                        .disj()\
                        .done()

    def match(self,s):
        return self.parser.match(s)       
################################################################3                             
################################################################3

class ProperListParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda ch: ch=='(')\
                        .delayed_parser(lambda: SexprParser())\
                        .star()\
                        .const(lambda ch: ch==')')\
                        .catens(3)\
                        .pack(lambda m: sexprs.Pair(m[1][0], m[1][1:]))\
                        .done()
    def match(self,s):
        return self.parser.match(s)       
################################################################3


class ProperListParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda ch: ch=='(')\
                        .delayed_parser(lambda: SexprParser())\
                        .star()\
                        .const(lambda ch: ch==')')\
                        .catens(3)\
                        .pack(lambda m: sexprs.Pair(m[1][0], m[1][1:]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)       
################################################################3

class ImProperListParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda ch: ch=='(')\
                        .delayed_parser(lambda: SexprParser())\
                        .plus()\
                        .const(lambda ch: ch=='.')\
                        .delayed_parser(lambda: SexprParser())\
                        .const(lambda ch: ch==')')\
                        .catens(5)\
                        .pack(lambda m: sexprs.Pair(m[1][0],(m[1][1:]),impro=m[3]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)     
################################################################3

class VectorParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcWord('#('))\
                        .parser(SexprParser())\
                        .star()\
                        .const(lambda ch: ch==')')\
                        .catens(3)\
                        .pack(lambda m: sexprs.Vector(m[1]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################

class QuotedParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='\'')\
                        .delayed_parser(lambda: SexprParser())\
                        .caten()\
                        .pack(lambda m: sexprs.Pair(sexprs.Symbol('quote'),m[1:]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################        
################################################################

class QQuotedParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m=='`')\
                        .delayed_parser(lambda: SexprParser())\
                        .caten()\
                        .pack(lambda m: sexprs.Pair(sexprs.Symbol('quasiquote'),[m[1]]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################   
################################################################

class UnquotedSplicedParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(pc.pcWord(',@'))\
                        .delayed_parser(lambda: SexprParser())\
                        .caten()\
                        .pack(lambda m: sexprs.Pair(sexprs.Symbol('unquote-splicing'),m[1:]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################        
################################################################

class UnQuotedParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .const(lambda m: m==',')\
                        .delayed_parser(lambda: SexprParser())\
                        .caten()\
                        .pack(lambda m: sexprs.Pair(sexprs.Symbol('unquote'),m[1:]))\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################             
################################################################

class QuotelikeParser(pc.AbstractParsingCombinator):
    def __init__(self):
        self.parser= pc.ParserStack()\
                        .parser(QuotedParser())\
                        .parser(QQuotedParser())\
                        .parser(UnquotedSplicedParser())\
                        .parser(UnQuotedParser())\
                        .disjs(4)\
                        .done()

    def match(self,s):
        return self.parser.match(s)      
################################################################      
