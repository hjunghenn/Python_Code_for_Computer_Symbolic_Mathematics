
#### MatAlg.py

import PolyAlg as pa
import LinSolve as ls
import Number as nm
import Arithmetic as ar
import Tools as tl
import math as ma


############################# mat ops ############################

def scalar_mult(z,A):  
    B = []
    for row in A:
        Brow = []
        for entry in row:
            prod = '('+z+')('+entry+')'          
            prod = ar.main(prod)[0]          
            Brow.append(prod)
        B.append(Brow)    
    return B

'''
z = '2/5'
#z = '3.2+(2/5)i'
A = '1,i,-3+7i; 22,-5+i,6+(2/3)i; -7+2i,8,1/3.7'
Atab = tl.string2table(A)
print('            A')
tl.format_print(Atab, 2, 'right')
#B = scalar_mult(z,Atab)
print('\n')
print('                     zA')
tl.format_print(scalar_mult(z,Atab), 2, 'right')
'''


def factor_matrix(A):
    B = tl.copylist(A)
    Bflat = tl.flatten_double_list(B)    
    denoms = pa.get_denoms(Bflat)                     
    lcm = nm.listlcm(denoms)                   # get lcm of denoms   
    lcm = str(lcm)
    C = scalar_mult(lcm,B)                     # clear denominators     
    g = int(C[0][0])

    for row in C:
        for entry in row:                        # get gcd of entries 
            g = ma.gcd(g,int(entry))                
    r = '1/' + str(g)
    D = scalar_mult(r,C)                              # divide by gcd
    factor = ar.main(str(g) + '/' + lcm)[0]
    factor = tl.add_parens(factor)
    return factor,D

'''
A = [['6/7', '30/11', '12/5'], ['24/13', '30/17', '18'],
        ['32/9', '132/7', '24/7']]
print('A:')
tl.format_print(A,3, 'right'); print('\n')
factor, B = factor_matrix(A)
print('factorization:')
print(factor,'times')
tl.format_print(B,3,'right'); print('\n')
print('check:')
tl.format_print(scalar_mult(factor,B),3, 'right')
'''


'''
A = [['6/7', '30/11', '12/5'], ['24/13', '30/17', '18'], ['32/9', '132/7', '24/7']]    
tl.format_print(A,3, 'right')
print('\n')
factor, B = factor_matrix(A)
print(factor)
tl.format_print(B,3, 'right')
#check:
print('\n')
tl.format_print(scalar_mult(factor,B),3, 'right')
'''
    

def add_mat(A,B):      
    C = []
    for i in range(len(A)):
        Crow = []
        for j in range(len(A[0])):
            sum = ar.main(A[i][j]+'+('+B[i][j]+')')[0]
            Crow.append(sum)
        C.append(Crow)
    return C


def subt_mat(A,B):
    C =  scalar_mult('-1',B)
    if A == '0':
        return C
    return add_mat(A,C)

'''             
A = tl.string2table('1,2,3;4,5,6')
B = tl.string2table('6,5,4;3,2,1')
C = add_mat(A,B)    
D = subt_mat(A,B)   
print('     A')
tl.format_print(A,2,'right')
print('\n')
print('     B')
tl.format_print(B,2,'right')
print('\n')
print('   A + B')
tl.format_print(C,2,'right')
print('\n')
print('     A - B')
tl.format_print(D,2,'right')
'''


def mult_mat(A,B):                                                       
    if isinstance(A,str):       
        return scalar_mult(A,B)                                          
    if isinstance(B,str):                                                
        return scalar_mult(B,A)                                          
    C = []                                                               
    for i in range(len(A)):                # run through rows of A
        Crow = []                                                        
        for j in range(len(B[0])):         # run through cols of B
            s = '0'                                                      
            for k in range(len(A[0])):  
                s =  s + '+('+A[i][k]+')('+B[k][j]+')'                                  
                s = ar.main(s)[0]                                
            Crow.append(s)                                               
        C.append(Crow)                                                       
    return C                                            

