import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize
#flag 
global specialFlag
specialFlag=0
global feFlag
feFlag=0
global ifFlag
ifFlag=0
#check
global curStmt
curStmt=''
global nextToken
nextToken=''
global indexKeep
indexKeep=0

rarray=["abstract","continue","new","switch","assert","default","goto","package","synchronized","boolean","private","this","break","double","implements","protected","throw","byte","import","public","throws","case","enum","instanceof","return","transient","catch","extends","short","try","char","final","interface","static","void","class","finally","long","strictfp","volatile","const","native","super"]

earray=["do","if","while","for","int","float","switch","else"]

type=["int", "float", "double","char","boolean"]

scarray=['``','\'\'','~','!','#','$','%','^','&','*','(',')','_','+',',','.','/','|','\\','\'','-','=','<','>','?','{','}','[',']',':',';']

pairay=['(','[','{','\'\'','\'','``']

#keeps track of special char that need to be found before the end of program
stack=[]

#keeps track of special statement until end
specialArray=[]

#hold next lexeme
holdNext=[]
#token identifiers
keyword=11
special_symbol=12
user_defined_identifier=13
integer_literal=14
floating_point_literal=15
octal_literal=16
hex_literal=17
#special token identifiers
for_statement=30
if_statement=31
else_statement=32
do_statement=34
while_statement=33
int_declaration=35
float_declaration=36
switch_statement=37
forEach_statement=38
dec_statement=70
assign_statement=71

#GOES UNTIL ;
#valid declaration TYPE UID-->place UID in declared array
#valid assignment check the declared array for the UID '='

def printNclear(stmt):
  global specialFlag
  specialFlag=0
  global feFlag
  feFlag=0
  global curStmt
  curStmt=''
  if(stmt=='for_stmt'):
    for lexeme in specialArray:
      if (lexeme!='ENTER EXPRESSION3')and(lexeme!='END EXPRESSION3')and(lexeme!='ENTER EXPRESSION')and (lexeme!='END EXPRESSION')and(lexeme!='ENTER EXPRESSION2')and(lexeme!='END EXPRESSION2'):
        lex(lexeme)
      else:
        print(lexeme)
  specialArray.clear()




def initialized():
  print('initialize')



def declared():
  print('declare')




def error():
  print('Something went wrong',stack)



def statement():
  print('statement')



def condition():
  print('condition')

def setForEach():
  global feFlag
  feFlag=1


def expr(stmt,lexeme):
  #FOR EXPRESSIONS
  if(stmt=='for'):
    if(feFlag==1):
      specialArray.append(lexeme)
    elif(lexeme!=';') and (lexeme!=':'):
      specialArray.append(lexeme)
    elif(lexeme==';'):
      specialArray.append('END EXPRESSION')
      specialArray.append(lexeme)
    elif(lexeme!=':'):
      setForEach()
      specialArray.remove('ENTER EXPRESSION')
      specialArray.append(lexeme)
  elif(stmt=='for2'):
    specialArray.append('ENTER EXPRESSION2')
    specialArray.append(lexeme)
  elif(stmt=='for3'):
    specialArray.append('END EXPRESSION2')
    specialArray.append(lexeme)
    specialArray.append('ENTER EXPRESSION3')
    
def for_stmt(lexeme):
  if(len(specialArray)==0):
    if(lexeme == '('):
      specialArray.append('ENTER EXPRESSION')
      specialArray.append(lexeme)
      # print(specialArray)
      # error if the following lexeme isnt (
    else:
      error()
  # elif('END EXPRESSION3' in specialArray)and('END EXPRESSION2' in specialArray)and('END EXPRESSION1' in specialArray):
  #   print('end')
  elif(lexeme == ')'):
    specialArray.append('END EXPRESSION3')
    specialArray.append(lexeme)
    # print(specialArray)
  elif(')' not in specialArray):
    if('END EXPRESSION' not in specialArray):
      expr('for',lexeme)
      # print(specialArray)
    elif('ENTER EXPRESSION2'in specialArray) and (lexeme!=';'):
      specialArray.append(lexeme)
      # print(specialArray)
    elif('ENTER EXPRESSION2'in specialArray):
      expr('for3',lexeme)
      # print(specialArray)
    elif('END EXPRESSION'in specialArray):
      expr('for2',lexeme)
      # print(specialArray)
    else:
      error()
  else:
    printNclear('for_stmt')
    lex(lexeme)
    

def do_stmt(lexeme):
  if(len(specialArray)==0):
    
    if(lexeme == '{'):
      specialArray.append(lexeme)
    else:
      error()
  elif('}' not in specialArray):
    specialArray.append(lexeme)
  elif('}' in specialArray)and ('while' not in specialArray):
    specialArray.append(lexeme)
  else:
    printNclear('do_stmt')
    lex(lexeme)

