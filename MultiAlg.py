###### MultiAlg.py

import Number as nm
import Arithmetic as ar
import Tools as tl
import math as ma
from operator import itemgetter


############################ scalar conversion ##########################

def scalar2mono(s):          # attach scalar to zero list
    return [s] + [0 for k in range(len(varlist))]   

def scalar2rat(s):
    return [[scalar2mono(s)], [scalar2mono('1')]] 

# varlist = list('xyz')
# print(scalar2rat('2.3/i'))    

########################## variable conversion ##########################

def var2mono(var,exp):                 # variable and its exponent NEW
    # 'x^2' -> ['1',2,0,...]  
    M  = scalar2mono('1')    
    position = varlist.index(var)             
    M[position+1] = exp         # put exponent in correct var position                     
    return M

def var2rat(var,exp):
    num = var2mono(var,exp)           
    den = scalar2mono('1')                       
    return [[num], [den]]    

# varlist = list('xyz')
# print(var2rat('y',7))

############################### calculations ############################

def combine_monos(P):  
    # P = [['2',3,4], ['5',3,4],['-3',8,9]] --> [['7',3,4],['-3',8,9]]                  
    Q = []                           # for reduced polynomial        
    if len(P) == 1: 
        return P    
    for i in range(len(P)-1):        
        if P[i] == '': continue      # already added        
        M = P[i]               # ith monomial: [coeff,powers]        
          
        for j in range(i+1,len(P)):  # add succeeding like monomials to M
            if P[j] == '':
                continue
            N = P[j]
            if M[1:] == N[1:]:  # if powers the same, add the coefficients
               coeffsum = ar.main(M[0] + '+(' + N[0] +')')[0]
               M[0] = coeffsum               # update M's coefficient    
            
               P[j] = '' # mark as already added
        Q.append(M)  # append nonzero monomial in P[i]              
      
    leftover_mono = P[len(P)-1]
    if leftover_mono != ''  and leftover_mono[0] != '0':     
       Q.append(leftover_mono)    # pick up leftover monomial at end
    return Q    

'''
P1 = [['14', 15, 17, 19],['-5', 15, 17, 19],['-5', 14, 17, 19],\
     ['-1', 15, 17, 19],['3', 14, 17, 19],['17', 13, 16, 18]]
P2 = [['-4', 1, 16, 18],['1', 15, 17, 19],['2', 15, 17, 19],['3', 15, 17, 19]]
P3 = [['2',3,4], ['5',3,4],['-3',8,9]]  
P4 = [['-3', 1], ['0', 0], ['7', 0],['0',3]]
P5 = [['-3', 1], ['7', 4]]

P = P1
#print(775,P)
#print(777,combine_monos(P))
'''

def multiply_monos(M,N):          
    # returns product of monomials M,N    
    K = []                     # for output
    # multiply coefficients:   
    coeff_prod  = ar.main('(' + M[0] +')(' + N[0] + ')')[0]    
    K.append(coeff_prod)
    # add integer exponents of same variables:      
    for i in range(1,len(N)): 
        K.append(M[i] + N[i])  
    return K

'''
M = ['2',3,4,5]
N = ['-3',6,7,8]
#print(multiply_monos(M,N))
'''

def multiply_pols(P,Q):       
    # multiplies 2 lists of monomials    
    R = []               # list for product polynomial    
    for M in P:          # get all possible products M*N
        for N in Q:
            K = multiply_monos(M,N)   
            ##print(606061,K)    
            R.append(K)                      
    return R

'''
P = [ ['2',3,4,5], ['-1',6,7,8] ]
Q = [ ['5',9,10,11], ['7',12,14,16] ]
R = multiply_pols(P,Q)
#print(P)
#print(Q,'\n')
#print(R,'\n')
'''

def multiply_rationals(R, S):         
    num = multiply_pols(R[0], S[0]) # multiply numerators
    den = multiply_pols(R[1], S[1]) # multiply denominators 
    return [num,den]
'''
R = [ [['2',3,4,5], ['-1',6,7,8]], [['5',9,10,11], ['7',12,14,16]] ]
S = R
##print(multiply_rationals(R,S))
'''

def divide_rationals(R,S):  
    T = [S[1],S[0]] 
    return multiply_rationals(R,T)

