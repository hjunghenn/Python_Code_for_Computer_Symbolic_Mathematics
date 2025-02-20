
#### Tools.py

global upper,lower,letters #,numeric,symbols
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lower = 'abcdefghjklmnopqrstuvwxyz' # no 'i' 
letters = upper+lower              
numeric = '.0123456789i'
#symbols = letters+numeric


################################ category ###############################

def isarithmetic(expr):
    for ch in expr:      
        if ch in letters: 
            return False
    return True

def isnumeric(ch):    
    return ch in numeric

def isletter(ch):    
    return ch in letters

def isupper(ch):
    return ch in upper

def islower(ch):
    return ch in lower


########################### index retrieval #############################

def movepast(expr,start,string): 
    k = start              # index of character in expr   
    while k  < len(expr):
       if expr[k] not in string: # quit 
            break         
       k+=1         
    return k  # k points to the right of a string symbol

'''
expr = 'abc76.543de' 
start = 3           # index of '5'
string = '.123456789' 
end = movepast(expr,start,string)  
print(end,expr[end])
'''

def move2rparen(expr,start):
     # returns index of matching right paren; start is at '('
    numleft = 0; numright = 0
    idx = start
    while idx < len(expr): 
        ch = expr[idx]      
        if ch == '(': numleft += 1
        if ch == ')': numright += 1      
        if numleft == numright: break
        idx += 1
    return idx  # idx now at matching ')'
'''
expr = '(1+(2+(3+4)))'
start = 3
print(move2rparen(expr,start))
'''

############################# get symbols ###############################

def get_var(expr):
    for ch in expr:      
        if ch in lower: 
            return ch
    return ''

def get_vars(expr):   
    varlist = []      
    j=0
    while j < len(expr):
        if expr[j] in letters:          
           start = j        
           end = movepast(expr,start+1,'1234567890')  # possible subscripts         
           var = expr[start:end]                          # get the variable          
           varlist = varlist + [var]                        # attach to list
           j = end      
        else:
           j += 1    
    varlist = sorted(list(set(varlist)))        # remove duplicates and sort     
    varstring = ''.join(varlist)                               # string form  
    return varlist,varstring                        # return list and string 


def get_lower(expr):
    variables = []
    for ch in expr:
        if ch in lower:
            variables = variables + [ch]
    if variables == []: return ''        
    return ''.join(sorted(list(set(variables))))

def get_upper(expr):
    variables = []
    for ch in expr:
        if ch in upper:
            variables = variables + [ch]
    if variables == []: return ''        
    return ''.join(sorted(list(set(variables))))

'''
expr = '7x11 + 11ABcd'  
print(get_vars(expr)[0])
print(get_lower(expr))
print(get_upper(expr))
'''


############################ prepare expression #########################

def insert_asterisks(expr,varlist): 
    expr = expr.replace(' ','')
       
         # insert between parens
    expr = expr.replace(')(',')*(')
    
       # insert between paren and var
    for v in varlist:
        expr = expr.replace(')'+v,')*'+v)
        expr = expr.replace(v+'(',v+'*(')
        
        # insert between paren and numeric    
    for n in numeric:
        expr = expr.replace(')'+n,')*'+n)
        expr = expr.replace(n+'(',n+'*(')
  
    # insert between variables        
    for m in varlist:
        for n in varlist:
            expr = expr.replace(m+n,m+'*'+n)
        
       # insert between variable and constants
    for v in varlist:
        for n in numeric:
            #expr = expr.replace(m+n,m+'*'+n)
            expr = expr.replace(n+v,n+'*'+v)
        
       # insert between accent and variable (for logic)
    for v in varlist:
        expr = expr.replace("'"+v,"'*"+v)
 
    expr = expr.replace("'(","'*(") 
    return expr

'''
expr = 'Ayz34v+uB(3.7i+x2F11G12)^w5'
#expr = "(p->r'q)(q->(r+p'))"
varbs = get_vars(expr)[0]
print(varbs)
print(insert_asterisks(expr,varbs))
'''


def fix_operands(expr):   
    if expr[0] == '-':                  # if '-' at beginning, then
       expr = '0-' + expr[1:]                         # insert '0'
    if expr[0] == '+':                          # similarly for '+'
       expr = '0+' + expr[1:] 
    expr = expr.replace('(-', '(0-',) 
    expr = expr.replace('(+', '(0+',) 
    #expr = expr.replace('^(0', '^(',)    # exponenent fix; don't use    
    return expr

