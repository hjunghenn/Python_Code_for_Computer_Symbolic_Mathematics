
import Tools as tl
import Arithmetic as ar
import LinSolve as ls
import MatAlg as mat
import Vectors as vec
import PolyAlg as pa
import PolyDiv as pd
import MultiAlg as mu

# string2table,string2list, 

############################# permutations ##############################


def permutations(n):                  # generates length n+1 perms 
    perms = [[k] for k in range(1,n+1)]    # first perm list (singles) 
    perm_lists = [perms]                    # put in list of perms 
    
    #print(perms)                           # print first perm list 
    
    for i in range(1,n):        # generate higher order perm lists 
        previous_perms = perm_lists[i-1]         
        new_perms = []                      
        for j in range(1,n+1):   # attach symbols to previous perms
            for k in range(len(previous_perms)):                   
                if j not in previous_perms[k]:                     
                    new_perms.append([j]+previous_perms[k])        
        perm_lists.append(new_perms)     # next higher length perm 
        #print(new_perms)                  # print newest perm list 
    return perm_lists[len(perm_lists)-1]                           

#print(permutations(3))

def permutation_sign(p):
    L = len(p)
    parity = 0
    for i in range(L):    
        for j in range(i+1,L):                
            if p[j]  < p[i]:   # if i before j and p[j] before p[i]
                parity += 1
    return (-1)**parity   

#p = [3,5,2,4,1]; q = [3,5,2,1,4]
#print(permutation_sign(p),',', permutation_sign(q))
   

############################### Leibnitz ################################

def perm_term(A,p):
    n = len(A[0])   # determinant size
    s = permutation_sign(p)
    prod = '1'    
    for j in range(n):        
        prod = ar.main('(' + prod + ')*('+ A[j][p[j]-1] +')')[0]      
    return  ar.main(str(s) + '*('+ prod +')')[0]      

'''
A = '1,2,3,4; 5,6,7,8; 9,10,11,12; 13,14,15,16'
A = tl.string2table(A)
#print(A)
p = [3,4,2,1]; q = [3,4,1,2]
print(perm_term(A,p))
'''

def det_leibnitz(A):
    n = len(A[0])   # determinant size   
    perms = permutations(n)    
    d = '0'    
    for p in perms:
        d = ar.main(d + '+(' + perm_term(A,p) + ')')[0]
    return d
'''
A = '1,2,3,4; 5,6,7,8; 9,10,11,12; 13,14,15,16'
A = '2,9,3;2,6,0;3,14,-5'
A = tl.string2table(A)
print(det_leibnitz(A))
'''

############################### Laplace #################################

def remove_row_col(A,row,col):
    n = len(A) # size of determinant
    B = []
    C = []
    D = []  
    for k in range(n):
        if k != row:            # skip row
            B.append(A[k])      
    C = ls.transpose(B)
    for k in range(n):
        if k != col:            # skip col 
            D.append(C[k])
    return ls.transpose(D)


def det_laplace(A):
    n = len(A)
    if n == 2:
        return ar.main( '('+ A[0][0] + ')('+ A[1][1] +')-\
                              ('+ A[1][0] +')('+ A[0][1] +')')[0]
    d = '0'                         
    for k in range(n):
        B = remove_row_col(A,0,k)
        sign = str((-1)**k)
        d = ar.main(d + '+('+ sign +')('+ A[0][k] +') \
                               ('+ det_laplace(B) + ')')[0]
    return d


def det_params(A):
    n = len(A)        
    if n == 2:
        return mu.main( '('+ A[0][0] + ')('+ A[1][1] +')-    \
                              (('+ A[1][0] +')('+ A[0][1] +'))')[0]
    d = '0'                         
    for k in range(n):        
        B = remove_row_col(A,0,k)                    
        sign = str((-1)**k)      
        d = mu.main(d + '+('+ sign +')('+ A[0][k] +') \
            ('+ det_params(B) + ')')[0]    
    return d


#A = [['-1','2x','3x^2'],['4x^3','-5x^4','6x^5'],['7x^6','8x^7','-9x^8']]
#A = [['1','-x','x^2'],['2','-x^3','x^4'],['3','-x^5','x^6']]
#A = '7-x,1,3;-3,2-x,-3;-3,-2,-1-x'
#A = '1-x,2;3,2-x' 
#A = '1-x,1,2y;3,2-ax,-1;-1,2,3-xz'
#A = tl.string2table(A)
#print(det_params(A))