def rational_power(R,n):    
    need_to_invert = False
    if n == 1: return R
    if n == 0:        
        num = ['1'] + [0 for k in range(len(R[0][0])-1)]
        den = num
        return [num,den]   
    if n < 0:
        n = -n
        need_to_invert = True        
  
    S = R  
    for i in range(n-1):    # multiply R times itself n-1 times
        S = multiply_rationals(S, R)    
    num = S[0]  #combine_monos(S[0])
    den = S[1]  #combine_monos(S[1])
        
    if need_to_invert:
        return [den,num]    
    return [num,den]

'''
P = [ ['2',3,4,5], ['-1',6,7,8] ]
Q = [ ['5',9,10,11], ['7',12,14,16] ]
R = [P,Q]
print(rational_power(R,3))
'''

def mono_scalar_prod(s,M):
    prod  = '(' + s +')(' + M[0] + ')' 
    prod  = ar.main(prod)[0]
    return [prod] + M[1:]

def pol_scalar_prod(s,P):
    # multiplies a  polynomial  by a scalar: 
    # '3'*[['5',6,7],['7',8,9]] = [['15',6,7], ['21',8,9]]      
    Q = []
    ##print(4000,s,P)
    for M in P:              
        N = mono_scalar_prod(s,M)
        Q.append(N)
    return Q        

def rat_scalar_prod(s,R):
    # multiplies a rational function by a scalar:     
    return [pol_scalar_prod(s,R[0]),R[1]]        

'''
s = '1/2'
R = [ [['2',3,4,5], ['-1',6,7,8]], [['5',9,10,11], ['7',12,13,14]] ]
#print(rat_scalar_prod(s,R))
'''

def add_pols(P,Q):  
    if P == []: return Q
    if Q == []: return P
    S = P+Q           # concatenation   
    return S #combine_monos(S)     

def add_rationals(R,S):                                           
    numR = R[0]; denR = R[1]                     
    numS = S[0]; denS = S[1]                     
    A = multiply_pols(denR,numS)                                  
    B = multiply_pols(denS,numR)                                  
    num = add_pols(A,B)                    # denR*numS + denS*numR
    #num = combine_monos(num)                                      
    den = multiply_pols(denR,denS)                     # denR*denS
    #den = combine_monos(den)                                      
    return [num,den]           # (denR*numS + denS*numR)/denR*denS

def subtract_rationals(R, S):
    minusS = rat_scalar_prod('-1',S)
    return add_rationals(R,minusS)         

'''
R = [ [['2',3,4], ['-1',6,7]], [['3',9,10], ['-2',12,13]]]
S = R
R = [ ['1',2,3],['2',4,5],['1',2,3],['2',4,5]  ]

R = [  [['1',2,3]], [['1',4,5],['2',3,0]] ]
S = R
##print(add_rationals(R,S))
##print(rat_scalar_prod('2',R))
'''


################################ sorting ################################   
   
def sort_list(P):                                # polynomial list             
    l = len(P)                       # number of mono lists in pol
    m = len(P[0])                          # length of a mono list    
    if l == 1:
        return P    
    Q = tl.copylist(P)                           # don't change P
   
    for i in range(l):          # sum the powers of each mono list
        sum = 0            
        for j in range(1,m):          # sum the powers of ith mono
            sum = sum + Q[i][j]
        Q[i] = [sum] + Q[i]      # attach sum to start of ith mono
        # sort pol_list on the first field (sum of powers):     
    sorted_list = sorted(Q, key=itemgetter(0), reverse = True)              
      
    for i in range(l):       # remove sum of powers from each mono
        # extract 1st part of the mono sorted_list[i]:                    
       sorted_list[i] = sorted_list[i][1:]      
    return sorted_list             
     

######################## reducing coefficients ##########################

def reduce_coeffs(R):                                               
    num = R[0]; den = R[1]                                              
    numden = num + den                             # combine lists  
    coeffs = []                                                     
    for i in range(len(numden)):                                    
        n = numden[i][0]                     # get the coefficient  
        re = int(ar.real(n))                                        
        im = int(ar.imag(n))                                        
        coeffs.append(re)              # append real and imaginary  
        coeffs.append(im)                    # parts to coeff_list  
    #gcd = nm.list_extended_gcd(coeffs)[0]  # largest common factor  
    gcd = nm.multi_extended_gcd(coeffs)[0]
    for i in range(len(num)):     # divide numerator coeffs by gcd  
        n = num[i][0]                                               
        num[i][0] = ar.main('('+ n +')/('+ str(gcd) +')')[0]   
    for i in range(len(den)):   # divide denominator coeffs by gcd  
        n = den[i][0]                                               
        den[i][0] = ar.main('('+ n +')/('+ str(gcd) +')')[0]   
    return [num,den]                                                
