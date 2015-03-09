from sexprs import*

#******** Label generator ****
class labelGen:

  def __init__(self):
    self.num = 1000

  def getNextNum(self):
    self.num += 1
    return self.getNum()

  def getNum(self):
    return str(self.num)

 #global stuff   
class Data(object):

  def __init__(self):
    self.initData()

  def initData(self):
    self.n = 0
    self.free_in_mem=7
    self.used_run_time = []
    self.first_bucket = -1
    self.last_bucket=-1
    self.freeVars= []
    self.expressionsToGenerate = []
    self.constant_table = {'Void' : [1,"T_VOID"] , "()": [2,"T_NIL"], "#f": [3,"T_BOOL",0], "#t": [5,"T_BOOL",1] }
    self.symbol_table = {}     #STR(SYMBOL)->ADRESS OF BUCKET
    self.symbol_to_string = {}   #STR(SYMBOL)-> ADRESS OF SOB_STRING IN CONSTANT TABLE
    self.string_to_symbol_in_constant_table = {}   #STR(SYMBOL)->ADRESS OF SOB_SYMBOL IN CONSTANT TABLE 
    

label= labelGen() # label number genarator
data = Data()
#********************************************************************************************************************
#                 ABSTRACT_SCHEME_EXPR - an abstract base class for scheme expresseinos
#********************************************************************************************************************

