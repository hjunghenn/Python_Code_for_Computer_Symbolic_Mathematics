
####### LinSolve 

import Arithmetic as ar
import Tools as tl
import MultiAlg as mu
global prod      # for future use
global switches  # for future use
global ops
global display

############################## echelon functions ###########################

def sym2op(opsym):              # expand string opsym  into list op
    opsym = opsym.replace(' ','')
    if '<' in opsym:                                        # a<->b
       a,b = opsym.split('<->')                         # no scalar
       a = a.replace('r','')                # remove the 'r' prefix
       b = b.replace('r','') 
       op = [1,'',int(a),int(b)]      # type 1: switch the rows
       return op
    ### extract scalar t from (t)a or (t)a+b:
    right_most_paren = opsym.rfind(')')              # index of ')'
    s = opsym[:right_most_paren+1]      # extract scalar and parens 
    the_rest = opsym[right_most_paren+1:] # stuff after right paren
    the_rest = the_rest.replace('r','')     # remove the 'r' prefix
    s =  '(' + ar.main(s)[0] + ')'             # simplify 
    if '+' in the_rest:                              # '(scalar)a+b'    
       a, b = the_rest.split('+')                # extract the rows           
       op = [3,s,int(a),int(b)]                        # type 3 
    else:                              # remaining case '(scalar)a'
       op = [2,s,int(the_rest), '']                      # type 2
    return op

def op2sym(op):
    if op[0] == 1:                           #[1,'',a,b], a<->b
        a = op[2]; b = op[3]            # adjust rows
        op = 'r' + str(a) + '<->' + 'r' + str(b)
    elif op[0] == 2:                      # [2,t,a,''], (t)a
        scalar = op[1]; a = op[2]
        op = scalar + 'r' + str(a)          
    else:                              # [3,t,a,b], (t)a + b
        scalar = op[1]
        a = op[2]                     
        b = op[3]
        op = scalar + 'r' + str(a) +  '+' + 'r' + str(b)
    return op

'''
print('symbolic form:      ','list form:')
print('r2<->r3             ',sym2op('r2<->r3'))
print('(4.2-7/2i + 3.2i)r5 ',sym2op('(4.2-7/2i + 3.2i)r5'))
print('(4.6/5.78)r7 + r11  ',sym2op('(4.6/5.78)r7 + r11'),'\n')

print(op2sym([1,'',7,5]))
print(op2sym([2,'(2+3i)',7,'']))
print(op2sym([3,'(2+3i)',7,5]),'\n')

print('r2<->r3', op2sym(sym2op('r2<->r3')))
print('(4.2-7/2i + 3.2i)r5',op2sym(sym2op('(4.2-7/2i + 3.2i)r5')))
print('(4.6/5.78)r7 + r11',op2sym(sym2op('(4.6/5.78)r7 + r11')),'\n')
'''


############################### row_op_calc ################################


def row_op_calc(op, A):  # op = operation in list form, matrix A   
    nrows, ncols = len(A), len(A[0])      
    optype = op[0]; scalar = op[1]     
    B = tl.copylist(A)
    if optype == 1:                # switch rowa and rowb
        for j in range(ncols):
            rowa = op[2]-1; rowb = op[3]-1     # for list notation
            temp = B[rowa][j]       # store rowa entry
            B[rowa][j] = B[rowb][j] # copy rowb entry into rowa
            B[rowb][j] = temp       # copy old rowa entry into rowb            
    elif optype == 2:              # scalar mult
        rowa = op[2]-1 
        for j in range(ncols):      # scalar times row   
            a = '(' + scalar + ')(' + B[rowa][j] + ')'         
            B[rowa][j] = ar.main(a)[0]               
    elif optype == 3:              # add scalar*rowa to rowb
        rowa = op[2]-1; rowb = op[3]-1 
        for j in range(ncols):              
            a = '(' + scalar + ')(' + B[rowa][j] + ')+' + B[rowb][j]
            a = tl.fix_signs(a)                        
            B[rowb][j] = ar.main(a)[0]       
    return B  


def run_ops(opsyms_list,A):                  # apply a list of opsyms to A
    #print('       A')
    tl.format_print(A,2,'right'); print('\n') 
    B = tl.copylist(A)
    for opsym in opsyms_list:
        op = sym2op(opsym)           # convert operation to list form
        B = row_op_calc(op,B)        
        #print('  ',opsym) 
        tl.format_print(B,2,'right'); print('\n')
    return B

