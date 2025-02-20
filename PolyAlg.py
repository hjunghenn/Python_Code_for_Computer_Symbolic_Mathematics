
############################ PolyAlg.py ############################
####################################################################

import Number as nm
import Arithmetic as ar
import Tools as tl
import math as ma

####################################################################

#e = '(x/(3.4+2.7i)+2.4i/7.8)^2(x-5)'
#e = '(1/2^2)((x+2i)^10-(x-2i)^10))'
#e = '(.5x+3/4)^2'
#e = '4((2n^3+3n^2+n)/6)'
#e = '(x+1)(x/(x+1))'
#e = '1-(x^2+3x + 5)'
#e = '((1/5)x+(3/25)i)(5ix+7)^2+(-46/25i)+(x^2 + 2x - 1)^3'
#e = '(-46/25)-(x^2 + 2x - 1)'
#e = '((1/5)x+(3/25))(5x+7) +(-46/25) -(x^2 + (2.3+5/i)x) - 1'
#e = '(3.1/2.5i)^21(x+(1/8))x'
#e = '(5ix+7)^5'
#e = 'x+(2.1/3.8+4.7i)^2'
#e = 'x^0'
#e = '4((x^2+x)/2)'
#e = '(x^2+7x)/2i'
#e = '(2x^2 + x + 4)((1/2i)x^2 - (7/3)x - 11/8)'
#e = '(x^2+x+1)^2(x-1)(x+2)(2x-3)^3'
#e = '(2x+3)(4x-5)(x+2)(2x-3)^3'
#e = '(2x+3i)(4.7ix-5)'
#e = '5x^2+3x-5+3i-3i+12'
#e = '3 -3i'
#e = '(x^2-3x)x'
#e = '(2/3)ix'
#e = '(x+1)-1'

####################################################################

############################# operations ###########################

def prependzeros(P,Q):
    numzeros = abs(len(P)-len(Q))
    Z = tl.zero_list(numzeros)
    if len(P) > len(Q):
       Q = Z+Q                 # prepend zero list to Q
    if len(Q) > len(P):
       P = Z+P                 # prepend zero list to P
    return P,Q        
 
def remove_leading_zeros(P):
    if len(P) == 1: return P  # don't remove everything       
    while len(P) > 1 and  P[0] == '0':
        P = P[1:]         
    return P

'''
print(remove_leading_zeros(['1','2','3']))
print(remove_leading_zeros(['0','0','1']))
print(remove_leading_zeros(['0','0']))
print(remove_leading_zeros(['0']))
'''

def pol_sum(P,Q):         
    P,Q = prependzeros(P,Q) 
    #print(P,'\n',Q)
    S = []
    for i in range(len(P)):                  # add termwise
        s = ar.main('('+ P[i] +')+('+ Q[i] + ')')[0]     
        #S = S + [s]
        S.append(s)
    S = remove_leading_zeros(S)  
    return S

def pol_scalar_prod(scalar,P):               # returns scalar*P
    Q = []
    if isinstance(P,str):
        P = [P]        
    for entry in P:       # multiply each item in P by scalar
       s = ar.main('(' + scalar + ')*(' + entry + ')')[0]
       Q.append(s)  
    return Q 

def pol_diff(P, Q):                       # returns  P - Q
    R = pol_scalar_prod('-1',Q)    
    return pol_sum(P,R)
    
def pol_prod(P, Q):
    M = []
    L = len(P)+len(Q)-1
    for k in range(L):       # for each k calculate c_k
        ck = '0'                          # reset
        for i in range(len(P)):          
            for j in range(len(Q)):
                if i+j == k:
                   ck = ar.main(ck + '+('+ P[i] +')('+ Q[j] + ')')[0]     
        M.append(ck)        
    return M

def pol_power(P,n):
    Q = P
    if n > 1:
       for i in range(n-1):             # multiply P by itself n-1 times
           Q = pol_prod(P, Q)
    return Q

def pol_quotient(P,q):                  # q a scalar   
    z = ar.main('1/('+q+')')[0]
    return pol_scalar_prod(z,P)