def if_stmt():
  print('if')

def else_stmt():
  print('else')

def switch_stmt():
  print('switch')

def process(curStmt,lexeme):
  if (curStmt=='for'):
    for_stmt(lexeme)
  elif(curStmt=='do'):
    do_stmt(lexeme)
  elif(curStmt=='while'):
    specialArray.append(lexeme)
  elif(curStmt=='if'):
    if_stmt()
  elif(curStmt=='else'):
    else_stmt()
  elif(curStmt=='switch'):
    switch_stmt()

def special(lexeme):
  if(feFlag==1):
    print(lexeme + " is token " +str(forEach_statement))
  elif(lexeme=='for'):
    global curStmt
    curStmt='for'
    print(lexeme + " is token " +str(for_statement))
  elif(lexeme=="do"):
    curStmt='do'
    print(lexeme + " is token " +str(do_statement))
  elif(lexeme=='while'):
    curStmt='while'
    print(lexeme + " is token " +str(while_statement))
  elif(lexeme=='if'):
    curStmt='if'
    print(lexeme + " is token " +str(if_statement))
  elif(lexeme=='else') and (ifFlag==1):
    curStmt='else'
    print(lexeme + " is token " +str(else_statement))
  elif(lexeme=='switch'):
    curStmt='switch'

#these can be declared or declared and assigned, but make sure to be declared first for syntax
  elif(lexeme=='int'):
    print(lexeme + " is token " +str(int_declaration))
  elif(lexeme=='float'):
    print(lexeme + " is token " +str(float_declaration))
  else:
    print(lexeme + " is token!! " +str(switch_statement))

#function to ensure that these chars have ending match if not throw error
def needToPair(special):
  if(special=='\'\''):
    stack.append('\'\'')
  if(special=='``'):
    stack.append('\'\'')
  elif(special=='{'):
    print('ENTER BLOCK ')
    stack.append('}')
  elif(special=='\''):
    stack.append('\'')
  elif(special=='('):
    stack.append(')')
  elif(special=='['):
    stack.append(']')

def setSpecial():
  global specialFlag
  specialFlag=1
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#3. categorize
def lex(lexeme):
  #still continues special statement processing 
  if(specialFlag==1):
    #categorizes the statement based on statement syntax
    process(curStmt,lexeme)
  #SPECIAL CHAR
  elif(lexeme in scarray):
    #place the special char if its ( { '  [ to be ) } '  ] onto stack 
    if(lexeme in stack):
      # print('remove')
      stack.remove(lexeme)
      if(lexeme=='}'):
        print('EXIT BLOCK')
    elif(lexeme in pairay):
      needToPair(lexeme)
    print(lexeme +' is token '+ str(special_symbol))

  #SPECIAL STATEMENTS
  elif(lexeme in earray):
    setSpecial()
    special(lexeme)
  #finds if reserved word
  elif(lexeme in rarray):
    print(lexeme+' is token '+ str(keyword))
  #finds if user ident
  elif(bool(re.match("[a-zA-Z|_a-zA-Z][_0-9a-zA-Z]", lexeme))):
    print(lexeme + " is token " +str(user_defined_identifier))


    #checks all other values
  else:
      if(bool(lexeme.isnumeric())):
        if(bool(re.search("^[0-7]{1,3}$", lexeme))):
         #check if octal or integer
            print(lexeme + " is token "+str(octal_literal))
        else:
          print(lexeme + " is token "+str(integer_literal))
          #check hex
      elif(bool(re.search("^0[xX][0-9a-fA-F]+$", lexeme))):
        print(lexeme + " is token "+str(hex_literal))
        #check if float or print something else
      elif(bool(re.search("^[0-9]+\.[0-9]*$", lexeme))) or (bool(re.search("^[0-9]*\.[0-9]+$", lexeme))):
        print(lexeme + " is token " +str(floating_point_literal))
      else:
        print(lexeme + " is something else... ")

#2. file is found and process file continues read until no lines
def fileFound():
  if((open('ah.txt', 'r').read().find('VOID MAIN ()') != -1)):
      # print('main found')
    while True:
        lexeme = ""
        # read a single line
        text = filehandle.read()
        line = word_tokenize(text)
        for lexeme in line:
          holdNext.append(lexeme)
        for lexeme in line:
          # print(stack)
          global indexKeep
          indexKeep=indexKeep+1
          lex(lexeme)
        break
    if(len(stack)!=0):
      error()
    else:
      print('eof')
    # close the pointer to that file
    filehandle.close()
  else:
      print('ERROR: no main method')


# MAIN FUNCTION define the name of the file to read from
filename = "ah.txt"
#1.opens file if found
try:
    filehandle = open(filename, 'r')
    fileFound()
except:
    print('error opening file')

