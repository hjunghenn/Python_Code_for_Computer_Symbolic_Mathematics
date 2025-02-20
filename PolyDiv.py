
### PolyDiv

import PolyAlg as pl
import Arithmetic as ar
import Tools as tl
import Number as nm
import math as ma

# get_var(),fix_signs

######################### division algorithm  ##########################

def div_alg(A,B):               # pol strings   
    var =  tl.get_var(A)
    pl.var = var               # global for PolyAlg   
    AL = pl.main(A)[1]     # polynomial list for A
    BL = pl.main(B)[1]        # polynomial list for B      
    degree_A = len(AL) - 1
    degree_B = len(BL) - 1
   
    if degree_A < degree_B:     # trivial case 
        Q = '0';
        R = A;
        return Q, R
   
    if degree_B == 0 and B != '0':                
        Q = pl.main('('+ A +')/('+ B + ')')[0]       
        R = '0'
        return Q, R
    
    Q = ''   # initialize quotient string     
    while True:                                        
        degree = len(AL) - len(BL)
        q = '('+ AL[0] +')/('+ BL[0] +')'   # q = AL[0]/BL[0]                     
        q = ar.main(q)[0]         
        # attach power to q:
        Q = Q + '+(' + '('+q+')' + var + '^' + str(degree) + ')'                                     
        Q,QL = pl.main(Q)[0:2]                                                                
        CL = pl.pol_scalar_prod(q,BL)               
        # attach 0's to DL to match degree of AL                 
        CL = CL + tl.zero_list(len(AL) - len(BL)) #['0' for k in range(len(AL) - len(BL))]                   
        AL = pl.pol_diff(AL,CL)                                                                     
        if len(AL)< len(BL): break            # done     
    RL = AL    
    R =pl.flist2pol(RL)        # convert to polynomial   
    return Q, R

'''
#A = 'x^5 + 2x + 3'
#B = '2x-1'
A=  '6x^7 + (2/5+3i)x^3 + (5.3/2)x^2 - 3.4x + 2'
B=  '2x^2+x+4/i'
#B = 'x^2+1'
#A = '1'
#A = '17x^5+22x^4-x^2+1'
#B = '34x^3+3'
Q,R = div_alg(A,B)
print(5656,Q,R)
diff = '(' + Q + ')('  + B + ')+' + R + '-(' + A + ')'
diff = pl.main(diff)[0]
print('Q*B + R - A =', diff)
'''

'''
A0 = 'x^3 + 2x + 3'
A1 = '5x^2 + 3ix + 7'
A2 = 'x^4 - 3x^3 - (5/2i)x^2 + 7x + 10'
A3 = 'x^2-3x+2' 
A4 = '3x^9-2x^3+5x^2-7xi+10/i'
A5 = 'x^5-2x^3+7x^2-5x+11'
A6 = '6x^7 + (2/5+3i)x^3 + (5.3/2)x^2 - 3.4x + 2'
A7 = '100x+2x^2'

B0 = 'x+i'
B1 = 'x+1'
B2 = '2x^2 - 4'
B3 = 'x-1'
B4 = '2x^2+x+4/i'
B5 = '2x+3'
B6 = '2x^5+1'
B7 = '5'

Alist = [A0,A1,A2,A3,A4,A5,A6,A7]
Blist = [B0,B1,B2,B3,B4,B5,B6,B7]
  
for i in range(len(Alist)):
    A = Alist[i]
    for j in range(len(Blist)):
        B = Blist[j]
        #print('A'+ str(i) + '= ',A)
        #print('B'+ str(j) + '= ',B)
        Q, R = div_alg(A,B)
        #print('Q =',Q)
        #print('R =',R)
        diff = '(' + Q + ')('  + B + ')+' + R + '-(' + A + ')'
        diff = pl.main(diff)[0]
        print('Q*B + R - A =', diff)
        #print('\n')
'''


################################ gcd ####################################