'''
P = ['1','2','3','4']
Q = ['1','1','1','1','1']
P = ['1','2','3']
Q = ['2','1']
print(pol_sum(P,Q))
print(pol_diff(P,Q))
print(pol_prod(P,Q))
print(pol_power(Q,4))
'''

############################ allocate ops ##########################

def allocate_ops(expr,mode):
    global idx,var 
 
    P = []
    
    while idx < len(expr):
        
        ch = expr[idx]   
        if ch in '.0123456789i':
            start = idx
            r,idx = tl.extract_numeric(expr, start)
            P = [r]
     
        elif ch == var:           # e.g x^3
            idx +=1               # move var to '^'
            exp,idx = tl.extract_exp(expr,idx)           
            n = int(exp)                   
            P = ['1'] + tl.zero_list(n)   # list for x^n  
  
        elif ch == '+':
            if mode > 0: break              # wait for higher mode
            idx += 1
            Q = allocate_ops(expr,0)
            P = pol_sum(P,Q)   

        elif ch == '-':
            if mode > 0: break              # wait for higher mode
            idx += 1
            Q = allocate_ops(expr,1)
            P = pol_diff(P,Q)
   
        elif ch == '*':
            if mode > 1: break
            idx += 1                      
            Q = allocate_ops(expr,1)
            P = pol_prod(P,Q)
               
        elif ch == '^':
            idx += 1 
            exp = allocate_ops(expr,2)[0]  # inside of singleton list            
            P = pol_power(P, int(exp))  
           
        elif ch == '/':
            if mode > 1: break 
            idx += 1
            Q = allocate_ops(expr,1) # get denominator, a scalar         
            q = Q[0]       
            P = pol_quotient(P,q)
        
        elif ch == '(':            
            start = idx
            paren_expr,end = tl.extract_paren(expr,start) 
           
            if not var in paren_expr:
                r = ar.main(paren_expr)[0] # arith expression
                P = [r]
                idx=end
            else:
                idx+=1
                P = allocate_ops(expr,0)
                idx+=1
        elif ch == ')': break  
    return P


############################### pol2lists #############################


def expr2flist(expr):
    global idx,var
    #expr = tl.attach_missing_coeff(expr,var)  
    expr = tl.attach_missing_exp(expr,var)    
    expr = tl.insert_asterisks(expr,var)
    idx = 0                                  # start of expression          
    flist = allocate_ops(expr,0)       # fraction coefficients         
    return flist 

   
def flist2mlist(flist):    
    if len(flist) <= 1: return flist
    mlist = []                                                 
    multiplier = flist[0]               # leading coefficient of flist
    # invert leading coefficient                   
    reciprocal = ar.main( '1/('+ multiplier + ')')[0]   
    # multiply each coefficient except the first by reciprocal
    for c in flist[1:]:  
        z = ar.main( '('+ reciprocal + ')(' + c + ')')[0]
        mlist.append(z)
    mlist = ['1'] + mlist                           # make monic 
    mlist = [multiplier] + mlist          # attach compensating factor     
    return mlist

def get_denoms(flist):
    denoms = [1]            # default            
    for i in range(len(flist)):
        coeff = flist[i]
        re = ar.real(coeff)
        im = ar.imag(coeff)    
        if '/' in re:
            den = int(re.split('/')[1])  # get denominator of real part
            denoms.append(den)
        if '/' in im:
            den = int(im.split('/')[1]) # get denominator of imag part
            denoms.append(den)        
    return list(set(denoms))   # remove duplicates

#flist = ['1/12','1/5','1/4','1/3']
#print(get_denoms(flist))

def flist2ilist(flist):     
    ilist = []       
    denoms = get_denoms(flist)              
    lcm = nm.listlcm(denoms)    # get least common multiple of denoms   
    for item in flist:           # multiply each item by the lcm
        prod = ar.main(str(lcm) + '*(' + item + ')')[0]
        ilist.append(prod) 
    multiplier = '1/'+ str(lcm)                    # compensatory factor
    multiplier = ar.main(multiplier)[0]                 # reduce factor        
    #if factor == '1': factor = ''
    ilist = [multiplier] + ilist        
    return ilist