'''
R = [ [['2+10i',3,4,5], ['4',3,7,8]],[['6',3,4,9], ['8',3,8,11]] ]
print(R)
print(reduce_coeffs(R))
'''


########################### reducing variables ##########################

def get_smallest_exp(R,k): 
    # minimum of all exponents in R in kth monomial position
    num = R[0]; den = R[1]                # polynomials
    min_exp = 100000     
    for M in num:    
        #if M[k] == 0: continue                  # NEW
        if min_exp > M[k]: min_exp = M[k]
    for M in den:
        #if M[k] == 0: continue                  # NEW
        if min_exp > M[k]: min_exp = M[k]          
    return min_exp


def reduce_vars(R):                                                           
    #S = tlk.copylist(R)
    num = R[0]; den = R[1]          
    L = len(num[0])                           # monomial length       
    for k in range(1,L):  # k = position of kth variable's exponent in monomial              
        min_exp = get_smallest_exp(R,k)       
        for M in num:                  # run through monomials in numerator                                                                                  
            if M[k] != 0:
                M[k] = M[k] - min_exp      # reduce kth exponent                       
        for M in den:                  # run through monomials in denomerator          
            if M[k] != 0:  
                M[k] = M[k] - min_exp      # reduce kth exponent                 
    return [R[0],R[1]]                               

'''
R = [ [['2',2,5],['5',7,8]], [['7',3,4],['9',2,11]] ] 
#R = [ [['2.1',3,4,5], ['2.2',3,7,8]],[['6.1',3,4,9], ['6.2',3,8,11]] ]
#print(R)
#print(reduce_vars(R))
'''

############################ clearing fracs #############################

def get_mono_denoms(M):
        mono_denoms = [1]            # default
        coeff = M[0]
        re = ar.real(coeff)
        im = ar.imag(coeff)   
        if '/' in re:  
           mono_denoms += [int(re.split('/')[1])]       
        if '/' in im: 
           mono_denoms += [int(im.split('/')[1])]       
        return mono_denoms

def get_pol_lcm(P):
    pol_denoms = []
    for M in P:
        mono_denoms = get_mono_denoms(M)
        pol_denoms = pol_denoms + mono_denoms          
    return nm.listlcm(pol_denoms)    
    
def clear_pol(P):
    Q = []      
    lcm = str(get_pol_lcm(P))       
    for M in P:
        prod = ar.main( lcm +'('+ M[0] +')' )[0]        
        N = [prod] + M[1:]
        Q.append(N)   
    return lcm, Q  

'''    
P = [['3/2',3,4,5], ['5/12i',3,7,8], ['7/3+(5/6)i',3,4,9]]
lcm, Q = clear_pol(P)
print(lcm)
print(Q)
'''


########################### list to rational ############################

def list2monomial(Mlist):           # ['2',3,4,5] --> 2x^3y^4z^5    
    # takes monomial list and returns monomial          
    coeff = Mlist[0]            
    if coeff == '0' or coeff == '-0' : return '0'   
    mono = ''   
    for k in range(1,len(Mlist)):             
        var = varlist[k-1]         
        exp = Mlist[k]               # exponent of variable 
        if exp == 0: continue    # don't include var with zero exponent
        mono = mono + var        # attach variable
        if exp != 1:             # and exponent 
            mono = mono + '^' + str(exp) # attach exp != 1    
    if coeff == '1' and mono != '': 
        coeff = ''        # coeff '1' not needed 
    if coeff == '-1' and mono != '':  
        coeff = '-'                   
    if coeff != '' or exp != 0:          
        coeff = tl.add_parens(coeff)   # attach suitable parens        
    return tl.fix_signs(coeff + mono)          

'''
Mlist = ['5.3/2.7+2.3i',5,6,7]
varbs = 'xyz'
#print(Mlist)
#print(list2monomial(Mlist))
'''

def list2polynomial(P): # [['2',3,4],['5',6,7]] -->  5x^6y^7+ 2x^3y^4 
    Q = sort_list(P)
    pol = ''      
    for M in Q:                      
        mono = list2monomial(M)           # get the monomial                          
        if mono == '0': continue         # skip any zero coeff    
        pol = pol + '+' + mono            # attach to pol
    if pol  == '': pol= '0'
    pol = tl.fix_signs(pol)          
    return pol  