############################### echelon #################################


def det_echelon(A):   
    n = len(A[0])                           #size of determinant    
    R = ls.row_echelon(A)[0]
    d = R[0][0]                             # first diagonal entry
    for k in range(1,n):                  # get product of diagonal entries
        d =  ar.main( '('+ d + ')('+ R[k][k] +')')[0]
    s = str((-1)**ls.switches)
    p = ls.prod
    return ar.main('('+d+')('+s+')('+p+')')[0] 


A1 = '1,2,3;4,5,6;7,8,9'

A2 = '0,0,0,0,0,0,0,0,1,1,1;\
       0,0,0,0,0,0,0,1,2,2,10;\
       0,0,0,0,0,0,1,3,3,9,0;\
       0,0,0,0,0,1,4,4,8,0,0;\
       0,0,0,0,1,5,5,7,0,0,0;\
       0,0,0,1,6,6,6,0,0,0,0;\
       0,0,1,7,7,5,0,0,0,0,0;\
       0,1,8,8,4,0,0,0,0,0,0;\
       1,9,9,3,0,0,0,0,0,0,0;\
       10,10,2,0,0,0,0,0,0,0,0;\
       11,1,0,0,0,0,0,0,0,0,0' 

A3 = '0,0,0,0,0,0,0,0,0,0,1;\
       0,0,0,0,0,0,0,0,0,2,0;\
       0,0,0,0,0,0,0,0,3,0,0;\
       0,0,0,0,0,0,0,4,0,0,0;\
       0,0,0,0,0,0,5,0,0,0,0;\
       0,0,0,0,0,6,0,0,0,0,0;\
       0,0,0,0,7,0,0,0,0,0,0;\
       0,0,0,8,0,0,0,0,0,0,0;\
       0,0,9,0,0,0,0,0,0,0,0;\
       0,10,0,0,0,0,0,0,0,0,0;\
      11,0,0,0,0,0,0,0,0,0,0'


A4 = ' 0,0,0,0,0,1;\
       0,0,0,0,2,0;\
       0,0,0,3,0,0;\
       0,0,4,0,0,0;\
       0,5,0,0,0,0;\
       6,0,0,0,0,0'
       
A5 =    '1,2,3,4,5,6;\
         7,8,9,10,11,12; \
         13,14,15,16,17,18; \
         19,20,21,22,23,24; \
         25,26,27,28,29,30;\
         31,32,33,34,35,36'

A6 =    '1,2,3,4,5,6,7;\
         8,9,10,11,12,13,14; \
         15,16,17,18,19,20,21; \
         22,23,24,25,26,27,28; \
         29,30,31,32,33,34,35;\
         36,37,38,39,40,41,42;\
         43,44,45,46,47,48,47' 

A7= '6,1,1;4,-2,5;2,8,7/2+i'
A8 = '-3,2,-5;-1,0,-2;3.09876,-4,1'
A9 = '1,-1,2;2,3,5;1,0,3'

'''
A = A3
A = tl.string2table(A)
print(det_echelon(A))
#print(det_leibnitz(A))
#print(det_laplace(A))
'''


############################### cramer #################################

def replace_col(A,B,col):
    n = len(A) # size of determinant
    C = []   
    At = ls.transpose(A)
    for k in range(n):
        if k < col:                 
            C.append(At[k])         # keep column k
        if k == col:                # replace column col with B
            C.append(B)                 
        if k > col and k < n:       # keep column k  
            C.append(At[k])        
    return ls.transpose(C)


def cramer_rule(A,B):   
    S = []                         # for solution
    d = det_echelon(A)
    if d == '0': return []
    for k in range(len(A[0])):
        C = replace_col(A,B,k)               
        c = det_echelon(C)
        ratio = ar.main('('+c+')/'+'('+d+')')[0]
        #print('x'+str(k+1)+'=',ratio) 
        S.append(ratio)
    return S

'''
A1 = '-3,2,-5;-1,0,-2;3.09876,-4,1'
B1 = '1,2,3'
A2 = '1,2,3;5,-3.1-i,1;-1,5,6+2i'
B2 = '4,7,8'

A = A2; B = B2
A = tl.string2table(A)
B = B.split(',')
print('\n',cramer_rule(A,B))
'''


