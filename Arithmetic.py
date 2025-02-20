
### Arithmetic.py


import Tools as tl
import math as ma
###########################################################################

#e = '2*3^2' 
#e = '(2*i^7+3.1/2.2)^(3)'
#e = '1.2i*4.3+ (2.1*(3.1/4.2 - 5.3i)^11)/(6.4i + 7)^(-3)'
#e = '(1.2*4.3 + 2.1*(3.1/4.2 - 5.3i)^(10)/(6.4i + 7)^(-3))^3' 
#e = '3/4 - 5.3i^2/(6.4i + 7)^(-3)'
#e = '1/2-5.3i'
#e = '(1.7+3.3)^(-7)*1/5^(-10)'  # book
#e = '1/2 - 2/3'
#e = '3.1^2'
#e = '(4(2+3i) - 3(1/i+2) + 5)^2'
#e = '3+2.5i'
#e =  '5*57^4+32*57^3+56*57^2+13*57^1+14*57^0'
#e = '-2-3-4'
#e =  '(4.2-(7/2)i + 3.2i)'
#e =  '-(7/2)i + 3.2i'
#e = '2i-3i'
#e = '3-2'
#e =  '(((4.2-(7/2)^(-1))i + 3.2i)^10'
#e =  '(4.2-7/2)^(-1)'
#e =  '2^(-1)'
#e = '2i^3'      # -8i 
#e = '(3 - 0i)(2+0i)'
#e = '-5+3i+12-3i'
#e = '3-3i'
#e = '1.2*4.3 + 2.1*(3.1/4.2 - 5.3i)^(10)/(6.4i + 7)^(-3)' 
#e = '(-9)/((3)-1) + (-7)/((3)-1)^2 + (9)/((3)-2)'
#e = '(-9)/((3)-1)'      # -9/2
#e = '(-7)/((3)-1)^2'    # -7/4
#e = '(9)/((3)-2)'       # 9
#e = '(-9)/((3)-1) + (-7)/((3)-1)^2' 
#e = '(-9)/((3)-1) + (-7)/((3)-1)^2 + (9)/((3)-2)'
#e = '(-9)/((3)-1) + (-7)/((3)-1)^2'# + (9)/((3)-2)'
#e = '(2(3)+5)/((3)-1)^2((3)-2)' 
#e = '1/4 - 3/4 + 1/2'
#e = '1 - 2 + 3 -4 -5 + 7'
#e = '- 2 + 3 -4 -5 + 7'
#e = '(-9/2 -7/2)'# + 9'
#e =  '(3.2/3)+4(1+(2.5/3i))-1.7i'
#e = '- (.4i)^6 - 6(.4i)^5 - 9(.4i)^4 - (.4i)^3 + (9 + 11i)(.4i)^2 + (-23/5)(.4i) + 1 + (1093/25)i'
#e = '(1/25)(-25(.4i)^6 - 150(.4i)^5 - 225(.4i)^4 - 25(.4i)^3 + (225 + 275i)(.4i)^2 - 115(.4i) + 25 + 193i)'
#e = '(3(2)+5)/(5(2)-7)(2(2)+1)-((-460/19)/(5(2)-7)+(70/19)/(2(2)+1))'


##### good with current setting
#e = '1 - 2 + 3 -4 + 5 - 6'    # -3
#e = '-1 + 2 - 3 + 4 -5 + 6'   # 3
#e = '3/2^(-1)' # 6
#e = '3/4*2'    # 3/8  
#e = '3*4/2'    # 6
#e = '2/3^4'   # 2/81
#e = '2^3/4'   # 2
#e = '1-2-3'   # -4
#e = '2*3-4'   # 2
#e = '2-3*4'   # -10
#e = '3^(-1)/2' # 1/6
#e = '2-3/4'   # 5/4 
#e = '1/2 -1/8' # 3/8 
#e = '2^3*(4/5)' # 32/5
#e = '(1/2.897)^(-1)'
#e = '3*4*5'
#e = '3*(4/5)'
#e = '(3*4)/5'
#c =  '130/3'
#e = '(' + c + ')'
#e = '1/(' + c + ')'
#e = '(' + c + ')' + e 

############################ conversions #############################


