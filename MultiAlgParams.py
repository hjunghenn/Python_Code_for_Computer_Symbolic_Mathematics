###### MultiAlgParams.py

import Number as nm
import Arithmetic as ar
import Tools as tl
import MultiAlg as mu
import LinSolve as ls
import PolyAlg as pa
import PolyDiv as pd
from operator import itemgetter
#global reverse
#reverse = False                                                  # default


#global dsymbols
# get_lower,get_upper, rest same as MultiAlg

############################ scalar conversion ##########################

def scalar2mono(s):
    return [s] + [0 for k in range(len(varbs))]

def scalar2rat(s):
        num = scalar2mono(s)  
        den = scalar2mono('1')
        return [[num], [den]] 

#varbs = 'xyz'
#print(scalar2rat('1.1-2i'))


########################## variable conversion ##########################

def var2mono(var,exp):                 # variable and its exponent NEW
    # 'x^2' -> ['1',2,0,...]  
    M  = scalar2mono('1')    
    position = varbs.index(var)   # varbs global; contains variable str            
    M[position+1] = exp         # put exponent in correct var position                     
    return M
    
def var2rat(var,exp):
    num = var2mono(var,exp)           
    den = scalar2mono('1')                       
    return [[num], [den]]    

#varbs = 'xyz'
#print(var2rat('y',7))


############################### calculations ############################

def combine_monos(P):  
    Q = []              
    for i in range(len(P)-1):        
        ##print(25,P)        
        if P[i] == '': continue      # already added        
        M = P[i]               # ith monomial: [coeff,powers]                 
        if M == [] or  M[0] == '0': 
            continue                     
        for j in range(i+1,len(P)):  # add succeeding like monomials to M
            if P[j] == '':
                continue
            N = P[j]
            if M[1:] == N[1:]:  # if powers the same, add the coefficients
               coeffsum = mu.main(M[0] + '+(' + N[0] +')')[0]
               M[0] = coeffsum               # update M's coefficient                
               P[j] = '' # mark as already added       
        Q.append(M)  # append nonzero monomial in P[i]              
    
    leftover_mono = P[len(P)-1]
    if leftover_mono != ''  and leftover_mono[0] != '0':     
        Q.append(leftover_mono)    # pick up leftover monomial at end
    
    return Q    

def multiply_monos(M,N):   
    # returns product of monomials M,N
    K = []                     # for output
    # multiply coefficients:          
    coeff_prod  = mu.main('(' + M[0] +')(' + N[0] + ')')[0]    
    #coeff_prod  = ar.main('(' + M[0] +')(' + N[0] + ')')[0]        
    K.append(coeff_prod)
    # add integer exponents of same variables:      
    for i in range(1,len(N)): 
        K.append(M[i] + N[i])  
    return K

#M = ['2a',3,4,5]; N = ['-3b',6,7,8]
#print(multiply_monos(M,N))


def multiply_pols(P,Q):                   
    # multiplies 2 lists of monomials    
    R = []               # list for product polynomial
    for M in P:          # get all possible products M*N
        for N in Q:
            K = multiply_monos(M,N)   
            R.append(K)                
    R = combine_monos(R)      
    return R
'''
P = [ ['2a',3,4,5], ['-b',6,7,8] ]
Q = [ ['5.7c',9,10,11], ['(3/2)d',12,14,16] ]
R = multiply_pols(P,Q)
#print(P)
#print(Q,'\n')
#print(R,'\n')
'''

def multiply_rationals(R, S):      # multiplies two poly ratios    
    num = multiply_pols(R[0], S[0]) # multiply numerators
    den = multiply_pols(R[1], S[1]) # multiply denominators 
    return [num,den]

def divide_rationals(R,S):  
    T = [S[1],S[0]] 
    return multiply_rationals(R,T)

def mono_scalar_prod(s,M):
    # '3'*['5',6,7] = ['15',6,7]        
    prod  = mu.main('(' + s +')(' + M[0] + ')')[0] 
    #prod  = ar.main('(' + s +')(' + M[0] + ')')[0] 
    return [prod] + M[1:]