'''
opsyms = 'r1<->r2,(1/2)r1,(-7)r1+r3,(-4)r1+r2,\
         (-1)r2+r3,(-1)r2+r1,(-2/3)r3,(-3/2)r3+r1'
opsyms_list = opsyms.split(',')
A ='4,5,6,12; 2,2,3,9; 7,8,9,15'
A = tl.string2table(A)
#print('matrix:',A)
print(run_ops(opsyms_list,A))
'''


################################ row_echelon ###############################


def row_echelon(A):        
    global prod, switches      # for future use
    global ops
    prod = '1'; switches = 0           # initialize (later chapter)              
    ops = []
    nrows, ncols = len(A), len(A[0])
    toprow = 0; row = 0; col = 0         # begin here  
    B = tl.copylist(A)                        # don't change A

    while toprow < nrows and col < ncols:      # find pivot columns
        row = toprow                  # potential leading entry row
      # search in col and below toprow for row with entry != 0:
        while row < nrows and B[row][col] == '0':
            row += 1   # keep going until found entry!=0 in col   
        if row < nrows:        
            if B[row][col] != '0':            # if found entry != 0       
                # update prod and move row to first
                prod = '('+ prod +')('+ B[row][col] +')'
                prod = ar.main(prod)[0] 
                if row != toprow:              
                    switches += 1                          # update
                    op = [1,'',row+1,toprow+1]  # switch row and toprow
                    ops.append(op)                  # keep a record
                    B = row_op_calc(op, B)               # switched                                 
                B =  clear_col(B, toprow, col)    # toprow lead row
                toprow = toprow + 1                   # next toprow
        col = col + 1     # next col to search for next pivot entry
    return B, ops # return echelon form and operations 
   

def clear_col(B, toprow, col):                 
    global ops
    nrows, ncols = len(B), len(B[0])
    pivot_entry = B[toprow][col]           # use entry to clear col
    scalar = '1/(' + pivot_entry + ')'  
    op = [2, scalar, toprow+1, '']     # divide toprow by pivot_entry
    ops.append(op)                                   # save for log
    B = row_op_calc(op, B)           # make the division
       # replace each row by 'row -B[row, col]*toprow:
    for row in range(nrows):  
        if row == toprow or B[row][col] == '0':
            continue        # skip toprow and zero entry multiplier      
        simplify = ar.main('-' + '(' + B[row][col] + ')')[0]        
        op = [3, '(' + simplify + ')', toprow+1, row+1]       
        B =  row_op_calc(op, B)             # do the operation on B
        ops.append(op)                               # save for log   
    return B

#A =  '0,1,0;2,0,0;0,0,3'
#A =  '1.2,3/4;5.6^2,7;8,9' 
#A = '4.5,5,6,12;1,-2,3,9;7,8.24,9,15'
#A =  '4,5,6,12;1,2.8,3,9;7,8,9,15'
#A =  '0,-3,-6,4,9;-1,-2,-1,3,1;-2,-3,0,3,-1;1,4,5,-9,-7' 
#A =  '1,-6,4,-2;-1,-5,0,4;2,7,-3,1'   
#A = '0,0,1,-1,-2;2,-4,-2,4,18;-1,2,3,-5,-16'  
#A =  '1,2,3,4,5,6,7,8,9,10; 11,12,13,14,15,16,17,18,19,20; 21,22,23,24,25,26,27,28,29,30; 31,32,33,34,35,36,37,38,39,40; 41,42,43,44,45,46,47,48,49,50'
#A = '0,1,0; 2,0,0; 0,0,3'
#A = '1.2,3/4; 5.6^2,7; 8,9' 
#A ='4.5,5,6,12; 1,-2,3,9; 7,8.24,9,15'
#A = '4,5,6,12; 1,2.8,3,9; 7,8,9,15'
#A = '1,-6,4,-2; -1,-5,0,4; 2,7,-3,1'
#A = '0,0,1,-1,-2;2,-4,-2,4,18;-1,2,3,-5,-16'
#A = '1,2,3,4,5i,6,7,8,9,10;11,12,13,14i,15,16,17,18,19,20; 21i,22,23,24,25,26,27,28,29,30'
#A = '0,2,3;4,5,6;7,8,9'             
#A =  '0,-11,7-4i,-10; -i,-2,7.8+3.8i,-15; 1,i,1,-20'
#A = '0,-3,-6,4,9;-1,-2,-1,3,1;-2,-3,0,3,-1;1,4,5,-9,-7'  
A =  '1/3,-11,7-4i,-10; -i,-2,7.8+3.8i,-15; 1,i,1,-20'
#A = '6,1,1;4,-2,5;2,8,7'
#A = '0,0,0,1; 0,0,2,0; 0,3,0,0; 4,0,0,0'