def decimal2frac(numeric):   
    if '.' not in numeric:  
        return numeric
    whole, decimal = numeric.split('.')       # 12.34 --> 12, 34
    zeros = '0'*(int(len(decimal)))           # '00'
    denominator = '1' + zeros                 # 100 
    numerator = whole + decimal
    return numerator + '/' + denominator      # 1234/100    

def frac2intpair(r):                          # r = 'm/n' 
    if '/' not in r: r = r + '/1'             # for uniformity
    m,n  = r.split('/')
    return int(m),int(n)           # integer numerator and denominator

def reduce_int_pair(a,b):   
    c =  ma.gcd(a,b)           # largest common factor of a and b
    return a//c, b//c         # integer division

def pair2frac(num,den):   
    if  num == 0: return '0'
    if den < 0: num = -num; den = -den   # put minus sign on top
    if  num == den: return '1'
    if  num == -den: return '-1'
    if  den == 1: return str(num)        # no denominator needed   
    num,den = reduce_int_pair(num,den)   # cancel largest common factor
    return str(num) + '/' + str(den)     # combine parts

# num,den = 40,-555
# print(pair2frac(num,den))

def numeric2list(r):                       
    if r == 'i': return ['0','1']
    if r == '-i': return ['0','-1']
    if 'i' not in r: 
        return [decimal2frac(r),'0']    # purely real
    r = r.replace('i','')    
    return ['0', decimal2frac(r)]       # purely complex          

# print(numeric2list('2.3'), numeric2list('.56i'))

def pair2complex(c):            # c = [a, b], a, b string fractions
    real = c[0]; imag = c[1]
    if '/' in real:
        num,den = real.split('/')
        real = pair2frac(int(num),int(den))      # format real part   
    if '/' in imag:
        num,den = imag.split('/')
        imag = pair2frac(int(num),int(den))      # format imag part
        imag = '(' + imag + ')'    
    if real != '0':
        imag = imag.replace('(-','-(')     # pull '-' outside paren
    
    #### special cases: 
    if real == '0' and imag == '0': return '0'     
    if real == '0' and imag == '1': return 'i'     
    if real == '0' and imag == '-1': return '-i'   
    if imag == '0': return real    
    if real == '0': return imag  + 'i'
             
    if imag == '1':  imag = ''              # coefficient 1 not needed
    if imag == '-1': imag = '-'
    
    #### general case:
    c  = real + '+' + imag + 'i'
    c = tl.fix_signs(c)   
    return c #tl.remove_extra_parens(c)   

# c = ['12/34','-1/5']; print(pair2complex(c))


#################### operations on real fractions ####################

def frac_sum(r,s):  # r=m/n, s=p/q, r + s = m/n + p/q = (mq+np)/nq
    m,n  = frac2intpair(r)      # convert fraction to integer pair
    p,q  = frac2intpair(s)                                        
    return pair2frac(m*q + n*p, n*q)     # return reduced fraction
                                                                  
def frac_diff(r,s):                                               
    t = '-'+s                                    # make s negative
    t = tl.fix_signs(t)              # remove extraneous '+', '-'
    return frac_sum(r,t)                                          
                                                                  
def frac_prod(r,s):                    # r*s = m/n * p/q = m*p/n*q
    m,n  = frac2intpair(r)                                        
    p,q  = frac2intpair(s)                                        
    return pair2frac(m*p,n*q)                                     
                                                                  
def frac_recip(s):                                       # s = p/q
    p,q = frac2intpair(s)                                         
    return pair2frac(q,p)                                    # q/p
                                                                  
def frac_quo(r,s):                                                
    t =  frac_recip(s)                                   # t = q/p
    return frac_prod(r,t)                            # (m/n)*(q/p)
                                                                  
def frac_power(s,exp):                                 # (p/q)^exp
    if exp == 0: return '1'                                         
    t = s;                                               # default
    if exp < 0:                                                   
       exp = -exp                         # make exponent positive
       t = frac_recip(t)                                # invert t
    num,den = frac2intpair(t)      
    num,den = num**exp, den**exp    # raise both to positive power
    return pair2frac(num,den)                        # reduced m/n