def pol_scalar_prod(s,P):
    # multiplies a  polynomial  by a scalar: 
    # '3'*[['5',6,7],['7',8,9]] = [['15',6,7], ['21',8,9]]      
    Q = []
    for M in P:
        N = mono_scalar_prod(s,M)
        Q.append(N)
    return Q        

def rat_scalar_prod(s,R):
    # multiplies a rational function by a scalar: 
    return [pol_scalar_prod(s,R[0]),R[1]]        

def rational_power(R,n):    
    S = R
    if n > 1:
       for i in range(n-1):    # multiply P times itself n-1 times
           S = multiply_rationals(S, R)    
    num = combine_monos(S[0])
    den = combine_monos(S[1])
    return [num,den]

def add_pols(P,Q):
    if P == []: return Q
    if Q == []: return P
    S = P+Q           # concatenation
    #S =  combine_monos(S)     
    return S

def add_rationals(R,S):
    numR = R[0]
    denR = R[1]
    numS = S[0]
    denS = S[1]
    A = multiply_pols(denR,numS)
    B = multiply_pols(denS,numR)
    num = add_pols(A,B)
    #num = combine_monos(num)     
    den = multiply_pols(denR,denS) 
    #den = combine_monos(den)         
    return [num,den]     

def subtract_rationals(R, S):
    minusS = rat_scalar_prod('-1',S)
    return add_rationals(R,minusS)       
  
'''
R = [ [['2a',3,4,5], ['-b',6,7,8]], [['5a',9,10,11], ['7b',12,14,16]]]
S = [ [['b',3,4,5], ['-d',6,7,8]], [['5c',9,10,11], ['7d',12,14,16]]]
varbs = 'xyz'
#print(divide_rationals(R,S))
'''

################################# sorting ################################   

def sort_list(P): ###same              # polynomial list    
    import copy    
    Q = copy.deepcopy(P)
    l = len(Q)                     # number of mono lists in pol
    m = len(Q[0])                 # length of a mono list
    for i in range(l):       # sum the powers of each mono list
        sum = 0            
        for j in range(1,m):      # sum the powers of ith mono
            sum = sum + Q[i][j]
        Q[i].append(sum)   # append sum to end of ith mono list
         # sort pol_list on the last field (sum of powers)  
    sorted_list = sorted(Q, key=itemgetter(m), reverse = True)           
    for i in range(l):
        sorted_list[i] = sorted_list[i][:m] # remove sum of powers          
    return sorted_list            


############################ clearing fracs #############################

def get_mono_denom(M):
    # e.g. M = [ (1/2)a+(3/5+(6/7)i)b^2,4,5] --> [2,5]
    mono_denoms = [1]            # default
    idx = 0
    while idx < len(M[0]):
        if M[0][idx] != '/': 
            idx +=1; continue 
        d,end = tl.extract_integer(M[0],idx+1) 
        idx = end        
        mono_denoms = mono_denoms+ [int(d)]
    return mono_denoms

#M = ['(1/2)A+(3/5+(6/7)i)B^2',4,5]
##print(get_mono_denom(M))


def get_pol_lcm(P):
    pol_denoms = []
    for M in P:
        mono_denoms = get_mono_denom(M)
        pol_denoms = pol_denoms + mono_denoms       
    return nm.listlcm(pol_denoms)    
    
#P = [['(1/2)A+(3/5+(6/7)i)B',4,5], ['(1/8)a+ (6/21)B',6,7]]
##print(get_pol_lcm(P))


def clear_pol(P):
    Q = []
    lcm = str(get_pol_lcm(P))
    for M in P:
        prod = mu.main(lcm +'('+ M[0] +')' )[0]        
        #prod = ra.rational_calc( lcm +'('+ M[0] +')' )[0]                
        N = [prod] + M[1:]
        Q.append(N)
    return lcm, Q  
        
#P = [['(1/2)A+(3/5+(6/7)i)A',4,5], ['(1/8)A+ (6/5)B',6,7]]
##print(clear_pol(P))


############################### conversions #############################       