'''
A = tl.string2table(A)
print('              A')
tl.format_print(A,2,'right')
print('\n')
B, ops = row_echelon(A)
#print('\n',ops,'\n')
print('              reduced')
tl.format_print(B,2,'right')
'''

################################ col_echelon ###############################

def transpose(A):
    nrows, ncols = len(A),len(A[0])
    T = [['' for j in range(nrows)] for i in range(ncols)] 
    for j in range(nrows):
        for i in range(ncols):                      
            T[i][j] = A[j][i] 
    return T

def col_echelon(A):
    T = transpose(A)
    return transpose(row_echelon(T)[0])

'''
A = '1,-2,3,-4,5;-6,7,-8,9,-10;11,-12,13,-14,15'
A = tl.string2table(A)
#print('A:')
tl.format_print(A,2,'right');print('\n')

RA = row_echelon(A)[0]
print('row echelon of A:')
tl.format_print(RA,2,'right');print('\n')

CA = col_echelon(A)
print('col echelon of A:')
tl.format_print(CA,2,'right');print('\n')

CRA = col_echelon(RA)
print('col echelon of row echelon A:')
tl.format_print(CRA,2,'right');print('\n')

RCA = row_echelon(CA)[0]
print('row echelon of col echelon A:')
tl.format_print(RCA,2,'right')
'''


############################## linear systems ##############################


def is_zero_row(row):
    L = len(row)
    for entry in row:
       if entry == '0': L -=1    
    return L == 0


def has_zeros_one_row(R):                   
    for row in R:      
        num_zeros = 0
        if row[len(row)-1] != '1':
           continue
        for j in range(len(row)-1):           
            if row[j] == '0': num_zeros += 1
        if num_zeros == len(row)-1: 
           return True               
    return False

def get_system_variables(equations):    
    variables = []    
    for eqn in equations:      
        eqn = eqn.replace(' ','')        
        variables += tl.get_vars(eqn)[0]
    return sorted(list(set(variables)))    


def make_variables(dim,letter):      
    varlist = []    
    for n in range(1,dim+1):  
       varlist.append(letter+ str(n))           
    return varlist

def insert_coeff(expr,vars):
    expr = expr.replace(' ','')
    if expr[0] in vars: expr = '1'+expr
    i = 1
    while i < len(expr): 
        if expr[i] in vars and expr[i-1] in '(+-':
            expr = expr[:i]+'1'+ expr[i:]
        i += 1  
    return expr



############################ equations to augmat ###########################

def insert_coeff(eqn,varbs):
    eqn = eqn.replace(' ','')
    if eqn[0] in varbs: eqn = '1'+eqn
    i = 1
    while i < len(eqn): 
        if eqn[i] in varbs and eqn[i-1] in '(+-':
            eqn = eqn[:i]+'1'+ eqn[i:]
        i += 1  
    return eqn


def insert_delimiters(eqn):         # place commas around variables       
    letters = tl.letters
    eqn = insert_coeff(eqn,letters) # attach missing 1      
    for letter in letters:              # place comma before letter
        eqn = eqn.replace(letter,','+letter)    
    i = 0
    while i < len(eqn):     
        if eqn[i] not in letters:                # skip non letters
            i += 1; continue                            
        start = i+1                            # index j after variable                
        end = tl.movepast(eqn,start,'1234567890')        
        eqn =  tl.insert_string(eqn,',',end)[0]  # insert at position end      
        #eqn = eqn[0:end] + ',' + eqn[end:]   # place comma after letter
        i = end     
    return eqn     
      
#eqn = 'v+x4+3x1+4x2+5x3-u+6=7'
#print(insert_delimiters(eqn))