'''
r = '2/3'; s = '-5/7'; exp = -4
print('r+s   = ', frac_sum(r,s))
print('r-s   = ', frac_diff(r,s))
print('r*s   = ', frac_prod(r,s))
print('r/s   = ', frac_quo(r,s))
print('r^exp = ', frac_power(r,exp))
'''


##################### operations on complex numbers #######################

def complex_sum(u,v):      # u = [a,b], v = [c,d], a,b,c,d fractions
    a,b = u[0],u[1]            # a = m/n, b = p/q, m,n,p,q integers
    c,d = v[0],v[1]
    real = frac_sum(a,c)                   # add real parts: a+c
    imag = frac_sum(b,d)                   # add imag parts: b+d
    return [real,imag]                         # return string list

def complex_diff(u,v):                        #u = [a,b], v = [c,d]
    a,b = u[0],u[1]
    c,d = v[0],v[1]
    real = frac_diff(a,c)                                  # a-c
    imag = frac_diff(b,d)                                  # b-d
    return [real,imag] 

def complex_prod(u,v):                        #u = [a,b], v = [c,d]
    a,b = u[0],u[1]
    c,d = v[0],v[1]
    ac = frac_prod(a,c)
    bd = frac_prod(b,d)
    ad = frac_prod(a,d)
    bc = frac_prod(b,c)
    real = frac_diff(ac,bd)                   # ac - bd, ad + bc
    imag = frac_sum(ad,bc) 
    return [real,imag]

def complex_recip(u):                            # u = [a,b] = a+bi
    a,b = u[0],u[1]
    if a == 0: return ['0','-'+frac_recip(b)]          # ['0',-1/b]
    if b == 0: return [frac_recip(a),'0']               # [1/a,'0']
    a2 = frac_power(a,2)              
    b2 = frac_power(b,2)
    a2_plus_b2 = frac_sum(a2,b2)     
    real = frac_quo(a,a2_plus_b2)              # a/(a^2 + b^2)
    imag = frac_quo(b,a2_plus_b2)     
    imag = frac_diff('0',imag)                  # -b/(a^2 + b^2)
    return [real,imag]            # a/(a^2 + b^2) - i a/(a^2 + b^2)

def complex_quo(u,v):   
    w = complex_recip(v)  
    return complex_prod(u,w)                              # u*(1/v)

def complex_power(u,exp):                                   # u^exp
    if exp == 0: return ['1','0']
    if  exp < 0: 
        exp = -exp
        u = complex_recip(u)   
    v = u      
    for k in range(exp-1):    # multiply u times itself exp-1 times
        v = complex_prod(u,v)   
    return v

'''
u = ['2/3','4/5']
v = ['2','-7']
print('sum   = ',complex_sum(u,v))
print('diff  = ',complex_diff(u,v))
print('prod  = ',complex_prod(u,v))
print('recip = ',complex_recip(v))
print('quo   = ',complex_quo(u,v))
print('power = ',complex_power(u,3))
print('power = ',complex_power(u,-3))
'''

'''
def conj(z):   # not needede
    r = complex2list
    return [r[0], '-(' + r[1] + ')']
'''


################################# allocate ################################

def allocate_ops(expr,mode):              # returns pair of fractions
    global idx
    while idx < len(expr):
        ch = expr[idx]              # character at index idx       

        if ch in '.0123456789i':          # beginning of a numeric     
            start = idx
            r,idx = tl.extract_numeric(expr, start)
            r = numeric2list(r)
         
        elif ch == '+':
            if mode > 0: break              # wait for higher mode
            idx += 1
            s =  allocate_ops(expr,0)
            r = complex_sum(r,s)

        elif ch == '-':
            if mode > 0: break              # wait for higher mode
            idx += 1
            s =  allocate_ops(expr,1)            
            r = complex_diff(r,s)            
   
        elif ch == '*':
            if mode > 1: break  
            idx += 1
            s =  allocate_ops(expr,1)
            r = complex_prod(r,s)
        
        elif ch == '^':                  
            idx += 1
            exp =  allocate_ops(expr,2)[0]  # get exponent
            r = complex_power(r, int(exp))

        elif ch == '/':
            if mode > 1: break 
            idx += 1
            s = allocate_ops(expr,1) # get denominator
            r = complex_quo(r,s)

        elif ch == '(':
            idx = idx + 1                     # skip '('
            r =  allocate_ops(expr,0)              # calculate stuff inside ()
            idx = idx + 1                     # skip")"
        elif ch == ')': break
    return r