#expr = '-1+(+2 - 3)^(-4)'
#print(fix_operands(expr))


def attach_missing_exp(expr,varlist):  # can't contain both x and x1
    expr = expr.replace(' ','')          
    for v in varlist:
        expr = expr.replace(v,v + '^1') 
    return  expr.replace('^1^','^')   

'''
expr = 'x123+y^456z789'
var_list = ['x123','y','z789']  
print(attach_missing_exp(expr,var_list))
'''


def fix_signs(expr):    
    if expr == '' or expr == '0': return expr             
    #expr = expr.replace('(-)', '-')
    expr = expr.replace(' ', '')      
    expr = expr.replace('(+', '(')                       
    expr = expr.replace('++','+')
    expr = expr.replace('-+','-')
    expr = expr.replace('+-','-')
    expr = expr.replace('--','+')
    expr = expr.replace('+=','=')
    expr = expr.replace('-=','=')
    expr = expr.replace('=+','=')
    expr = expr.replace('=0-', '=-')     
    expr = expr.replace('=0+', '=')               
    if expr[0] == '+': expr = expr[1:]                    
    L = len(expr)
    if L>1 and expr[L-1] in '+-': expr = expr[:L-2]                    
    return expr

########################### extraction functions ########################

def extract_sequence(expr,start,characters):
    end = movepast(expr,start,characters) # one past end of characters
    return expr[start:end], end                       

def extract_numeric(expr,start): 
    return extract_sequence(expr,start,'.0123456789i')

def extract_integer(expr,start): 
    return extract_sequence(expr,start,'0123456789')

def extract_var(expr,start): # allows subsripts
    end = extract_sequence(expr,start,letters + '_')[1]    
    if end < len(expr) and expr[end] in '0123456789':        
        end = extract_integer(expr,end)[1]         
    return expr[start:end], end                           

def extract_paren(expr,start):                # index start is at '('
    end = move2rparen(expr,start)             # end at ')'           
    end += 1                                  # one past ')'         
    return expr[start:end], end               # return (...)                                                                            

def extract_exp(expr,start):     # index start is at '^'
    start += 1                   # move one past '^'
    k = start                                            
    if expr[k] == '(':           # parenthetic exponent?
        return extract_paren(expr,start) # return group inside parens  
    if expr[k] == '-':                 # negative exp?
        k+=1                           # skip past
    string = '1234567890t' # allowable characters left (t = transpose)
    end = movepast(expr,k,string)  # end is one past exponent      
    return expr[start:end], end

'''
expr = '3-4+.5432ia5+6'
start = 4
print(extract_numeric(expr, start))

start = 10
print(extract_var(expr, start))

expr = '3+(7-i+x)^(-54t)+11'
start = 9
print(extract_exp(expr,start))

expr = '3+(7-i+x)^-54t+11'
start = 9
print(extract_exp(expr,start))

expr = '(1+(2+((3+4)+5))+6)' 
start = 7                                # index of 4th left paren
print(extract_paren(expr,start))
'''


#################### insert, remove, replace strings ####################

def add_parens(expr): 
    if expr == '' or expr == '-' : 
        return expr     
    if expr[0]  == '(':
        return expr       # already has parens        
    if '/' in expr or '+' in expr[1:] or '-' in expr[1:]:      
        return '(' + expr + ')'
    return expr


def replace_string(string,replacement,idx):
     L = len(replacement)
     left = string[:idx]                # portion of expr up to idx-1
     right = string[idx+L:]                              
     return left + replacement + right, idx + L  

'''
string = 'abcdefg'
replacement = 'xy'
print(string)
print(replace_string(string,replacement,0)) # replace ab with xy
print(replace_string(string,replacement,3)) # replace de
idx = len(string)-2
print(replace_string(string,replacement,idx)) # replace fg
'''


def insert_string(expr,insertion,idx):    
    #if idx == len(expr)-1:
    #    return expr + insertion, idx == len(expr) -1    
    outstring =  expr[:idx] + insertion + expr[idx:] 
    return outstring, idx + len(insertion) 

'''
expr = 'abcd'
insertion = 'xy'
print(insert_string(expr,insertion,0)) # inserts before expression
#print(insert_string(expr,insertion, -len(insertion))) # inserts before expression
#print(insert_string(expr,insertion, len(insertion)))  # inserts after expression
print(insert_string(expr,insertion,2))  # inserts after b so x is at index 2
'''


#########################################################################
############## string, list conversion and construction #################