def eqn2row(eqn,varlist):         # convert equation to augmat row  
    eqn = insert_delimiters(eqn)   # enclose variables with commas  
    #print('delimiters  ',eqn,'\n')    
    components = eqn.split(',')        # split off vars and coeffs      
    #print('components  ',components,'\n')    
    C = len(components)                                             
    last = components[C-1]                                            
    if last[0] != '=':        # place constant if any on right  
        last = last.split('=')                                      
        new_right_side = last[1] + '-(' + last[0] + ')'             
        new_right_side = ar.main(new_right_side)[0]            
        components[C-1]= new_right_side                              
                                                                    
    V = len(varlist)                                                
    components[C-1] = components[C-1].replace('=','')  # right side 
    row = ['0' for k in range(V)]       # initialize row with zeros 
                                                                    
    for i in range(V):     # run through variables in varlist order 
        var = varlist[i]             # var in position i in varlist 
        for j in range(0,C-2,2): # 2-step iteration; stop before '='
            c = components[j]                         # coefficient 
            v = components[j+1]                          # variable 
            if var == v:                                            
               row[i] = c   # put coeff of var in position i of row 
                                                                    
    row.append(components[C-1])  # last component: put on right side
    for i in range(len(row)):                                       
        row[i] = tl.fix_signs(row[i])                              
    return row                                                      

'''
varlist = ['x1','x2','x3','x4','u','v']
eqn = '5v-3x4+5x1-4x2+11x3-9u+8=-7'
#eqn = '3x1+4x2+5x3=7'
print(eqn)
print(varlist)
print('row         ',eqn2row(eqn,varlist))
'''

def get_augmat(eqnlist,varlist):   
    augmat = []
    for eqn in eqnlist:
        row = eqn2row(eqn,varlist) 
        augmat.append(row)
    return augmat 

'''
eqnlist = ['x4+3x1+4x2+5x3-u=7','5v-7x1+9x2-x3+u=-67','2x2-4x3=3.2i']
A = get_augmat(eqnlist,varlist)
tlk.format_#print(A, 3, 'right')
'''

def get_solution_list(reduced,varlist):                              
    if has_zeros_one_row(reduced):                      
        return []                     # no solution
    
    sol_list = tl.copylist(varlist)   # initialize
    L = len(reduced)                  # number of rows
    M = len(reduced[0])               # number of columns
    
    for k in range(L):                # run throught rows              
        if is_zero_row(reduced[k]):
            break
        right_side = reduced[k][M-1]  # last entry in row                
        idx = reduced[k].index('1')   # column of leading entry '1'                        
        v = varlist[idx]              # corresponding variable                                 
      
        # subtract other variables from right side:
        for j in range(idx+1,M-1):
            #right_side = right_side + '-('+reduced[k][j]+')' + varlist[j]
            right_side = right_side + '-'+reduced[k][j]+ varlist[j]
            
            right_side = tl.fix_signs(right_side)   
                 
        right_side = mu.main(right_side)[0]                            
        sol_list[idx] = v + '='   + right_side      
    return sol_list


def linsolve(equations,augmat,letter,display):              
    global varlist                           
    if equations != []:            
        eqnlist = equations.split(',')        # strings to lists                            
        varlist = get_system_variables(eqnlist)                     
        augmat = get_augmat(eqnlist,varlist)  # create augmented matrix                 
    
    else:
         varlist = make_variables(len(augmat[0])-1,letter)   
    
    if display:
        print('augmat:')                         # intermediate display
        tl.format_print(augmat,4, 'right'); print('\n')       
    
    reduced = row_echelon(augmat)[0]      # get row reduced form 
          
    if display:
        print('reduced:')
        tl.format_print(reduced,4, 'right');print('\n')  
    
    sol_list = get_solution_list(reduced,varlist)              
    return sol_list 


################################## examples #################################

e1 =   'x2   +  x3   +  x4  + x5 = 1,\
            x1   +  x3   +  x4  + x5 = 2, \
            x1   +  x2   +  x4  + x5 = 3,\
            x1   +  x2   +  x3  + x5 = 4,\
            x1   +  x2   +  x3  + x4 = 5'    

e2 = '-x3 +x5 - x6 -((5.2+(2.5)i)^4)x11 = 4/(7.3 + 7.8i),\
          7x1 - (5/(2.1+3i)^(-5))x10 = 3-10i,\
          2.1ix4 + x6 -x9 = 3.2'         

e3 = 'x1+2x2+3x3+4x4=5,\
          6x1+7x2+8x3+9x4=10,\
          11x1+12x2+13x3+14x4=15,\
          16x1  +  17x2  +  18x3  + 19x4  = 20'
                   
