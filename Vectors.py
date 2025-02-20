
##### Vectors.py

import Arithmetic as ar
import LinSolve as ls
import MatAlg as mat
import MultiAlg as mu
import Tools as tl


############################# vector operations ##########################

def scalar_mult_vec(z,v):                 
    u = []
    for i in range(len(v)):   
        prod = '(' + z + ')('+ v[i] + ')'           
        u.append(ar.main(prod)[0])      
    return u

def add_vec(u,v):                         
    vecsum = []
    for i in range(len(u)):
        s = u[i] + '+' + '(' + v[i] + ')'        
        vecsum.append(ar.main(s)[0] )
    return vecsum

def subt_vec(u,v):                   
        w = scalar_mult_vec('(-1)',v)   
        return add_vec(u,w)           

def add_vecs(vecs):  
    vecsum = vecs[0]
    for i in range(1,len(vecs)):
        vecsum = add_vec(vecsum,vecs[i])
    return vecsum    

def dot_prod(u,v):      
        dprod = ''  
        for i in range(len(v)):
            prod = '(' + u[i] + ')('+ v[i] + ')'  
            dprod = ar.main(dprod + '+' + prod)[0]      
        return dprod

def mult_mat_vec(A,u):           # used for check
        v = []
        for i in range(len(A)):
             v.append(dot_prod(A[i],u))
        return v   

'''
u =  '1,1,1' 
v = '4,5,6'
A = '7,8,9;10,11,12;13,14,15'
u = u.split(',')
v = v.split(',')
A = tl.string2table(A)
#print(add_vec(u,v))
#print(subt_vec(u,v))
#print(mult_mat_vec(A,u))
'''

def reduce_lincomb(coeffs,vectors):
    lc = []   
    for i in range(len(coeffs)): # multiply coeff by vector
        c = coeffs[i]
        v = vectors[i]        
        lc.append(scalar_mult_vec(c,v))
    return add_vecs(lc)

'''
vectors = '1,2,3,4;5,6,7,8;9,10,11,12'
coeffs = ['1','1','1']
vectors = '1,2,3; 4,5,6; 7,8,9'
coeffs = '5.7, -1 ,3/3+i'
coeffs = coeffs.split(',')
vectors = tl.string2table(vectors)
print(reduce_lincomb(coeffs,vectors))
'''

############################# linear dependence ##########################

### not needed
def are_linear_indep(vectors):    
    A = tl.string2table(vectors)
    zero_row = ['0' for k in range(len(A[0]))]
    augmat = mat.transpose(A + [zero_row])       
    solution_list = ls.linsolve([],augmat,'c',False)    # solutions c1,c2,...
    if not ls.is_zero_row(solution_list): 
      return False   # solution_list has a non zero entry, so not l.i.
    else: return True   
   
#vectors = '1,2,3,4;5,6,7,8;9,10,11,12'    
##print(are_linear_indep(vectors))
    
       
def get_lin_ind_rows(A):
    B = tl.copylist(A)                        # don't change A    
    while True:
        C = B[1:]+ [B[0]] # put first row on bottom   
        augmat = ls.transpose(C)    
        #print('augmat')
        #tl.format_print(augmat,4, 'right')
        #print('\n')
        solution_list = ls.linsolve([],augmat,'c',False)                 
        if solution_list == []: 
            return B   # no solution; return remaining li vectors
        B = B[1:]             # remove top row and proceed again                                               
             
        
def print_dependency_relation(A,LI):       
    for row in A:                # run through the rows of A not in LI
        if row in LI: continue
        B = LI+[row]             # put row at bottom of LI
        augmat = ls.transpose(B)  # for system             
        sol = ls.linsolve([],augmat,'x',False)    
        print(row,'=')
        for i in range(len(sol)):
            coeff = sol[i].split('=')[1]
            if i < len(sol)-1:
                print('    ('+ coeff +')', LI[i],'+')        
            else:
                print('    ('+ coeff +')', LI[i])                
        print('\n')


def get_row_rank(A):
    return len(get_lin_ind_rows(A))

'''
A1 = '1,2,3;4,5,6;7,8,9'
A2 = '1,2,3,4,5,6,7,8;\
     9,10,11,12,13,14,15,16;\
     17,18,19,20,21,22,23,24;\
     25,26,27,28,29,30,31,32;\
     33,34,35,36,37,38,39,40'       
A3 = '1,2,3;4,5,6'
A4 = '1,2,3;2,4,6'
A5 = '1,2,3,4,5,6,7,8,9;\
     11,12,13,14,15,16,17,18,19;\
     9,8,7,6,5,4,3,2,1'
A6 = '4,5,6,12; 1,2,3,9; 7,8,9,15'
A7 = '4,2,7; 5,2,8; 6,3,9;12,9,15'
A8 = '1,2,3;4,5,6;7,8,10'   

A9 = '1,2,3,4,5,6;\
     7,8,9,10,11,12;\
     13,14,15,16,17,18;\
     19,20,21,22,23,24;\
     25,26,27,28,29,30;\
     31,32,33,34,35,36'

A10 = '1,2,3,4,5;\
       6,7,8,9,10;\
       11,12,13,14,15;\
       16,17,18,19,20'

A = A10
A = tl.string2table(A) 
tl.format_print(A,3,'right')
print('\n')

LI = get_lin_ind_rows(A) 
print(LI,'\n')  
print_dependency_relation(A,LI)           
'''

################################## range #################################

def range_basis(A):
    At = ls.transpose(A)
    return get_lin_ind_rows(At) 

'''
A = '1,2,3,4,5;\
     6,7,8,9,10;\
     11,12,13,14,15;\
     16,17,18,19,20'
A = tl.string2table(A) 
print(range_basis(A))   
'''


################################# kernel #################################

def kernel_basis(A):        
    zero_row = tl.zero_list(len(A[0]))
    At = ls.transpose(A)
    augmat = ls.transpose(At + [zero_row])       
    sol_vec = ls.linsolve([],augmat,'x',False)      
         
    free_vars = []
    for v in sol_vec:         # get free variables
        for j in range(1,len(sol_vec)+1):
            var = 'x'+ str(j)
            if v == var:
                free_vars = free_vars + [v]     
    basis = []      
    sol_string  = ','.join(sol_vec)   
         
    for v in free_vars:
        s = sol_string        
        s = s.replace(v,'(1)')            
        for w in free_vars:
            if w != v:                
                s = s.replace(w,'(0)')    
        s = s.split(',')               
        basis = basis+[s]       
     
    for k in range(len(basis)):
        for j in range(len(basis[k])):
            if '=' in basis[k][j]:
                right_side = basis[k][j].split('=')[1]                
                basis[k][j] = mu.main(right_side)[0] 
            else: 
                basis[k][j] = mu.main(basis[k][j])[0]    
    return basis

'''
A1 = '1,2,3,4,5;\
     6,7,8,9,10;\
     11,12,13,14,15;\
     16,17,18,19,20'

A2 = '1,2,3,4,5;\
     6,7,8,9,10;\
     11,12,13,14,15'

A3 = '1,2,3,4,5,6,7;  \
      8,9,10,11,12,13,14; \
      15,16,17,18,19,20,21;\
      22,23,24,25,26,27,28'

A4 = '0,-1,0;-1,1,1;0,-1,0'


A = tl.string2table(A3) 

#A = [['-56', '84', '0'], ['0', '0', '0'], ['24', '-36', '-32']]

KB = kernel_basis(A)
tl.format_print(KB,2,'right')
print('\n')

#check:
for u in KB:    
    print(mult_mat_vec(A,u))    
'''