def cramer_rule_params(A,B):   
    S = []                         # for solution
    d = det_params(A)    
    if d == '0': return []
    for k in range(len(A[0])):
        C = replace_col(A,B,k)               
        c = det_params(C)
        ratio = '('+c+')/'+'('+d+')'
        print('x'+str(k+1)+' =',ratio) 
        S.append(ratio)
    return S

def evaluate_cramer(S,substitutions,p):
    for k in range(len(S)):        
        e = mu.evaluate(S[k],substitutions,p)
        print('x'+str(k+1)+' =',e) 

'''
A = '-3,2a,-5;-1,0,-2;3.09876,-4,1'
B = '1,2,3+a'
A = tl.string2table(A)
B = B.split(',')
S = cramer_rule_params(A,B)
substitutions = 'a=1.0001'
evaluate_cramer(S,substitutions,5)
'''


############################ common solution ###########################
      

def make_mat(listP,listQ):
    M = []    
    LP = len(listP)
    LQ = len(listQ)
        
    if LP < LQ: 
        listP =  tl.zero_list(LQ - LP) + listP # prepend zeros to listP
  
    if LQ < LP: 
        listQ =  tl.zero_list(LP - LQ) + listQ # prepend zeros to listQ       
    LP = len(listP); LQ = len(listQ)             # adjust values     
 
    for j in range(LP):                         # make top half of matrix
        row = tl.zero_list(j) + listP + tl.zero_list(LQ-1-j)      
        M.append(row)
    
    for j in range(LQ):        # makebottom half of matrix
        row = tl.zero_list(j) + listQ + tl.zero_list(LP-1-j)       
        M.append(row)
    
    return M

'''
listP = ['1','2','3']
listQ = ['4','5','6','7','8']
A = make_mat(listP,listQ)
tl.format_print(A, 2, 'right')
'''

def has_common_root(P,Q):    
    listP = pa.main(P)[1]   # get the flists of the polynomials
    listQ = pa.main(Q)[1]    
    M = make_mat(listP,listQ)   # make the matrix
    tl.format_print(M, 2, 'right');print('') 
    return det_echelon(M) == '0' 
'''
P = 'x^2 + 2x + 3'
Q = '4x^3 + 5x^2 + 6x + 7'
print(has_common_root(P,Q),'\n')
P = 'x^2-2x+1'
Q = 'x^3-3x^2+3x-1'
print(has_common_root(P,Q))
'''


######################### plane through 3 points #######################

def plane(P1,P2,P3):    
    A = [[P1[1],P1[2],'1'], [P2[1],P2[2],'1'],  [P3[1],P3[2],'1'] ]
    B = [[P1[0],P1[2],'1'], [P2[0],P2[2],'1'],  [P3[0],P3[2],'1'] ]
    C = [[P1[0],P1[1],'1'], [P2[0],P2[1],'1'],  [P3[0],P3[1],'1'] ]
    D = [[P1[0],P1[1],P1[2]],[P2[0],P2[1],P2[2]], [P3[0],P3[1],P3[2]]]
   
    #tl.format_print(A,3,'right'); print('\n')  
    #tl.format_print(B,3,'right'); print('\n')    
    #tl.format_print(C,3,'right'); print('\n')    
    #tl.format_print(D,3,'right'); print('\n')    

    A = det_echelon(A)      
    B = det_echelon(B)      
    C = det_echelon(C)      
    D = det_echelon(D)      
 
    A = tl.add_parens(A)
    B = tl.add_parens(B)
    C = tl.add_parens(C)
    D = tl.add_parens(D)
    eqn = A + 'x' ' - ' + B + 'y' ' + ' + C + 'z' ' = ' + D
    return tl.fix_signs(eqn)

'''
P1 ='1,0,-3'.split(',') 
P2 ='0,-2,3'.split(',') 
P3 ='1,-4,0'.split(',')
print(plane(P1,P2,P3))
'''

######################## sphere through 4 points #######################


