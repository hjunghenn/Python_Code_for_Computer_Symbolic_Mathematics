
### Number.py

import Tools as tl
import math as ma


############################### number bases ############################

def value_to_digits(n, b):
    # returns the digit list in base for the value n
    if n == 0: return [0]
    base_digit_list = []
    while n > 0:                        
        digit = n % b   # digit is remainder  
        base_digit_list = [digit] +  base_digit_list
        n =  n // b            
    base_digit_list = [b] + base_digit_list  
    return base_digit_list


def digits_to_expansion(base_digit_list):
    # converts a base b digit list to a base b expansion      
    expansion = ''
    b = base_digit_list[0]
    digits = base_digit_list[1:]                   # extract base
    L = len(digits)
    for i in range(L):
        exp = str(L-i-1)  
        digit = digits[i]
        if digit == 0: continue          
        if exp == '0':
            expansion = expansion + ' + ' + str(digit)
        elif exp == '1':
            expansion = expansion + ' + ' + str(digit) + '*' + str(b)
        else:
            expansion = expansion + ' + ' + str(digit) + '*' + \
            str(b) + '^' + exp          
    return expansion[3:]   # remove last padded '+'

'''
n = 12345678901234567890
b = 2025
print(n)
digit_list = value_to_digits(n,b)
print(digit_list)
expansion = digits_to_expansion(digit_list)
print(expansion)
'''

def digits_to_value(base_digit_list):    
    #print(222,base_digit_list)    
    expansion = digits_to_expansion(base_digit_list)
    expansion = expansion.replace('^','**') 
    return eval(expansion)

'''    
b = 2025
base_digit_list = [2025,362, 1150, 1666, 1308, 268, 1440]
value = digits_to_value(base_digit_list)
print(value)
'''

def value_to_symbols(n,b):
    # converts value n into a symbol string    
    digit_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                            + 'abcdefghijklmnopqrstuvwxyz'
    
    if b > 62: return                    # not enough digits available
    base_digit_list = value_to_digits(n,b)   # extrct digit part    
    digits = base_digit_list[1:]
    symbolstring = ''
    for digit in digits:      # replace each digit by its symbol
        symbolstring = symbolstring + digit_symbols[digit]
    return symbolstring

'''
n = 12345678901234567890
print(value_to_symbols(n,2))
print(value_to_symbols(n,8))
print(value_to_symbols(n,16))
print(value_to_symbols(n,62))
print(value_to_symbols(n,63))
'''

def symbols_to_value(symbolstring,b):
    # converts a symbol string in base b to its numerical value
    digit_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                            + 'abcdefghijklmnopqrstuvwxyz'
    digit_list = []
    for symbol in symbolstring: 
        index =  digit_symbols.index(symbol)  # position of symbol
        digit_list.append(index)
    return digits_to_value([b]+digit_list)

'''
symbol_string = 'AB54A98CEB1F0AD2'
print(symbols_to_value(symbol_string,16))
print(value_to_symbols(12345678901234567890,16))
'''

def base2base(symbolstring,a,b):   
    n = symbols_to_value(symbolstring,a) 
    return value_to_symbols(n,b)

'''  
a = 39
b = 5
a = 52
b  =62
message = 'THEFILESMUSTBEDELETED'
print(message)
coded_message = base2base(message,a,b)
print(coded_message)
decoded_message = base2base(coded_message,b,a)
print(decoded_message)
'''


############################# generate divisors ###########################