'''
A = tl.string2table('1,2,3,4;5,6,7,8;9,10,11,12')
I = tl.string2table('1,0,0,0;0,1,0,0;0,0,1,0;0,0,0,1')
#B = tls.string2table('1,1,1,1;1,1,1,1;1,1,1,1;1,1,1,1')
AI = mult_mat(A,I)
print('        A')
tl.format_print(A,2,'right');print('\n')
print('       I')
tl.format_print(I,2,'right');print('\n')
print('       AI')
tl.format_print(AI,2,'right'); print('\n')
I = tl.string2table('1,0,0;0,1,0,;0,0,1')
print('     I')
IA = mult_mat(I,A)
tl.format_print(I,2,'right');print('\n')
print('       IA')
tl.format_print(IA,2,'right');print('\n')
'''


def makeid(n):
    global I
    I = [['0' for j in range(n)] for i in range(n)]
    for i in range(n):   
         for j in range(n):    
             if i == j: I[i][j] = '1'   # 1's along the diagonal
    return I

def attach_id(A):                    
    nrows =len(A)
    I = makeid(nrows)   
    B = ls.transpose(A)
    C = []
    for i in range(nrows):              #  put rows of B in C
        C.append(B[i])
    for row in I:                            # put I below B
        C.append(row)       
    return ls.transpose(C)    

def split_mat(A):     # into right and left parts    
    B = ls.transpose(A)
    nrows = len(A)
    top = []; bottom = []    
    for i in range(nrows):
        top.append(B[i])    
    for i in range(nrows,2*nrows):
        bottom.append(B[i]) 
    return ls.transpose(top), ls.transpose(bottom)

'''
A = tl.string2table('a,b,c,d,e,f; g,h,i,j,k,l;m,n,o,p,q,r')   
left_part,right_part = split_mat(A)
tl.format_print(A,1,'left'); print('\n')
tl.format_print(left_part,1,'left'); print('\n')
tl.format_print(right_part,1,'left')
'''

def invert_mat(A):
    nrows = len(A)
    B = attach_id(A)        # attach identity I to right of A
    C = ls.row_echelon(B)[0]         # row reduce  
    left,right = split_mat(C)    # extract left and right parts
    I = makeid(nrows)                
    if left == I:                    # compare left part with I
        return right                 # inverse exists
    else: return []                  # fails to exist

'''
A = '1+2i,2,3;4,5+3i,6;7,8,9+4i'
#A = '1,0,3;0,5,6;7,8,0'
print('A')
A = tl.string2table(A)
tl.format_print(A,4,'left')
print('\n')
X = invert_mat(A)
print('A^(-1)')
tl.format_print(X,4,'left')
print('\n')
print('check AA^(-1):')
tl.format_print(mult_mat(A,X),4,'left')
'''

def power_mat(A,p):
    if p == 0: 
        return makeid(len(A))
    if p == 1: 
        return A
    B = tl.copylist(A)
    if p < 0: 
        B = invert_mat(A)                                  # get A^(-1)
        p = -p 
    if B == []: 
        return []
    prod = B
    for i in range(p-1):           # multiply B times itself p-1 times
        prod = mult_mat(prod,B)
    return prod

'''
#A = '1/3, 0, 7-4i; -i, -2, 7.8+3.8i; i,  1, -20'
A = '3,1,2;5,4,7;-1,8,3'
A = tl.string2table(A)
B = power_mat(A,7)
C = power_mat(A,-3)
D = mult_mat(B,C)  
E = power_mat(A,4)

print('A')
tl.format_print(A,2,'right'); print('\n') 
print('A^7')
tl.format_print(B,2,'right'); print('\n') 
print('A^(-3)')
tl.format_print(C,2,'right'); print('\n') 
print('A^7*A^(-3)')
tl.format_print(D,2,'right'); print('\n') 
print('A^4')
tl.format_print(E,2,'right')
'''