def list2monomial(Mlist): ### multi variable
    # takes monomial list and returns monomial              
    expr = ''    
    coeff = Mlist[0]            
    coeff = mu.main(coeff)[0]   
    if coeff == '0' or coeff == '-0': 
        return '0'       
    if len(Mlist) == 1: 
        return coeff  
    mono = ''       
    for i in range(1,len(Mlist)):
        var  = varbs_list[i-1]
        exp = Mlist[i]                 # exponent of variable 
        #print(2224,i,var,exp)       
        if exp > 1:          
            mono = mono + var + '^' + str(exp)    # attach exp != 1                 
        elif exp == 1:
            mono = mono + var     
    
    if coeff == '1': 
        coeff = ''        # coeff '1' not needed 
    if coeff == '-1':  
        coeff = '-'                   
    if coeff != '' or exp != 0:       
        coeff = tl.add_parens(coeff)   # attach suitable parens        
    
    expr = coeff +  mono                    
    expr = tl.fix_signs(expr)         
    return expr

def list2polynomial(P):
    pol = ''      
    P = combine_monos(P)                  
    Q = sort_list(P)       
 
    for M in Q:                      
        mono = list2monomial(M)           # get the monomial                              
        if mono == '0': continue          # skip any zero coeff    
        pol = pol + '+' + mono            # attach to pol
    if pol  == '': pol= '0' 
    pol = tl.fix_signs(pol)              
    return pol  

def list2rational(R):                   
    num = list2polynomial(R[0])  
    den = list2polynomial(R[1])                     
       
    if num == '0': return '0'
    if den == '1' or den == '': return num
    if den == '-1': 
       num = tl.add_parens(num) 
       return '-' + num    
    if len(R[0]) > 1: num = '('+ num + ')'
    if len(R[1]) > 1: den = '('+ den + ')'        
    return num + '/' + den  

'''    
R = [ [['2',3,4,5], ['-1',6,7,8]], [['5',9,10,11], ['7',12,14,16]]]
varbs = 'xyz'
#print(list2rat(R))
##print(tlk.#print_fraction(R[0],R[1]))
'''

def list2int_rational(R):  
    # converts rational list into integer rational function    
    numR = R[0] 
    denR = R[1]    
    if numR == denR: return '1',''    
    lcmP,P = clear_pol(numR)           
    lcmQ,Q = clear_pol(denR)       
    #factor = ar.main(lcmQ +'/'+ lcmP)[0]
    factor = mu.main(lcmQ +'/'+ lcmP)[0]   
    irat_list = [P,Q]       
    ###irat_list = reduce_coeffs(irat_list) # not used here        
    irat = list2rational(irat_list)                    
    if factor == '1': factor = ''         
    factor = tl.add_parens(factor) 
    if factor != '':
        irat = tl.add_parens(irat)           
    return factor+irat, irat_list   
  

############################ the allocator ##########################

def allocate_ops(expr,mode):
    global idx, varbs,pars          
    R = []
    while idx < len(expr):
        ch = expr[idx]
         
        if ch in tl.numeric:
             start = idx
             s,idx = tl.extract_numeric(expr, start)                      
             R = scalar2rat(s)        
        
        elif ch in varbs:            
             idx +=1              
             exp,idx = tl.extract_exp(expr, idx)           
             exp = ar.main(exp)[0]           
             R = var2rat(ch,int(exp))
        
        elif ch in pars:                             ## added
             idx +=1              
             exp,idx = tl.extract_exp(expr, idx)           
             exp = ar.main(exp)[0]             
             ch = ch + '^' + exp
             R = scalar2rat(ch)
    
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
            idx += 1 
            exp = allocate_ops(expr,2)[0][0][0]  # [['exp',0,...,0]]            
            R = rational_power(R, int(exp))

        elif ch == '(':
            start = idx
            paren_expr,end = tl.extract_paren(expr,start)          
            if  tl.isarithmetic(paren_expr):              
                r = ar.main(paren_expr)[0]  # constant expression  
                num = scalar2mono(r)
                den = scalar2mono('1')
                R = [[num],[den]]               
                idx=end            
            else:
                idx+=1             
                R = allocate_ops(expr,0)
                idx+=1     
        
        elif ch == ')': break
    return R 