############################### list2pol #############################

def attach_parens(pol_list):
    L = len(pol_list)
    if L <= 1: return pol_list   
    P = []
    for k in range(L-1):    # attach parens to all but constant term
        coeff = pol_list[k]       
        #if '/' in coeff or '+' in coeff or '-' in coeff:
        coeff = tl.add_parens(coeff)        
        coeff = tl.fix_signs(coeff)
        P.append(coeff)              
    P.append(pol_list[L-1])           # pick up constant term          
    return P    

#flist = ['-1/2','3', '(3/2)i', '3/2i', '5-2i', '2-4i']
#print(attach_parens(flist))



def flist2pol(flist):       
    P = attach_parens(flist)  # enclose fractions and complex no.s                    
    pol = ''                  # initialize polynomial string
    L = len(P)          
    # attach coeffs to var  
    for exp in range(L):                     # exponent of term
        v = var
        if exp == 0: v = ''                       # omit x^0
        coeff = P[L-exp-1]                 # coefficient of x^exp
        if coeff == '0': continue               # skip zero coeff    
        if coeff == '1' and exp != 0: coeff = ''    # redundant
        if coeff == '-1' and exp != 0: coeff = '-'  # redundant        
        term = coeff + v           
        if exp > 1:                # omit power x^exp for exp = 1
            term = term + '^' + str(exp)   
        pol = term + '+' + pol
    if  pol == '': return '0'
    pol =  pol[:len(pol) - 1]                 # remove extra '+'        
    #pol = tl.fix_signs(pol)   
    pol = pol.replace('( - ', '(-')          # make pretty
   #pol = tl.remove_extra_parens(pol)     
    pol = tl.fix_signs(pol)  
    return pol

#var = 'x'
#flist = ['-1/2','3', '2i', '5-7i', '2-4i']
#print(flist2pol(flist))


def is_single_term(pol_list):                     
    L = len(pol_list)    
    if L == 1: 
        return True                 # polynomial has only one term       
    numzeros = 0
    for item in pol_list:   # calculates number n of zeros in list 
        if item == '0':
            numzeros +=1
    return numzeros == L-1    # has only one term if all L-1 zeros        

def attach_multiplier(pol_list,pol,multiplier):     
    if multiplier == '1': return pol    
    if ar.is_complex(multiplier) or ar.is_frac(multiplier): 
        multiplier = '(' + multiplier + ')'
    if not is_single_term(pol_list):
        pol = '(' + pol + ')'   
    return multiplier+pol   

def mlist2pol(mlist):          
    if len(mlist) == 1: 
        return mlist[0]
    multiplier = mlist[0]         
    P = mlist[1:]           # list without multiplier       
    pol = flist2pol(P)            
    return attach_multiplier(P,pol,multiplier)    

def ilist2pol(ilist):          
    multiplier = ilist[0]         
    P = ilist[1:]        
    pol = flist2pol(P)                       
    return attach_multiplier(P,pol,multiplier)    


################################# main ###############################

def main(expr):   
    global var
    var = tl.get_var(expr)
    flist = expr2flist(expr)          
    fpol = flist2pol(flist)        # general fractional form    
    mlist = flist2mlist(flist)       
    mpol = mlist2pol(mlist)        # monic form    
    ilist = flist2ilist(flist)             
    ipol = ilist2pol(ilist)       # integer coefficient form                    
    return fpol,flist,mpol,mlist,ipol,ilist


#e = '(2x^2 + x + 4)^3(1+(1/2i)x^2 - (7/3)x - 11/8)'
e = '(3.1x +1-2.4i)^2 - 7x + 5/8i'
#e = '5'
#e = '(x^3+1)-1'
#e = '0'
#e = '(2x^4 + 5x^3 + 3x)^3'
#e = '(2.7x+1)^2'
#e = '(.5x+1/3)^2'
#e = '(2x+3)(5x+7) + 3'
#e = 'x^3 - 3x^2 + 3x - 1'
#e = '(5x)^2'