def list2rational(R):
    # [  [['2',3,4],['5',6,7]],[['8',1,0],['9',0,1]]  ] 
    # -->  (5x^6y^7 + 2x^3y^4)/(8x + 9y)                         
    R = reduce_vars(R)                    
    num = list2polynomial(R[0])  
    den = list2polynomial(R[1])             
       
    if num == '0': return '0'
    if den == '1' or den == '':         
        return num
     
    if den == '-1':               
       num = tl.add_parens(num) 
       return '-' + num  
          
    num = tl.add_parens(num) 
    den = tl.add_parens(den)     
    
    return num + '/' + den 

'''    
R = [ [['2',3,4,5], ['-1',6,7,8]], [['5+i',9,10,11], ['7',12,14,16]]]
#R = [ [['2',3,4,5], ['-1',6,7,8]], [['-1',0,0,0]] ]
varlist = list('xyz')
print(R)
print(list2rational(R))
'''

############################ list to int rational ##########################

def list2int_rational(R):  
    # converts rational list into integer rational function
    numR = R[0] 
    denR = R[1]    
    if numR == denR: return '1',''    
    lcmP,P = clear_pol(numR)           
    lcmQ,Q = clear_pol(denR)   
    factor = ar.main(lcmQ +'/'+ lcmP)[0]
    irat_list = [P,Q]          
    irat_list = reduce_coeffs(irat_list)      
    irat = list2rational(irat_list)                    
    if factor == '1': factor = ''         
    if factor == '-1': factor = '-'         
    factor = tl.add_parens(factor)    
    if factor != '': 
       irat = tl.add_parens(irat)                
    return factor+irat,irat_list   

'''
R = [ [['1/2',2,3], ['1/3',4,5]], [['1/4+i/5',6,7], ['1/6',8,9]] ]    
varbs = ['x','y']
#print(R),'\n'
#print(list2int_rational(R)[0])       
'''

############################## the allocator ##########################

def allocate_ops(expr,mode):
    global idx, varbs          
    R = []
    while idx < len(expr):
        ch = expr[idx]
        
        
        if tl.isnumeric(ch):
             start = idx
             s,idx = tl.extract_numeric(expr, start)                                   
             R =  scalar2rat(s)
                  
        elif tl.isletter(ch):
             var,idx = tl.extract_var(expr,idx)              
             R = var2rat(var,1)    
             
      
        elif ch == '+':             
            if mode > 0: break               # wait for higher mode
            idx += 1
            S = allocate_ops(expr,0)          
            R = add_rationals(R,S)                 

        elif ch == '-': 
            if mode > 0: break               # wait for higher mode
            idx += 1
            S = allocate_ops(expr,1)             
            R = subtract_rationals(R,S)            
   
        elif ch == '*':
           if mode > 1: break 
           idx += 1                              
           S = allocate_ops(expr,1)                              
           R = multiply_rationals(R,S)   
           
        elif ch == '/':
            if mode > 1: break 
            idx += 1                        
            S = allocate_ops(expr,1) 
            R = divide_rationals(R,S)   
        
        elif ch == '^':
            exp,idx = tl.extract_exp(expr,idx)
            exp = ar.main(exp)[0]            
            R = rational_power(R, int(exp))

        elif ch == '(':
            start = idx
            paren_expr,end = tl.extract_paren(expr,start)          
            if  tl.isarithmetic(paren_expr):                              
                r = ar.main(paren_expr)[0]  # constant expression                   
                num = scalar2mono(r)             ##NEW
                den = scalar2mono('1')            ###New
                R = [[num],[den]]               
                idx=end            
            else:
                idx+=1
                R = allocate_ops(expr,0)
                idx+=1     
        elif ch == ')': break   
    return R 


################################## main ###############################

def main(expr):                                           
    global idx               # points to current character in expr 
    global varlist                        # variable names in expr                                           
    varlist = tl.get_vars(expr)[0]           # extract variable list   
    if varlist == []:                                    # no varbs? 
        z,c = ar.main(expr)                  # use arithmetic   
        return z,c,'',''                                                                 
    expr = tl.attach_missing_exp(expr,varlist)                      
    expr = tl.fix_signs(expr)                                     
    expr = tl.fix_operands(expr)                                  
    expr = tl.insert_asterisks(expr,varlist)                                                                                                       
    idx = 0                           # point to beginning of expr 
    R = allocate_ops(expr,0)                 # do the calculations    
    num = R[0]; den = R[1]                                                          
    num = combine_monos(num)                 # simplify polynomial         
    den = combine_monos(den)                                                   
    num = sort_list(num)      
    den = sort_list(den)  
    ratlist = [num,den]            
    rat = list2rational(ratlist)           
    irat, iratlist = list2int_rational(ratlist)                             
    return rat,ratlist,irat,iratlist                               