def poly_gcd(A,B,var):     # assumes degree A > degree B       
    R0 = A; R1 = B 
    S0 = '1'; T0 = '0' # initial values 
    S1 = '0'; T1 = '1' 
    i = 0
    while True:
        if i == 0: Q = ''
        #print(i,'Q =',Q,'  R0 =',R0,'  S0 =',S0,'  T0=',T0)

        G = R0; S = S0; T = T0   # save: to be returned
        
        if R1 == '0': break
        Q,R2 = div_alg(R0,R1)   # R0 = Q*R1 + R2, 
        
        S2  = S0 +  '-('+ Q +')('+ S1 +')'  # S2 = S0 - Q*S1
        T2  = T0 +  '-('+ Q +')('+ T1 +')'  # T2 = T0 - Q*T1
        
        S2 =pl.main(S2)[0]       
        T2 =pl.main(T2)[0]
         
        R0 = R1; R1 = R2       # shift                 
        S0 = S1; S1 = S2       # shift
        T0 = T1; T1 = T2       # shift
        i += 1
    
    Gmonic,Gmoniclist = pl.main(G)[2:4]  # monic version of G
    Gmultiplier = Gmoniclist[0]                     
    # divide by Gmultiplier
    S = pl.main('(1/('+ Gmultiplier + '))' + '(' + S + ')')[0]
    T = pl.main('(1/('+ Gmultiplier + '))' + '(' + T + ')')[0]
    if tl.isarithmetic(G):              # G a constant
        G = '1' 
    else:
        G = pl.main('(1/('+ Gmultiplier + '))' + '(' + G + ')')[0]    
    return G,S,T                    

'''
A0 = 'x^3 + x^2 + 2x - 10i'
B0 = '3x - 7'
A1 = 'x^4 + 5x^3 + 2.7x^2 - 10x + 11'
B1 = '3x^2 - 7/2'
A2 = '18x^3 -42x^2 + 30x -6'
B2 = '-12x^2 + 10x - 2'
A3 = '(3/2+2i)x^4 + 7ix^3 + 2.7x^2 - 10.4x + (11/2)i'
B3 = '3x - 7/2 +4i'
A4 = 'x^4 + 5x^3 + 2.7x^2 - 10x + 11'
B4 = '3x^3 - 7/2'
A5 = 'x^5+2ix^4-x^2+1'
B5 = 'x^3+3'
A6 = '(x^3 + 2x - 10i)(3x-2)'
B6 = '(x - 2i)(3x-1)'
Alist = [A0,A1,A2,A3,A4,A5]
Blist = [B0,B1,B2,B3,B4,B5]

print(poly_gcd(A2,B2,'x'))
'''

'''
for i in range(len(Alist)):
    A = Alist[i] 
    B = Blist[i]  
    #A =pl.polycalc(A,'x')[1]
    #B =pl.polycalc(B,'x')[1]
    G,S,T = poly_gcd(A,B,'x')
    print('i= ',i)
    print('A = ',A)
    print('B = ',B)
    print('G = ',G)
    print('S = ',S)
    print('T = ',T)
    #gcd_eqn = G + ' = ('+ S +')('+  A +')' + ' + (' + T +')('+  B + ')'
    #print('gcd_eqn:')
    #print(gcd_eqn)
    check = G + '- ((' + S  +')('+  A +')'+ ' + ('+ T +')('+  B +'))'   
    check = pl.main(check)[0]  
    print('check',check,'\n')
'''


############################ rational roots #############################

def form_ratios(N,D):
    # input: positive numerator N, denominator D
    # output: reduced ratios divN/divD as strings
    R = []                       # for ratios    
    divN = nm.generate_divisors(N)   # list of divisors of N 
    divD = nm.generate_divisors(D)   # list of divisors of D     
    
    for i in range(len(divN)):
        for j in range(len(divD)):
            g = ma.gcd(divN[i], divD[j])
            rnum = divN[i]/g     # reduces ratio divN[i]/divD[j]
            rden = divD[j]/g        
            r = ar.main(str(rnum) +'/'+ str(rden))[0]
            R.append(r)           # append reduced fraction r
            if r != '0':
                r = tl.fix_signs('-' + r) 
                R.append(r)       # append negative of r as well
    R = list(set(R))              # remove duplicates        
    return R 

'''
N = 2*3**4*5**3
D = 3**6*7**5
N = 2*3**2
D = 5**2
R = form_ratios(N,D)
for r in R: print(r)
'''