def sphere(P1,P2,P3,P4):                                
    A = []; B = []                                      
    x1 = P1[0]; y1 = P1[1]; z1 = P1[2]                  
    x2 = P2[0]; y2 = P2[1]; z2 = P2[2]                  
    x3 = P3[0]; y3 = P3[1]; z3 = P3[2]                  
    x4 = P4[0]; y4 = P4[1]; z4 = P4[2]                  
                                                        
    a11 = ar.main('2('+ x1 +')')[0]                     
    a12 = ar.main('2('+ y1 +')')[0]                     
    a13 = ar.main('2('+ z1 +')')[0]                     
    A.append([a11,a12,a13,'1'])                         
                                                        
    a21 = ar.main('2('+ x2 +')')[0]                     
    a22 = ar.main('2('+ y2 +')')[0]                     
    a23 = ar.main('2('+ z2 +')')[0]                     
    A.append([a21,a22,a23,'1'])                         
                                                        
    a31 = ar.main('2('+ x3 +')')[0]                     
    a32 = ar.main('2('+ y3 +')')[0]                     
    a33 = ar.main('2('+ z3 +')')[0]                     
    A.append([a31,a32,a33,'1'])                         
                                                        
    a41 = ar.main('2('+ x4 +')')[0]                     
    a42 = ar.main('2('+ y4 +')')[0]                     
    a43 = ar.main('2('+ z4 +')')[0]                     
    A.append([a41,a42,a43,'1'])                         
                                                        
    b1 = ar.main(x1+'^2+' +  y1 +'^2+' + z1 +'^2')[0]   
    b2 = ar.main(x2+'^2+' +  y2 +'^2+' + z2 +'^2')[0]   
    b3 = ar.main(x3+'^2+' +  y3 +'^2+' + z3 +'^2')[0]   
    b4 = ar.main(x4+'^2+' +  y4 +'^2+' + z4 +'^2')[0]   
                                                        
    B = [b1,b2,b3,b4]                                   
    C = cramer_rule(A,B)                                
    if C == []:                                         
        print('no sphere')                              
        return '','',''                                       
    a,b,c,k = C[0], C[1], C[2], C[3]                    
    d = '('+ a +')^2+' + '('+ b +')^2+' + '('+ c +')^2' 
    rsquared = ar.main(k + '+' + d)[0]                  
    radius = '('+ rsquared + ')^(1/2)'
    center = [a,b,c]                                        
    return center, radius, rsquared # last for checking only
                                                        
 
def check(P,C,rsq):       
    equation = '(x-' + C[0] + ')^2 + ' + '(y-' + C[1] + ')^2 + ' \
               + '(z-' + C[2] + ')^2 = ' + rsq       
    equation = equation.replace('x','('+ P[0] + ')')
    equation = equation.replace('y','('+ P[1] + ')')
    equation = equation.replace('z','('+ P[2] + ')')
    left,right = equation.split('=')
    expr = left + '-(' + right + ')'
    print(ar.main(expr)[0])

'''
P1 ='1,0,3'.split(',') 
P2 ='0,2,3'.split(',') 
P3 ='1,4,0'.split(',') 
P4 ='1,2,5'.split(',') 

#P1 ='1,1,1'.split(',') 
#P2 ='2,2,2'.split(',') 
#P3 ='3,3,3'.split(',') 
#P4 ='4,4,4'.split(',') 

C,r,rsq = sphere(P1,P2,P3,P4)
if C != '':  
   print('center   = ',C)
   print('radius   = ',r)
   check(P1,C,rsq)
   check(P2,C,rsq)
   check(P3,C,rsq)
   check(P4,C,rsq)
'''


######################## characteristic polynomial ########################

def char_pol(A): 
    B = tl.string2table(A)
    for i in range(len(B)):
        B[i][i] =  '(' + B[i][i] + '-x)'     
    return det_params(B)

A = '1+i,2-3i,3;4,5,6;7,8-5i,9'
#A = '1,2;3,4'
#A = '1+3i,2-002i,3/7; 4.8,5.9,6 -.8i;7/11,8.4,9'
#A = '1+3i,(2-7i)^3,3/7.12i; 4.8,5.9,6 -.8i;7/11,8.4,(9-.0987i)^2'  
#A = '5,-3,-2;1,1,-2;3,2,0'
#A = '4,2,-1;-5,-3,1;3,2,0'         
#A = '4,2,-1;-1,-3,1;3,2,-7' 
# A = '2,-1,0;-3,2,1;0,-2,1'     
#A = '1,-1,0;-1,2,1;0,1,1'          # eigenvalues 0,3,1
#A = '-16,84,0;0,40,0;24,-36,8'    # eigenvalues 8,-16,40
#A = '-4,21,0;0,10,0;8,-9,2'       # eigenvalues 2,-4,10