def evaluate(expr,substitutions,p):            
    if substitutions == '':
        return expr
    substitutions = substitutions.split(',')       
    for i in range(len(substitutions)):        
        substitutions[i] = substitutions[i].replace(' ','')
        var,val = substitutions[i].split('=')         
        if var == '' or var not in expr: continue          
        expr = expr.replace(var,'(' + val + ')')                              
    expr = tl.fix_signs(expr)                                  
    if tl.isarithmetic(expr) and p != '':         
        return ar.decimal_approx(expr,p)[0]
    return main(expr)[0]

e1 = '-a+(-a)'
e2 = '-2+(-3)'
e3 = '1-(-2)'
e4 = '-2-3'
e5 = '(5.4xy^2+(7/2)y+3iz^11)y'
e6 = '2xy+3xy'
e7 = '2zzzzx+y'
e8 = '3zzzzx^4y^5z^6'
e9 = '2zzzx+1y+3xzzz'
e10 = '(5.4xx^2+(7/2)ix+3.87ix^11)yzx'
e11 = '((37/10)c+a^12b(2))/(64d^2(3)^2+16d(2)(3)+(2)^2)'
e12 = '(4.3zax-3yc)^3'
e13 = '(2x+c)^3 + 5ax^2'
e14 = '(A2Bx+3.7C)/(x+8yD)^2'
e15 = '(c^3z+6c^2x+12cx^2+8x^3y)/(c^3z+6c^2x+12cx^2+8x^3y)' # =1 
e16 = 'yz/(.1x-1)+xz/(.2y-3i)'
e17 = '(1/2i)x+(3/2)z+(5/6)z'
e18 = '(x+2y)/(2x+3y) + (x+2y)/(2x+3y)'
e19 = '2((x+2y)/(2x+3y))'
e20 = e5 + '-' + e6
e21 = 'x^(-3)'
e22 = '((-c)+(14a)+(-5b))/(1)'
e23 = '(a)(b)'
e24 = '-x^3'
e25 = '(x+1)-1'

e26 = 'z_2/(x-1.1) + 3x/(y1-3.2i)'# + 4y/(z-3)'
s26 = 'x = 1,y3 = 3,y3 = -1, z1=i'

e27 = '(1/3)n^3+ (1/2)n^2+ (1/6)n'
e28 = '17(z^9+5)^2'
e29 = '3An^2+3An+1A+2Bn+1B+1C-n^2-2n-1'
e30= '6A+3B-3+3'
e31 = '(z^4x^3-y^(-2))^2'#  /(3.7^2+7x^3z)'
e32 = 'z/x+y^(-3)'  # works
e33 = '(2+1)^2(x^(-2)+5)^9'
e34 = '((1.3/2 + 7)zx-y^2/(3.7y+7x^3z))^2'
e35 = 'b(x^3+az)^-4 +(17)^(-2)'
e36 = '(n+1)^3 - n^3'
e37 = '3.2xy^3 + 4.7yz^2 + x/(2.7z+y)'
e38 = '1'
e39 = '1^2/2^2z^6'
e40 = '(3x1 + 2x7)^2'
e41 = '(x+y)^2'
e42 = '7+(3x)'   # ok
e43 = '7+(-3x)'  # ok
e44 =  'x^2 + x^3 + 5x + 7x + 500x^3'
e45 =  'x^2 + x^2 +  500x^2'
e46 = 'yx^2 + x^3 + 5xy + 7x + 500x^3'    
e47 = '(2+x1^3y2^3+y4^2z+3z^2+x3)/(2z+y3^10))^2'
s47 = 'x1 = 2, x3 = 7,y2 = 3, y3 = 4, y4 = 5, z=i'
e48 = '2+xy^3+yz+3z^2+x/(2.1z+y)'
s48a ='x=3,y=4,z=5'
s48b ='x=3,y=4'
s48c ='x=3'
e49 = '(1+2(x-1)+2(y-1)+(x-1)^2+4(x-1)(y-1)+(y-1)^2)'