def string2table(s):
    # takes a comma, semicolon delimited string and prints a list
    s = s.replace(' ','')    # remove extra space
    if ';' not in s:
       row = s.split(',')       # no semicolon
       T = [row]         
       return T             # single row
    rows = s.split(';')        # split into lists at semicolon 
    T = []
    for row in rows:            # split each  at commas
       rowlist = row.split(',') 
       T.append(rowlist)   
    return T
'''
s = '1,2;3;4,5,6'                                          # 3 rows
print(string2table(s))
s = '1;2;3;4;5;6'                                          # 6 rows 
print(string2table(s))
s = '1,2,3,4,5,6'                                           # 1 row
print(string2table(s))
'''

def table2string(T):
    # takes a table and prints a comma, semicolon delimited string
    if isinstance(T[0],str): return ','.join(T)       
    s = ''
    for row in T:
        rowstr = ','.join(row)    
        s = s + ';' + rowstr
    return s[1:] 

'''
T = [['1','2','3'],['4','5']]
#T = ['1','2','3','4','5','6']
s = table2string(T)
print(s)
'''

def zero_list(n):
    return ['0' for k in range(n)]

def copylist(A):   # duplicates list A without changing A
    import copy
    return copy.deepcopy(A)  

def flatten_double_list(dlist):
    slist = []    
    for d in dlist:
        for s in d:
            slist.append(s)
    return slist

#dlist = [['1','2','3'],['4','5','6'],['7','8'],['9']]
#print(flatten_double_list(dlist))



########################### print functions #############################

def print_list(A,direction):   
    if A == [] or A == '': return
    if type(A) == str:
        A = A.split(',')        
    for item in A:
        if direction == 'h':         # horizontal
            print(item,end = ' ')      
        if direction == 'v':  # vertical
            print(item)

'''
A = ['1', '2', '3']
print(A,'\n')
print_list(A,'h')
print('\n')
print_list(A,'v')
'''