'''
C = char_pol(A)
print(C)
#print(pd.factor_polynomial(C)) not for complex entries
'''

############################# Caley Hamilton ############################

def caley_hamilton(A):   
    c = char_pol(A)       
    #print(c)    
    constant_term = ar.evaluate(c,'0','')[0]   
    c = pa.main(c + '-(' + constant_term + ')')[0]
    c = c.replace('x','A')         # expression in A
    c = c + '+(' + constant_term + ')A^0' 
    matrix_list = ['A='+A]
    #print(matrix_list)    
    return mat.calculator(c,matrix_list)

#A = '1+3i,(2-7i)^3,3/7.12i; 4.8,5.9,6 -.8i;7/11,8.4,(9-.0987i)^2'
#A = '2,2,3;4,5,6;7,8,9'
#A = '1,2;3,4'
#tl.format_print(caley_hamilton(A),2,'right')

############################### Eigenspace ##############################

def eigenspace(A,x):
    I = mat.makeid(len(A[0]))
    xI = mat.scalar_mult(x,I)   
    B = mat.subt_mat(A,xI)  # ok
    return vec.kernel_basis(B)

A1 = '1,-1,0;-1,2,1;0,1,1'    
A1 = tl.string2table(A1)
e1a = eigenspace(A1,'0')      
e1b = eigenspace(A1,'3')      
e1c = eigenspace(A1,'1')     

A2 = '-16,84,0;0,40,0;24,-36,8'   
A2 = tl.string2table(A2)
e2a = eigenspace(A2,'8')  
e2b = eigenspace(A2,'-16')
e2c = eigenspace(A2,'40') 

A3 = '-4,21,0;0,10,0;8,-9,2'  
A3 = tl.string2table(A3)
e3a = eigenspace(A3,'2')  
e3b = eigenspace(A3,'-4')
e3c = eigenspace(A3,'10') 

'''
A = A2; e = e2c
for v in e:
    print(e)
    print(vec.mult_mat_vec(A,v))
'''

############################## adjugate ################################

def adjugate(A):
    n = len(A)
    B = []    
    for j in range(n):
        row = []
        for k in range(n):
            C = remove_row_col(A,j,k)
            d = det_echelon(C)
            sign = str((-1)**(j+k))
            d = ar.main('(' + sign + ')(' + d + ')')[0]    
            row = row + [d] 
        B.append(row)  
    return ls.transpose(B) 

'''
A = '1+3i,(2-7i)^3,3/7.12i; 4.8,5.9,6 -.8i;7/11,8.4,(9-.0987i)^2'
A = '2,2,3;4,5,6;7,8,9'
A = tl.string2table(A)
Adj = adjugate(A)
print('adjugate of A')
tl.format_print(Adj,2,'right'); print('\n')
B = mat.mult_mat(Adj,A)
print('A times the adjugate of A')
tl.format_print(B,2,'right'); print('\n')
print('determinant of A')
print(det_echelon(A))
'''

def adjugate_params(A):
    n = len(A)
    B = []    
    for j in range(n):
        row = []
        for k in range(n):
            C = remove_row_col(A,j,k)
            d = det_params(C)
            sign = str((-1)**(j+k))
            d = mu.main('(' + sign + ')(' + d + ')')[0]    
            row = row + [d] 
        B.append(row)  
    return ls.transpose(B) 


def mult_mat_params(A,B):                                                                                                        
    C = []
    for i in range(len(A)):                # run through rows of A
        Crow = []                                                        
        for j in range(len(B[0])):         # run through cols of B
            s = '0'                                                      
            for k in range(len(A[0])):  
                s =  s + '+('+A[i][k]+')('+B[k][j]+')'                                  
                s = mu.main(s)[0]                                
            Crow.append(s)                                               
        C.append(Crow)                                                       
    return C                                            


'''
A = '2,2x^2,3;4x+y,5,6;7,8,-3ax'
A = tl.string2table(A)
print('A:')
tl.format_print(A,2,'right'); print('\n')
Adj = adjugate_params(A)
print('adjugate of A:')
tl.format_print(Adj,2,'right'); print('\n')
B = mult_mat_params(Adj,A)
print('A times the adjugate of A:')
tl.format_print(B,2,'right'); print('\n')
print(B); print('\n')
print('determinant of A:')
print(det_params(A))
'''