############################# mat calc ############################

def load_dict(matrices):
    global mat_dict
    mat_dict = {}
    for mat in matrices:              # run through the set of matrices
        mat = mat.replace(' ','')
        label, entries = mat.split('=')   # left and right parts of def.
        mat_dict[label] = tl.string2table(entries) # enter in dictionary
   
def print_mat_dict():
    global mat_dict
    for item in mat_dict:
        print('    ',item)
        tl.format_print(mat_dict[item],2,'right')
        print('\n')

'''
matrices = ['A = 1,0,3;0,5,6;7,8,0',\
            'B = 0,2,3;4,6,0;7,0,9', \
            'C = -5,0,7;8,-1,0;4,3,0']
load_dict(matrices)
print_mat_dict()
'''

def allocate_ops(mode):
    global expr
    global idx            
    global mat_dict
    r = []
   
    while idx < len(expr):
        ch = expr[idx]

        if tl.isnumeric(ch):
            z,idx = tl.extract_numeric(expr,idx)
            r = ar.main(z)[0]
        
        elif tl.isupper(ch): 
            r = mat_dict[ch]
            idx += 1
                           
        elif ch == '+':
            if mode > 0: break              # wait for higher mode
            idx += 1
            s = allocate_ops(0)
            r = add_mat(r,s)

        elif ch == '-':
            if mode > 0: break              # wait for higher mode
            idx += 1
            s = allocate_ops(1)
            r = subt_mat(r,s)
        
        elif ch == '*':
            idx += 1
            s = allocate_ops(1)
            r = mult_mat(r,s)
                   
        elif ch == '^':                       # highest mode         
            if expr[idx+1] == 't':
                r = ls.transpose(r)
                idx+=2                  # skip ^t and move on
                continue                      
            exp,idx = tl.extract_exp(expr,idx)                
            exp = ar.main(exp)[0]        # fix exp = 0-1
            
            if isinstance(r,str):
                r = ar.main( '('+ r + ')^(' + exp + ')')[0]                                           
            else: 
                r = power_mat(r, int(exp))
                if r == []: return r       # inverse may not exist
        
        elif ch == '(':        
            start = idx                        
                        
            paren_expr,end = tl.extract_paren(expr,start)
                       
            if tl.isarithmetic(paren_expr):
                 r = ar.main(paren_expr)[0]                 
                 idx = end                           
            else:
                 idx+=1
                 r = allocate_ops(0)
                 idx+=1
        elif ch == ')': break
    return r


def calculator(expression,matrices):   
    global expr
    global idx     
    global mat_dict
    #print(545,expression,matrices)
    load_dict(matrices)
    expr = expression         
    expr = expr.replace(' ','')    
    #expr = tlk.attach_missing_coeff(expr,tlk.upper)                    
    expr = tl.attach_missing_exp(expr,tl.upper+'t')                      
    expr = tl.fix_signs(expr)                                     
    expr = tl.fix_operands(expr)                                  
    expr = tl.insert_asterisks(expr,tl.upper)         
    idx = 0   
    r = allocate_ops(0)        
    return r