def generate_divisors(a):
    divisors = [1,a]
    for b in range(2,a//2+1):
        if a%b == 0: 
            divisors.append(b)
    divisors = list(set(divisors))   # eliminate duplicates
    return sorted(divisors)          # for clarity

'''
a = 2**8*3**10
a = 3**18
a = 2**5*3**6
divisors = generate_divisors(a)
print(divisors)
'''

def div_alg(a,b):
    return a//b,a%b
 
'''
#test Python gcd:
import math
g1 = math.gcd(63,27)
g2 = math.gcd(-63,27)
g3 = math.gcd(63,-27)
g4 = math.gcd(-63,-27)
print(g1,g2,g3,g4)
'''    

def extended_gcd_pos(a,b):        # assumes a,b > 0      
    r0 = a; r1 = b 
    s0 = 1; t0 = 0 
    s1 = 0; t1 = 1
    q = ' ' 
    #display = []          
    while True:        
        #display.append(['q = '+str(q),'r0 = '+str(r0), 's0 = '+str(s0), 't0 = '+str(t0)])        
        #print(display)
        #print('q =',q,'  r0 =',r0,'  s0 =',s0,'  t0 =',t0)             
        
        if r1 == 0:          
            #tlk.format_print(display, 2, 'left')            
            return [r0, s0, t0]       # gcd and Bezout coefficients
        q,r2 = div_alg(r0,r1)                     # r0 = q*r1 + r2
      
        s2 = s0 - q*s1
        t2 = t0 - q*t1
        r0 = r1; r1 = r2                                    # shift                 
        s0 = s1; s1 = s2                                    # shift
        t0 = t1; t1 = t2                   

def extended_gcd(a,b):        # general integers a, b      
    if a == 0 and b == 0:
        return [0,0,0]        # 0 = 0*0 + + 0*0 
    if a == 0 and b >= 0:     
        return [b,0,1]        # b = 0*0 + + 1*b 
    if a >= 0 and b == 0:
        return [a,1,0]        # a = 1*a + + 0*b      
    if a < 0 and b < 0:
         g,s,t = extended_gcd_pos(-a,-b)     # g = s(-a) + t(-b)
         return [g, -s, -t]                  # g = (-s)a + (-t)b         
    if a < 0 and b >= 0:
         g,s,t = extended_gcd_pos(-a,b)     # g = s(-a) + tb
         return [g, -s, t]                 # g = (-s)a + tb
    if a >= 0 and b < 0:
         g,s,t = extended_gcd_pos(a,-b)     # g = sa + t(-b)        
         return [g, s, -t]                 # g = sa + (-t)b
    if a >= 0 and b >= 0:
        g,s,t = extended_gcd_pos(a,b)     # g = sa + tb   
    return [g, s, t]                     

def print_Bezout(inputlist,g,coefflist):
    Bezout = ''
    for i in range(len(inputlist)):       
        coeff = tl.add_parens(str(coefflist[i]))
        integer = tl.add_parens(str(inputlist[i]))
        Bezout = Bezout + '('+ coeff +')*(' + integer + ')+'
    Bezout = Bezout[0:len(Bezout)-1]       # remove last '+'
    #Bezout = tlk.fix_signs(Bezout)
    print(str(g) + ' = ' + Bezout)

'''
a = 12356
b = -68
g,s,t = extended_gcd(a,b)
inputlist = [a,b] 
coefflist = [s,t]
print_Bezout(inputlist,g,coefflist)
'''

def multi_extended_gcd(inputlist):
    global coefflist     
    n = len(inputlist)
    coefflist = ['' for x in range(n)] 
    coefflist[0] = 1                      # initialize active part of list
    get_coeffs(inputlist)                   # implements the recursion     
    g = 0
    for i in range(len(inputlist)):      # get the gcd from coefficients
        g = g +  coefflist[i]*inputlist[i]     
    return g,coefflist

def get_coeffs(inputlist): 
    global coefflist    
    n = len(inputlist)                 # current length of variable list
    a = inputlist[0]; b = inputlist[1]     # first 2 entries of current list  
    G = extended_gcd(a,b)         # latest gcd with coefficients   
    x = G[1]; y = G[2]                    # coefficients of a, b    
    i = 0
    while coefflist[i] != '':        # update coefficients        
        coefflist[i] = x*coefflist[i]
        i = i+1
    coefflist[i] = y                      # attach new coeff at end     
    if n == 2: return coefflist            # finished       
    inputlist = inputlist[1:]           # otherwise replace 1st entry
    inputlist[0] = G[0]                # with latest gcd
    get_coeffs(inputlist)      # and do the process again
   
'''
ilist1 = '1666,21,10,118'  # 3
ilist2 = '1665,21,10,118'  # 3
ilist3 = '1665,21,10,117'  # 3
ilist4 = '21111,21,10,117' # 3
ilist5 = [6,8,10,3]        # 3 
ilist6 = ['6,8,10,7']        # 3 
ilist7 = '12,8,10,7'         # 4 
ilist8 = [24,16,20,14]        # 4 
ilist9 = [24,-16,20,14,-21]      # 5
ilist  = ilist9
g,coefflist = multi_extended_gcd(ilist)
print(g,coefflist,ilist)
print_Bezout(ilist,g,coefflist)
'''


def lcm(m,n):
    g  = ma.gcd(m,n)
    return m*n//g

def listlcm(inputlist):                # integers
    #ilist = ilist.split(',')
    m = inputlist[0]                 # initialize
    for k in range(1,len(inputlist)):     
        m = lcm(m,inputlist[k])
    return m

#inputlist = [2,3,6,9]
#print(listlcm(inputlist))

################################# sieve #################################
          
def sieve(N):
       marks = [1 for i in range(N+1)] 
       k = 2
       while (k * k <= N): 
           if marks[k] == 1:  # at this stage, k is prime
               for i in range(k * k, N+1, k): 
                   marks[i] = 0    
           k += 1                
       primes = []
       for i in range(2,len(marks)):
           if marks[i] == 1: 
              primes.append(i)
       return primes

# print(sieve(500))
   
############################# prime factorization #######################

def prime_factorization(N):
    prime_list = sieve(N//2+1)    # get primes less than N/2 + 1
    exponents = [] 
    primes = []
    for i in range(len(prime_list)):       # run through the primes
        p = prime_list[i]
        e = 0                  # initialize exponent for this prime
        while N % p == 0:                      # if prime divides N
            N = N/p                          # keep dividing it out
            e = e+1                           # and update exponent 
        if e != 0:                                 # if p divided N 
            primes.append(p)                           # include it 
            exponents.append(e)                  # and its exponent          
    return primes, exponents     

def print_factorization(primes,exponents):
         P = ''                       # string for prime factorization
         for i in range(len(primes)):            
             p = primes[i]
             e = exponents[i]
             if e > 1:
                 P = P + '('+ str(p) +'^'+ str(e) + ')*'
             else:
                 P = P + str(p) + '*'
         print(P[:len(P)-1])      

'''
N = 300042
primes,exponents = prime_factorization(N)
print(primes,exponents)
print_factorization(primes,exponents)
'''


################################## mod ##################################

def addition_modtable(m):
    table = []
    header = []
    for k in range(m):
        header = header+[str(k)]
    header = ['+'] + header
    table = [header]

    for i in range(m):
        row = [] 
        for j in range(m):
            row = row + [str((i+j)%m)]
        row = [str(i)] + row
        table = table + [row]
    return table
    
   
def multiplication_modtable(m):
    table = []
    header = []
    for k in range(m):
        header = header+[str(k)]
    header = ['*'] + header
    table = [header]

    for i in range(m):
        row = [] 
        for j in range(m):
            row = row + [str((i*j)%m)]
        row = [str(i)] + row
        table = table + [row]
    return table    
   
'''   
table = addition_modtable(5)
print('mod 5')
tl.format_print(table, 3, 'left'); print('\n')               
table =multiplication_modtable(5)
tl.format_print(table, 3, 'left')

print('\n') 
table = addition_modtable(4)
print('mod 4')
tl.format_print(table, 3, 'left')
print('\n')               
table =multiplication_modtable(4)
tl.format_print(table, 3, 'left')
'''

def mod_add_inv(a,m):
    a = a%m
    for b in range(0,m):
        if (a+b)%m  == 0: break                    
    return b
    
def mod_mult_inv(a,m):
    for b in range(1,m):       
        x = a*b                   
        if (x%m)  == 1:         
            return b 
    return -1        # no inverse   

#print(mod_add_inv(40,7))         
#print(mod_mult_inv(678,7))    

'''
m = 6
a = 40    
b = mod_add_inv(a,m)
print('additive inverse of',a,'mod',m,'=',b)
print('check:', (a+b)%m)

a = 678
c = mod_mult_inv(a,m)
if c != -1: 
    print('multiplicative inverse of',a,'mod',m,'=',c)
else: print('no inverse')     
print('check:', (a*c)%m)
'''


################################## not used ###############################

def greater_int(a, b):                                
    La = len(a); Lb = len(b)                                         
    if La > Lb: return a                                                    
    if La < Lb: return b                                                                                                                                
    for i in range(La):         # compare digits from left to right   
        if int(a[i]) < int(b[i]):                                     
            return b                                                
    return a                    

def is_less_pos(a, b):                                             
    La = len(a); Lb = len(b)                                       
    if La > Lb: return False                                       
    if La < Lb: return True                                        
    for i in range(La):        # compare digits from left to right 
        if int(a[i]) < int(b[i]):                                  
            return True               # found a smaller digit in a 
    return False                                                   
                                                                   
def is_less(a, b):                                                 
    if a[0] == '-' and b[0] != '-': return True                    
    if a[0] != '-' and b[0] == '-': return False                   
    if a[0] != '-' and b[0] != '-':                                
        return is_less_pos(a, b)                                   
    if a[0] == '-' and b[0] == '-':                                
       c = a[1:]; d = b[1:]                                        
       return is_less_pos(d,c)                                     

'''
a = '12345678987654321'
b = '12345678987654322'
a = '0'
print(is_less(a, b))
'''