################################# arithcalc ###############################

def main(expr): 
    # input: complex arithmetic expression
    # output: formatted complex number z and list c = [real,imag]
    global idx   
    expr = expr.replace(' ','')   # remove extra spaces        
    expr = tl.fix_signs(expr)                                     
    expr = tl.fix_operands(expr)                                  
    expr = tl.insert_asterisks(expr,'')    # no variables               
    idx = 0                       # start        
    c = allocate_ops(expr,0)      # does the calculations, returns list
    z = pair2complex(c)    # convert list c into final expression   
    return z,c        

'''
e = '(2/7)^10*(1/5^8)'
print(main(e)[0])
'''

'''
e = '(2/7)**10*(1/5**8)'
print('3/4*2', main('3/4*2')[0])  
print('3*4/2', main('3*4/2')[0]) 
print('2/3^4', main('2/3^4')[0])
print('2^3/4', main('2^3/4')[0])
print('2*3-4', main('2*3-4')[0]) 
print('2-3*4', main('2-3*4')[0])
#print(eval(expr))
#fact = '(1/'+ str(ma.factorial(5)*ma.factorial(3)) + ')'
#print(arithcalc(fact)[0])
'''


################################# category ##############################

def is_complex(z):          # True if both real and imag parts not zero
    if z == '': return False
    #return 'i' in z and ('-' in z or '+' in z)    
    z = main(z)[1]  
    return z[0] != '0' and z[1] != '0'

def is_frac(z):           # True if expr is a fraction 
    if z == '': return False    
    return '/' in z          

def real(z):
    return main(z)[1][0]  

def imag(z):
    return main(z)[1][1]  


########################### decimal approximations ########################


def scientific_notation(decimal):
    if '.' not in decimal:
        D = len(decimal)
        if D == 1:                                    # 3 --> 3
            return decimal
        if D == 2:
            return tl.insert_string(decimal,'.',1)[0] + '*' + '10'   # 33 --> 3.3 * 10
        if D > 2:                                  # 333 --> 3.33 * 10^2
           return tl.insert_string(decimal,'.',1)[0] + '*' + '10^'  + str(D - 1) 
        
    left,right = decimal.split('.')
   
    if left != '' and main(left)[0] == '0': 
        left = ''
       
    if left == '':
        R = len(right)
        right = right.replace('.','')
        if R == 1:                                  #.3 --> 3*10^(-1) 
            return right + ' *10^(-1)'
        if R > 1:                                   #.33 --> 3.3*10^(-1)                           
            return tl.insert_string(right,'.',1)[0] + '*' + '10^(-1)' 
     
    L = len(left) 
    if L == 1:                                      #3.3 --> 3.3
        return decimal
    decimal = decimal.replace('.','')       
    if L == 2:                                      #3.3 --> 3.3       
        return tl.insert_string(decimal,'.',1)[0] + '*' + '10'
    exp = str(L-1)
    return tl.insert_string(decimal,'.',1)[0] + '*' + '10^' + str(exp) 
   
'''
dlist = ['1','12','123','.1','.12','.123','1.2', '12.3','123.4']
ddlist = []
for d in dlist:    # make a list of pairs [d,sci] for format print
    sci = scientific_notation(d)
    ddlist.append([d,'=',sci])        
tl.format_print(ddlist, 2, 'left')
'''


def frac_decimal_approx(fraction,p):                  # fraction = a/b
    # input: ratio of integers    
    # output: approximatoin to p places 
    if '/' not in fraction or p == '': 
        return fraction 
    a,b = frac2intpair(fraction)
    if a == b: return '1'                      # trivial case
    c = a*10**p                  
    q,r = c//b, c%b                          # div alg for c,b     
    q = str(q); r = str(r)        
    L = len(q)
           # place the decimal point p places to left in q
    if p < L:                 
        approx = q[:L-p]+ '.' + q[L-p:] 
    if p == L: 
        approx =  '.' + q 
    if p > L:
        #zeros = ['0' for i in range(p-L)]
        #zeros = ''.join(zeros)
        zerostring = (p-L)*'0'
        approx = '.' + zerostring + q
    L = len(approx)
    for i in range(L-1,-1,-1):              # remove trailing zeros
        if approx[i] != '0': 
            break                      # i at first nonzero in trail
    
    approx = approx[:i+1]                      # chop off zero trail
    if approx[len(approx)-1] == '.':             # last symbol '.'?
        approx = approx.replace('.','')                 # remove it
    return approx