'''
fpol,flist, mpol,mlist,ipol,ilist = main(e)
print('fpol: ',fpol)
print('flist:',flist)
print('mpol: ',mpol)
print('ipol: ',ipol)
print('ilist:',ilist)
print('\n')

varval = '4.1-(3/11)i'
p = 4
print('fpol: ',ar.evaluate(fpol,varval,p))
print('mpol: ',ar.evaluate(mpol,varval,p))
print('ipol: ',ar.evaluate(ipol,varval,p))
'''

############################ modular case ##########################


def strmod(a,m):     # string a integer m
    int_a = int(a)
    b = (int_a) % m
    return str(b)

def integerlist2modlist(L,m):
    modlist = []    
    for k in range(len(L)):
        modm = strmod(L[k],m)
        modlist = modlist + [modm]     
    return remove_leading_zeros(modlist)
   
def poly_mod(expr,m):       
    fpol,flist = main(expr)[0:2]  
    modlist = integerlist2modlist(flist,m)       
    modpol = flist2pol(modlist)
    return modpol, modlist

'''
expr = '(3x-57)^12'
for m in range(2,14):
    pol = poly_mod(expr,m)[0]
    print('mod',m,' ',pol)
print('\n')
'''

########################## complete square ##########################

# ax^2 + bx + c = a(x+(1/2)(b/a))^2 + c - a((1/2)(b/a))^2
# a = quad[0], b = quad[1], c = quad[2]

def complete_square(quad):
    coeffs = main(quad)[1]        
    a = coeffs[0]                        
    #print('a= ',a)                      
    
    b = coeffs[1]
    #print('b= ',b)                       
    
    c = coeffs[2]    
    #print('c= ',c)                       
    
    d = ar.main('(1/2)('+ b +'/' + a + ')')[0]    # (1/2)(b/a)
    #print('d= ',d)                       # -4/3
    
    e = ar.main(a+'('+ d + ')^2')[0]         # a((1/2)(b/a))^2
    #print('e= ',e)                           
    
    f = ar.main(c+ '-' + e)[0]             # c - a((1/2)(b/a))^2
    #print('f= ',f)                                  
    
    g = main('(x' + '+' + d + ')')[0]       # x + (1/2)(b/a)
    #print('g= ',g)
    
    s = tl.fix_signs(a + '('+ g +')^2' + '+' + f)
    
    return s #,a,b,c,d,e,f,g

'''
q = '3x^2 - 8x + 5'
qs = complete_square(q)
print('q   = ',q)    
print('qs  = ',qs)    
print(ar.evaluate(qs,'1.2',0))
print(ar.evaluate(q,'1.2',0))
'''

############################# lagrange interp #############################

def data2lists(data):
    data = data.replace(' ','')      
    data = data.replace('),(',';')      
    data = data.replace(')','')
    data = data.replace('(','')
    tab = tl.string2table(data) 
    return tab     # [['1.7','3.2'], ['2.2','5.4'], ['-2.98','.76']]
    
def lagrange_interp(data):
    sum = '0'
    data = data2lists(data)               # convert data to a table
    #print(data)
    
    for j in range(len(data)):  
        denprod = '1'
        numprod = '1'
         # get products of numerators and denominators in formula 
        for k in range(len(data)): 
            if k != j: 
                num  = '(x' '-(' + data[k][0] + '))' 
                numprod = num + '('+ numprod + ')'
                numprod =  main(numprod)[0]              
                den = '(' + data[j][0] +'-('+ data[k][0] +')' + ')'
                denprod = ar.main(den + '('+ denprod + ')')[0]
        Lj = '(' + numprod + ')/(' + denprod + ')'                       
        Pj = main('(' + data[j][1] + ')(' + Lj + ')')[0] 
        sum = main(sum + '+' + Pj)[0]         
    return main(sum)[0]  

'''
data = '(1,3),(7,8),(4,5)'
data =  '(1.7,3.2),(7.8,5.4),(-42.98,.76)'      
data =  '(1.7,3.2),(2.2,5.4),(-2.98,.76)' 

pol = lagrange_interp(data)
print('Lagrange polynomial:\n', pol)
data = data2lists(data)  
print(data)

for d in data:   
    #print(d)
    x = d[0]
    y = d[1]
    z = ar.evaluate(pol,x,3)[1]
    print(y,z)
'''