def get_roots_and_factors(pol):   
    # output:lists of roots, multiplicity, factors
    var = tl.get_var(pol)    
    ipol,ilist = pl.main(pol)[4:6]    
    L = len(ilist)
    #degree_pol = L-1
    N = ilist[L-1]      # constant term 
    M = ilist[0]        # multiplier
    D = ilist[1]        # leading coefficient
    pol = pl.flist2pol(ilist[1:])
    ratios = form_ratios(abs(int(N)),abs(int(D)))
    roots = []
    factors = []
    multiplicity = []    
    A = pol                 # dividend for division algorithm
    for r in ratios:      
        if A == '0': break
        if ar.evaluate(A,r,'')[0] != '0': # check if root
            continue                     # r not a root
        roots.append(r)                  # got a root
        
        # get factor var-r:
        if r == '0':
            B = var
        else:
            B = tl.fix_signs(var + '-'+ str(r))  
        
        m = 0                            # initialize multiplicity 
        while True:                      # keep dividing out factor        
            Q, R = div_alg(A,B)             
            if R == '0':                 # if B is a factor,           
                m += 1                   # update multiplicity
                A = Q         # old A with factor B divided out
            else: 
                break  
        factors.append(B)                       # linear factor x-r
        multiplicity.append(m)                  # its multiplicity   
    
    # A now has all linear factor divided out        
    A = pl.main( '('+ M +')(' + A +')')[2]     # absorb M into A   
    factors = [A] + factors 
    multiplicity = [1] + multiplicity  # trivial multiplicity for factor A
   
    return roots, multiplicity, factors


'''
pol = '60x^8+(-104)x^7+7x^6+85x^5+(-185)x^4+227x^3+(-136)x^2+38x-4'   
#pol = '(1/6)(2n^3+3n^2+n)'
roots, multiplicity, factors = get_roots_and_factors(pol)
print('roots:        ', roots) 
print('multiplicity: ', multiplicity)
print('factors:      ', factors) 
'''


def factor_polynomial(pol):   
    roots, multiplicity, factors = get_roots_and_factors(pol)        
    if len(factors) == 1: return pol   
    factorization = ''
    for k in range(len(factors)): # run through factors
         f = factors[k]
         if f == '1':                         # trivial factor
             continue         
         if '+' in f or '-' in f:
            f =  '(' + f + ')'
         m = multiplicity[k]                          
         if m == '':                    
             continue
         if m != 1:
             factorization += f + '^' + str(m)
         else:
             factorization += f          
    return factorization
    
'''        
pol1 = 'x(x-1/2)^2(x-2/3)^2(x-3/4)^4(x-4/5)^3(x-5/6)^2(x^2+1)'
pol2 = '60x^8-104x^7+7x^6+85x^5-185x^4+227x^3-136x^2+38x-4'
pol3 = 'x^2(1-x)'
pol4 = '5x+7'
pol5 = 'n^4-n^3+(1/4)n^2'
pol6 = '(1/4)(n^4+2n^3+n^2)'
pol7 = 'x^3-64x^2+1088x-5120'
pol8 = 'x^3-22x^2+152x-320'
pol9 = 'x^3-16x^2+68x-80'

pol_list = [pol2,pol5,pol7,pol8,pol9]

for pol in pol_list:
    roots, multiplicity, factors = get_roots_and_factors(pol)   
    print('polynomial:    ', pol)
    print('roots:         ', roots)
    print('multiplicity:  ', multiplicity)
    print('factors:       ', factors) 
    factorization = factor_polynomial(pol)
    print('factorization: ', factorization)    
    print('check:         ', pl.main(factorization)[0]) 
    print('\n')
'''


############################# div_alg_mod ###############################

def div_alg_mod(A,B,p):               # pol strings   
    var =  tl.get_var(A)   
    AL = pl.poly_mod(A,p)[1]  # reduced polynomial list of A           
    BL = pl.poly_mod(B,p)[1]  # reduced polynomial list of B       
    if BL[0] == '0': return
    
    degree_A = len(AL) - 1
    degree_B = len(BL) - 1

    if degree_A < degree_B:     # trivial case: no Q, R = A  
        Q = '0';
        R = A;
        return Q, R
   
    if degree_B == 0:                
        reciprocal =  str(nm.mod_mult_inv(int(BL[0]),p))               
        if reciprocal == '-1': return 'none','none'
        Q =pl.poly_mod('('+ A +')('+ reciprocal +')',p)[0]           
        R = '0'
        return Q, R   
    Q = ''   # initialize quotient string 
       
    while True:                                 
        degree = len(AL) - len(BL)
        reciprocal = str(nm.mod_mult_inv(int(BL[0]),p))                 
        if reciprocal == '-1': return 'none','none'  
        q = '('+ AL[0] +')('+ reciprocal +')'                         
        q = pl.strmod(ar.main(q)[0],p)          # q = AL[0]/BL[0]                     
            # attach power to q:
        Q = Q + '+(' + '('+q+')' + var + '^' + str(degree) + ')'                      
        Q,QL =pl.poly_mod(Q,p)[0:2]                                          
        CL =pl.pol_scalar_prod(q,BL)                # C = q*B.
            # attach 0's to DL to match degree of AL                 
        CL = CL + ['0' for k in range(len(AL) - len(BL))]                   
        AL =pl.pol_diff(AL,CL)                                                                 
        AL =pl.integerlist2modlist(AL,p)     # reduce       
        if len(AL)< len(BL): break            # done     
    RL = AL   
    R = pl.flist2pol(RL)                  # convert to polynomial    
    return Q, R