def decimal_approx(z,p):    
    # input: z = complex number, p = number of decmal places 
    # output: decimal complex number z and corresponding list d    
    c = main(z)[1]         # get real and imaginary parts of z        
    real = frac_decimal_approx(c[0],p)                  # approximate real
    imag = frac_decimal_approx(c[1],p)               # and imaginary parts       
    d = [real,imag]
    w = pair2complex(d)                             # format number       
    return w,d   # number, list form


#fraction = '45/67'   
#print(decimal_approx(fraction,21)[0])
#print(frac_decimal_approx(fraction,4))
#print(frac_decimal_approx(fraction,50))

#e = '76/7-(151/29)i'   
#e = '2/3'
#e = '1/3'
#e = '151/29'
#e =  '(3.2/5i)+ 4(7.1i + 2.5/3)^3-1.7'
#e = '(1.7+3.3)^(-7)*1/5^(-10)'
#e = '7+i'
#e = '2^2/3^2'

'''
e = main(e)[0]
print(e)
print(decimal_approx(e,4))
print(decimal_approx(e,50))
#e = e.replace('^','**')
#print(eval(e))
'''


######################## expression evaluation #####################

def evaluate(expr,varval,p):       
    var = tl.get_var(expr)
    if var == '':         
        return main(expr)[0],''              
    e = expr.replace(var,'(' + varval + ')')   
    e = tl.fix_signs(e)            
    e = main(e)[0]        
    if p == '': return e,''
    return e, decimal_approx(e,p)[0]

'''
expr = '(2x^2 + x + 4)^2/(1+(1/2i)x^2 - (7/3)x - 11/8)/(x^2+1)'
var_val = '1.1'
expr_val, dec_approx = evaluate(expr,var_val,9)
print('expression value:   ', expr_val) 
print('decimal approx:     ', dec_approx)
'''

def mod_evaluate(expr,varval,m):
    var = tl.get_var(expr)
    exprval = expr.replace(var,'(' + varval + ')')
    exprval = tl.fix_signs(exprval)   
    return int(main(exprval)[0])%m

'''
expr = '(3x-57)^177'
#expr = 'x^47'
#expr = 'x'
var_val = '2'
for m in range(2,14):
    expr_val = mod_evaluate(expr,var_val,m)
    print('mod',m,' ',expr_val)
'''

############################# ordering fractions ##########################


def min_max_frac(frac1,frac2): 
    fr1 = frac1; fr2 = frac2
    if '/' not in fr1: fr1 = fr1 + '/1'   # for uniformity
    if '/' not in fr2: fr2 = fr2 + '/1'
    a1,b1 = fr1.split('/')                    # a1/b1, b1>0
    a2,b2 = fr2.split('/')                    # a2/b2, b2>0   
    a1 = int(a1); b1 = int(b1)
    a2 = int(a2); b2 = int(b2)
    if  a1*b2 < a2*b1:
        return frac1,frac2 
    return frac2,frac1 

def is_less(frac1,frac2): 
    minfrac,maxfrac = min_max_frac(frac1,frac2)
    return minfrac == frac1     

'''
frac1 = '-3/4'
frac2 = '-5/6'
print(min_max_frac(frac1,frac2))
print(is_less(frac1,frac2))
'''

def frac_sort(frac_list):   # min to max
    L = len(frac_list)
    for i in range(L):    
        for j in range(i+1,L):                
            if is_less(frac_list[j],frac_list[i]): 
               swap = frac_list[i]      # put f(i) before f(j)
               frac_list[i] = frac_list[j] 
               frac_list[j] = swap 
    return frac_list

def index_of_min(frac_list):
    sorted_list = frac_sort(frac_list)
    return frac_list.index(sorted_list[0])

def index_of_max(frac_list):
    L = len(frac_list)
    sorted_list = frac_sort(frac_list)
    return frac_list.index(sorted_list[L-1])