'''
e = e26 
e = e48
print(e)
rat,rat_list,irat, irat_list = main(e)
print(rat)
#print(rat_list,'\n')
print(irat,'\n')
#print(irat_list)
'''

'''
s = s48a
print(evaluate(e,s,''))
print(evaluate(rat,s,5))
print(evaluate(irat,s,5))
'''

'''
e = '2 + xy^3 + yz + 3z^2 + x/(2z+y)'
s1 ='x=3,y=4,z=5'  # substitutions
s2 ='x=3,y=4'
s3 ='x=3'   
print(e)
print(evaluate(e,s1,5))
print(evaluate(e,s1,''))
print(evaluate(e,s2,'')) 
print(evaluate(e,s3,'')) 
'''


###################### rational differentiation ######################

def is_constant(Mlist):   # returns True if M = [c,0,0,...]
    if Mlist[0] == '0':    
        return True    
    for i in range(1,len(Mlist)):
        if Mlist[i] != '0': return False
    return True    

def der_mono(Mlist,var_position):    # mono list and var position  in list    
    L = len(Mlist)   
    # if variable  is missing or monomial a constant return zero             
    if Mlist[var_position] == 0  or is_constant(Mlist):        
       return ['0'] + [0 for i in range(L-1)]  
    coeff = Mlist[0]                    # coefficient of monomial 
    exp = Mlist[var_position]           # exponent of variable
    DMlist = tl.copylist(Mlist)         # list for derivative                      
    der_coeff = str(exp) + '('+ coeff +')'  # coefficient of derivative      
    DMlist[0] = ar.main(der_coeff)[0]      
    DMlist[var_position] -= 1          # reduce exponent by 1
    return DMlist

'''
Mlist = ['0',1,2,3]
Mlist = ['15',1,2,3]
#Mlist = ['3',0,0,0]
Mlist = ['7.5i',3,2,1]
var_position = 1
print(der_mono(Mlist,var_position))      
var_position = 3
print(der_mono(Mlist,var_position))      
'''

def der_pol(P,var):       
    varbs = tl.get_vars(P)[0]  
    if var not in P: return '0'   
    var_position = varbs.index(var) + 1                           
    Plist = main(P)[1][0] # list for P; discard trivial denominator    
    DPlist = []                                # list for derivative
    for Mlist in Plist:             # run through polynomial's monos
        
        DMlist = der_mono(Mlist,var_position) # mono derivative list      
        
        
        DPlist = [DMlist] + DPlist            # attach mono list                 
    return list2polynomial(DPlist)

'''
P = '3x^2y^3z^4 + 5x^2y^7z^4'   
P = '2x^3y^4z^5 + 3x^6y^7z^8'
var = 'y'
print(P)
print(der_pol(P,var))    
'''

def der_quotient(R,var):                   
    if var not in R: 
        return '0'                      
    if '/' not in R:
        return der_pol(R,var)
    
    num,den = R.split('/')
    
    der_num = der_pol(num,var) 
    der_den = der_pol(den,var)        
    
    der_quo_num = '('+ den +')('+ der_num +')-' + \
                       '(('+ num +')('+ der_den + '))'             
    der_quo_num = main(der_quo_num)[0]      # clean up
       
    der_quo_den = '(' + den + ')^2'
    der_quo_den = main(der_quo_den)[0]    
       
    der_quo =  '(' + der_quo_num + ')/(' + der_quo_den + ')'
    der_quo = main(der_quo)[0]                # clean up
    
    return der_quo

'''
#tl.print_fraction('     ','den * der_num - num * der_den', 'den^2','\n')    
#R = '7x^8/(3x^2y^3z^4)^3'    
R ='(7xy+3z)/(5z + 2y)'    
#R = '(7xy+3)/(3xy + 8)^4'    
#R = 'x/y^2'
#R = '1/y^2'
print(R) 
print('partial with respect to x:',der_quotient(R,'x'))
print('partial with respect to y:',der_quotient(R,'y'))
print('partial with respect to z:',der_quotient(R,'z'))
'''

def partial_derivative(R, wrt, substitutions):                
    wrt = list(wrt)      
    D = R
    for var in wrt:               # get successive derivatives
       D  = der_quotient(D,var)                     
    value = ''
    if substitutions != '':
        value = evaluate(D,substitutions,'')        
    return D,value    