'''
A = '17x^5+22x^4-x^2+1'
B = '34x^3+3'
A = 'x^5-2x^3+7x^2-4x+11'
B = '4x^2+3x+4'
print('A = ',A)
print('B = ',B)
print('\n')
Q,R = div_alg_mod(A,B,7)
print(Q,R)
diff = '(' + Q + ')('  + B + ')+' + R + '-(' + A + ')'
diff =pl.poly_mod(diff,7)[0]
print('Q*B+R-A =', diff)         


output_list = []
for p in range(2,12):   
    Q,R = div_alg_mod(A,B,p)
    row = ['mod',str(p),'  Q =',Q,'  R =',R]
    output_list.append(row)

tl.format_print(output_list, 3, 'left')      

print('\n')


for p in range(2,12):
   Q,R = div_alg_mod(A,B,p)
   print('mod',p,'  Q =',Q,'  R =',R)
   
   if Q != 'none' and R != 'none':
       diff = '(' + Q + ')('  + B + ')+' + R + '-(' + A + ')'
       diff =pl.poly_mod(diff,p)[0]
       print('Q*B+R-A =', diff)         
   print('')
'''


############################# poly_gcd_mod ##############################


def poly_gcd_mod(A,B,p):     # assumes degree A > degree B       
    #var =  tlk.get_var(A)
    R0 = A; R1 = B 
    S0 = '1'; T0 = '0' # initial values 
    S1 = '0'; T1 = '1' 
    i = 0
    
    while True:
        G = R0; S = S0; T = T0   # save: returned by function      
        if R1 == '0': break              
        Q,R2 = div_alg_mod(R0,R1,p)   # R0 = Q*R1 + R2,         
      
        if Q == 'none' or R2 == 'none':
            return 'none','none','none'       

        S2  = S0 +  '-('+ Q +')('+ S1 +')'  # S2 = S0 - Q*S1
        T2  = T0 +  '-('+ Q +')('+ T1 +')'  # T2 = T0 - Q*T1
        
        S2 =pl.poly_mod(S2,p)[0]       
        T2 =pl.poly_mod(T2,p)[0]
        
        R0 = R1; R1 = R2       # shift                 
        S0 = S1; S1 = S2       # shift
        T0 = T1; T1 = T2       # shift
        i += 1
    return G,S,T                    


'''
A0 = '11x^3 + x^2 + 2x - 10'
B0 = '3x - 7'
A1 = '14x^4 + 5x^3 + 23x^2 - 10x + 11'
B1 = '3x^2 - 7'
A2 = '18x^3 -42x^2 + 30x -6'
B2 = '-12x^2 + 10x - 2'
A3 = 'x^4 + 58x^3 + 2x^2 - 110x + 11'
B3 = '3x^3 - 13'
A4 = '17x^5+22x^4-x^2+1'
B4 = '34x^3+3'

Alist = [A0,A1,A2,A3,A4]
Blist = [B0,B1,B2,B3,B4]
p= 5

for i in range(len(Alist)):
    print('i=',i)
    A = Alist[i] 
    B = Blist[i]  
    A =pl.poly_mod(A,p)[0]
    B =pl.poly_mod(B,p)[0]
    G,S,T = poly_gcd_mod(A,B,p)
    if G == 'none': 
        print('none')
        continue   
    print('i= ',i)
    print('A = ',A)
    print('B = ',B)
    print('G = ',G)
    print('S = ',S)
    print('T = ',T)
    gcd_eqn = G + ' = ('+ S +')('+  A +')' + ' + (' + T +')('+  B + ')'
    print('gcd_eqn:')
    print(gcd_eqn)
    check = G + '- ((' + S  +')('+  A +')'+ ' + ('+ T +')('+  B +'))'
    check =pl.poly_mod(check,p)[0]  
    print('check',check,'\n')
'''