###########################  main ################################

def main(expr):
    global idx                  # points to current character in expr
    global varbs, varbs_list             # variable letters in expr 
    global pars,pars_list                # parameter letters in expr     
      
    varbs = tl.get_lower(expr)                  
    pars = tl.get_upper(expr)    
    if varbs == ''  or   pars == '': 
       return mu.main(expr)   
    
    varbs_list = list(varbs)
    pars_list = list(pars)
     
    expr = tl.attach_missing_exp(expr,varbs+pars)
    expr = tl.fix_signs(expr)
    expr = tl.fix_operands(expr)  
    expr = tl.insert_asterisks(expr,varbs+pars)                              
    idx = 0             # start at beginning of expr        
    R = allocate_ops(expr,0)       # make the calculations
    num = R[0]; den = R[1]        
    num = combine_monos(num)       
    den = combine_monos(den)                         
    num = sort_list(num)      
    den = sort_list(den)         
    ratlist = [num,den]      
    rat = list2rational(ratlist)               
    irat, iratlist = list2int_rational(ratlist)         
    return rat,ratlist,irat,iratlist
    
 
def evaluate(expr,substitutions):        
    if substitutions == '':
        return expr,'','','',''  
    substitutions = substitutions.split(',')    
    for i in range(len(substitutions)):        
        substitutions[i] = substitutions[i].replace(' ','')
        var,val = substitutions[i].split('=')         
        if var == '' or var not in expr: continue          
        expr = expr.replace(var,'(' + val + ')')                          
    expr = tl.fix_signs(expr)                                
    if tl.isarithmetic(expr): 
       return ar.main(expr)[0],'','',''  
    return mu.main(expr)

'''
e1 = '(4.3zAx-3yC)^3'
e2 = '(2x+C)^3 + 5Ax^2'
e3 = '(A2Bx+3.7C)/(x+8yD)^2'
e4 = '.5A^2x + By'
e5 = 'Ay/(x-1/2) + Bx/(z-2/3) + Cz/(y-3)'
e6 = 'Ay/(zx-1) + Bx/(yz-2) + Cz/(xy-3)'
e7 = 'A(2x+1)+B(5x-7)-(3x+5)'
e8 = '(3A+4B)^2x'
e9 = '(x+1)^2-1' # ok
e10 = 'x+B' #                           
e11 = '1.1Ay/(2.3Bx-1.1) + 4.5Cx/(6.7Dz-2.2)'
e12 = 'x^4/y^6z^6'
e13 = 'B(3x-5) + (3x+7)'
e14 = '5A+3xB+5x^3C'
e15 = '3xB+5xC'
e16 = '3x^2B + 5xC'
e17 = 'x^2A+2Ax'     
e18 = '(5Ax+B+C)^2' 
e19 = '(5Ax+B+1)^2' 
e20 = '5Ax+B+Cx^3'
e21 = '(x+A+1)^2'   
e22 = '(1.2Bx+A)^2'   
e23 = '(Bx+Ax^2)^2'  
e24 = '(By+Ax^2)^2'  
e25 = '(1.1Ax+2.3By)^2'
e26 = 'Ay/(Bx-1.1) + Cx/(Dz-2.2)'


e = e26
#print(e)
rat,rat_list, irat, irat_list = main(e)
print(rat,'\n')
print(irat)
print(e)

substitutions = 'x = (5),y = (7),z = (9), A = (8),B = (6),C = (2),D = (3)'
rat,rat_list,irat,irat_list = evaluate(rat,substitutions)
print(30,rat)
#print(rat_list)
print(irat)
#print(irat_list)

### check:
e = e.replace('x','(5)')
e = e.replace('y','(7)')
e = e.replace('z','(9)')
e = e.replace('A','(8)')
e = e.replace('B','(6)')
e = e.replace('C','(2)')
e = e.replace('D','(3)')
print(40,e)
print(41,ar.main(e)[0])
'''