'''
mat1 = ['A = 1,-1;2,3']
expr1 = 'A^2 - 4A + 5A^0'


mat2 = ['A = 1,2,1;0,-5,0;1,8,1']
expr2 = 'A^3-3A^2+10A'

mat3  = ['A = 1,2;3,4']
expr3 = 'A^2-5A-2A^0'

mat4  =['A = 1,0,0,0;3,2,0,0;5,-2,3,0;-1,4,7,4']
expr4 = 'A^4-10A^3+35A^2-50A+24A^0'

mat5 = ['A = 1,0,3;0,5,6;7,8,0','B = 1,1,1;1,1,1;1,1,1']
expr5 = 'A^(-1)*A'

mat6 = ['A = 1,0,3;0,5,6;7,8,0','B = 1,1,1;1,1,1;1,1,1']
expr6 = 'A-(2/3+.1i)B'

mat7 =\
['A = 1,0,3;0,5,6;7,8,0', \
'C = 1/3-(1/10)i,-2/3-(1/10)i,7/3-(1/10)i; \
-2/3-(1/10)i,13/3-(1/10)i,16/3-(1/10)i;\
19/3-(1/10)i, 22/3-(1/10)i,-2/3-(1/10)i']
expr7 = '(2/3+.1i)^(-1)(A-C)'

mat8 = ['C = 1+(2/3)i,-2,2i; -4,-1+(10/3)i,6+4i,(14/3)i,8+(16/3)i-9', \
            'B = 0,2,3;4,6,0;7,0,9']
expr8 = '(2i/3+1)^(-1)(C+4B)'

mat9 =  ['A = 1,2,3;4,5,6;7,8,9']
expr9 = '-A^3+15A^2+18A'
expr9A = '3A^2+(1+i)^2A+7A^0'

d1 = '(A+B)^t - A^t - B^t'
d2 = '(AB)^t - B^tA^t'
d3 = '(AB)^(-1) - B^(-1)A^(-1)'
d4 = '(A^t)^(-1) - (A^(-1))^t'
d5 = '(A+B)C - AC - BC'
d6 = '(A^t)^(-1)-(A^(-1))^t' 
D = [d1,d2,d3,d4,d5,d6]
matrices = ['A = 3,0,1  ;7,6,0  ;0,8,9',\
            'B = 0,2,3  ;4,0,6  ;7,8,0',\
            'C = 2,0,-3 ;0,6,-2 ;-7,4,0']

for d in D:
    tl.format_print(calculator(d,matrices),2,'right')
    print('\n')
'''


############################### moore penrose ########################

def delete_cols(A,col_list):           
    ncols = len(A[0])                  
    At = ls.transpose(A)                  
    B = []                             
    for j in range(ncols):             
        if j in col_list:          
            B.append(At[j])             
    C = ls.transpose(B)                   
    return C                           
                                       
def delete_last_rows(R,k):             
    D = []                             
    for i in range(k+1):          
        D.append(R[i])
    return D                           
                                       
def leading_entry_cols(R):             
    lead_cols = []                     
    for i in range(len(R)):            
        for j in range(len(R)):        
            if R[i][j] != '0':          
               lead_cols.append(j)     
               break   
    return lead_cols                   
                                       
def decompose(A):                          
    R = ls.row_echelon(A)[0]           
    lead_cols = leading_entry_cols(R)  
    r = len(lead_cols)
    m = len(A)
    C = delete_cols(A, lead_cols)     # delete all but these cols of A   
    D = delete_last_rows(R,m-r)       # delete rows r+1,...,m       
    return C,D,R

def moore_penrose(A):
    C,D,R = decompose(A)       
    
    tl.format_print(mult_mat(C,D),3,'right');  print('\n')
    print('     R')
    tl.format_print(R,3,'right');  print('\n')
    print('     C')
    tl.format_print(C,3,'right');  print('\n')
    print('     D')
    tl.format_print(D,3,'right');  print('\n')
    
    C = tl.table2string(C)
    D = tl.table2string(D)
    Aplus = 'D^t(DD^t)^(-1)(C^tC)^(-1)C^t'
    matrices = ['C='+C,'D='+D]    
    return calculator(Aplus,matrices)