'''
A =pl.main('(2x^2+3)(4x+7)(x^3+5)')[0] 
B =pl.main('(2x^2+3)(5x+9)(x^2+2)')[0] 
A = '8x^6+14x^5+12x^4+61x^3+70x^2+60x+105'
B = '10x^5+18x^4+35x^3+63x^2+30x+54'

output_list = []
for p in range(2,12):   
    G,S,T = poly_gcd_mod(A,B,p)
    row = ['mod',str(p),'G =',G,'S =',S,'T =',T]
    output_list.append(row)

tl.format_print(output_list, 2, 'left')      

## check
print('\n')  
print('A = ',A); print('B = ',B,'\n')
for p in range(2,8):   
    G,S,T = poly_gcd_mod(A,B,p)
    print('mod',p,'G = ',G,'   S = ',S,'   T = ',T)
    eqn = G + ' = (' + S  +')('+  A +')'+ ' + ('+ T +')('+  B +')'    
    if G != 'none':
        print(eqn)
        check = G + '- ((' + S  +')('+  A +')'+ ' + ('+ T +')('+  B +'))'
        check =pl.poly_mod(check,p)[0]  
        print(check)
    print('')
'''

############################### mod roots ##############################
 
def get_mod_roots(pol,p):
    roots = []
    for r in range(p):       
        if ar.mod_evaluate(pol,str(r),p) == 0:           
            roots.append(r)          # got a root 
    return roots
    
def get_mod_factors(P,p):                                             
    # output: roots, multiplicity, factors lists                      
    var = tl.get_var(P)                                              
    lin_factors = []                                                  
    multiplicity = []                                                 
    A = pl.poly_mod(P,p)[0]                                     
    roots = get_mod_roots(A,p)               # get all roots first
    if roots == []: return P                                          
    for r in roots:                                               
        if r == 0:                                                    
            B = var                                                   
        else:                                                         
            B = tl.fix_signs(var + '-'+ str(r))                      
        m = 0                                # initialize multiplicity
        while True:                       # keep dividing out factor B
            Q, R = div_alg_mod(A,B,p)                                 
            if R == '0':                              # if B a factor,
                 m += 1                      # update its multiplicity
                 A = Q               # old A with factor B divided out
            else: break                                               
        # A now has all linear factors divided out                    
        lin_factors.append(B)                   # append linear factor
        multiplicity.append(m)                  # and its multiplicity
    leftover_factor = A                                               
    return lin_factors, multiplicity, leftover_factor                 

'''
#P = '5x^5 - 2x^2 + 43'
#pol = '(3x-2)(4x-7)(2x-5)^2(x^2+1)'
pol = '(3x-2)(4x-7)(2x-5)^2'
P = pl.main(pol)[0]
P = '48x^6+(-356)x^5+984x^4+(-1361)x^3+1286x^2+(-1005)x+350'
print(P)
lin_factors, multiplicity,leftover_factor = get_mod_factors(P,2)
print(lin_factors, multiplicity,leftover_factor)
'''


def factor_pol_mod(P,p):                                         
    lin_factors, multiplicity, leftover = get_mod_factors(P,p)   
    factorization = ''                                           
    for k in range(len(lin_factors)):                            
         lf = lin_factors[k]                                     
         if '+' in lf or '-' in lf:                              
            lf =  '(' + lf + ')'                                 
         m = multiplicity[k]                                     
         if m == 0: continue                                     
         if m != 1:                                              
             factorization += lf + '^' + str(m)                  
         else:                                                   
             factorization += lf                                 
    
    if not tl.isarithmetic(leftover): 
       leftover = '(' + leftover + ')'
   
    if leftover == '1':                                          
       leftover = ''                   
    
    return leftover + factorization                              

'''
#P = '5x^5 - 2x^2 + 43'
P = '48x^6+(-356)x^5+984x^4+(-1361)x^3+1286x^2+(-1005)x+350'
for p in range(2,13):
    factorization = factor_pol_mod(P,p)
    print('mod',p,'  ',factorization)   
    diff = pl.poly_mod(P + '-('+ factorization +')',p)[0]
    print('check',diff)
    print('\n')    
    #for r in range(p):
    #    print(ar.mod_evaluate(diff,str(r),p))    
    #print('')
'''