########################## summation formulas ##########################

#global varletters
#varletters = tl.letters

def pol_diff(p):
    term = ''
    for k in range(p+1):        
        letter = tl.upper[k]
        power = p-k+1        
        term = term +'+'+ letter +'((n+1)^'+ str(power) +'-n^'+ str(power) +')'
    term = term + '- (n+1)^' + str(p)   
    return main(term)[1][0]    
#print(pol_diff(2))   
    

def get_coefficients(p):
    eqns = ''
    pol_diff_list = pol_diff(p)       
    for k in range(p+1):
        eqns += pol_diff_list[k][0] + '= 0,'
    coeffs = ls.linsolve(eqns[:len(eqns)-1],'','',False) 
    return coeffs


def make_formula(p):    
    coeffs = get_coefficients(p)       
    formula = ''
    L = len(coeffs)
    for k in range(len(coeffs)):
        if coeffs[k] == '0': continue        
        coeffs[k] = coeffs[k].split('=')[1]
        coeffs[k] = tl.add_parens(coeffs[k])            
        formula = formula + '+' + coeffs[k] + 'n^' + str(L-k)           
    formula = formula.replace('^1','')  
    formula = tl.fix_signs(formula)
    formula = pa.main(formula)[4]         
    formula = pd.factor_polynomial(formula)    
    return formula

#print(make_formula(11))

def check_formula(p,n):  
    summation = '1'
    for k in range(2,n+1):
        summation = summation + '+' + str(k) + '^' + str(p)                          
    summation = ar.main(summation)[0]                
    formula = make_formula(p)
    formula = formula.replace('n','(' + str(n) + ')')      
    formula = ar.main(formula)[0]  
    return summation, formula

#p = 11
#n = 8
#print(check_formula(p,n))
 

########################## partial fractions ###########################

def get_numerator_denominator():
    global numerator, denominator, rational
    rational = rational.replace(' ','')      
    numerator, denominator = rational.split('/')   
 

def get_denominator_factors():   
    global denominator, denominator_factors
    denominator_factors = denominator.replace('(',',(')
    denominator_factors = denominator_factors.split(',')
    denominator_factors = denominator_factors[1:]   # remove first comma 


def make_template():                                                
    global template, var                                            
    template= []                                                    
    var = tl.get_var(rational)                                     
    k = 65                                    # ASCII code for 'A'  
    for den in denominator_factors:                                 
        if ')^' not in den:                       # for uniformity  
            den = den+'^1'        # e.g. (x^2+x+1) --> (x^2+x+1)^1  
        factor,exp = den.split(')^') # (x^2+x+1)^2 --> (x^2+x+1, 2  
        factor = factor + ')'                      # --> (x^2+x+1)  
                                                                    
        if '^2' not in factor:                     # linear factor  
            for i in range(1,int(exp)+1):                           
                if i == 1:                       # (x+1) -->A(x+1)  
                   template.append([chr(k), factor])                
                else:                          # (x+1) -->A(x+1)^i  
                   template.append([chr(k), factor +'^'+ str(i)])   
                k += 1                                              
        else:                                   # quadratic factor  
            for i in range(1,int(exp)+1):                           
                if i == 1: # (x^2 + x + 1) --> Ax+B, (x^2 + x + 1)  
                    template.append(['('+ chr(k) + var +'+'+    \
                                          chr(k+1) +')',factor])    
                else:    # (x^2 + x + 1) --> Ax+B, (x^2 + x + 1)^i  
                    template.append(['('+ chr(k) + var +'+'+ \
                              chr(k+1) +')', factor +'^'+ str(i)])                           
                k += 2                                              
        if k == 90:                         # ran out of caps, sorry
            break                                                   
                                                                                                                                    

def clear_partial_fractions():  
    global partials_cleared 
    partials_cleared = []
    for t in template:       # eg. t = ['(Cx+D)', '(x^2+2x+5)^2']
        den = t[1]           # '(x^2+2x+5)^2'              
        Q,R = pd.div_alg(denominator,den)     # denominator/(x^2+2x+5),0               
        partials_cleared.append(Q)
    
    #print(8888888,partials_cleared)