############################# poly derivatives ############################


def deriv(P):     
    flist = main(P)[1]           
    L = len(flist)   
    dflist = []      # derivative flist    
    for k in range(L-1):  
        exp = str(L-1-k)
        coeff = flist[k]    
        dcoeff = ar.main(exp + '(' + coeff + ')')[0]        
        dflist = dflist + [dcoeff] 
    return flist2pol(dflist)

'''
P  = '2x^4+(5/9)x^2+7.9x+11/8'   
P = '(3/2)x^12 + 2.004 x^10 - 5ix^8 + 6x^4 + 7x^2 + (11-5i)x + 7.2'
dP = deriv(P)    
print(P)
print(dP)
'''

def tangent_line(P,a):
    #var = tlk.get_var(P)
    Q = deriv(P)
    b = ar.evaluate(P,a,'')[0]   # = P(a)
    m = ar.evaluate(Q,a,'')[0]   # slope  
    m = tl.add_parens(m)
    tan_eqn = b + ' +' + m + '('+ 'x' + '-' + a + ')'   # equation 
    tan_eqn = tl.fix_signs(tan_eqn)   
    return 'y = '+ tan_eqn

'''
P = '(3/2)x^12 + 2.4 x^10 - 5x^8 + 6x^4 + 7x^2 + 11'     
P = 'x^4+5x^3-3x^2 + 7x - 9'
a = '-3/4'    
#a = '-3'
#a = '-3.4'    
print(tangent_line(P,a))
'''

def dderiv(P,n):
    d = P
    for k in range(n):
        d = deriv(d)       
    return d

'''[]
P  = '2x^4+ (5/2)x^22 + 7.6x + 11'
P = '(2.4+3.1i)x^10 - 5ix^8 + 6x^4 + 7x^2 + 11 '
for k in range(12):
    print(dderiv(P,k))
'''

def taylor_series(P,a):    
    var = tl.get_var(P)
    PL = main(P)[1]      
    taylor = ''
            # calculate derivatives up to order degreeP = len(PL)-1:
    for n in range(len(PL)): 
        DP = dderiv(P,n)                             
        c = '('+  ar.evaluate(DP,a,'')[0] +')/('+ str(ma.factorial(n)) +')'                     
        c = ar.main(c)[0]       
        if c == '1': c = ''        
        if c == '-1': c = '-'        
        c = tl.add_parens(c)       
        if n == 1:
           taylor = c + '(' + var + '-' + a + ')' + '+' + taylor        
        elif n == 0:
           taylor = c + taylor        
        else:   
           taylor = c + '(' + var + '-' + a + ')^' + str(n) + '+' + taylor                   
    taylor = taylor[:len(taylor)]      
    return tl.fix_signs(taylor)


'''
P = 'x^4 -x^3 + x^2 + x + 1'
a = '1.1'
#P = '-x^3 + x^2 + x + 1'
#P = 'x^3 -10x^2 + 6'
#a = '3'   

T = taylor_series(P,a)
print(T,'\n')
print(main(T)[0])
'''

############################### poly integral #############################

def indef_int(P):   
    flist = main(P)[1]       
    L = len(flist)   
    #multiplier = flist[0]
    int_flist = []   
    for k in range(0,L):  
        exp = str(L-k)
        coeff = flist[k]    
        int_coeff = ar.main('('+ coeff +')/('+ exp +')')[0]
        int_flist = int_flist + [int_coeff] 
    int_flist = int_flist + ['0']   
    return flist2pol(int_flist)

'''
P  = '12x^3+12x^2+10x+6'  # [12,12,10,6], L = 4, L-k = 4,3,2,1
P = '(3/2)x^12 + 2.4 x^10 - 5ix^8 + 6x^4 + 7x^2 + 11' 
P = '(2.4+3.1i)x^10 - 5ix^8 + 6x^4 + 7x^2 + 13' 
#P = 'x^3 + x^2 + x + 5 '
P = main(P)[0]
print('P:',P,'\n')
I = indef_int(P)
print('indefinite integral of P:')
print(I,'\n')

D = deriv(I)
print('derivative of indefinite integral of P:')
print(D,'\n')

D = deriv(P)
I = indef_int(D)
print('indefinite integral of derivative of P:')
print(I)
'''