e4 = ' x1   +  2x2   +  3x3   + 4x4  + 5x5 = 6,  \
           7x1  +  8x2   +  9x3   + 10x4 + 11x5 = 0,\
          13x1  +  14x2  +  15x3  + 16x4 + 17x5 = 18'

e5 = '-s +x5 - x6 -(5.2+(2.5)i)^4x11 = 4/(7.3 + 7.8i), \
          7x3 - 5/(2.1+3i)^(-5)x1 = 10000i, \
          2.1ix4 + x6 -x9 = 3.2'

e6 = ' x1   +  2x2   +  3x3   + 4x4  + 5x5 = 6, \
          7x1   +  8x2   +  9x3   + 10x4 + 11x5 = 12,\
         13x1  +  14x2  +  15x3  + 16x4 + 17x5 = 18'
#sol: x1 = x3 + 2x4 + 3x5 - 4, x2 = - 2x3 - 3x4 - 4x5 + 5


#### book
e7 =  '4x1  +  5x2  +  6x3 = 12,\
              2x1  +  2x2  +  3x3 = 9, \
              7x1  +  8x2  +  9x3 = 15'

e7a =  '4x1  +  5x2  +  6x3 = 12,\
              2x1  -  2x2  -  3x3 = 9, \
              7x1  +  8x2  +  9x3 = 15'


#### book
e8 = 'x1  +   2x2  +  3x3   +  4x4  +  5x5 = 6,\
     7x1  +   8x2  +  9x3   + 10x4  + 11x5 = 12, \
    13x1  +  14x2  +  15x3  + 16x4  + 17x5 = 18, \
    19x1  +  20x2  +  21x3  + 22x4  + 23x5 = 23'

#### book
e9 = ' x1   +  2x2   +  3x3   + 4x4  + 5x5 = 6,\
      7x1  +  8x2   +  9x3   + 10x4 + 11x5 = 12, \
     13x1  +  14x2  +  15x3  + 16x4 + 17x5 = 18'

#### book  
e10 = '     (1+i)x2 +  (2+i)x3  +  x4  + x5 = 1/2,\
           x1                  +  x3  +  x4  + x5 = 2/3, \
           x1      +  x2              +  x4  + x5 = 3/4, \
           x1      +  x2       +  x3  +        x5 = 4/5, \
           x1      +  x2       +  x3  + x4       = 5/6'


'''
e = e10
solution_list = linsolve(e,[],'',True)
print(solution_list)
'''

'''
a1 = '1,2,3,4,5,6,7,8,9,0; 11,12,13,14,15,16,17,18,19,0;\
          9,8,7,6,5,4,3,2,1,0'
a2 = '0,4,7,1;0,5,8,2;0,6,9,3'
a3 = '4,7,1;5,8,2;6,9,3'
a4 = '1,2,3,4,0;5,6,7,8,0;9,10,11,12,0'
a5 = '0,1,2,3,0;0,4,5,6,0;0,7,8,9,0'
a6 = '1,2,3,4,5,0;6,7,8,9,10,0;11,12,13,14,15,0'
a7 = '0,2,3,4,5,0;0,7,8,9,10,0;0,12,13,14,15,0'
a8 = '1,2,3,4,5; 6,7,8,9,10; 11,12,13,14,15; 16,17,18,19,20'
a9 = '11,16,6;12,17,7;13,18,8;14,19,9;15,20,10'
a10 = '0,-1,0,0;-1,1,1,0;0,-1,0,0'
a11 = '3A-1= 0,3A+2B-2= 0,A+C+B-1= 0'


a = a6
a = tl.string2table(a)
solution_list = linsolve([],a,'x',True)
print(solution_list)
'''

def check_solution(equations,solutions,val):                                  
    eqnlist = equations.split(',')                                        
    if solutions == []:                                                   
        #print('no solution')                                              
        return                                                            
    for eqn in eqnlist:              # run through given equations        
        for sol in solutions:    # run through generated solutions        
            var,val = sol.split('=')                    # separate        
            var = var.replace(' ','')                                     
            val = val.replace(' ','')                                     
            eqn = eqn.replace(var,'('+ val +')')    # insert value        
        left_side,right_side = eqn.split('=')                             
        difference = left_side + '-('+ right_side +')'                    
        if ar.main(difference)[0] != '0':                            
            #print('solution false')      # left_side != right_side        
            return                                                        
    print('solution correct')                                             

#check_solution(e,solution_list,'1.001')                                  