def make_expression():   
    global expr 
    expr = '' 
    for i in range(len(partials_cleared)):
       prod = template[i][0] + '('+ partials_cleared[i] +')'
       expr  = expr  + '+' + prod    
    expr  = expr[1:]    # remove first plus
 

def make_equations(): 
    global equations
    equations = ''
    make_expression()        
    diff = expr +'-'+ numerator
    diff = main(diff)[1][0]     
    for entry in diff:
        eqn = entry[0] + '= 0'
        equations = equations + ',' + eqn                                         
    equations = equations[1:]               # remove initial comma
    
 
def get_letter_values():
    global letter_values
    letter_values = []
    letter_vals = ls.linsolve(equations,'','',False)   
    for item in letter_vals:
        letter,value = item.split('=')
        letter = letter.replace(' ','')
        value = value.replace(' ','')
        letter_values.append([letter,value]) 


def substitute_values():
    for j in range(len(template)):                                 
        num = template[j][0]
        for item in letter_values:          
            if item[0] in num:
                item[1] = tl.add_parens(item[1])                
                template[j][0]= template[j][0].replace(item[0],item[1])                    
        

def print_expansion():
    global template #letter_values
    substitute_values()           
    tl.print_fraction('',numerator,denominator,'')   # #print the rational    
    print('\n')
    for j in range(len(template)):                                        
        num = template[j][0]           
        den = template[j][1]
        num = pa.main(num)[0]                  # clean up            
        if num == '0':                        # nothing to #print
            continue            
        if j == 0:
            tl.print_fraction(' = ',num,den,'')   # #print the first term     
            print('\n')       
        else: 
            tl.print_fraction(' + ',num,den,'')  # #print the rest           
            print('\n')         
                  

def expansion_check(val):
    global template
    substitute_values()           
    expansion = ''
    for j in range(len(template)):                                 
        num = template[j][0]
        den = template[j][1]   
        #num = pl.polycalc(num)[0] 
        term =   '(' + num  + ')/(' + den + ')'
        expansion = expansion + '+(' + term+ ')'    
    expansion = tl.fix_signs(expansion)    
    diff = expansion + '-('+ rational + ')'
    print('\n',ar.evaluate(diff,val,'')[0])


def partial_fractions():   
    global equations, partials_cleared
        
    print('Step 1: get numerator and denominator of rational:') 
    get_numerator_denominator()   
    print(numerator,',',denominator,'\n')
      
    print('Step 2: get denominator factors:') 
    get_denominator_factors()   
    print(denominator_factors,'\n')
    
    print('Step 3: make template:')
    make_template()  
    print(template,'\n')   
           
    print('Step 4: clear partial fractions:')
    clear_partial_fractions()
    tl.print_list(partials_cleared,'v')
    print('\n')
    
    print('Step 5: make expression from cleared partial fractions:') 
    make_expression()
    print(expr,'\n')
         
    print('Step 6: make equations:') 
    make_equations()
    tl.print_list(equations,'v')
    print('\n')
      
    print('Step 7: get letter values:')    
    get_letter_values()
    print(letter_values,'\n')   
      
    print('Step 8: print the expansion:') 
    print_expansion()       
    
    print('Step 9: expansion check:') 
    expansion_check('(1/2)')
 


r = '(2x^2+5x-3)/(x^2+x+1)^4(x-5)^3(x+9)'
#r = '(2x^3+5x-3)/(2x-5)^2(x^2+1)^3'
#r = '(2x+5)/(x-1)^2(x-2)^3'
#r = '(2x^2 + 3x + 5)/(5x-7)^5(2x+1)(3x-8)'
#r = '(3x + 5)/(5x-7)(2x+1)'
#r = '(2x^2 + 3x + 1)/(x-1)(x+2)(2x-3)^2'
#r = '(2x^2 + 3x + 1)/(x^2+x+1)^2(x+2)(2x-3)^2'
#r = '(2x^2 + 3x + 1)/(x^2+x+1)(2x-3)^2'
#r = '(2x + 5)/(x-1)^2(x+2)'
#r = '(2x + 5)/(x+1)^2(x+2)'
r = '(7x^2+3)/(x+1)^2(x^2+2x+5)'
#r = '(7x^2+3)/(x+1)(x+2)(x^2+2x+5)^3'
#r = '(7x^2+3)/(x^2+2x+5)^3'
#r = '2x/(x^2+2x+5)^3'
rational = r                # global
partial_fractions()