class AbstractSchemeExpr(object):
    @staticmethod
    def parse(string):
        (m,r)= AbstractSexpr.readFromString(string)
        #print (m)
        return (tag(m).semantic_analysis().update_n_rank([],[],0,0).Constant_And_Symbols_Handler(),r)

    @staticmethod
    def generateCode():
      code = ""
      for exp in data.expressionsToGenerate:
        code += exp.code_gen()
        labelNum= label.getNextNum() 
        code += "CMP (R0,IMM(1));\n"
        code += "JUMP_EQ (DONT_WRITE_VOID_"+labelNum+");\n"
        code += "PUSH(R0);\n"
        code += "CALL(WRITE_SOB);\n"
        code += "DROP(1);\n"
        code += "CALL(NEWLINE);\n"
        code += "DONT_WRITE_VOID_"+labelNum+":\n"
      data.initData()
      return code


    def constants_initializaion(constant_table,start_free_in_mem,free_in_mem):
        #print (constant_table)
        string =""
        symbol_to_string = data.symbol_to_string
        

        for con in range(start_free_in_mem,free_in_mem):
                    for p in  constant_table:
                                if (constant_table[p][0])==con:
                                        t_type = constant_table[p][1] 
                                        if t_type=="T_VECTOR":
                                                num_Of_elements=constant_table[str(p)][2]
                                                elements=constant_table[str(p)][3]
                                                for i in range(0,num_Of_elements):
                                                         string += "PUSH (IMM("+str(constant_table[str(p)][3][i])+"));\n"

                                                string +="PUSH (IMM("+str(num_Of_elements)+"));\n"
                                                string +=  "CALL(MAKE_SOB_VECTOR);\n"  
                                                string += "DROP ("+str(num_Of_elements+1)+");\n" 
                                                #free_in_mem += 2+num_Of_elements

                                        elif t_type=="T_CHAR":
                                                string +="PUSH (IMM("+str(ord(constant_table[p][2]))+"));\n"
                                                string +=  "CALL(MAKE_SOB_CHAR);\n"   
                                                string += "DROP (1);\n"
                                                #free_in_mem += 2

                                        elif t_type=="T_INT":
                                                string +="PUSH (IMM("+str(constant_table[p][2])+"));\n"
                                                string +=  "CALL(MAKE_SOB_INTEGER);\n"   
                                                string += "DROP (1);\n"
                                                #free_in_mem += 2

                                        elif t_type=="T_FRAC":
                                                string +="PUSH (IMM("+str(constant_table[p][3])+"));\n"
                                                string +="PUSH (IMM("+str(constant_table[p][2])+"));\n"
                                                string +=  "CALL(MAKE_SOB_FRAC);\n"   
                                                string += "DROP (2);\n"
                                                #free_in_mem += 2


                                        elif t_type=="T_STRING":
                                                #print (free_in_mem)
                                                #print ("string updatse")
                                                num_Of_chars= constant_table[p][2]  
                                                chars = constant_table[p][3]
                                                for i in range(0,num_Of_chars):                 
                                                         string += "PUSH (IMM("+str(constant_table[p][3][i])+"));\n"

                                                string +="PUSH (IMM("+str(num_Of_chars)+"));\n"
                                                string +=  "CALL(MAKE_SOB_STRING);\n"  
                                                string += "DROP ("+str(num_Of_chars+1)+");\n" 

                                                symbol_to_string.update( {str(constant_table[p][4]) : constant_table[p][0]})     


                                        elif t_type=="T_PAIR":
                                               string +="PUSH (IMM("+str(constant_table[p][3])+"));\n"  
                                               string +="PUSH (IMM("+str(constant_table[p][2])+"));\n"
                                               string +=  "CALL(MAKE_SOB_PAIR);\n"  
                                               string += "DROP (2);\n"


                                        elif t_type=="T_SYMBOL":
                                                string +="PUSH (IMM("+str(constant_table[p][2])+"));\n"
                                                string +=  "CALL(MAKE_SOB_SYMBOL);\n"  
                                                string += "DROP (1);\n"
                                                data.string_to_symbol_in_constant_table.update( {str(p) : constant_table[p][0]} )

        data.symbol_to_string = symbol_to_string                         
        return (string)

    def Constant_And_Symbols_Handler(self):
          constants = []
          freeVars =data.freeVars
          new_free_vars=[]
          ast = self        
          AbstractSchemeExpr.getConstants(self,constants)
 
          sorted_Constants= AbstractSchemeExpr.send_constants_to_topology_Sort(constants,[])


          string_constant_initializaion =   AbstractSchemeExpr.build_constant_table(AbstractSchemeExpr.remove_duplicates(sorted_Constants))

          AbstractSchemeExpr.getFreeVars(self,new_free_vars)

          string_symbol_initialization = AbstractSchemeExpr.build_symbol_table(new_free_vars)


          string_initialization = string_constant_initializaion+string_symbol_initialization
          initialization = string_initialization

          data.expressionsToGenerate.append(self)

          final_assembly_code = initialization 



            #**************************************************************#
            #                                             RETURN                                                    #
            #**************************************************************#

          return final_assembly_code
         

    def build_symbol_table(new_free_vars):
      string = ""
      free_in_mem = data.free_in_mem
      first_bucket = data.first_bucket
      used_run_time = data.used_run_time
      last_bucket =data.last_bucket
      constant_table = data.constant_table
      symbol_table =data.symbol_table
      symbol_to_string = data.symbol_to_string

      for var in new_free_vars:
            if '$'+var in constant_table.keys():        
                     #^^^^^^^^^^^^^^^^^^ THE SYMBOL IS IN CONSTANT TABLE^^^^^^^^^^^^^^^^^^^   
                    #CREATE A BUCKET       
                    if first_bucket == -1:
                      first_bucket = free_in_mem

                    string += "PUSH (IMM(3));\n"
                    string += "CALL (MALLOC);\n"
                    string += "DROP(1);\n"

                    if last_bucket!= -1:
                                string += "MOV (R1 , IMM("+str(last_bucket)+"));\n"                      #get the pionter to last bucket
                                string += "MOV(INDD(R1,2), IMM("+str(free_in_mem)+"));\n"            #put the address of current bucket in his 3rd cell

                    last_bucket= free_in_mem                  #update the existing last bucket
                    free_in_mem +=3                                   #promote the free place adress 

                    #UPDATE THE VALUES OF THE CURRENT BUCKET
                    name_of_string = str(constant_table['$'+str(var)][4])
                    address_of_sob_string =  (symbol_to_string[(name_of_string)])
                    string += "MOV (INDD(R0,0),"+str(address_of_sob_string)+");\n"

                    string += "MOV (INDD(R0,1),IMM(777));\n"            
                    string += "MOV (INDD(R0,2), IMM(0));\n"        # until a new bucket be created, the pointer to the next bucket is empty

                    symbol_table.update ({str(var) : free_in_mem-3})

                    #FIND IN CONSTANT TABLE THE SOB_SYMBOL AND POINT IT TO THE CURRENT BUCKET 
                    symbol_in_memory = data.string_to_symbol_in_constant_table[str(var)]
                    string += "MOV (R3,IMM ("+str(symbol_in_memory)+"));\n"                                   #find the T_STMBOL in constant table
                    adress_of_bucket = symbol_table[str(var)] 
                    string += "MOV (INDD(R3,1),"+str(adress_of_bucket)+");\n"                                  # SET THE  POINTER TO THE  NEW BUCKET (INSTEAD OF 0)

                  

            else : #^^^^^^^^^^^^^^^^^^ THE SYMBOL ISNT IN CONSTANT TABLE^^^^^^^^^^^^^^^^^^^

                    #print (symbols)
                    chars = []
                    # CRETAE BUCKET
                    if first_bucket == -1:
                      first_bucket = free_in_mem

                    string += "PUSH (IMM(3));\n"
                    string += "CALL (MALLOC);\n"   
                    string += "MOV (R1,R0);\n"    
                    string += "DROP(1);\n"     

                    if last_bucket!= -1:
                                string += "MOV (R0 , IMM("+str(last_bucket)+"));\n"                      #get the pionter to last bucket
                                string += "MOV(INDD(R0,2), IMM("+str(free_in_mem)+"));\n"            #put the address of current bucket in his 3rd cell          
                    last_bucket = free_in_mem              #update the existing last bucket
                    free_in_mem +=3    
                  
                    # CREATE SOB_SYMBOL AND POINT IT TO BUCKET
                    string += "PUSH (IMM("+str(last_bucket)+"));\n"
                    string +=  "CALL(MAKE_SOB_SYMBOL);\n"   
                    string += "DROP(1);\n"

                    #UPDATE THE HASH TABLE OF SOB_SYMBOLS (NAME --> ADRESS OF BUCKET)
                    symbol_table.update ({str(var) : last_bucket})

                    #UPDATED THE NEXT FREE PLACE IN MEMORY
                    free_in_mem += 2

                    #CREATE SOB_STRING
                    for i in range(0,len(str(var))):
                                    chars.append(ord(str(var)[i]))
                                    string += "PUSH (IMM("+str(chars[i])+"));\n"            #PUSH CHARS

                    string +="PUSH (IMM("+str(len(str(var)))+"));\n"              #PUSH LENGTH
                    string +=  "CALL(MAKE_SOB_STRING);\n"           
                    string +="DROP("+str(len(str(var))+1)+");\n"

                    #UPDATE THE ADRESS OF SOB_STRING IN THE DICTIONARY
                    symbol_to_string.update( {str(var) : free_in_mem})        

                    free_in_mem += (len(str(var))+2)            

                    #UPDATE VALUES OF THE LAST BUCKET
                    string += "MOV (INDD(R1,0),R0);\n"
                    string += "MOV (INDD(R1,1) ,IMM(777));\n"    # CHECK IN SYMBOL_TABLE TO GET AN ADRESS OF BUCKET
                    string += "MOV (INDD(R1,2), IMM(0));\n"        # until a new bucket be created, the pointer to the next bucket is empty

        ########################################################################         
        # ADDING run-time functions to freeVars or symbols in constant table (update the vakue field of the bucket)#
        ########################################################################


      if "PAIR?" in symbol_table.keys() and "PAIR?" not in used_run_time:
                bucket_of_pair = symbol_table['PAIR?']
                used_run_time.append("PAIR?")
                string += AbstractSchemeExpr.run_time_is_pair(bucket_of_pair)
                free_in_mem +=3
      elif  "PAIR?" in constant_table.keys() and "PAIR?" not in used_run_time:
                used_run_time.append("PAIR?")
                bucket_of_pair = constant_table['PAIR?'][0]
                string += AbstractSchemeExpr.run_time_is_pair(bucket_of_pair)
                free_in_mem +=3

      if "INTEGER?" in symbol_table.keys() and "INTEGER?" not in used_run_time:
                used_run_time.append("INTEGER?")
                bucket_of_integer = symbol_table['INTEGER?']
                string += AbstractSchemeExpr.run_time_is_integer(bucket_of_integer)
                free_in_mem +=3
      elif  "INTEGER?" in constant_table.keys() and "INTEGER?" not in used_run_time:
                used_run_time.append("INTEGER?")
                bucket_of_integer = constant_table['INTEGER?'][0]
                string += AbstractSchemeExpr.run_time_is_integer(bucket_of_integer)
                free_in_mem +=3

      if "NUMBER?" in symbol_table.keys() and "NUMBER?" not in used_run_time:
                used_run_time.append("NUMBER?")
                bucket_of_number = symbol_table['NUMBER?']
                string += AbstractSchemeExpr.run_time_is_number(bucket_of_number)
                free_in_mem +=3
      elif  "NUMBER?" in constant_table.keys() and "NUMBER?" not in used_run_time:
                used_run_time.append("NUMBER?")
                bucket_of_number = constant_table['NUMBER?'][0]
                string += AbstractSchemeExpr.run_time_is_number(bucket_of_number)
                free_in_mem +=3

      if "ZERO?" in symbol_table.keys() and "ZERO?" not in used_run_time:
                used_run_time.append("ZERO?")
                bucket_of_zero = symbol_table['ZERO?']
                string += AbstractSchemeExpr.run_time_is_zero(bucket_of_zero)
                free_in_mem +=3
      elif  "ZERO?" in constant_table.keys() and "ZERO?" not in used_run_time:
                used_run_time.append("ZERO?")
                bucket_of_zero = constant_table['ZERO?'][0]
                string += AbstractSchemeExpr.run_time_is_zero(bucket_of_zero)
                free_in_mem +=3

      if "NULL?" in symbol_table.keys() and "NULL?" not in used_run_time:
                used_run_time.append("NULL?")
                bucket_of_null = symbol_table['NULL?']
                string += AbstractSchemeExpr.run_time_is_null(bucket_of_null)
                free_in_mem +=3
      elif  "NULL?" in constant_table.keys() and "NULL?" not in used_run_time:
                used_run_time.append("NULL?")
                bucket_of_null = constant_table['NULL?'][0]
                string += AbstractSchemeExpr.run_time_is_null(bucket_of_null)  
                free_in_mem +=3

      if "CDR" in symbol_table.keys() and "CDR" not in used_run_time:
                used_run_time.append("CDR")
                bucket_of_cdr = symbol_table['CDR']
                string += AbstractSchemeExpr.run_time_cdr(bucket_of_cdr)
                free_in_mem +=3
      elif  "CDR" in constant_table.keys() and "CDR" not in used_run_time: 
                used_run_time.append("CDR")
                bucket_of_cdr = constant_table['CDR'][0]
                string += AbstractSchemeExpr.run_time_cdr(bucket_of_cdr)
                free_in_mem +=3

      if "CAR" in symbol_table.keys() and "CAR" not in used_run_time:
                used_run_time.append("CAR")
                bucket_of_car = symbol_table['CAR']
                string += AbstractSchemeExpr.run_time_car(bucket_of_car)
                free_in_mem +=3
      elif  "CAR" in constant_table.keys() and "CAR" not in used_run_time:
                used_run_time.append("CAR")
                bucket_of_car = constant_table['CAR'][0]
                string += AbstractSchemeExpr.run_time_car(bucket_of_car)  
                free_in_mem +=3

      if "STRING?" in symbol_table.keys() and "STRING?" not in used_run_time:
                used_run_time.append("STRING?")
                bucket_of_string = symbol_table['STRING?']
                string += AbstractSchemeExpr.run_time_is_string(bucket_of_string)
                free_in_mem +=3
      elif  "STRING?" in constant_table.keys() and "STRING?" not in used_run_time:
                used_run_time.append("STRING?")
                bucket_of_string = constant_table['STRING?'][0]
                string += AbstractSchemeExpr.run_time_is_string(bucket_of_string)
                free_in_mem +=3

      if "PROCEDURE?" in symbol_table.keys() and "PROCEDURE?" not in used_run_time:
                used_run_time.append("PROCEDURE?")
                bucket_of_procedure = symbol_table['PROCEDURE?']
                string += AbstractSchemeExpr.run_time_is_procedure(bucket_of_procedure)
                free_in_mem +=3
      elif  "PROCEDURE?" in constant_table.keys() and "PROCEDURE?" not in used_run_time:
                used_run_time.append("PROCEDURE?")
                bucket_of_procedure = constant_table['PROCEDURE?'][0]
                string += AbstractSchemeExpr.run_time_is_procedure(bucket_of_procedure)  
                free_in_mem +=3

      if "SYMBOL?" in symbol_table.keys() and "SYMBOL?" not in used_run_time:
                used_run_time.append("SYMBOL?")
                bucket_of_symbol = symbol_table['SYMBOL?']
                string += AbstractSchemeExpr.run_time_is_symbol(bucket_of_symbol)
                free_in_mem +=3
      elif  "SYMBOL?" in constant_table.keys() and "SYMBOL?" not in used_run_time:
                used_run_time.append("SYMBOL?")
                bucket_of_symbol = constant_table['SYMBOL?'][0]
                string += AbstractSchemeExpr.run_time_is_symbol(bucket_of_symbol)  
                free_in_mem +=3

      if "STRING-LENGTH" in symbol_table.keys() and "STRING-LENGTH" not in used_run_time:
                used_run_time.append("STRING-LENGTH")
                bucket_of_stringLength = symbol_table['STRING-LENGTH']
                string += AbstractSchemeExpr.run_time_string_length(bucket_of_stringLength)
                free_in_mem +=3
      elif  "STRING-LENGTH" in constant_table.keys() and "STRING-LENGTH" not in used_run_time:
                used_run_time.append("STRING-LENGTH")
                bucket_of_stringLength = constant_table['STRING-LENGTH'][0]
                string += AbstractSchemeExpr.run_time_string_length(bucket_of_stringLength)  
                free_in_mem +=3

      if "VECTOR?" in symbol_table.keys() and "VECTOR?" not in used_run_time:
                used_run_time.append("VECTOR?")
                bucket_of_vector = symbol_table['VECTOR?']
                string += AbstractSchemeExpr.run_time_is_vector(bucket_of_vector)
                free_in_mem +=3
      elif  "VECTOR?" in constant_table.keys() and "VECTOR?" not in used_run_time:
                used_run_time.append("VECTOR?")
                bucket_of_vector = constant_table['VECTOR?'][0]
                string += AbstractSchemeExpr.run_time_is_vector(bucket_of_vector)  
                free_in_mem +=3

      if "VECTOR-LENGTH" in symbol_table.keys() and "VECTOR-LENGTH" not in used_run_time:
                used_run_time.append("VECTOR-LENGTH")
                bucket_of_vectorLength = symbol_table['VECTOR-LENGTH']
                string += AbstractSchemeExpr.run_time_vector_length(bucket_of_vectorLength)
                free_in_mem +=3
      elif  "VECTOR-LENGTH" in constant_table.keys() and "VECTOR-LENGTH" not in used_run_time:
                used_run_time.append("VECTOR-LENGTH")
                bucket_of_vectorLength = constant_table['VECTOR-LENGTH'][0]
                string += AbstractSchemeExpr.run_time_vector_length(bucket_of_vectorLength)  
                free_in_mem +=3

      if "STRING-REF" in symbol_table.keys() and "STRING-REF" not in used_run_time:
                used_run_time.append("STRING-REF")
                bucket_of_string_ref = symbol_table['STRING-REF']
                string += AbstractSchemeExpr.run_time_string_ref(bucket_of_string_ref)
                free_in_mem +=3
      elif  "STRING-REF" in constant_table.keys() and "STRING-REF" not in used_run_time:
                used_run_time.append("STRING-REF")
                bucket_of_string_ref = constant_table['STRING-REF'][0]
                string += AbstractSchemeExpr.run_time_string_ref(bucket_of_string_ref)      
                free_in_mem +=3

      if "INTEGER->CHAR" in symbol_table.keys() and "INTEGER->CHAR" not in used_run_time:
                used_run_time.append("INTEGER->CHAR")
                bucket_of_integer_to_char = symbol_table['INTEGER->CHAR']
                string += AbstractSchemeExpr.run_time_integer_to_char(bucket_of_integer_to_char)
                free_in_mem +=3
      elif  "INTEGER->CHAR" in constant_table.keys() and "INTEGER->CHAR" not in used_run_time:
                used_run_time.append("INTEGER->CHAR")
                bucket_of_integer_to_char = constant_table['INTEGER->CHAR'][0]
                string += AbstractSchemeExpr.run_time_integer_to_char(bucket_of_integer_to_char)      
                free_in_mem +=3        

                #TO ADD FROM HERE

      if "CONS" in symbol_table.keys() and "CONS" not in used_run_time:
                used_run_time.append("CONS")
                bucket_of_cons = symbol_table['CONS']
                string += AbstractSchemeExpr.run_time_cons(bucket_of_cons)
                free_in_mem +=3
      elif  "CONS" in constant_table.keys() and "CONS" not in used_run_time:
                used_run_time.append("CONS")
                bucket_of_cons = constant_table['CONS'][0]
                string += AbstractSchemeExpr.run_time_cons(bucket_of_cons)      
                free_in_mem +=3         

      if "VECTOR-REF" in symbol_table.keys() and "VECTOR-REF" not in used_run_time:
                used_run_time.append("VECTOR-REF")
                bucket_of_vector_ref = symbol_table['VECTOR-REF']
                string += AbstractSchemeExpr.run_time_vector_ref(bucket_of_vector_ref)
                free_in_mem +=3
      elif  "VECTOR-REF" in constant_table.keys() and "VECTOR-REF" not in used_run_time:
                used_run_time.append("VECTOR-REF")
                bucket_of_vector_ref = constant_table['VECTOR-REF'][0]
                string += AbstractSchemeExpr.run_time_vector_ref(bucket_of_vector_ref)      
                free_in_mem +=3                

      if "MAKE-VECTOR" in symbol_table.keys() and "MAKE-VECTOR" not in used_run_time:
                used_run_time.append("MAKE-VECTOR")
                bucket_of_make_vector = symbol_table['MAKE-VECTOR']
                string += AbstractSchemeExpr.run_time_make_vector(bucket_of_make_vector)
                free_in_mem +=3
      elif  "MAKE-VECTOR" in constant_table.keys() and "MAKE-VECTOR" not in used_run_time:
                used_run_time.append("MAKE-VECTOR")
                bucket_of_make_vector = constant_table['MAKE-VECTOR'][0]
                string += AbstractSchemeExpr.run_time_make_vector(bucket_of_make_vector)      
                free_in_mem +=3                      

      if "MAKE-STRING" in symbol_table.keys() and "MAKE-STRING" not in used_run_time:
                used_run_time.append("MAKE-STRING")
                bucket_of_make_string = symbol_table['MAKE-STRING']
                string += AbstractSchemeExpr.run_time_make_string(bucket_of_make_string)
                free_in_mem +=3
      elif  "MAKE-STRING" in constant_table.keys() and "MAKE-STRING" not in used_run_time:
                used_run_time.append("MAKE-STRING")
                bucket_of_make_string = constant_table['MAKE-STRING'][0]
                string += AbstractSchemeExpr.run_time_make_string(bucket_of_make_string)      
                free_in_mem +=3                      

      if "CHAR->INTEGER" in symbol_table.keys() and "CHAR->INTEGER" not in used_run_time:
                used_run_time.append("CHAR->INTEGER")
                bucket_of_char_to_integer = symbol_table['CHAR->INTEGER']
                string += AbstractSchemeExpr.run_time_char_to_integer(bucket_of_char_to_integer)
                free_in_mem +=3
      elif  "CHAR->INTEGER" in constant_table.keys() and "CHAR->INTEGER" not in used_run_time:
                used_run_time.append("CHAR->INTEGER")
                bucket_of_char_to_integer = constant_table['CHAR->INTEGER'][0]
                string += AbstractSchemeExpr.run_time_char_to_integer(bucket_of_char_to_integer)      
                free_in_mem +=3                        

      if "+" in symbol_table.keys() and "+" not in used_run_time:
                used_run_time.append("+")
                bucket_of_plus = symbol_table['+']
                string += AbstractSchemeExpr.run_time_plus(bucket_of_plus)
                free_in_mem +=3
      elif  "+" in constant_table.keys() and "+" not in used_run_time:
                used_run_time.append("+")
                bucket_of_plus = constant_table['+'][0]
                string += AbstractSchemeExpr.run_time_plus(bucket_of_plus)      
                free_in_mem +=3       

      if "-" in symbol_table.keys() and "-" not in used_run_time:
                used_run_time.append("")
                bucket_of_minus = symbol_table['-']
                string += AbstractSchemeExpr.run_time_minus(bucket_of_minus)
                free_in_mem +=3
      elif  "-" in constant_table.keys() and "-" not in used_run_time:
                used_run_time.append("")
                bucket_of_minus = constant_table['-'][0]
                string += AbstractSchemeExpr.run_time_minus(bucket_of_minus)      
                free_in_mem +=3                      

      if "*" in symbol_table.keys() and "*" not in used_run_time:
                used_run_time.append("*")
                bucket_of_multi = symbol_table['*']
                string += AbstractSchemeExpr.run_time_multi(bucket_of_multi)
                free_in_mem +=3
      elif  "*" in constant_table.keys() and "*" not in used_run_time:
                used_run_time.append("*")
                bucket_of_multi = constant_table['*'][0]
                string += AbstractSchemeExpr.run_time_multi(bucket_of_multi)      
                free_in_mem +=3                       

      if "/" in symbol_table.keys() and "/" not in used_run_time:
                used_run_time.append("/")
                bucket_of_devide = symbol_table['/']
                string += AbstractSchemeExpr.run_time_divide(bucket_of_devide)
                free_in_mem +=3
      elif  "/" in constant_table.keys() and "/" not in used_run_time:
                used_run_time.append("/")
                bucket_of_devide = constant_table['/'][0]
                string += AbstractSchemeExpr.run_time_divide(bucket_of_devide)      
                free_in_mem +=3                               

      if ">" in symbol_table.keys() and ">" not in used_run_time:
                used_run_time.append(">")
                bucket_of_greater_than = symbol_table['>']
                string += AbstractSchemeExpr.run_time_greater_than(bucket_of_greater_than)
                free_in_mem +=3
      elif  ">" in constant_table.keys() and ">" not in used_run_time:
                used_run_time.append(">")
                bucket_of_greater_than = constant_table['>'][0]
                string += AbstractSchemeExpr.run_time_greater_than(bucket_of_greater_than)      
                free_in_mem +=3                       

      if "<" in symbol_table.keys() and "<" not in used_run_time:
                used_run_time.append("<")
                bucket_of_less_than = symbol_table['<']
                string += AbstractSchemeExpr.run_time_less_than(bucket_of_less_than)
                free_in_mem +=3
      elif  "<" in constant_table.keys() and "<" not in used_run_time:
                used_run_time.append("<")
                bucket_of_less_than = constant_table['<'][0]
                string += AbstractSchemeExpr.run_time_less_than(bucket_of_less_than)      
                free_in_mem +=3                    

      if "=" in symbol_table.keys() and "=" not in used_run_time:
                used_run_time.append("=")
                bucket_of_equal_than = symbol_table['=']
                string += AbstractSchemeExpr.run_time_equal_than(bucket_of_equal_than)
                free_in_mem +=3
      elif  "=" in constant_table.keys() and "=" not in used_run_time:
                used_run_time.append("=")
                bucket_of_equal_than = constant_table['='][0]
                string += AbstractSchemeExpr.run_time_equal_than(bucket_of_equal_than)      
                free_in_mem +=3                        

      if "BOOLEAN?" in symbol_table.keys() and "BOOLEAN?" not in used_run_time:
                used_run_time.append("BOOLEAN?")
                bucket_of_boolean = symbol_table['BOOLEAN?']
                string += AbstractSchemeExpr.run_time_is_boolean(bucket_of_boolean)
                free_in_mem +=3
      elif  "BOOLEAN?" in constant_table.keys() and "BOOLEAN?" not in used_run_time:
                used_run_time.append("BOOLEAN?")
                bucket_of_boolean = constant_table['BOOLEAN?'][0]
                string += AbstractSchemeExpr.run_time_is_boolean(bucket_of_boolean)      
                free_in_mem +=3                        

      if "REMAINDER" in symbol_table.keys() and "REMAINDER" not in used_run_time:
                used_run_time.append("REMAINDER")
                bucket_of_reminder = symbol_table['REMAINDER']
                string += AbstractSchemeExpr.run_time_reminder(bucket_of_reminder)
                free_in_mem +=3
      elif  "REMAINDER" in constant_table.keys() and "REMAINDER" not in used_run_time:
                used_run_time.append("REMAINDER")
                bucket_of_reminder = constant_table['REMAINDER'][0]
                string += AbstractSchemeExpr.run_time_reminder(bucket_of_reminder)      
                free_in_mem +=3       


      if "CHAR?" in symbol_table.keys() and "CHAR?" not in used_run_time:
                used_run_time.append("CHAR?")
                bucket_of_char = symbol_table['CHAR?']
                string += AbstractSchemeExpr.run_time_char(bucket_of_char)
                free_in_mem +=3
      elif  "CHAR?" in constant_table.keys() and "CHAR?" not in used_run_time:
                used_run_time.append("CHAR?")
                bucket_of_char = constant_table['CHAR?'][0]
                string += AbstractSchemeExpr.run_time_char(bucket_of_char)      
                free_in_mem +=3    
    ##########                       NOT IMPLEMENTED YET !                    #########
    #################################################

      if "APPLY" in symbol_table.keys() and "APPLY" not in used_run_time:
                used_run_time.append("APPLY")
                bucket_of_apply = symbol_table['APPLY']
                string += AbstractSchemeExpr.run_time_apply(bucket_of_apply)
                free_in_mem +=3
      elif  "APPLY" in constant_table.keys() and "APPLY" not in used_run_time:
                used_run_time.append("APPLY")
                bucket_of_apply = constant_table['APPLY'][0]
                string += AbstractSchemeExpr.run_time_apply(bucket_of_apply)      
                free_in_mem +=3       

      if "STRING->SYMBOL" in symbol_table.keys() and "STRING->SYMBOL" not in used_run_time:
                used_run_time.append("STRING->SYMBOL")
                bucket_of_string_to_symbol = symbol_table['STRING->SYMBOL']
                string += AbstractSchemeExpr.run_time_string_to_symbol(bucket_of_string_to_symbol)
                free_in_mem +=3
      elif  "STRING->SYMBOL" in constant_table.keys() and "STRING->SYMBOL" not in used_run_time:
                used_run_time.append("STRING->SYMBOL")
                bucket_of_string_to_symbol = constant_table['STRING->SYMBOL'][0]
                string += AbstractSchemeExpr.run_time_string_to_symbol(bucket_of_string_to_symbol)      
                free_in_mem +=3       

      if "SYMBOL->STRING" in symbol_table.keys() and "SYMBOL->STRING" not in used_run_time:
                used_run_time.append("SYMBOL->STRING")
                bucket_of_symbol_to_string = symbol_table['SYMBOL->STRING']
                string += AbstractSchemeExpr.run_time_symbol_to_string(bucket_of_symbol_to_string)
                free_in_mem +=3
      elif  "SYMBOL->STRING" in constant_table.keys() and "SYMBOL->STRING" not in used_run_time:
                used_run_time.append("SYMBOL->STRING")
                bucket_of_symbol_to_string = constant_table['SYMBOL->STRING'][0]
                string += AbstractSchemeExpr.run_time_symbol_to_string(bucket_of_symbol_to_string)      
                free_in_mem +=3       

      if "EQ?" in symbol_table.keys() and "EQ?" not in used_run_time:
                used_run_time.append("EQ?")
                bucket_of_eq = symbol_table['EQ?']
                string += AbstractSchemeExpr.run_time_eq(bucket_of_eq)
                free_in_mem +=3
      elif  "EQ?" in constant_table.keys() and "EQ?" not in used_run_time:
                used_run_time.append("EQ?")  
                bucket_of_eq = constant_table['EQ?'][0]
                string += AbstractSchemeExpr.run_time_eq(bucket_of_eq)      
                free_in_mem +=3       

      if "MAP" in symbol_table.keys() and "MAP" not in used_run_time:
                used_run_time.append("MAP")
                bucket_of_map = symbol_table['MAP']
                string += AbstractSchemeExpr.run_time_map(bucket_of_map)
                free_in_mem +=3
      elif  "MAP" in constant_table.keys() and "MAP" not in used_run_time:
                used_run_time.append("MAP")
                bucket_of_map = constant_table['MAP'][0]
                string += AbstractSchemeExpr.run_time_map(bucket_of_map)      
                free_in_mem +=3       



      if "APPEND" in symbol_table.keys() and "APPEND" not in used_run_time:
                used_run_time.append("APPEND")
                bucket_of_append = symbol_table['APPEND']
                string += AbstractSchemeExpr.run_time_append(bucket_of_list)
                free_in_mem +=3
      elif  "APPEND" in constant_table.keys() and "APPEND" not in used_run_time:
                used_run_time.append("APPEND")
                bucket_of_append = constant_table['APPEND'][0]
                string += AbstractSchemeExpr.run_time_append(bucket_of_list)      
                free_in_mem +=3   


      data.symbol_to_string =symbol_to_string
      data.symbol_table = symbol_table
      data.constant_table = constant_table
      data.last_bucket =last_bucket
      data.used_run_time = used_run_time
      data.free_in_mem = free_in_mem 
      data.first_bucket = first_bucket
      return string

    def run_time_reminder(bucket_of_append):

                string = "MOV (R1,IMM("+str(bucket_of_append)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(APPEND_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_reminder(bucket_of_reminder):

                string = "MOV (R1,IMM("+str(bucket_of_reminder)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(REMINDER_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_is_boolean(bucket_of_boolean):

                string = "MOV (R1,IMM("+str(bucket_of_boolean)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(BOOLEAN_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_cons(bucket_of_cons):

                string = "MOV (R1,IMM("+str(bucket_of_cons)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(CONS_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_make_vector(bucket_of_make_vector):

                string = "MOV (R1,IMM("+str(bucket_of_make_vector)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(MAKE_VECTOR_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string
    def run_time_make_string(bucket_of_make_string):

                string = "MOV (R1,IMM("+str(bucket_of_make_string)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(MAKE_STRING_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_vector_ref(bucket_of_vector_ref):

                string = "MOV (R1,IMM("+str(bucket_of_vector_ref)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(VECTOR_REF_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_equal_than(bucket_of_equal_than):

                string = "MOV (R1,IMM("+str(bucket_of_equal_than)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(EQUAL_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_less_than(bucket_of_less_than):

                string = "MOV (R1,IMM("+str(bucket_of_less_than)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(LESS_THAN_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_greater_than(bucket_of_greater_than):

                string = "MOV (R1,IMM("+str(bucket_of_greater_than)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(GREATER_THAN_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_divide(bucket_of_devide):

                string = "MOV (R1,IMM("+str(bucket_of_devide)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(DIVIDE_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_multi(bucket_of_multi):

                string = "MOV (R1,IMM("+str(bucket_of_multi)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(MULTI_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_plus(bucket_of_plus):

                string = "MOV (R1,IMM("+str(bucket_of_plus)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(PLUS_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_minus(bucket_of_minus):

                string = "MOV (R1,IMM("+str(bucket_of_minus)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(MINUS_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def run_time_char_to_integer(bucket_of_char_to_integer):

                string = "MOV (R1,IMM("+str(bucket_of_char_to_integer)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(CHAR_TO_INTEGER_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


             #################################################################################   
    #PAIR?
    def run_time_is_pair(bucket_of_pair):

                string = "MOV (R1,IMM("+str(bucket_of_pair)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(PAIR_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #INTEGER
    def run_time_is_integer(bucket_of_integer):
                          
                string = "MOV (R1,IMM("+str(bucket_of_integer)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(INTEGER_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #number?
    def run_time_is_number(bucket_of_number):
                string = "MOV (R1,IMM("+str(bucket_of_number)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(NUMBER_BODY));\n"
                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    #ZERO?
    def run_time_is_zero(bucket_of_zero):
                          
                string = "MOV (R1,IMM("+str(bucket_of_zero)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(ZERO_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #NULL?
    def run_time_is_null(bucket_of_null):
                          
                string = "MOV (R1,IMM("+str(bucket_of_null)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(NULL_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #CAR
    def run_time_car(bucket_of_car):
                          
                string = "MOV (R1,IMM("+str(bucket_of_car)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(CAR_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #CDR
    def run_time_cdr(bucket_of_cdr):
                          
                string = "MOV (R1,IMM("+str(bucket_of_cdr)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(CDR_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #PROCEDURE
    def run_time_is_procedure(bucket_of_procedure):

                string = "MOV (R1,IMM("+str(bucket_of_procedure)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(PROCEDURE_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #STRING?
    def run_time_is_string(bucket_of_string):

                string = "MOV (R1,IMM("+str(bucket_of_string)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(STRING_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #SYMBOL?
    def run_time_is_symbol(bucket_of_symbol):

                string = "MOV (R1,IMM("+str(bucket_of_symbol)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(SYMBOL_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    #STRING-LENGTH
    def run_time_string_length(bucket_of_stringLength):

                string = "MOV (R1,IMM("+str(bucket_of_stringLength)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(STRING_LENGTH_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    #VECTOR
    def run_time_is_vector(bucket_of_vector):

                string = "MOV (R1,IMM("+str(bucket_of_vector)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(VECTOR_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

   #VECTOR-LENGTH
    def run_time_vector_length(bucket_of_vectorLength):

                string = "MOV (R1,IMM("+str(bucket_of_vectorLength)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(VECTOR_LENGTH_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

   #STRING-REF
    def run_time_string_ref(bucket_of_string):

                string = "MOV (R1,IMM("+str(bucket_of_string)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(STRING_REF_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


   #INTEGER->CHAR
    def run_time_integer_to_char(bucket_of_integer_to_char):

                string = "MOV (R1,IMM("+str(bucket_of_integer_to_char)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(INTEGER_TO_CHAR_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


#                        <<  NOT IMPLEMENTED YET!!!  >> 

    def run_time_apply(bucket_of_apply):

                string = "MOV (R1,IMM("+str(bucket_of_apply)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(APPLY_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_map(bucket_of_map):

                string = "MOV (R1,IMM("+str(bucket_of_map)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(MAP_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_string_to_symbol(bucket_of_string_to_symbol):
                stb="""STRING_TO_SYMBOL_BODY:
                        PUSH(FP);
                        MOV(FP,SP);
                        PUSH(R1);
                        PUSH(R2);
                        PUSH(R9);
                        PUSH(R12);
                        PUSH(R10);
                        MOV(R1,FPARG(2)); // holds the ADRESS OF "given-string"
                        """
                stb_end ="""MOV (R9,R0); // SAVE THE ADRESS OF FIRST BUCKET

                        COMPARING_STRINGS:
                        CMP (R1,R0);     //COMPARE THE GIVEN _STRING WITH THE T_STRING AT THE FISRT CELL OF THE CHECKED BUCKET
                        JUMP_LT (SEARCH_IN_CONSTANTS_TABLE);
                        JUMP_NE(CHECK_NEXT_BUCKET);

                        //CREAT A NEW SYMBOL
                        PUSH (R0);
                        CALL(MAKE_SOB_SYMBOL);
                        DROP(1);
                        JUMP(FOUND);

                        CHECK_NEXT_BUCKET:
                        MOV(R0,INDD(R0,2)); //update R0 to point the adress of the next bucket
                        JUMP(COMPARING_STRINGS);

                        SEARCH_IN_CONSTANTS_TABLE:

                        MOV(R10,INDD(R1,1));   //GET THE NUM_OF_CHARS FROM THE GIVEN T_STRING
                        ADD(R10,2);     // ELTA TO NEXT CELL AFTER T_STRING/
                        ADD(R10,R1);      //KEPP IN R1 THE OPTINAL SYMBOL
                        MOV(R0,R10);
                        CMP (R10,T_SYMBOL);
                        JUMP_EQ(FOUND);

                        //CREATE A NEW SYMBOL POINTING TO A NEW BUCKET HOLDING IN THE FIRST CELL THE GIVEN T_STRING

                        PUSH(IMM(3));
                        CALL(MALLOC);
                        DROP(1);
                        MOV(R12,R0); //KEPP THE ADRESS OF THE CREATED BUCKET
                        MOV (INDD(R12,2),IMM(0)); //UPDATED PONITER TO THE NEXT BUCKET (ZERO)
                        MOV (INDD(R12,1),IMM(777)); //UPDATE FICTIVE VALUE
                        MOV (IND(R12),R1); //UPDATE THE T_STRING OF THE BUCKET
                        PUSH(R12);
                        CALL(MAKE_SOB_SYMBOL);
                        DROP(1);

                        FOUND:
                        POP(R10);
                        POP(R12);
                        POP(R9);
                        POP(R2);
                        POP(R1);
                        POP(FP);
                        RETURN;
                        """
                symbol_file = open("RTS/stb.asm","w")
                symbol_file.write(stb)
                line = "MOV(R0,IMM("+str(data.first_bucket)+"));\n"
                symbol_file.write(line)
                symbol_file.write(stb_end)
                symbol_file.close()
                string = "MOV (R1,IMM("+str(bucket_of_string_to_symbol)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(STRING_TO_SYMBOL_BODY));\n"



                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_symbol_to_string(bucket_of_symbol_to_string):

                string = "MOV (R1,IMM("+str(bucket_of_symbol_to_string)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(SYMBOL_TO_STRING_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_eq(bucket_of_eq):

                string = "MOV (R1,IMM("+str(bucket_of_eq)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(EQ_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_list(bucket_of_list):

                string = "MOV (R1,IMM("+str(bucket_of_list)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(LIST_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string

    def run_time_char(bucket_of_char):

                string = "MOV (R1,IMM("+str(bucket_of_char)+"));\n"
                #CREATE T_CLOSURE
                string+= "PUSH(IMM(3));\n"
                string+= "CALL(MALLOC);\n"
                string+= "DROP(1);\n"
                string+= "MOV(IND(R0),T_CLOSURE);\n"
                string+= "MOV(INDD(R0,1),0);\n"                                   #fictive value for env
                string+= "MOV(INDD(R0,2),LABEL(CHAR_BODY));\n"

                # UPDATE THE BUCKET
                string  += "MOV (INDD(R1,1),R0);\n"     #update the value of the bucket (filed number 2)
                return string


    def build_constant_table(constants):
        constant_table = data.constant_table
        free_in_mem = data.free_in_mem
        start_free_in_mem = free_in_mem
        for p in constants:
              if not isinstance(p,str) and p.accept(v)=="Symbol":
                       constant_table.update( {str(p) : [free_in_mem,"T_SYMBOL", 0]} )
                       free_in_mem += 2


              elif not isinstance(p,str) and p.accept(v)=="Integer":
                       constant_table.update( {str(p) : [free_in_mem,"T_INT",p.valued] } )
                       free_in_mem += 2

              elif not isinstance(p,str) and p.accept(v)=="Fraction":
                       constant_table.update( {str(p) : [free_in_mem,"T_FRAC",p.numerator.valued , p.denominator.valued] } )
                       free_in_mem += 3

              elif not isinstance(p,str) and p.accept(v)=='Pair':
                      if str(p) not in constant_table:
                          constant_table.update( {str(p) : [free_in_mem,"T_PAIR",constant_table[str(p.car)][0],constant_table[str(p.cdr)][0] ] } )
                          free_in_mem += 3

              elif not isinstance(p,str) and p.accept(v)=="Char":
                       constant_table.update( {str(p) : [free_in_mem,"T_CHAR",p.char] } )
                       free_in_mem += 2

              elif not isinstance(p,str) and p.accept(v)=="Vector":
                      if str(p) not in constant_table:
                          elements = []

                          for i in range(0,len(p.vector)):
                                        elements.append(constant_table[str(p.vector[i])][0] )

                          constant_table.update( {str(p) : [free_in_mem,"T_VECTOR",len(p.vector),elements] } )
                          free_in_mem +=(len(p.vector)+ 2)        

              #     ALL THE STRINGS STARTS WITH A '$''   

              elif not isinstance(p,str) and  p.accept(v)=="String":
              #elif isinstance(p,str):
                      chars = []

                      for i in range(1,len(str(p))-1):
                                    chars.append(ord(str(p)[i]))

                      constant_table.update({'$'+str(p) : [free_in_mem,"T_STRING",len(str(p))-2,chars,str(p)] } )
                      free_in_mem += (len(str(p)))

              elif  isinstance(p,str):
              #elif isinstance(p,str):
                      chars = []

                      for i in range(0,len(str(p))):
                                    chars.append(ord(str(p)[i]))

                      #print (chars)                
                      constant_table.update({'$'+str(p) : [free_in_mem,"T_STRING",len(str(p)),chars,str(p)] } )
                      free_in_mem += (len(str(p))+2)        

        init = AbstractSchemeExpr.constants_initializaion(constant_table,start_free_in_mem,free_in_mem)
        data.constant_table= constant_table
        data.free_in_mem = free_in_mem
        return init
        

#************ remove duplicates and send to topology sort ***********#

    def send_constants_to_topology_Sort(Constantslist,sorted_list):
      if len(Constantslist)==0:
        return Constantslist
      if len(Constantslist)==1:
        sorted_list.extend(AbstractSchemeExpr.topology_Sort(Constantslist[0].con))
        return sorted_list
      else:  
        sorted_list.extend(AbstractSchemeExpr.topology_Sort(Constantslist[0].con))
        return AbstractSchemeExpr.send_constants_to_topology_Sort(Constantslist[1:],sorted_list)

    def remove_duplicates(constants):
      return (AbstractSchemeExpr.remove_fraction_duplicates(AbstractSchemeExpr.remove_string_duplicates(AbstractSchemeExpr.remove_char_duplicates(AbstractSchemeExpr.remove_str_duplicates(AbstractSchemeExpr.remove_symbol_duplicates(AbstractSchemeExpr.remove_integer_duplicates(constants)))))))
  
    def remove_str_duplicates(constants):
      i=0
      n=len(constants)
      while  i< n:
                if isinstance(constants[i], str): 
                        pivot = constants[i] 
                        index = i 
                        next_index=index+1 
                        end = len(constants)
                        while next_index<end :
                             if isinstance (constants[next_index],str):
                                  if str(constants[next_index])==str(pivot):
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                next_index=next_index+1                              
                i=i+1     
      return constants    

    def remove_symbol_duplicates(constants):
      i=0
      n=len(constants)
      while  i<n:
                if (not isinstance(constants[i], str)) and constants[i].accept(v)=='Symbol': 
                        pivot = constants[i] 
                        index = i
                        next_index=index+1
                        end = len(constants)
                        while next_index<end :
                             if (not isinstance (constants[next_index],str)) and constants[i].accept(v)=='Symbol': 
                                  if constants[next_index].accept(v)=='Symbol' and constants[next_index].name ==pivot.name :
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                   next_index=next_index+1          
                i=i+1     
      return constants 

    def remove_char_duplicates(constants):
      i=0
      n=len(constants)
      while  i<n:
                if (not isinstance(constants[i], str)) and constants[i].accept(v)=='Char': 
                        pivot = constants[i] 
                        index = i
                        next_index=index+1
                        end = len(constants)
                        while next_index<end :
                             if (not isinstance (constants[next_index],str)) and constants[i].accept(v)=='Char': 
                                  if constants[next_index].accept(v)=='Char' and constants[next_index].char ==pivot.char :
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                   next_index=next_index+1          
                i=i+1     
      return constants   

    def remove_string_duplicates(constants):
      i=0
      n=len(constants)
      while  i<n:
                if (not isinstance(constants[i], str)) and constants[i].accept(v)=='String': 
                        pivot = constants[i] 
                        index = i
                        next_index=index+1
                        end = len(constants)
                        while next_index<end :
                             if (not isinstance (constants[next_index],str)) and constants[i].accept(v)=='String': 
                                  if constants[next_index].accept(v)=='String' and constants[next_index].string ==pivot.string :
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                   next_index=next_index+1          
                i=i+1     
      return constants   

    def remove_integer_duplicates(constants):
      i=0
      n=len(constants)
      while  i<n:
                if (not isinstance(constants[i], str)) and constants[i].accept(v)=='Integer': 
                        pivot = constants[i] 
                        index = i
                        next_index=index+1
                        end = len(constants)
                        while next_index<end :
                             if (not isinstance (constants[next_index],str)) and constants[i].accept(v)=='Integer': 
                                  if constants[next_index].accept(v)=='Integer' and constants[next_index].valued ==pivot.valued :
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                   next_index=next_index+1          
                i=i+1     
      return constants   

    def remove_fraction_duplicates(constants):
      i=0
      n=len(constants)
      while  i<n:
                if (not isinstance(constants[i], str)) and constants[i].accept(v)=='Fraction': 
                        pivot = constants[i] 
                        index = i
                        next_index=index+1
                        end = len(constants)
                        while next_index<end :
                             if (not isinstance (constants[next_index],str)) and constants[i].accept(v)=='Fraction': 
                                  if constants[next_index].accept(v)=='Fraction' and constants[next_index].numerator.valued == pivot.numerator.valued  and constants[next_index].denominator.valued == pivot.denominator.valued:
                                     del constants[next_index]
                                     end=end-1
                                     n=n-1
                                  else:   
                                     next_index=next_index+1 
                             else:        
                                   next_index=next_index+1          
                i=i+1     
      return constants   
       
#*************** Topology sort ************#

    def topology_Sort(constant):
      
        if constant.accept(v)=='Pair':
              l = AbstractSchemeExpr.topology_Sort(constant.car)
              l.extend(AbstractSchemeExpr.topology_Sort(constant.cdr))
              l.extend([constant])
              return l
        elif constant.accept(v)=='Symbol':
              l = ([constant.name])
              l.extend([constant])
              return l
        elif constant.accept(v)=='Vector':
             if  len(constant.vector)>0:
                      l = AbstractSchemeExpr.topology_Sort(constant.vector[0])
                      for i in range (1,len(constant.vector)):
                              l.extend(AbstractSchemeExpr.topology_Sort(constant.vector[i]))                                                               #for p in constant.vector[1:])
                      l.extend([constant])

                      return l 

             else:
                      return [constant]
        else: 
             return [constant]   


    def topology_Sort2(constant):
      return str(constant)
  
#********** update lamnda rank ************#

    def update_n_rank(e,bounds,params,n,rank):
      if e.accept(g)=='Variable' :
            if inparams(e,params)!=-1 :
              return VarParam(e.con , inparams(e,params))
            elif inbounds(e,bounds)!=None: 
              return inbounds(e,bounds)
            else:   
              return VarFree(e.con)
      elif e.accept(g)=='LambdaSimple':
          return LambdaSimple(e.args,AbstractSchemeExpr.update_n_rank(e.body,[params]+bounds,e.args,len(e.args),rank+1),len(e.args),rank) 
      elif e.accept(g)=='LambdaOpt':
          return LambdaOpt(e.args,AbstractSchemeExpr.update_n_rank(e.body,[params]+bounds,e.args,len(e.args),rank+1),len(e.args),rank)
      elif e.accept(g)=='LambdaVar':
          return LambdaVar(e.args,AbstractSchemeExpr.update_n_rank(e.body,[params]+bounds,[tag(e.args)],1,rank+1),1,rank)
      elif e.accept(g)=='Applic':
          return Applic(AbstractSchemeExpr.update_n_rank(e.car,bounds,params,n,rank),[AbstractSchemeExpr.update_n_rank(p,bounds,params,n,rank) for p in e.cdr])
      elif e.accept(g)=='ApplicTP':
          return ApplicTP(AbstractSchemeExpr.update_n_rank(e.car,bounds,params,n,rank),[AbstractSchemeExpr.update_n_rank(p,bounds,params,n,rank) for p in e.cdr])
      elif e.accept(g)=='IfThenElse':
          return IfThenElse(AbstractSchemeExpr.update_n_rank(e.exp,bounds,params,n,rank),AbstractSchemeExpr.update_n_rank(e.then,bounds,params,n,rank),AbstractSchemeExpr.update_n_rank(e.elsse,bounds,params,n,rank))
      elif e.accept(g)=='Def':
          return Def(AbstractSchemeExpr.update_n_rank(e.var,bounds,params,n,rank),AbstractSchemeExpr.update_n_rank(e.exp,bounds,params,n,rank))   
      elif e.accept(g)=='Or':
          return Or([AbstractSchemeExpr.update_n_rank(p,bounds,params,n,rank) for p in e.exp]) 
      else:
        return e  

    def getFreeVars(e,newVars):

        if e.accept(g) == 'Free' :
                if e.con.name not in data.freeVars:
                    data.freeVars.append(e.con.name)
                    newVars.append(e.con.name)
        elif e.accept(g) in ['Variable', 'Param','Bound','Constant']:
                pass
        elif e.accept(g)=='Or':
                for p in e.exp:
                  AbstractSchemeExpr.getFreeVars(p,newVars)               
        elif e.accept(g)=='IfThenElse':
                AbstractSchemeExpr.getFreeVars(e.exp,newVars)
                AbstractSchemeExpr.getFreeVars(e.then,newVars)
                AbstractSchemeExpr.getFreeVars(e.elsse,newVars)
        elif e.accept(g)=='Def':
                AbstractSchemeExpr.getFreeVars(e.var,newVars)
                AbstractSchemeExpr.getFreeVars(e.exp,newVars)
        elif e.accept(g) == 'LambdaSimple':
                AbstractSchemeExpr.getFreeVars(e.body,newVars)
        elif e.accept(g) == 'LambdaOpt':
                AbstractSchemeExpr.getFreeVars(e.body,newVars)
        elif e.accept(g) == 'LambdaVar':
               AbstractSchemeExpr.getFreeVars(e.body,newVars)
        elif e.accept(g)=='Applic' or e.accept(g)=='ApplicTP':
              AbstractSchemeExpr.getFreeVars(e.car,newVars)
              for p in e.cdr:
                AbstractSchemeExpr.getFreeVars(p,newVars)  


    def getConstants(e,constants):
        if e.accept(g) == 'Constant':
              constants.append(e)
              #return (e,constants)
        elif e.accept(g) in ['Variable', 'Param','Bound','Free']:
                #return (e,constants)
                pass
        elif e.accept(g)=='Or':
                #a = [AbstractSchemeExpr.getConstants(p,constants) for p in e.exp[:-1]]
                #a.append(AbstractSchemeExpr.getConstants(e.exp[-1],constants))
                #return  (Or(a),constants)
                for exp in e.exp:
                  AbstractSchemeExpr.getConstants(exp,constants)
        elif e.accept(g)=='IfThenElse':
                AbstractSchemeExpr.getConstants(e.exp,constants)
                AbstractSchemeExpr.getConstants(e.then,constants)
                AbstractSchemeExpr.getConstants(e.elsse,constants)
                #return (IfThenElse(AbstractSchemeExpr.getConstants(e.exp,constants),AbstractSchemeExpr.getConstants(e.then,constants),AbstractSchemeExpr.getConstants(e.elsse,constants)),constants)
        elif e.accept(g)=='Def':
                #return Def(e.var,AbstractSchemeExpr.getConstants(e.exp,constants)),constants
               AbstractSchemeExpr.getConstants(e.exp,constants)

        elif e.accept(g) == 'LambdaSimple':
               #return   LambdaSimple(e.args,AbstractSchemeExpr.getConstants(e.body,constants) ,0,0),constants
               AbstractSchemeExpr.getConstants(e.body,constants)
        elif e.accept(g) == 'LambdaOpt':
               #return   LambdaOpt(e.args,AbstractSchemeExpr.getConstants(e.body,constants) ,0,0),constants
              AbstractSchemeExpr.getConstants(e.body,constants)
        elif e.accept(g) == 'LambdaVar':
              # return   LambdaVar(e.args,AbstractSchemeExpr.getConstants(e.body,constants) ,0,0),constants
             AbstractSchemeExpr.getConstants(e.body,constants)
        elif e.accept(g)=='Applic':
               #return   Applic(AbstractSchemeExpr.getConstants(e.car,constants),[AbstractSchemeExpr.getConstants(p,constants) for p in e.cdr]),constants 
                AbstractSchemeExpr.getConstants(e.car,constants)
                for p in e.cdr:
                  AbstractSchemeExpr.getConstants(p,constants)
        elif e.accept(g)=='ApplicTP':
               #return   ApplicTP(AbstractSchemeExpr.getConstants(e.car,constants),[AbstractSchemeExpr.getConstants(p,constants) for p in e.cdr]),constants     
              AbstractSchemeExpr.getConstants(e.car,constants)
              for p in e.cdr:
                  AbstractSchemeExpr.getConstants(p,constants)                                

#************  Semantic analysis functions ***************#

    def semantic_analysis(self):
        return self.debruijn()      
        #return self.debruijn().annotateTC()

    def annotateTC_helper(e,tp):
        if e.accept(g) in ['Constant' ,'Variable', 'Param','Bound','Free']:
                return e
        elif e.accept(g)=='Or':
                a = [AbstractSchemeExpr.annotateTC_helper(p,False) for p in e.exp[:-1]]
                a.append(AbstractSchemeExpr.annotateTC_helper(e.exp[-1],tp))
                return  Or(a)
        elif e.accept(g)=='IfThenElse':
                return IfThenElse(AbstractSchemeExpr.annotateTC_helper(e.exp,False),AbstractSchemeExpr.annotateTC_helper(e.then,tp),AbstractSchemeExpr.annotateTC_helper(e.elsse,tp))
        elif e.accept(g)=='Def':
                return Def(e.var,AbstractSchemeExpr.annotateTC_helper(e.exp,False))
        elif e.accept(g) == 'LambdaSimple':
               return   LambdaSimple(e.args,AbstractSchemeExpr.annotateTC_helper(e.body,True),0,0)
        elif e.accept(g) == 'LambdaOpt':
               return   LambdaOpt(e.args,AbstractSchemeExpr.annotateTC_helper(e.body,True) ,0,0)
        elif e.accept(g) == 'LambdaVar':
               return   LambdaVar(e.args,AbstractSchemeExpr.annotateTC_helper(e.body,True) ,0,0)   
        elif e.accept(g)=='Applic':
               if tp==False:
                      return   Applic(AbstractSchemeExpr.annotateTC_helper(e.car,False),[AbstractSchemeExpr.annotateTC_helper(p,False) for p in e.cdr])                                      
               else:
                      return   ApplicTP(AbstractSchemeExpr.annotateTC_helper(e.car,False),[AbstractSchemeExpr.annotateTC_helper(p,False) for p in e.cdr]) 
             
        
    def debruijn(self):
        return AbstractSchemeExpr.debruijnHelper(self,[],[])

    def annotateTC(self):
       return  AbstractSchemeExpr.annotateTC_helper(self,False)  
                                                     

    def debruijnHelper(e,bounds,params):
      if e.accept(g)=='Variable' :
            if inparams(e,params)!=-1 :
              return VarParam(e.con , inparams(e,params))
            elif inbounds(e,bounds)!=None: 
              return inbounds(e,bounds)
            else:   
              return VarFree(e.con)
      elif e.accept(g)=='LambdaSimple':
          return LambdaSimple(e.args,AbstractSchemeExpr.debruijnHelper(e.body,[params]+bounds,e.args),0,0)
      elif e.accept(g)=='LambdaOpt':
          return LambdaOpt(e.args,AbstractSchemeExpr.debruijnHelper(e.body,[params]+bounds,e.args) ,0,0)
      elif e.accept(g)=='LambdaVar':
          return LambdaVar(e.args,AbstractSchemeExpr.debruijnHelper(e.body,[params]+bounds,[tag(e.args)]) ,0,0)
      elif e.accept(g)=='Applic':
          return Applic(AbstractSchemeExpr.debruijnHelper(e.car,bounds,params),[AbstractSchemeExpr.debruijnHelper(p,bounds,params) for p in e.cdr])
      elif e.accept(g)=='IfThenElse':
          return IfThenElse(AbstractSchemeExpr.debruijnHelper(e.exp,bounds,params),AbstractSchemeExpr.debruijnHelper(e.then,bounds,params),AbstractSchemeExpr.debruijnHelper(e.elsse,bounds,params))
      elif e.accept(g)=='Def':
          return Def(AbstractSchemeExpr.debruijnHelper(e.var,bounds,params),AbstractSchemeExpr.debruijnHelper(e.exp,bounds,params))   
      elif e.accept(g)=='Or':
          return Or([AbstractSchemeExpr.debruijnHelper(p,bounds,params) for p in e.exp]) 
      else:
        return e  

      
    def codeGen(self):
      pass

def inparams(e,params):
  ret=-1
  for x in range(0,len(params)):
        if str(params[x]) == str(e):
           ret=x
           x=len(params )

  return ret               

def inbounds(e,bounds):
  for x in range(0,len(bounds)):
    for y in range(0,len(bounds[x])):
      #print (bounds[x][y])
      if bounds[x][y].accept(g)=='Variable':
        if str(bounds[x][y].con) == str(e.con):
          return VarBound(e.con,x,y)

         

#********************************************************************************************************************
#                 Classes : CONSTANT , VARIABLE (and fvar,pvar,bvar)
#********************************************************************************************************************

class Constant(AbstractSchemeExpr):
    def __init__(self,con,q=False):
        self.con=con
        self.q=q

    def __str__(self):
        if self.q == True:
            return "'"+str(self.con)
        else:
            return str(self.con)

    def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitConstant()      

    def code_gen(self):
      string = ""
      if not isinstance(self.con,str) and self.con.accept(v)=="String":
        key= "$"+str(self.con)
      else:
        key= str(self.con)
      if key in data.constant_table.keys():
        place_in_memory = data.constant_table[key][0]
        string = "MOV (R0 , IMM("+str(place_in_memory)+"));\n"
      return string

#**********************************************
class Variable(AbstractSchemeExpr):
    def __init__(self,con):
        self.con=con

    def __str__(self):
       return str(self.con)

    def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitVariable()   

    def code_gen(self):
      return ""
#********************************************
class VarFree(Variable):
  def __init__(self,con):
    super(self.__class__,self).__init__(con)

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitVarFree()    

  def code_gen(self):
    #print ("yese")
    string=""
    if (str(self.con)) in data.symbol_table.keys():
      #print ("no")
      place_in_memory = data.symbol_table[(str(self.con))]
      string = "MOV (R1 , IMM("+str(place_in_memory)+"));\n"
      string += "MOV (R0, INDD(R1,1));\n"
      string += "CMP (R0,0);\n"
      string += "JUMP_EQ(Error_UNDEFINED_VAR);\n"   #TODO: ADD that label!
    return string

#********************************************
class VarParam(Variable):
  def __init__(self,con,minor):
    super(self.__class__,self).__init__(con)
    self.minor=minor

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitVarParam()     
      
  def code_gen(self):
    index = str(2+self.minor)  # not sure about the 2. the point is to get to the A0 argument by adding it, maybe need another number
    string = "MOV(R0,FPARG("+index+"));\n"
    return string
  		   
#*******************************************
class VarBound(Variable):
  def __init__(self,con,major,minor):
    super(self.__class__,self).__init__(con)
    self.minor=minor
    self.major=major

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitVarBound()   
  
  def code_gen(self):
    string ="MOV(R0,FPARG(0));\n"
    string += "MOV(R0,INDD(R0,"
    string += str(self.major)
    string += "));\n"
    string += " MOV(R0,INDD(R0,"
    string += str(self.minor)
    string += "));\n"
    return string
#**********************************************

def makePvars(args):
    params=[]
    for i in range (0,len(args)):
        params.append(VarParam(args[i],i))
    return params
#********************************************************************************************************************
#                 Classes : AbstractLambda , LambdaSimple, LambdaOpt,LambdaVar
#********************************************************************************************************************

class AbstractLambda(AbstractSchemeExpr):
  pass
#**************************************************

class LambdaSimple(AbstractLambda): 
  def __init__(self,args,body,n,rank):

    self.args=args
    self.body=body
    self.n=n
    self.rank=rank

  def __str__(self):
      return '(lambda ('+" ".join(map(str, self.args))+') '+str(self.body)+')'

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitLambdaSimple()       
    
  def code_gen(self):

    lableNum = label.getNextNum()
    n=str(self.rank+1)
    string = "MOV(R2,IMM("+n+"));\n"
    string+= "PUSH(R2);\n"
    string+= "CALL (MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R1,R0);\n"  #pointer to new env

    string+= "CMP(R2,IMM(1));\n"
    string+= "JUMP_LE(SIMPLE_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"

    string+= "MOV(R2,FPARG(0));\n"  #pointer to old env
    string+= "MOV(R3,IMM(0));\n" #counter to old env
    string+= "MOV(R4,IMM(1));\n" #counter to new env

    string+= "SIMPLE_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,IMM("+n+"));\n"
    string+= "JUMP_GE(SIMPLE_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R1,R4),INDD(R2,R3));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(SIMPLE_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "SIMPLE_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    
    string+= "PUSH(FPARG(1));\n" #num of args
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R2,R0);\n" #pointer to arg list
    string+= "MOV(R3,IMM(0));\n" #copied args counter
    string+= "MOV(R4,IMM(2));\n" #next arg pointer
    
    string+= "SIMPLE_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,FPARG(1));\n"
    string+= "JUMP_GE(SIMPLE_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R2,R3),FPARG(R4));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(SIMPLE_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "SIMPLE_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    string+= "MOV(IND(R1),R2);\n"

    string+= "PUSH(IMM(3));\n"
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(IND(R0),T_CLOSURE);\n"
    string+= "MOV(INDD(R0,1),R1);\n"
    string+= "MOV(INDD(R0,2),LABEL(L_simple_code_"
    string+= lableNum
    string+= "));\n"
    string+= "JUMP(L_simple_exit_"
    string+= lableNum
    string+= ");\n"

    string+= "L_simple_code_"
    string+= lableNum
    string+= ":\n"
    string+= "PUSH(FP);\n"
    string+= "MOV(FP,SP);\n"

    string+= self.body.code_gen()
    string+= "POP(FP);\n"
    string+= "RETURN;\n"
    string+= "L_simple_exit_"
    string+= lableNum
    string+= ":\n"
    
    return string

    

#************************************************* 

class LambdaOpt(AbstractLambda):
  def __init__(self,args,body,n,rank):
    self.args=args
    self.body=body
    self.n=n
    self.rank=rank

  def __str__(self): 
      if self.args != []:
          return '(lambda ('+" ".join(map(str, self.args[:-1]))+" . "+str(self.args[len(self.args)-1])+') '+str(self.body)+')'
      else:
          return '(lambda () '+str(self.body)+')'       

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitLambdaOpt()

  def code_gen(self):
    lableNum = label.getNextNum()
    n=str(self.rank+1)
    string = "MOV(R2,IMM("+n+"));\n"
    string+= "PUSH(R2);\n"
    string+= "CALL (MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R1,R0);\n"  #pointer to new env

    string+= "CMP(R2,IMM(1));\n"
    string+= "JUMP_LE(OPT_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"

    string+= "MOV(R2,FPARG(0));\n"  #pointer to old env
    string+= "MOV(R3,IMM(0));\n" #counter to old env
    string+= "MOV(R4,IMM(1));\n" #counter to new env

    string+= "OPT_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,IMM("+n+"));\n"
    string+= "JUMP_GE(OPT_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R1,R4),INDD(R2,R3));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(OPT_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "OPT_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    
    string+= "PUSH(FPARG(1));\n" #num of args
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R2,R0);\n" #pointer to arg list
    string+= "MOV(R3,IMM(0));\n" #copied args counter
    string+= "MOV(R4,IMM(2));\n" #next arg pointer
    
    string+= "OPT_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,FPARG(1));\n"
    string+= "JUMP_GE(OPT_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R2,R3),FPARG(R4));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(OPT_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "OPT_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    string+= "MOV(IND(R1),R2);\n"

    string+= "PUSH(IMM(3));\n"
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(IND(R0),T_CLOSURE);\n"
    string+= "MOV(INDD(R0,1),R1);\n"
    string+= "MOV(INDD(R0,2),LABEL(L_OPT_code_"
    string+= lableNum
    string+= "));\n"

    string+= "JUMP(L_OPT_exit_"
    string+= lableNum
    string+= ");\n"

    string+= "L_OPT_code_"
    string+= lableNum
    string+= ":\n"
    string+= "PUSH(FP);\n"
    string+= "MOV(FP,SP);\n"
    string+= "PUSH(R1);\n"
    string+= "PUSH(R2);\n"
    string+= "PUSH(R3);\n"

    string+= "MOV(R2,IMM("+str(self.n)+"));\n"
    string+= "MOV(R1,FPARG(1));\n" #R1 = num of args currently on stack.
    string+= "INCR(R1);\n"
    string+= "OPT_MAGIC_LOOP_"+lableNum+":\n"
    string+= "CMP(R1,R2);\n"
    string+= "JUMP_EQ(OPT_MAGIC_LOOP_END_"+lableNum+");\n"
    string+= "INCR(R1);\n"
    string+= "PUSH(FPARG(R1));\n"
    string+= "DECR(R1);\n"
    string+= "PUSH(FPARG(R1));\n"
    string+= "CALL(MAKE_SOB_PAIR);\n"
    string+= "DROP(2);\n"
    string+= "MOV(FPARG(R1),R0);\n"
    string+= "DECR(R1);\n"
    string+= "JUMP(OPT_MAGIC_LOOP_"+lableNum+");\n"
    string+= "OPT_MAGIC_LOOP_END_"+lableNum+":\n"


    #now we copy the stack down by R2
    string+= "MOV(R3,FPARG(1));\n"
    string+= "MOV(FPARG(1),R2);\n"
    string+= "SUB(R3,FPARG(1));\n"    #R3 now is the num of cells down in the stack we need to move each arg
    string+= "MOV(R1,FP);\n"
    string+= "SUB(R1,4);\n"
    string+= "SUB(R1,R2);\n"

    string+= "OPT_COPY_STACK_DOWN_"+lableNum+":\n"
    string+= "CMP(R1,SP);\n"
    string+= "JUMP_EQ(OPT_COPY_STACK_DOWN_END_"+lableNum+");\n"
    string+= "MOV(R2,R1);\n"
    string+= "SUB(R2,R3);\n"
    string+= "MOV(STACK(R2),STACK(R1));\n"
    string+= "INCR(R1);\n"
    string+= "JUMP(OPT_COPY_STACK_DOWN_"+lableNum+");\n"

    string+= "OPT_COPY_STACK_DOWN_END_"+lableNum+":\n"
    string+= "SUB(SP,R3);\n"
    string+= "SUB(FP,R3);\n"

    string+= self.body.code_gen()
    string+= "POP(R3);\n"
    string+= "POP(R2);\n"
    string+= "POP(R1);\n"
    string+= "POP(FP);\n"
    string+= "RETURN;\n"
    string+= "L_OPT_exit_"
    string+= lableNum
    string+= ":\n"
    
    return string
#************************************************

class LambdaVar(AbstractLambda): 
  def __init__(self,args,body,n,rank):

    self.args=args
    self.body=body
    self.n=n
    self.rank=rank


  def __str__(self):
    return '(lambda '+str( self.args)+' '+str(self.body)+')'

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitLambdaVar()

  def code_gen(self):
    lableNum = label.getNextNum()
    n=str(self.rank+1)
    string = "MOV(R2,IMM("+n+"));\n"
    string+= "PUSH(R2);\n"
    string+= "CALL (MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R1,R0);\n"  #pointer to new env

    string+= "CMP(R2,IMM(1));\n"
    string+= "JUMP_LE(VAR_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"

    string+= "MOV(R2,FPARG(0));\n"  #pointer to old env
    string+= "MOV(R3,IMM(0));\n" #counter to old env
    string+= "MOV(R4,IMM(1));\n" #counter to new env

    string+= "VAR_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,IMM("+n+"));\n"
    string+= "JUMP_GE(VAR_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R1,R4),INDD(R2,R3));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(VAR_ENV_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "VAR_ENV_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    
    string+= "PUSH(FPARG(1));\n" #num of args
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(R2,R0);\n" #pointer to arg list
    string+= "MOV(R3,IMM(0));\n" #copied args counter
    string+= "MOV(R4,IMM(2));\n" #next arg pointer
    
    string+= "VAR_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ":\n"
    string+= "CMP(R3,FPARG(1));\n"
    string+= "JUMP_GE(VAR_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ");\n"
    string+= "MOV(INDD(R2,R3),FPARG(R4));\n"
    string+= "INCR(R4);\n"
    string+= "INCR(R3);\n"
    string+= "JUMP(VAR_ARG_COPY_LOOP_"
    string+= lableNum
    string+= ");\n"
    string+= "VAR_ARG_COPY_LOOP_END_"
    string+= lableNum
    string+= ":\n"
    string+= "MOV(IND(R1),R2);\n"

    string+= "PUSH(IMM(3));\n"
    string+= "CALL(MALLOC);\n"
    string+= "DROP(1);\n"
    string+= "MOV(IND(R0),T_CLOSURE);\n"
    string+= "MOV(INDD(R0,1),R1);\n"
    string+= "MOV(INDD(R0,2),LABEL(L_var_code_"
    string+= lableNum
    string+= "));\n"

    string+= "JUMP(L_var_exit_"
    string+= lableNum
    string+= ");\n"

    string+= "L_var_code_"
    string+= lableNum
    string+= ":\n"
    string+= "PUSH(FP);\n"
    string+= "MOV(FP,SP);\n"
    string+= "PUSH(R1);\n"
    string+= "PUSH(R2);\n"
    string+= "PUSH(R3);\n"

    string+= "MOV(R1,FPARG(1));\n" #R1 = num of args currently on stack.
    string+= "INCR(R1);\n"
    string+= "VAR_MAGIC_LOOP_"+lableNum+":\n"
    string+= "CMP(R1,IMM(1));\n"
    string+= "JUMP_EQ(VAR_MAGIC_LOOP_END_"+lableNum+");\n"
    string+= "INCR(R1);\n"
    string+= "PUSH(FPARG(R1));\n"
    string+= "DECR(R1);\n"
    string+= "PUSH(FPARG(R1));\n"
    string+= "CALL(MAKE_SOB_PAIR);\n"
    string+= "DROP(2);\n"
    string+= "MOV(FPARG(R1),R0);\n"
    string+= "DECR(R1);\n"
    string+= "JUMP(VAR_MAGIC_LOOP_"+lableNum+");\n"
    string+= "VAR_MAGIC_LOOP_END_"+lableNum+":\n"
    #now we copy the stack down by R2
    string+= "MOV(R3,FPARG(1));\n"
    string+= "MOV(FPARG(1),R1);\n"
    string+= "SUB(R3,FPARG(1));\n"    #R3 now is the num of cells down in the stack we need to move each arg
    string+= "MOV(R1,FP);\n"
    string+= "SUB(R1,5);\n"

    string+= "VAR_COPY_STACK_DOWN_"+lableNum+":\n"
    string+= "CMP(R1,SP);\n"
    string+= "JUMP_EQ(VAR_COPY_STACK_DOWN_END_"+lableNum+");\n"
    string+= "MOV(R2,R1);\n"
    string+= "SUB(R2,R3);\n"
    string+= "MOV(STACK(R2),STACK(R1));\n"
    string+= "INCR(R1);\n"
    string+= "JUMP(VAR_COPY_STACK_DOWN_"+lableNum+");\n"

    string+= "VAR_COPY_STACK_DOWN_END_"+lableNum+":\n"
    string+= "SUB(SP,R3);\n"
    string+= "SUB(FP,R3);\n"

    string+= self.body.code_gen()
    string+= "POP(R3);\n"
    string+= "POP(R2);\n"
    string+= "POP(R1);\n"
    string+= "POP(FP);\n"
    string+= "RETURN;\n"
    string+= "L_var_exit_"
    string+= lableNum
    string+= ":\n"
    
    return string
#********************************************************************************************************************
#                 Classes : Applic , Or , Def , IfThenElse , GenSym
#********************************************************************************************************************

class Applic(AbstractSchemeExpr):
  def __init__(self,car,cdr):
    self.car=car
    self.cdr=cdr
    self.magic= str(2)

  def __str__(self):  
    return  '('+str(self.car) +' '+" ".join(map(str, self.cdr))+')'

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitApplic()

  def code_gen_help(self,param):
    string= param.code_gen()
    string+= "PUSH(R0);\n"
    return string

  def code_gen(self):
    string = "PUSH(IMM("+self.magic+"));\n"
    string += ''.join(map(self.code_gen_help,reversed(self.cdr)))
    string+= "PUSH(IMM("+str(len(self.cdr))+"));\n"
    string+= self.car.code_gen()
    string+= "CMP(IND(R0),T_CLOSURE);\n"
    string+= "JUMP_NE(NOT_CLOSUR_ERROR);\n"  #need to create such global label. 
    string+= "PUSH(INDD(R0,1));\n"
    string+= "CALLA(INDD(R0,2));\n"
    string+= "DROP(IMM(1));\n"
    string+= "POP(R1);\n"
    string+= "DROP(R1);\n"
    string+= "DROP(1);\n"
    return string
    
#*************************************************** 
class ApplicTP(Applic):
  def __init__(self,car,cdr):
    super(self.__class__,self).__init__(car,cdr)

  def getCar( self ):
    return self.car   

  def getCdr( self ):
    return self.cdr   

  def code_gen_help(self,param):
    string= param.code_gen()
    string+= "PUSH(R0);\n"
    return string

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitApplicTP()


  def code_gen(self):

    lableNum = label.getNextNum()
    string = "PUSH(IMM("+self.magic+"));\n"
    string += ''.join(map(self.code_gen_help,reversed(self.cdr)))
    string+= "PUSH(IMM("+str(len(self.cdr))+"));\n"
    string+= self.car.code_gen()
    string+= "CMP(IND(R0),T_CLOSURE);\n"
    string+= "JUMP_NE(NOT_CLOSUR_ERROR);\n"  #need to create such global label. 
    string+= "PUSH(INDD(R0,1));\n" #push env
    string+= "PUSH(FPARG(-1));\n"  #return address of the old function (where we need to return after the jump)
    string+= "MOV(R14,FP);\n" #r14 = address on stack to copy from (src: stack[R14 to SP])
    string+= "MOV(R15,FP);\n"
    string+= "SUB(R15,IMM(5));\n"
    string+= "SUB(R15,FPARG(1));\n" #r15 = address on stack to copy to(src: stack[R15 to R15+(SP-R14)])
    string+= "MOV(FP,FPARG(-2));\n"  # move to FP the old FP (saved in fp-1)
    #begin copy loop:
    string+= "TC_APPLIC_COPY_LOOP_"+lableNum+":\n"
    string+= "CMP(R14,SP);\n"
    string+= "JUMP_EQ(TC_APPLIC_COPY_LOOP_END_"+lableNum+");\n"
    string+= "MOV(STACK(R15),STACK(R14));\n"
    string+= "INCR(R15);"
    string+= "INCR(R14);"
    string+= "JUMP(TC_APPLIC_COPY_LOOP_"+lableNum+");\n"

    string+= "TC_APPLIC_COPY_LOOP_END_"+lableNum+":\n"
    string+= "MOV(R14,SP);\n"
    string+= "SUB(R14,R15);\n"
    string+= "SUB(SP,R14);\n"
    string+= "JUMPA(INDD(R0,2));\n" 
    return string
#*****************************************************
class Or(AbstractSchemeExpr):
  def __init__(self,exp):
    self.exp=exp

  def __str__(self):
    return  '(OR ' +" ".join(map(str,self.exp))+')' 

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitOr()   

  def code_gen_help(self,exp):
    lableNum=  label.getNum()
    string = exp.code_gen()
    string+= "CMP(R0,IMM(3));\n"
    string+= "JUMP_NE(L_or_out_"
    string+= lableNum
    string+= ");\n"
    return string

  def code_gen(self):
    lableNum = label.getNextNum()
    string= ''.join(map(self.code_gen_help,self.exp))
    string+= "L_or_out_"
    string+= lableNum
    string+= ":\n"
    return string
#**************************************************
class Def(AbstractSchemeExpr):
  def __init__(self,var,exp):
    self.var=var
    self.exp=exp

  def __str__(self):
    return '(define '+str(self.var).lower()+' '+str(self.exp)+')' 

  def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitDef()     

  def code_gen(self):
      string = self.exp.code_gen()
      adress_of_bucket = data.symbol_table[str(self.var)]
      string += "MOV (R1, IMM("+str(adress_of_bucket)+"));\n"
      string += "MOV (INDD(R1,1),R0);\n"
      string += "MOV(R0, IMM(1));\n"    
      #print (WALLA)
      return string
#*************************************************
class IfThenElse(AbstractSchemeExpr):
    def __init__(self,exp,then,elsse):
        self.exp=exp
        self.then=then
        self.elsse=elsse

    def __str__(self):
       return '(if '+str(self.exp)+' '+str(self.then)+" "+str(self.elsse)+')'

    def accept (self,visitor):
      self.visitor=visitor
      return visitor.visitIfThenElse()   

    def code_gen(self):
      lableNum = label.getNextNum()
      string = self.exp.code_gen()
      string+="CMP(R0,IMM(3));\n"
      string+= "JUMP_EQ(L_else_"
      string+= lableNum
      string+= ")\n;"
      string+= self.then.code_gen()
      string+= "JUMP(L_if_end_"+str(lableNum)+");\n"
      string+= "L_else_"
      string+= lableNum
      string+= ":\n"
      string+= self.elsse.code_gen()
      string+= "L_if_end_"
      string+= lableNum
      string+= ":\n"
      return string
#******************************************************
class GenSym(object):

    @staticmethod
    def generate(): 
        data.n=data.n+1         
        return  '@'+str(data.n)   


#********************************************************************************************************************
#                The Tag Function
#********************************************************************************************************************
def tag(exp):  
      if findConstant(exp)!=None:
        return findConstant(exp)    
      elif findQuasiquoted(exp)!=None:
       return findQuasiquoted(exp)  
      elif findLetRec(exp)!=None:
       return findLetRec(exp)              
      elif findLetStar(exp)!=None:
       return findLetStar(exp)                       
      elif findLet(exp)!=None:
       return findLet(exp)              
      elif findCond(exp)!=None:
        return findCond(exp)          
      elif findIfThanElse(exp)!=None:
        return findIfThanElse(exp)           
      elif findIfThan(exp)!=None:
        return findIfThan(exp)   
      elif findLambdaVar(exp)!=None:
        return findLambdaVar  (exp)         
      elif findLambdaOpt(exp)!=None:
        return findLambdaOpt(exp)              
      elif findLambdaSimple(exp)!=None:
        return findLambdaSimple(exp)    
      elif findAnd(exp)!=None:
        return findAnd(exp)      
      elif findOr(exp)!=None:
        return findOr(exp)     
      elif findDefine(exp)!=None:
        return findDefine(exp)
      elif findMITDefine(exp)!=None:
        return findMITDefine(exp)      
      elif  findApplic(exp) !=None:
        return findApplic(exp)
      elif  findVariable(exp) !=None:
        return findVariable(exp)


      else:
        return "no-match!"


#********************************************************************************************************************
#                 functions: findVariable,  findConstant, findLambdot
#********************************************************************************************************************
def findVariable(m):
    if m.accept(v) in ['Symbol']:
      return Variable(m)
#*************************************
def findConstant(m):
    args=[]
    if m.accept(v) in ['Boolean','Char','String','Integer','Fraction']:
      return Constant(m)
    elif  m.accept(v)=='Pair' and m.getcar().accept(v)=='Symbol':
       if m.getcar().name =='QUOTE'  :
            #print(m)
            return Constant((m.cdr).car,True)
       elif m.getcar().name == 'VECTOR':
            ops=m.cdr
            while ((ops).accept(v))=='Pair':
              args.append(ops.car)
              ops=ops.cdr  
            #print (args)
            return Constant(Vector(args))
               
#*********************************************************************

def findLambdaSimple(m):
  args=[]
  if m.accept(v) == 'Pair' and m.car.accept(v)=='Symbol':
    if m.car.name=='LAMBDA': 
        if m.cdr.car.accept(v)!='Nil':
            if  m.cdr.car.getType()==False:
                ops= m.cdr.car
                while ((ops).accept(v))=='Pair':
                    args.append(tag(ops.car))
                    ops=ops.cdr   
                return (LambdaSimple(args,tag(m.cdr.cdr.car),0,0))
        else:
            return (LambdaSimple(args,tag(m.cdr.cdr.car),0,0))
#*******************************************************************
def findLambdaVar(m):
  if m.accept(v) == 'Pair' and m.car.accept(v)=='Symbol':
    if m.car.name=='LAMBDA':
        if  (m.cdr.car.accept(v))=='Symbol':
              arg=m.cdr.car
              return (LambdaVar((arg),tag(m.cdr.cdr.car),0,0))
#******************************************************************** 
def findLambdaOpt(m):
  args=[]
  if m.accept(v) == 'Pair' and m.car.accept(v)=='Symbol':
    if m.car.name=='LAMBDA': 
        if m.cdr.car.accept(v)!='Nil':
          if m.cdr.car.getType()!=False:
              last = m.cdr.car.getType()       
              ops= m.cdr.car
              while ((ops).accept(v))=='Pair':
                  args.append(tag(ops.car))
                  ops=ops.cdr   
              args.append(tag(last)) 
              return (LambdaOpt(args,tag(m.cdr.cdr.car),0,0))
  
#********************************************************************************************************************
#                 functions: findApplic,findOr,findLet(star,rec)
#********************************************************************************************************************

def findApplic(functor):
      args=[] 
      if functor.accept(v) in ['Pair']:
        func=tag(functor.car)
        while (functor.cdr.accept(v))=='Pair':
            functor=functor.cdr
            if functor.car.accept(v)!='Nil':
              args.append(tag(functor.car))
        if functor.cdr.accept(v)!='Nil':
            args.append(tag(functor.cdr))
        return Applic(func,args)
#********************************************
def findOr(m):
    args=[]
    if m.accept(v)=='Pair' and (m.car).accept(v)=='Symbol' and (m.cdr).accept(v)=='Nil' :
      if m.car.name=='OR':
        return Constant(Boolean('#f'))
    elif m.accept(v) in ['Pair']:
        if (m.car).accept(v)=='Symbol' and m.car.name=='OR' :
            while ((m.cdr).accept(v))=='Pair':
               m=m.cdr
               args.append(tag(m.car)) 
        if args!=[]:       
          return Or(args)
        else:
          return None
#******************************************************

def findLet(m):
    args=[]
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='LET' :
        vaars= getVars(m.cdr.car)
        exps= getExps(m.cdr.car)
        body =  m.cdr.cdr.car
        lam = LambdaSimple(vaars,tag(body),0,0)
        app= Applic(lam,exps)
        return app
#*************************
def findLetStar(m):
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='LET*' :
        ret = letStar_To_Let(m.cdr.car, m.cdr.cdr.car)
        return tag(ret)
#*************************
def findLetRec(m):
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='LETREC' :
        vaars= getVars(m.cdr.car)
        x=Variable(Symbol(GenSym.generate()))
        vaars.insert(0,x)
        exps= getExps(m.cdr.car)
        body =  m.cdr.cdr.car
        exps.insert(0,tag(body))
        #print(vaars)
        #print("******")
        
        #print(exps)
        return rec_to_app(vaars,exps)

#********************************************************************************************************************
#                 functions: findDefeine, findMITDefine, findCond, find IfThen(+else),findAnd
#********************************************************************************************************************

def findDefine(m):
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='DEFINE' :
          if m.cdr.car.accept(v)!='Pair': 
            return Def(findVariable((m.cdr).car),tag(((m.cdr).cdr).car))
            
#*******************************************
def findMITDefine(m):
    argList=[]
    bodyList=[]
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='DEFINE' :
        if m.cdr.car.accept(v)=='Pair':
            name =  m.cdr.car.car   #symbol
            args = m.cdr.car.cdr
            body = tag(m.cdr.cdr.car)
            if args.accept(v)== 'Symbol':
                return Def(tag(name),LambdaVar(args,body,0,0))
            if args.accept(v)== 'Pair' and args.cdr.accept(v)=='Nil':
                return Def(tag(name),LambdaSimple([args.car],body,0,0))           
            while args.accept(v)== 'Pair':
                argList.append(args.car)
                args = args.cdr
            impro = m.cdr.car.cdr.getType()
            if impro != False:
               argList.append(args)
               return Def(tag(name),LambdaOpt(argList,body,0,0)) 
            else:
               return Def(tag(name),LambdaSimple(argList,body,0,0)) 
            
#**********************************************
def findCond(m):
    args=[]  
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='COND'  :
        while ((m.cdr).accept(v))=='Pair':
            m=m.cdr
            args.append(tag(m.car))     
        if (args[len(args)-1]).car.con.accept(v)=='Symbol':
            if (args[len(args)-1]).car.con.name=='ELSE':
              last = args[len(args)-1].cdr
              args.pop()
              return cond_to_if(args,last)
            else:
               return (cond_to_if(args,Constant(Void())))
        else:
             return (IfThenElse(args[0],args[1],Constant(Void())))  


#*********************************************               
def findIfThanElse(m):
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='IF'  and (m.cdr.cdr.cdr).accept(v)!= 'Nil' :
           return(IfThenElse(tag(m.cdr.car),tag(m.cdr.cdr.car),tag(m.cdr.cdr.cdr.car)))
  #********************************************                   

def findIfThan(m):
    if m.accept(v) in ['Pair']:
      if (m.car).accept(v)=='Symbol' and m.car.name=='IF' and (m.cdr.cdr.cdr).accept(v)== 'Nil':
            return(IfThenElse(tag(m.cdr.car),tag(m.cdr.cdr.car),Constant(Void())))
  #*************************************************         
def findAnd(m):
    args=[]
    i=0;
    if m.accept(v)=='Pair' and (m.car).accept(v)=='Symbol' and (m.cdr).accept(v)=='Nil' :
      if m.car.name=='AND' :
        return Constant(Boolean('#t'))
    elif m.accept(v) in ['Pair']:
        if (m.car).accept(v)=='Symbol' and m.car.name=='AND' :
            while ((m.cdr).accept(v))=='Pair':
               m=m.cdr
               args.append(tag(m.car)) 
        return (create_if(args))
#********************************************************************************************************************
#                 functions: getVars,getExps, letStar_To_Let, rec_to_app,createIF, cond2IF
#********************************************************************************************************************

def getVars(exp):
    vaars=[]
    while ((exp).accept(v))=='Pair':
        if exp.car.accept(v)!='Pair':
          return vaars.append(tag(exp))
        else: 
          vaars.append(tag(exp.car.car))
          exp=exp.cdr
    return vaars   
#******************************************
def getExps(exp):
  exps=[]
  while ((exp).accept(v))=='Pair':
        if exp.car.accept(v)!='Pair':
          return exps.append(tag(exp))
        else: 
         exps.append(tag(exp.car.cdr.car))
         exp=exp.cdr 
  return exps   
#******************************************
def letStar_To_Let(bindings,body):
    if bindings.accept(v)=='Nil':
        return body
    else: 
        l = [Symbol('LET'), Pair(bindings.car,Nil()), letStar_To_Let(bindings.cdr,body)] 
        return Pair(l[0],l[1:])  
#***************************************************
def rec_to_app(vaars,exps):
  args=[]
  for r in range(0,len(vaars)):
      args.append(LambdaSimple(vaars,exps[r],0,0))
  x= Applic(Variable(Symbol('yag')),args)    
  #print (x)
  return  x  
#*********************************************************
def create_if(exp):
    if len(exp)==1:
        return (IfThenElse(exp[0],exp[0],Constant(Boolean('#f'))))
    elif len(exp)==2:
        return (IfThenElse(exp[0],exp[1],Constant(Boolean('#f'))))
    elif len(exp)>2:
        return (IfThenElse(exp[0],create_if(exp[1:]),Constant(Boolean('#f'))))
#***************************************************************
def cond_to_if(exp,last):
    if len(exp)==0:
        return last[0]
    if len(exp)>=1:
        #return exp[0].cdr[0]
        return (IfThenElse(exp[0].car,exp[0].cdr[0],cond_to_if(exp[1:],last)))
    
#********************************************************************************************************************
#                 QuasiQuote functions
#********************************************************************************************************************
def expand_qq(exp):
  if Check_Unquote(exp)==True:
    return exp.cdr.car
  elif Check_UnquoteSplicing(exp)==True:
    return 'error'
  elif (exp.accept(v)=="Pair"):
        a = exp.car
        b= exp.cdr
        if (Check_UnquoteSplicing(a))==True:
            return Pair(Symbol('APPEND'),[a.cdr.car],expand_qq(b))
        elif (Check_UnquoteSplicing(b))==True:
            return Pair(Symbol('CONS'),[expand_qq(a)],b.cdr.car) 
        else:
            return Pair(Symbol('CONS'),[expand_qq(a)],expand_qq(b))
  elif (exp.accept(v)=='Vector'):
      return Pair(Symbol('LIST->VECTOR'),expand_qq(Pair(Symbol('VECTOR->LIST'),exp)))
  elif(exp.accept(v)=='Symbol' or exp.accept(v)=='Nil') :
    return Symbol(str(exp))
  else:
    return exp 

#*********************************************************************

def findQuasiquoted(exp):
  if exp.accept(v)=='Pair' and exp.car.accept(v)=='Symbol': 
     if exp.car.name=='QUASIQUOTE':
         return tag(expand_qq(exp.cdr.car))
     
#**********************************************************************

def Check_Unquote(exp):
    if exp.accept(v)=='Pair' and exp.car.accept(v)== 'Symbol' and exp.car.name=='UNQUOTE' and exp.cdr.accept(v)=='Pair' and exp.cdr.cdr.accept(v)=='Nil':
      return True
    else:
      return False 
#************************************************************************
def Check_UnquoteSplicing(exp):
    if exp.accept(v)=='Pair' and exp.car.accept(v)=='Symbol' and exp.car.name=='UNQUOTE-SPLICING' and exp.cdr.accept(v)=='Pair' and exp.cdr.cdr.accept(v)=='Nil':
      return True
    else:
      return False 


#********************************************************************************************************************
#                 VISITOR?
#********************************************************************************************************************      
class SchemeExprVisitor(AbstractSchemeExpr):
    def __init__(self):
        pass

    def visitLambdaVar(self):
             return 'LambdaVar'     
    def visitLambdaSimple(self):
             return 'LambdaSimple'     
    def visitLambdaOpt(self):
             return 'LambdaOpt'       
    def visitApplic(self):
             return 'Applic'     
    def visitApplicTP(self):
             return 'ApplicTP'  
    def visitVarFree(self):
             return 'Free'     
    def visitVarParam(self):
             return 'Param'       
    def visitVarBound(self):
             return 'Bound'     
    def visitVariable(self):
             return 'Variable'    
    def visitOr(self):
             return 'Or'     
    def visitConstant(self):
             return 'Constant'       
    def visitIfThenElse(self):
             return 'IfThenElse'     
    def visitDef(self):
             return 'Def'    




g=SchemeExprVisitor()      
env={}







