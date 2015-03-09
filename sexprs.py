
import reader 

class AbstractSexpr(object):
    def __init__(self):
      pass

    @staticmethod
    def readFromString(s):
      return reader.SexprParser().match(s)

#################################
class Void(AbstractSexpr):
    def __init__(self):
        pass

    def __str__(self):
       return str('(Void)') 

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitVoid() 
#################################    
class Nil(AbstractSexpr) :
    def __init__(self):
        pass
    def __str__(self):
       return "()" 

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitNil() 
#################################

class Boolean(AbstractSexpr) :
    def __init__(self,value):
        self.value=value

    def __str__(self):
       return str(self.value)   

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitBoolean()        
#################################
class Char(AbstractSexpr) :
    def __init__(self,typed,char):
        self.char=char
        self.typed=typed
        if typed=='named':
                 self.string=self.toString(self.char)
        else:
                self.string=self.char       


    def toString(self,char):
         if ord(self.char)==10:
                 return 'newline'
         elif ord(self.char)==13:
                 return 'return'
         elif ord(self.char)==9:
                  return 'tab'
         elif ord(self.char)==12:
                  return 'page'
         else:
                 return 'lambda' 

    def __str__(self):
         return "#\\"+str(self.string)

    def accept (self,visitor):
         self.visitor=visitor
         return visitor.visitChar()

#################################
class AbstractNumber(AbstractSexpr):
    pass
#################################
class Integer(AbstractNumber):
    def __init__(self,sign,base,unvalued):
        if base==10:
            self.valued=int(unvalued)  
        else:
            self.valued= int(unvalued, 16)      
        self.sign=sign
        if self.sign=='-':
            self.valued=-self.valued
        self.base=base
    def __str__(self):    
        return str(self.valued)
    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitInteger() 
#################################
class Fraction(AbstractNumber):
    def __init__(self,numerator,denominator):
        self.numerator=numerator
        self.denominator=denominator
        self.value=self.numerator.valued/self.denominator.valued

    def __str__(self):
       return str(self.numerator)+'/'+str(self.denominator)

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitFraction() 
#################################
class String(AbstractSexpr):
    def __init__(self,typed,string):
        self.string=string
        self.typed=typed
        if typed=='quoted':
            self.string="\""+self.string+"\""

    def __str__(self):
       return str(self.string)   

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitString() 
#################################
class Symbol(AbstractSexpr):
    def __init__(self,Symbol):
        self.name=Symbol.upper()

    def __str__(self):
       return str(self.name)   

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitSymbol() 
#################################
class Pair(AbstractSexpr):
    def __init__(self,car,cdr,impro=False):
        self.jump=0
        self.car=car
        self.cdr=cdr
        self.impro=impro
        self.point = 0

        '''def list2pairs(s, a):
    if s:
        return sexprs.Pair(s[0], list2pairs(s[1:], a))
    else:
        return a
        '''
        if self.impro==False or self.impro.accept(v)=='Nil':
                 self.cdr= self.foo(cdr,Nil())  
        else:
                self.cdr= self.foo(cdr,self.impro)
                if self.cdr ==self.impro:
                        self.point +=1

    def getType(self):
        return self.impro

    def foo(self,s,a):
        if  s and str(s)!='()':
            return Pair(s[0], s[1:],a)
        else:
            return a

    def getcar(self):
                return self.car        

    def __str__(self):
        return '(' + str(self.car) + ' . ' + str(self.cdr) + ')'

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitPair()
#############################################         
class Vector(AbstractSexpr):
    def __init__(self,vector):
        self.vector=vector

    def __str__(self):
            s="#("
            for obj in self.vector:
                s+= " "+str(obj)
            s+=")"
            return s

    def accept (self,visitor):
        self.visitor=visitor
        return visitor.visitVector()             
#############################################         
class ClassVisitor(AbstractSexpr):
    def __init__(self):
        pass

    def visitVoid(self):
             return 'Void'     
    def visitChar(self):
             return 'Char'     
    def visitString(self):
             return 'String'       
    def visitInteger(self):
             return 'Integer'     
    def visitFraction(self):
             return 'Fraction'     
    def visitVector(self):
             return 'Vector'     
    def visitNil(self):
             return 'Nil'     
    def visitBoolean(self):
             return 'Boolean'     
    def visitSymbol(self):
             return 'Symbol'     
    def visitPair(self):
             return 'Pair'     
#############################################      

#############################################         
v=ClassVisitor()
#############################################      