'''
def no_reverselist2monomial(Mlist): ### working
    # takes monomial list and returns monomial          
    coeff = Mlist[0]            
    if coeff == '0' or coeff == '-0': 
        return '0'   
    
    if len(Mlist) == 1 or Mlist[1] == 0:   
        return coeff
    
    #if Mlist[1] == 1
    #   return
        
 
    var = 'x'               
    exp = Mlist[1]               # exponent of variable 
        
    ##print(4550,mono,var)
    ##print(4555,mono+var)
    ##print(4556,var+mono)            
    #mono = mono + var                   
    
    mono = var
    
    if exp != 1:          
        mono = mono + '^' + str(exp)    # attach exp != 1    
     
  
    if coeff == '1': 
        coeff = ''        # coeff '1' not needed 
    if coeff == '-1':  
        coeff = '-'                   
    if coeff != '' or exp != 0:         
        coeff = tl.add_parens(coeff)   # attach suitable parens        
                
    expr = coeff + mono
     
    expr = tl.fix_signs(expr) 
   
    return expr


M = ['A+7i',5,6,7]
varbs = 'xyz'
#print(M)
#print(list2monomial(M))

M = ['A+7i',5,6,7]
varbs = 'xyz'
#print(M)
#print(list2monomial(M))
'''


'''
def expand_power_differences(p):
    powers = []    
    for k in range(p+1,0,-1):
        term = '(n+1)^' + str(k) + '-n^' + str(k)
        term = main(term)[0]
        powers.append(term)
    return powers        

#print(expand_power_differences(2))


def attach_coefficients(p):
    pol = '' 
    powers = expand_power_differences(p)
    L = len(powers)       
    for k in range(L):
        v = tl.upper[k]  
        term = v + '(' + powers[k] + ')'  # attach cap
        pol = pol + '+' + term    
    pol = pol[1:]                       # remove extra '+'     
    return main(pol)[1][0]           # numerator only  

#print(attach_coefficients(2))

def make_equations(p):
    equations = ''
    left_side = attach_coefficients(p)        
    right_side = main('(n+1)^' + str(p))[1][0]
    for k in range(len(left_side)):
        eqn = left_side[k][0] + '='+ right_side[k][0] 
        equations =  equations  +','+ eqn
    return equations[1:]


def list2monomial(Mlist): # with revese
    # takes monomial list and returns monomial              
    expr = ''    
    coeff = Mlist[0]            
    coeff = mu.main(coeff)[0]   
    if coeff == '0' or coeff == '-0': 
        return '0'       
    if len(Mlist) == 1: 
        return coeff  
    mono = ''       
    for i in range(1,len(Mlist)):
        var  = varbs_list[i-1]
        exp = Mlist[i]                 # exponent of variable 
        #print(2224,i,var,exp)       
        if exp > 1:          
            mono = mono + var + '^' + str(exp)    # attach exp != 1                 
        elif exp == 1:
            mono = mono + var     
    
    if coeff == '1': 
        coeff = ''        # coeff '1' not needed 
    if coeff == '-1':  
        coeff = '-'                   
    if coeff != '': # or exp != 0:  ???       
        coeff = tl.add_parens(coeff)   # attach suitable parens        
 
    if not reverse:
        expr = coeff +  mono      
    else:                        
       coeff1,end = tl.extract_sequence(coeff,0,'()/.1234567890')   
       coeff2 = coeff[end:]  
       
       print(3030,coeff1,coeff2)
       
       
       expr = expr + '+' + coeff1 + mono + coeff2         
    expr = tl.fix_signs(expr)         
    return expr

'''