'''
A = '1,2,3,4,5,6; \
     7,8,9,10,11,12; \
     13,14,15,16,17,18; \
     19,20,21,22,23,24'    

A = '1,2,3,12;4,5,6,15;7,8,9,18' 

A = '4,5,6;1,2,3;7,8,9'
B = '12,9,14'             

A = '4,5,6;1,2,3;7,8,9'
B = '12,9,14'             

A = tl.string2table(A)
B = tl.string2table(B)
print('      A')
tl.format_print(A,3, 'right'); print('\n')       
print('   B^t:')
tl.format_print(ls.transpose(B),3, 'right'); print('\n')       
Aplus = moore_penrose(A)
print('           Aplus')
tl.format_print(Aplus,3,'right'); print('\n')    
LS = mult_mat(Aplus,ls.transpose(B))
print('   minimal least squares solution')
tl.format_print(LS,3,'right')   
#print('\n')
#print(mult_mat(invert_mat(A),transpose(B)))
'''

  
################################ poly_fit ##############################

def S(k,data):   # returns S_k
    s_sum = '0'
    for j in range(len(data)):       
        x = data[j][0]
        power = x + '^' + str(k)        
        s_sum = ar.main(s_sum + '+' + power)[0]
    return s_sum 

def S_mat(m,data): # returns matrix of S_k entries 
    s_mat = []
    for i in range(m+1):
        row = []
        for j in range(m+1):
            row.append(S(i+j,data))
        s_mat.append(row)
    return s_mat 

def T(k,data):    # returns T_k
    t_sum = '0'
    for j in range(len(data)):
        x = data[j][0]; y = data[j][1]
        power_prod = '('+ x + '^'+ str(k)+ ')*('+ y + ')'
        t_sum = ar.main(t_sum + '+' + power_prod)[0]
    return t_sum 

def T_mat(m,data): # returns column matrix of T_k entries 
    t_mat = []
    for k in range(m+1):
        t_mat.append([T(k,data)])
    return t_mat 

def poly_fit(data,m):
    data = pa.data2lists(data) 
    if len(data) <= m: return
    s_mat = S_mat(m,data)    
    
    #R = ec.row_echelon(s_mat)[0]
    #tlk.format_print(s_mat, 2, 'right'); print('\n')   
    #tlk.format_print(R, 2, 'right'); print('\n')  

    t_mat = T_mat(m,data) 
    s_mat_inv = invert_mat(s_mat)  
    C = mult_mat(s_mat_inv,t_mat)  # C = s_mat^(-1)*t_mat
    #C = tlk.table2string(C)   
   
    flist = tl.flatten_double_list(C)
    flist = flist[::-1]                  # reverse flist
    pa.var = 'x'
    return pa.flist2pol(flist)


data1 = '(6,2.3),(4.5,8),(11,12.8),(7,6),(14.99,33)'  # num = 5
data2 = '(1,3),(2,1.1),(3,5),(4,4.2),(5,9),(6,8.1)'   # num = 6
data3 = '(1,3),(2,1.1),(3,5),(4,4.2),(5,8.1)'   # num = 5
data4 = '(1,3.7), (2,1.4), (3,5.3), (4,4.2), (5,8.1)'  
# need m < num data; get exact fit when m = n-1

data = data2
pol1 = poly_fit(data,1)
pol2 = poly_fit(data,2)
pol3 = poly_fit(data,3)
pol4 = poly_fit(data,4)
pol5 = poly_fit(data,5)
pol6 = poly_fit(data,6)

print('degree 1  ',pol1,'\n')
print('degree 2  ',pol2,'\n')
print('degree 3  ',pol3,'\n')
print('degree 4  ',pol4,'\n')
print('degree 5  ',pol5,'\n')
print('lagrange  ',pa.lagrange_interp(data),'\n')
print('degree 6  ',pol6,'\n')



def comparisons(pols,data,p):
    data = pa.data2lists(data)        
    for m in range(1,len(pols)):  # run through the list of pols
        table = []           
        pol = pols[m]               
        error = '0'                                    # initialize
        for k in range(len(data)):  # run through the data points
            xk = data[k][0]
            yk = data[k][1]        
            xk = ar.main(xk)[0]      # convert x,y data to fractions
            yk = ar.main(yk)[0]                                 
            zk = ar.evaluate(pol,xk,p)[0]  # value of polynomial at x data                         
            diff_squared = '((' + zk + ')-(' + yk + '))^2'
            error = ar.main(error + '+' + diff_squared)[0]   
            yk = ar.decimal_approx(yk,p)[0]                # approx. y data            
            zk = ar.decimal_approx(zk,p)[0]                                                                    
            table.append(['  ',xk,yk,zk, '  '])                  
        error = ar.decimal_approx(error,p)[0]
        header = ['m = '+str(m), 'xk','yk','zk', 'error = '+ error]
        table = [header] + table
        tl.format_print(table, 4, 'right'); print('\n')