def format_print(A, nspaces, flush):                       
    if len(A) == 0: return
    if isinstance(A,str):                  # if string
        print(A); return                   # return string
    if isinstance(A,list):                 # if list
        if not isinstance(A[0],list):      # but not double list
            print_list(A,'horizontal')     # print horizontally
            return
    nrows, ncols = len(A), len(A[0])          # dimensions of A
    col_width = [0 for j in range(len(A[0]))] # array for column widths   
    B = copylist(A)                      # don't destroy A
    
    for i in range(nrows): 
        for j in range(ncols):                # get width of each column
            if len(A[i][j]) > col_width[j]:   # col width[j] = width of 
                col_width[j] = len(A[i][j])   # largest  entry in col j        
    for i in range(nrows):                    # add spaces to A's entries 
        for j in range(ncols): 
                # spaces to left or right of entry:             
            this_many_spaces = col_width[j] + nspaces - len(A[i][j]) 
            width = ' '*this_many_spaces 
            half_width = ' '*((this_many_spaces+1)//2) 
            if flush == 'left': 
               B[i][j] = B[i][j] + width      # entry at left
            elif flush == 'right': 
               B[i][j] = width + B[i][j]     # entry at right 
            else:                               
                B[i][j] = half_width + B[i][j] + half_width    # entry in middle   
    for i in range(len(B)):
        for entry in B[i]:
            print(entry, end = '')            # print on single line
        if i < len(B) - 1:
           print('')

'''
s = '1, 2+3i, 1.2356789,4; 5, 6, 7, 8+9i'
#s = '1, 2+3i, 1.2356789,4;----------,'','','';5, 6, 7, 8+9i'
A = string2table(s)
print('left flush:')
format_print(A,2,'left')
print('\n')
print('center:')
format_print(A,2,'center')
print('\n')
print('right flush:')
format_print(A,2,'right')
'''


def print_fraction(prepend,num,den,append):
    maxlen = max(len(num),len(den))
    leftspace = ' '*len(prepend)
    dash = '-'*maxlen    
    A = [[leftspace+num],[prepend+ dash + append],[leftspace+den]]        
    format_print(A, 1, 'center')

'''
print_fraction('','2345','7.6547777','=')
print('\n')
print_fraction('5 + ','2345','7.6547777','')

print_fraction('  ','2468 ','abcdefg','=')
print('\n')
print_fraction('2*','1234 ','abcdefg','')
'''

############################### print_brackets #############################


'''
def print_brackets(expr1,expr2,expr3,expr4):
    L1 = len(expr1)
    L2 = len(expr2)
    L3 = len(expr3)
    spaces1 = L1*' '    
    spaces2 = L2*' '    
    spaces3 = L3*' '    
    print('--')
    print('| '+ spaces1 + ' --')
    print('| '+ spaces1 + ' | ' + spaces2 + ' --')    
    print('| '+ spaces1 + ' | ' + spaces2 + ' | ' + spaces3 + ' -- ')
    print('| '+ expr1   + ' | ' + expr2   + ' | ' + expr3   + ' | ' + expr4) 
    print('| '+ spaces1 + ' | ' + spaces2 + ' | ' + spaces3 + ' -- ')
    print('| '+ spaces1 + ' | ' + spaces2 + ' --') 
    print('| '+ spaces1 + ' --')
    print('--')


#expr1 = 'testing'
#expr2 = expr1
#print_brackets(expr1,expr1,expr1,expr1
'''


'''

#letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def get_varpar_list(expression,variables,parameters):     
    # input: mathematical expression string
    #        string of allowable variables
    #        string of allowable parameters  
    # sorted lists of variables and parameters in expression
    varlist = []            
    parlist = []
    for ch in expression:
        if ch in variables:                    
            varlist.append(ch)  # found a variable, append to list           
        if ch in parameters:                    
            parlist.append(ch) # found a parameter, append to list
    varlist = list(set(varlist))            # eliminate duplicates      
    parlist = list(set(parlist))                           # ditto       
    return sorted(varlist),sorted(parlist)      # sort for clarity

    
expression = '2C+3z-4By+7w-5Azu'
variables = 'abcdefghijklmnopqrstuvwxyz'   # no letter i (numeric)
parameters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#parameters = ''
#variables = ''
varlist,parlist = get_varpar_list(expression,variables,parameters)
print(varlist,',',parlist)


########################### string/list conversons #######################

def list2virtual(L):
    virtual= '['
    
    for item in L:
        virtual = virtual + item +','   
    virtual = virtual[:len(virtual)- 1]
    return virtual+']'
 
def virtual2list(V):
    V = V[1:len(V)- 1]
    return V.split(',')


L = list('12345')
print(L)
print(virtual2list(list2virtual(L)),'\n')

V = '[1,2,3,4,5]'
print(V)
print(list2virtual(virtual2list(V)))


############################ index functions #############################

def moveright(expr,start,string):
    # Asumes that expr[start] is an item in string. Returns
    # one more than the index for which expr[index] is in string.
    
    idx = start
    while idx  < len(expr):
        if expr[idx] not in string: break         
        idx += 1                            # increment idx    
    return idx  

def moveleft(expr,start,string):
    # Asumes that expr[start] is an item in string. Returns
    # one more than the index for which expr[index] is in string.
    
    idx = start
    while idx  > 0:
        if expr[idx] not in string: break         
        idx -= 1                            # increment idx    
    return idx  


#z = '-3.1+5.6i'
#idx = moveleft(z,7,')(.0123456789')
#print(idx)


############################### insert,split mat ################################

def transpose(A):
    nrows, ncols = len(A),len(A[0])
    B = [['' for j in range(nrows)] for i in range(ncols)] 
    for j in range(nrows):
        for i in range(ncols):   # make column j of B row j of A                                           
            B[i][j] = A[j][i] 
    return B

def insert_mat(A,B,col):
    # insert rows of matrix B as columns into matrix A
    # starting at col 
    nrows, ncols = len(A),len(A[0])
    TA = transpose(A)
    C = []
    for i in range(col):  # put top portion of B in C
        C.append(TA[i])
    for row in B:         # put in middle portion of C
        C.append(row)
    for i in range(col,ncols): # put bottom portion of TB in C
        C.append(TA[i])
    return transpose(C)       # make rows into columns

def remove_insert_mat(A,B,col):
    # insert rows of matrix B as columns into matrix A
    # starting at col, removing first the columns of A 
    nrows, ncols = len(A),len(A[0])
    width = len(B)
    TA = transpose(A)
    C = []
    for i in range(col):  # put top portion of B in C
        C.append(TA[i])
    for i in range(col+width,ncols): # put bottom portion of TB in C
        C.append(TA[i])
    D = transpose(C)          # A with removed cols 
    E = insert_mat(D,B,col)
    return E 



A1 = 'a,b,c,d,e;\
      f,g,h,i,j;\
      k,l,m,n,o'
B1 = '1,2,3;\
      4,5,6'

A2 = 'a,b,c,d,e,f,g,h,i,j'   # single row
B2 = '1'

A3 = 'a;b;c;d;e'             # single col
B3 = '1,2,3,4,5'

A =A1; B = B1
A = string2mat(A); B = string2mat(B);

col1 = 2              # middle
col2 = len(A[0])-1    # at second to last column
col3 = len(A[0])      # after last column
col4 = 0              # before A
col = col4

format_print(A,1,'left');print('\n')
format_print(B,1,'left');print('\n')
format_print(insert_mat(A,B,col),1,'left');print('\n')
format_print(remove_insert_mat(A,B,col),1,'left')



def split_mat(A,col):     # into right and left parts
    nrows, ncols = len(A),len(A[0])
    B = transpose(A)
    top = []; bottom = []
    for i in range(col):
        top.append(B[i]) 
    for i in range(col,ncols):
        bottom.append(B[i]) 
    return transpose(top), transpose(bottom)


A = string2mat('a,b,c,d,e; f,g,h,i,j; k,l,m,n,o')
left_part,right_part = split_mat(A,3)
format_print(A,1,'left'); print('')
format_print(left_part,1,'left'); print('')
format_print(right_part,1,'left')


expr = '(1+2+3)^-44'
start = 7
print(extract_exp(expr,start))     # index start is at '^'
expr = '(1+2+3)^(-44)'
start = 7
print(extract_exp(expr,start))


def xis_single_term(expr):
    return '+' not in expr and '-' not in expr

def xhas_no_letters(expr):
    for ch in letters:
        if ch in expr: return False
    return True

def xhas_no_caps(expr):
    for ch in upper:
        if ch in expr: return False
    return True


def xisarithmetic(expr): 
    for ch in letters:
        if ch in expr: return False  
    return True

def xare_disjoint(A,B):   
    for ch in A:
        if ch in B: return False
    for ch in B:
        if ch in A: return False
    return True

def xis_subset(A,B):
    for a in A:
        if a not in B: return False
    return True
 
def xlist_intersection(A,B):
    I = []
    for a in A:        
        if a in B: I += [a]
    for b in B:
        if b in A: I += [b]
    return list(set(I))         #### for strings:''.join(list(set(I)))

def xcontains_member(expr,string):
    for s in string:
        if s in expr: return True
    return False
 
def xget_letters(expr):
    variables = []
    for ch in expr:
        if ch in letters and ch != 'i':
            variables = variables + [ch]
    if variables == []: return ''        
    return ''.join(sorted(list(set(variables))))


def xstring2list(s):  ## needed?
    return s.split(',')

def xstrlist2intlist(slist):
    ilist = []    
    for item in slist:
        ilist.append(int(item))
    return ilist

def xintlist2strlist(ilist):
    slist = []    
    for item in ilist:
        slist.append(str(item))
    return slist


slist = ['1','2','3','4',]
ilist = [1,2,3,4]
print(strlist2intlist(slist))
print(intlist2strlist(ilist))


def xextract_paren_with_exp(expr,start):      # need to restrict to varbs
    parens, idx  = extract_paren(expr,start)  
    if idx < len(expr) and expr[idx] == '^':
        exp, idx = extract_exp(expr,idx)    
        parens = parens + '^' + exp
    return  parens, idx  


def xremove_segment(expr,idx,L): 
    # remove substring of length L starting at idx
    left = expr[:idx]
    right = expr[idx+L:]
    return left + right

string = 'abcdefg'
idx = 2
L = 1
print(remove_segment(string,idx,L))  


def xremove_and_insert(expr,remove,insert,idx):   
    L = len(remove)
    left = expr[:idx]
    right = expr[idx+L:]
    
    print(999,right)
    
    print(1000,left,',',remove,',',insert,',', right)
    
    expr = left + insert + right
    return expr,idx + L - len(insert)

expr = 'abcdefg'
remove = 'cdef'
insert = 'xy'
idx = 2;   # remove 'cdef' and insert 'xy'
print(remove_and_insert(expr,remove,insert,idx))   


############################# parentheses ###############################

def get_matches(expr):   # in to out 
    lparens = []
    rparens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == '(':
            lparens =  lparens + [i]
            j = move2rparen(expr,i)
            rparens = rparens + [j]
        i += 1            
    lparens.reverse() 
    rparens.reverse()
    
    return lparens,rparens


def xxget_matches(expr):   # out  to in
    lparens = []
    rparens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == '(':
            lparens =  lparens+[i]
            j = move2rparen(expr,i)
            rparens = rparens + [j]
        i += 1            
      
    return lparens,rparens


#e =  '((a+b)+c)'
#   print(get_matches(e))


def xremove_extra_parens(expr):        
    
     #(c(a+b))--> c(a+b) 
     #((a+b)c)--> (a+b)c 
     #(c+(a+b))--> (a+b+c)
     #((a+b)+c)--> (a+b+c)
     # ((a+b)+(c+d)) --> (a+b+c+d)
     # (c(a+b)d) --> c(a+b)d
     # ((a+b)(c+d)) --> (a+b)(c+d)     
    
   
    lparens,rparens = get_matches(expr)      # out to in
    #print('out to in', '(c(a+b))--> c(a+b)' )           
    for i in range(len(lparens)):
        left = lparens[i]
        right = rparens[i]                                 
        #print(4546,left,right)            
        if  right-1 == rparens[i-1] and \
            (left == 0 or (expr[left-1] not in '/*)')):
            expr = replace_string(expr,'%', left)[0]
            expr = replace_string(expr,'%',right)[0]              
    
    lparens,rparens = get_matches(expr)      # out to in
    #print('out to in', '((a+b)c)--> (a+b)c' )           
    for i in range(len(lparens)):
        left = lparens[i]
        right = rparens[i]                                 
        #print(4546,left,right)            
        if  i < len(lparens)-1 and left == lparens[i+1] and \
            (right == len(expr)-1 or (expr[right+1] not in '/*)')):
            expr = replace_string(expr,'%', left)[0]
            expr = replace_string(expr,'%',right)[0]              
        
    lparens,rparens = get_matches(expr)           # out to in
    lparens.reverse(); rparens.reverse()
    #print('in to out', '((a+b)+c)--> (a+b+c)')
    for i in range(len(lparens)-1):
        left = lparens[i]
        right = rparens[i]                                 
        #print(4547,left,right)            
        if  i < len(lparens)-1 and left+1 == lparens[i+1] and \
            (i < len(rparens)-1 or expr[right+1] not in '/*)'):
            expr = replace_string(expr,'%', left)[0]
            expr = replace_string(expr,'%',right)[0]          
      
    lparens,rparens = get_matches(expr)     
    lparens.reverse(); rparens.reverse()
    #print('in to out','(a + (b + c)) --> (a + b + c)',lparens,rparens)             
    # (a + (b + c)) --> (a + b + c)
    for i in range(len(lparens)-1):
        left = lparens[i]
        right = rparens[i]                               
        if  i < len(rparens)-1 and right+1 == rparens[i+1] and \
            expr[left-1] not in '0123456789/*)':
            expr = replace_string(expr,'%', left)[0]
            expr = replace_string(expr,'%',right)[0]          
   
   
    expr = expr.replace('%','')        
    return expr     


e1 = '(((((1+((5*(x+(y+z))-4*((5-x)))-7)+2)))) + 3sin^2((x+1)))'
e2 = '(1+((5(x+y)+(5-x))8-7))9'
e3 = '(((60(x^4-x^2-2))(x-1/2)^2(x-1/3)(x-2/5)))' 
e4 = '((1+(2+3))+4)'
e5 = '((1+(2+3))4)'
e6 = '(((^(*2 x^3) 5)))'
e7 = '(x^3+(2x+7))'
e8 =  '((a+b)+c)'
e9 =  '((a+(b+c)))'
e10 = '(((60(x^4-x^2-2))))'
e = e1


def paren_pair_count(expr):
    count = 0
    for ch in expr:
        if ch == '(': count += 1
    return count
    
def remove_extra_parens(expr):
    expr = expr.replace(' ','')
    if paren_pair_count(expr) == 1 \
        and '+' not in expr and '-' not in expr:
        expr = expr.replace('(','')
        expr = expr.replace(')','')
        return expr
    if '+' in expr or '-' in expr: return expr
    if not (expr[0] == '(' and expr[1] == '('):
       return expr
    last_rparen = move2rparen(expr,0,'(',')')
    next2last_rparen = move2rparen(expr,1,'(',')')
    stuff_between = expr[next2last_rparen:last_rparen]
    if '+' in stuff_between or '-' in stuff_between:
       return expr
    return expr[1:len(expr)-1]


expr = '((1+(2+3)+4)+5)'
print(remove_extra_parens(expr))
expr = '((1+(2+3)+4)5)'
print(remove_extra_parens(expr))

'''