def def_integral(P,a,b):   
    I = indef_int(P)
    A = ar.evaluate(I,a,'')[0]
    B = ar.evaluate(I,b,'')[0]
      # apply fundamental theorem of calculus:
    return ar.main(B + '-('+ A +')')[0] 

'''
P = 'x^3 - 7x^2 + 9x-5'
P = 'x^2+ 1.3ix - 7/2'
P = '(3/2)x^12 + 2.4 x^10 - 5ix^8 + 6x^4 + 7x^2 + 11' 
a = '1'
b = '3'
print(def_integral(P,a,b))
'''

def indef_integral_with_condition(P,s,t):   # I(s) = t
    I = indef_int(P)    
    B = ar.evaluate(I,s,'')[0]
    c = t +  '-('+ B +')' # solve for c          
    return main(I + '+' + c)[0]

'''
#P = 'x^2' 
P = 'x^3 - 7x^2 + 9'
#P = 'x^3 - 7x^2 + 9x-5'
#P = '5x^4 - 2x^3 + 3x^2 - 7x + 5.2'
#P = '(3/2)x^12 + 2.4 x^10 - 5ix^8 + 6x^4 + 7x^2 + 11' 
#P = 'x^2 + 3x + 5'
s = '1'; t = '11'
s = '1.2'; t = '3/4'
s = '1'; t = '7'
s = '1.1'; t = '2.7'
I = indef_integral_with_condition(P,s,t)
print(P)
print('I = ',I)
print(t,ar.evaluate(I,s,'')[0])
'''

def indef_integral_with_conditions(P,C):   
    C = tl.string2table(C)         
    I = P
    for item in C: #  apply indef_integral_with_condition successively
        s = item[0]; t = item[1]
        I = indef_integral_with_condition(I,s,t)          
        print('I = ',I)  
    return main(I)[0]   # formatted I

'''
C = '1,2; 3,7; 5,9' # three integrations
#C = '0,1; 0,1; 0,1' # three integrations
P = 'x^2-3x+ 7'

print('P: ', P)
I = indef_integral_with_conditions(P,C)
print('I: ',I)

# check
order = 3
D = dderiv(I,order)   # three differentiations
print('D: ',D)

# check
C = tl.string2table(C)
L = len(C)
D = I
for i in range(L):
    s = C[L-i-1][0] 
    t = C[L-i-1][1]       
    B = ar.evaluate(D,s,'')[0]        
    print(t,'   ',B)
    D = deriv(D)  
'''

############################### special pols ##############################

def ChebyshevPol(n):
    if n == 0: return '1'
    if n == 1: return 'x'
    A = ChebyshevPol(n-1)
    B = ChebyshevPol(n-2)
    pol = '(2x)('+ A + ')-('+ B + ')'
    return main(pol)[4]

#for n in range(11): print(ChebyshevPol(n)); print('\n')

def LegendrePol(n):
    if n == 0: return '1'
    if n == 1: return 'x'
    A = LegendrePol(n-1)
    B = LegendrePol(n-2)
    pol = '(2-1/'+str(n)+ ')x('+ A + ')+(1/'+str(n)+'-1)('+ B + ')'     
    return main(pol)[4]

#for n in range(11): print(LegendrePol(n)); print('\n')

def LagurrePol(n):
    if n == 0: return '1'
    if n == 1: return '1-x'
    A = LagurrePol(n-1)
    B = LagurrePol(n-2)
    pol = '(2-1/'+str(n)+ '-x/'+str(n)+ ')('+ A +')+(1/'+str(n)+'-1)('+ B +')'    
    return  main(pol)[4]

#for n in range(11): print(LagurrePol(n)); print('\n')

def HermitePol(n):
    if n == 0: return '1'
    A = HermitePol(n-1)
    B = deriv(A)
    pol = 'x('+ A + ')-('+ B + ')'
    return main(pol)[4]

#for n in range(11): print(HermitePol(n))