'''
R = '7x^8/3x^2y^3z^4'    
R = '(2xy+3z)/(xy - 1)'
#R = 'x/y'
R = 'x^2+y^2'
wrt = 'xxyyy'
subs = 'x = 1,y = 1'
#subs = ''
D,val = partial_derivative(R, wrt, subs)
print('derivative wrt '+ wrt +':\n', D)
print('value at ' + subs + ':', val)
'''

####################### tangent plane  #############################

def tangent_plane(R,a,b):   
    a = str(a)
    b = str(b)    
    subs = 'x =' + str(a) + ',y =' + str(b)
    c = evaluate(R,subs,'')        
    pdx = partial_derivative(R, 'x',subs)[1]    # value at (a,b)
    pdy = partial_derivative(R, 'y',subs)[1]        
    pdx = tl.add_parens(pdx)
    pdy = tl.add_parens(pdy)       
    plane = c + '+' + pdx + '(x-' + a + ')+' + pdy + '(y-'+ b +')'  
    plane = tl.fix_signs(plane)                 
    return 'z = '+ plane

#R = '(2x^2y+3)/(3xy^3-1)'   
#print(tangent_plane(R,1,2))


######################## taylor series  ############################

def term_coeff(R,a,b,j,k):  
    wrt = j*'x'+ k*'y'   
    pval = partial_derivative(R,wrt,'x ='+ a + ',y = '+ b)[1]       
    f = str(ma.factorial(j)*ma.factorial(k))
    coeff = ar.main( '(1/('+ f +'))*(' + pval + ')')[0]  
    return coeff

def fixed_order_term(R,a,b,n):       
    S = ''    
    for k in range(n+1):
        j = n-k
        coeff = term_coeff(R,a,b,j,k)
        if coeff == '0' or coeff == '': 
            continue     
        if coeff == '1' and  n != 0: 
            coeff = ''
        if coeff == '-1': 
            coeff = '-'        
        exp_s = str(j)
        exp_t = str(k)
        coeff = tl.add_parens(coeff) 
        term  =  coeff + 's^'+ exp_s + 't^'+ exp_t                  
        if exp_s == '1':
            term = term.replace('s^1','s')
        if exp_t == '1':
            term = term.replace('t^1','t')
        term = term.replace('s^0','')
        term = term.replace('t^0','')
        
        S = S + ' + ' + term     
    
    if S == '':
       return ''   
   
    S = S.replace('s','(' + main('x-('+ a +')')[0] + ')')    
    S = S.replace('t','(' + main('y-('+ b +')')[0] + ')')   
    S = S.replace('(x-0)','x')
    S = S.replace('(y-0)','y')          
    S= tl.fix_signs(S)   
    return S

def taylor_series(R,a,b,N):   
    TS = ''
    TS = fixed_order_term(R,a,b,0)
    #print(0,TS)
    
    for n in range(1,N+1):        
        fot = fixed_order_term(R,a,b,n)
        if fot == '':
           continue
        TS = TS + '+' + fot
        #print(n,TS)
    TS = tl.fix_signs(TS)
    return TS

'''
R = '7x^8/3x^2y^3'
R = '3x^2y^3'
R = 'x/y'
R = 'x^2y^3'
R = 'x^2+y^2'
R = 'x^4y^6'
#R = 'x^2y^2'
a = '1'
b = '1'
a = '.5'
b = '.3'
N = 10

TS = taylor_series(R,a,b,N)
print(TS,'\n')
# check:
print(main(TS)[0])    
'''


###############################################
### old version with denominator squared, not expanded
### too complicated
'''
def der_quotient(num,den,var):                   
    if var not in num + den: 
        return '0','1'                  
    if den == '':
        return der_pol(num,var),''
    if ')' not in den:
        den = '(' + den + ')^1'       
        
    der_num = der_pol(num,var) 
    der_den = der_pol(den,var)        
    der_quotient_num = '('+ den +')('+ der_num +')-' + \
                       '(('+ num +')('+ der_den + '))'             
    der_quotient_num = main(der_quotient_num)[0] # clean up
       
    paren_factor,exp = den.split(')^')     # (2x^5+1)^3 --> (2x^5+1 3
    paren_factor =  paren_factor + ')'                   # (2x^5+1)       
    exp = str(2*int(exp))                                # 6                           
    den_squared = paren_factor + '^' + exp               # (2x^5+1)^6       
    return der_quotient_num, den_squared
'''