'''
frac_string = '43/46,-81/83,-64/67,-33/34,671/678,52/55,11/12,7/77'
frac_list = frac_string.split(',') 
print(frac_sort(frac_list))
idx_min = index_of_min(frac_list)
idx_max = index_of_max(frac_list)
print(frac_list[idx_min], frac_list[idx_max]) 
'''

def is_positive(frac): 
    return is_less('0',frac)

def is_negative(frac): 
    return is_less(frac,'0')

def absval(a):   
        b = main(a)[0] # convert possible decimal into fraction
        if is_less(b,'0'):   
            return tl.fix_signs('-'+ a) 
        else:
            return a

#b = absval('.000345') 
#print(b)


########################### interval halving #########################


def interval_halving(f, a, b, accuracy):    # enter all as strings                                          
    accuracy =  main(accuracy)[0]   # convert to fraction form                                                                                            
    while True:                                                   
            # midpoint of current interval:                       
        c = main('('+ a + '+' + b + ')/2')[0]           
        cval = evaluate(f,c,'')[0]     # expression values                                   
        aval = evaluate(f,a,'')[0]   
        bval = evaluate(f,b,'')[0]                              
        prod = main('('+ aval +')('+ bval + ')')[0]       
        if is_less('0',prod):                                  
            return  'none'          # no zero in interval [a,b]      
        if aval == '0': return a    # special cases
        if bval == '0': return b                                  
        if cval == '0': return c                                
                                                                  
        prod = main('('+ aval +')('+ cval + ')')[0]       
        if is_less(prod,'0'):    # a zero between a and c    
            b = c              # new interval is left half            
                                                                  
        prod = main('('+ cval +')('+ bval + ')')[0]       
        if is_less(prod,'0'):    # a zero between c and b    
            a = c              # new interval is right half         
        z = c                          # approximate zero       
                                                                  
        interval_length = main(b + '-('+ a +')')[0]       
        if is_less(interval_length,accuracy):                  
           break                                                  
    return z              

'''
f = '(2.4-x^2)(x^2+x+1)^2' #'(.3-2x^2)(x+1)'
a = '.5'
b = '2'
p = 50

print(f)
for i in range(10):
    zeros = '0'*i
    accuracy = '.'+ zeros + '1'   
    approx_root = interval_halving(f, a, b, accuracy)
    if approx_root == 'none':
        print('no root')
        break
    dec_approx = frac_decimal_approx(approx_root,p)
    print('accuracy:            ', accuracy)
    print('approximate root:     ', approx_root)
    print('decimal approximation:', dec_approx,'\n')
''' 


####################### linear fractional cipher #######################

def encryption(message,a,b,c,d):                # string message
    coded_message = ''                          # initialize
    for i in range(len(message)): 
        x = str(ord(message[i]) - 65)               # alpha value
        y = '(' + a + '*' + x + '+' + b +')/' \
            '(' + c + '*' + x + '+' + d + ')'   # formula for y
        y = main(y)[0]                           # value of y
        u,v = y.split('/')                      # get num,den
        if v == '': v = '1'
        coded_message =  coded_message + u + ' ' + v + ' '
    L = len(coded_message)-1
    return coded_message[:L] # remove last space


def decryption(coded_message,a,b,c,d): 
    coded_message = coded_message.split(' ')  # split out the base 26 numbers 
    i = 0
    message = ''                              # initialize
    while i < len(coded_message)-1: 
        u = coded_message[i]                  # first member of pair
        v = coded_message[i+1]                # second member of pair
        y = '(' + '('+ u + ')/(' + v + ')' + ')'  # form fraction u/v
        x = '(' + b + '-' + d + '*' + y +')/'  \
            '(' + c + '*' + y + '-' + a + ')' # formula for x
        x = main(x)[0]                   # value of x (alpha number)
        letter = chr(int(x) + 65)             # convert to letter
        message = message + letter            # attach to message
        i += 2                                # next pair 
    return message

''' 
a = '15.23'
b = '42.72'
c = '63.91'
d = '27.45'
message = 'RUNFORYOURLIVES'
print(message)
coded_message = encryption(message,a,b,c,d)
print(coded_message)
message = decryption(coded_message,a,b,c,d) 
print(message)
'''