#pols  = ['',pol1,pol2,pol3,pol4,pol5]     # from previous run 
#comparisons(pols,data,4)

def Vandermonde(data):
    V = []
    n = len(data)
    for i in range(n):   
        row = []
        for j in range(n):
            x = data[i][0]
            row.append(ar.main(x + '^' + str(j)))
        V.append(row)
    return V     

#V = Vandermonde(data)
#print('V')
#tls.format_print(V,2,'left')



######################### elementary matrices #####################

def elementary_matrices(A):
       # returns list of elementary matrices and their product
       #nrows = len(A)
       I = makeid(len(A))   # ops are applied to identity matrix
       B, ops = ls.row_echelon(A) # echelon matrix and operations
       E = []
       Eprod = I        # intial factor in the product 
       n = 1 
       for op in ops:               # apply each op to I
           C = ls.row_op_calc(op,I)
           print('      E'+ str(n)); n+=1       # print a label for
           tl.format_print(C,2,'right') # the elementary mat C
           print('\n')
           E.append(C)                        # keep C
           Eprod = mult_mat(C,Eprod)      # update product 
       return E, Eprod
   
'''
A = '-2,0,3;0,5,6;7,8,0'
A = tl.string2table(A)
E,Eprod = elementary_matrices(A)
print('        Eprod')
tl.format_print(Eprod,2,'right')
print('\n')     
print('  Eprod*A')
tl.format_print(mult_mat(Eprod,A),2,'right')
'''

##################################################################

'''
A = '1,2,3;7,6,5;8,9,10;11,12,13;14,15,16'
A = '1,2,3;4,5,6;7,8,9'
A = '0,1,2,-1; -2,0,0,6; 4,-2,-4,-10'
A = '1,2,3;7,6,5;8,9,10;11,12,13;14,15,16;17,18,19'
#A = '1,2;3,4;5,6'
A =  '1/3, 0, 7-4i, -10;  -i, -2, 7.8+3.8i, -15;  1, i,  1, -20'

A = mt.string2mat(A)
print('A:')
mt.format_print(A,2,'left')
P,B = row_ele_mat_prod(A)
PA = mult_mat(P,A)
print('row echelon:')
mt.format_print(B,2,'left')
print('row mat prod PA:')
mt.format_print(PA,2,'left')
At = mt.transpose(A)
Qt,C = row_ele_mat_prod(At)
Q = mt.transpose(Qt)
AQ = mult_mat(A,Q)
print('col mat prod AQ:')
mt.format_print(AQ,2,'left')
print('col echelon A:')
mt.format_print(ec.col_echelon(A),2,'left')
R,D = row_ele_mat_prod(AQ)
RAQ = mult_mat(R,AQ)
print('PAQ:')
mt.format_print(RAQ,2,'left')
'''


##################################################################

'''
NOT USED
def conj_transpose(A):
    B = transpose(A)
    nrows, ncols = len(B),len(B[0])
    for i in range(nrows):
        for j in range(ncols):   # make column j of B row j of A                                           
            B[i][j] = ar.conj(A[i][j]) # don't have'
    return B

A = tlk.string2table('i,2+3i,3-4i,4;5,6-4.3i,7+(1/2)i,8')
B = conj_transpose(A)
print('        A ')         
tl.format_print(A,2,'right')
print('')
print(' A conjugate transpose ')
tl.format_print(B,2,'right')
'''    
   

