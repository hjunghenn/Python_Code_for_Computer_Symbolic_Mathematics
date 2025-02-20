
                    ###### Essentials.py ######

print(int(3.9999),int(-3.9999))

###################################################################

help('keywords')

###################################################################
 
v1 = 37; v2 = 3.7; v3 = 'thirtyseven'; v4 = 3 < 7 
print(type(37), type(3.7), type('thirtyseven'), type(3 < 7)) 
print(type(v1), type(v2), type(v3), type(v4))
print('\n')

###################################################################
 
print(int(-3.7),float(37),float(3.7e-4),float(3.7e4),str(3.7))
print('\n')

###################################################################

print(5-6*3/2,5-6/3*2,5-6/2**3,5-6**2/3,6+7/8-(6+7)/8)
print('\n')

###################################################################

v1 = 2.3; v2 = 3.2       # assign values to variables v1 and v2
v = v1*v2 + v1/v2 - v1**v2          # assign an expression to v
print(v)
print('\n')

###################################################################

print(9//2, -9//2, 9//-2, -(9//2))
print('\n')

###################################################################

def modulo_test(a,b):                           # enter integers a, b      
       return a % b, b*(a/b - a//b)    

print(modulo_test(3,5))
print(modulo_test(-3,5))
print(modulo_test(3,-5))
print(modulo_test(-3,-5))
print('\n')

def xmodulo_test(a,b):                           # enter integers a, b      
       return a % b - b*(a/b - a//b)             # always returns zero 

print(modulo_test(3,5), modulo_test(-3,5),\
      modulo_test(3,-5), modulo_test(-3,-5))
print('\n')
###################################################################

v1 = (4 == 2*2)                           # parentheses are optional
v2 = 6 > 3*2
v3 = 6 != 3*2
print(v1, v2,v3)
print('\n')

###################################################################

print(1 < 2 and not 3 < 4 or 5 < 6) 
print(1 < 2 and not (3 < 4 or 5 < 6))
print('\n')

###################################################################

print('fiddle' + 'faddle')
print('bibbity ' + 'bobbity ' + 'boo')
print('\n')

###################################################################

print('fiddle' in 'fiddlefaddle', 'fuddle' in 'fiddlefaddle')
print('\n')

###################################################################

v = 'framosham'
print('framosham'[0],'framosham'[-3], v[2])
print('\n')

###################################################################

print('framosham'[3:8],'framosham'[5:9],'framosham'[5:])
print('\n')

###################################################################

print('drizzle'[2:7],'drizzle'[2:])
print('drizzle'[0:5],'drizzle'[:5])
print('\n')


###################################################################

def switch_first_and_last(string):
    L = len(string)
    first = string[0]
    last  = string[L-1]
    middle = string[1:L-1]
    return last + middle + first

string = 'read'
print(switch_first_and_last(string))
print('\n')

###################################################################

def insert_string(strA,strB,idx): # insert strB into strA at position idx
    outstring =  strA[:idx] + strB + strA[idx:]
    return outstring

print(insert_string('abcde','xy', 2))
print('\n')

###################################################################

farmsound = "cockadoodledoo"                    # create a string
newfarmsound = farmsound.replace("doo", "noo")  # invoke replace method
print(farmsound + ',', newfarmsound)
print('\n')

###################################################################

print('frazzle'.upper())               # invoke upper() method
print('2BEES OR NOT 2BEES'.lower())    # invoke lower() method
print('\n')

###################################################################

s = "framosham"
n1 = s.count("am")                   # total no. of am's in str
n2 = s.count("am",7)          # no. of am's starting at index 7 
n3 = s.count("am",2,4)      # no. of am's from 2 to 3 inclusive
n4 = s.count("am",8)          # no. of am's starting at index 8
print(n1, n2, n3, n4)
print('\n')

###################################################################

s = "framosham"
s1 = s.find("am")                       # index of 1st am in str
s2 = s.find("am",7)        # index of 1st am starting at index 7
s3 = s.find("am",2,4)   # index of 1st am between 2, 3 inclusive
s4 = s.find("am",8)        # index of 1st am starting at index 8
print(s1, s2, s3, s4)
print('\n')

###################################################################

print(ord("a"), ord("e"), ord("i"), ord("o"), ord("u"))
print(chr(97), chr(101), chr(105), chr(111), chr(117))

###################################################################

def isletter(ch):
    return (65 <= ord(ch) and ord(ch) <= 90) or \
           (97 <= ord(ch) and ord(ch) <= 122)  
   
print(isletter('x'), isletter('5'))
print('\n')

###################################################################

listA = ['frobish', -4.2, 11, 4 == 5, type(3+2j)]
print(listA)

###################################################################

listB = [listA, 'I am not a list']
print(listB)
print('\n')

###################################################################

print(["alpha","beta"] +  [1,2,3])
print('\n')

###################################################################

listC = [['a','b','c'], 3,2,1]
print(listC[0], listC[1], listC[0][2])
print('\n')
 
###################################################################

print(['a','b','c','d'].index('c'))
print('\n')

###################################################################

listA = ['frobish', -4.2, 11, 4 == 5, type(3+2j)]
print(listA[1:3])                # print items with indices 1 and 2
print(listA[2:])                      # print items from index 2 on
print(listA[:3])               # print items with indices 0,1 and 2
print('\n')

###################################################################

river = 'Mississippi'
print(river.split('i'), river.split('s'))
print('\n')

###################################################################

river = 'Mississippi'
river_list = list('Mississippi')
print(river_list)
print('\n')

###################################################################

listA = ['frobish', -4.2, 11, 4 == 5, type(3+2j)]
print('frobish' in listA, 'frubish' in listA)
print('\n')

###################################################################

listE = []                  # start with an empty list}
listE.append('Afghanistan') # first member
print(listE)
listE.append('Stand')       # second member
print(listE)
listE.insert(1,'Banana')    # insert 'Banana after 'Afghanistan'
print(listE)
print('\n')

###################################################################

t = (1,2,3,4,5)                           # create a tuple variable
print(t)
s = list(t)                                  # convert it to a list
s[3] = 7                                      # change the 4 to a 7
t = tuple(s)                                # convert list to tuple
print(t)
#t[3] = 11                             # error: can't change a tuple
#print('\n')

###################################################################

s = {1, 2, 3, 'x', 'y'}         # initialize set
print(2 in s, 5 in s)           # check membership
print(s)                        # see what we've got
s.add('b')                      # add another member
print(s)                        # see what we've got
s.remove('y')                   # get rid of 'y'
print(s)
print('\n')


###################################################################

scores = {'Betty':82, 'Ralph':67, 'Aaron':85, 'Sally':91}
print(scores['Sally'])         # reveal Sally's score
del scores['Ralph']            # Ralph dropped course
scores['Betty'] = 84           # give Betty 2 more points
scores['Bruce'] = 72           # add late test score
print(scores)
print('\n')


###################################################################

def in_between(a,b,c):
       if c < a and a < b or c > a and a > b:
           return a
       elif c < b and b < a or c > b and b > a:
           return b
       elif a < c and c < b or a > c and c > b:
           return c
       else:
          return "There is no such number."
print(in_between(3,1,2), in_between(3,2,2))
print('\n')

###################################################################

def reversepairs(str):
    L = len(str)
    n = 0                               # index for str
    revpairs = ""                       # create an empty string
    while n <= L-2:
        revpairs = revpairs + str[n+1]  # reversing characters in pair
        revpairs = revpairs + str[n]
        n = n+2                         # increment index by 2
  
    if L%2 != 0:
        revpairs = revpairs + str[L-1]   # odd number of letters 
    return revpairs

print(reversepairs('123456'),reversepairs('1234567'))
#print('abcdefg', reversepairs('abcdefg'))
print('\n')

###################################################################

def num_reciprocals(U):
    s = 0                          # initialize sum
    n = 0                            # initialize counter
    while s <= U:
        n = n + 1                    # increment n
        s = s + 1/n              # update sum with new term
    return n                     

print('number of reciprocals = ', num_reciprocals(10))
print('\n')


###################################################################

def num_odd_reciprocals(U):
    s = 0                          # initialize sum
    n = 0                            # initialize counter
    while s <= U:                  # stop loop when sum > U
        n = n + 1                    # increment n
        if n%2 == 0: continue        # skip even numbers
        s= s+ 1/n                  # update sum with new term
    return n                    

# Input:
print('number of odd reciprocals = ',num_odd_reciprocals(10))
print('\n')

# same speed:
def num_odd_reciprocals2(U):
    s = 0                          # initialize sum
    n = 0                            # initialize counter
    while s <= U:                  # stop loop when sum > U
        n = n + 1                    # increment n
        if n%2 == 0: continue        # skip even numbers
        s= s+ 1/(2*n+1)                  # update sum with new term
    return n                    

# Input:
print('number of odd reciprocals = ',num_odd_reciprocals(7))
print('\n')


###################################################################

def invert_and_multiply(numberstring):   
    numberlist = numberstring.split(',')
    L = len(numberlist)
    prod = 1                            # initialize product
    i = 0                               # start here   
    while i < L:
        if numberlist[i] == '0':
            break    # shortcut for if statements
        reciprocal = 1/float(numberlist[i])
        prod = prod*reciprocal
        i += 1               # simplified notation for i = i+1
    if i == L:                          # made it through ok?
        return prod

numberstring = '2,-1,3.3,4.7,5.2,.00003'
print(invert_and_multiply(numberstring))
print('\n')

###################################################################

def separate_vowels_consonants(instring):
       vowels = ''; consonants = ''          
       for ch in instring: 
           if ch in 'aeiou':            
              vowels  = vowels  + ch
           if  ord(ch) in range(97,123) and ch not in 'aeiou':
              consonants = consonants + ch
       return vowels, consonants               # return both

  
instring = 'honorificabilitudinatatibus'
print(separate_vowels_consonants(instring))
print('\n')


###################################################################

for k in range(3):
     print(k, end=" ")
print('\n')
 
for k in range(2,5):
    print(k, end=" ")
print('\n')

for k in range(2,12,3):
    print(k, end=" ")    # print every third item
print('\n')

for k in range(12,2,-3):
    print(k, end=" ")   # print every 3rd item starting from the end

print('\n')    
for item in "Mississippi":
    if item == "s" or item == "M": continue
    if item == "p": break
    print(item,end=" ")

print('\n')    
gradebook = {"Betty" : 82, "Ralph" : 67, "Aaron" : 85, "Sally" : 91}

for student in gradebook:
    print(student, end=" ")
print("\n")

for grade in gradebook:
    print(gradebook[grade], end=" ")
print("\n")


###################################################################

from random import seed         
from random import random
print(random(),random()) # no seed; generates different numbers
seed(1)                           # initialize seed 
print(random(),random()) # generates different numbers
seed(1)                           # set seed to same value
print(random(),random()) # generates same sequence
seed(37)                          # arbitrarily change seed value 
print(random(),random()) # generates different sequence
print('\n')

###################################################################

import random as r

def area_under_curve(function, left, right, top, num_points):
    pts_below = 0
    for n in range(num_points):       
        x = left + (right - left)*r.random()
        y = eval(function)
        z =  top*r.random()
        if z < y: pts_below = pts_below + 1        #points below graph
    boxarea = top * (right - left)
    rel_freq = pts_below /num_points  # relative frequency of points under graph
    return rel_freq*boxarea

function = 'x**2'
left, right, top = .8,4.4,19.36
num_points = 10000
area = area_under_curve(function, left, right, top, num_points)
print(area)
print('\n')

###################################################################

def factorial(n):
    f = 1                           
    if n > 1:
        f = n * factorial(n - 1)            #do the recursion
    return f   

print(factorial(50))
print('\n')

###################################################################

###################################################################

def square_root(r,n):
    a = 1                           
    if n > 1:
        a = square_root(r,n-1)
        a = (a + r/a)/2                 # do the recursion
    return a   
r = 2
n = 100
print(square_root(r,n)- 2**(1/2))


def is_in_category(instring,category):
    outstring = ''
    for ch in instring: 
        if category == 'vowels' and is_vowel(ch):
           outstring = outstring + ch
        if category == 'consonants' and is_consonant(ch):
           outstring = outstring + ch
    return outstring

def is_upper(ch):
    return ord(ch) in range(65,91)
def is_lower(ch):
    return ord(ch) in range(97,123)
def is_letter(ch):
    return is_upper(ch) or is_lower(ch)
def is_vowel(ch): 
    return ch in 'aeiou' or ch in 'AEIOU'
def is_consonant(ch): 
    return is_letter(ch) and not is_vowel(ch)

instring = 'honorificabilitudinatatibus123'
print(is_in_category(instring,'vowels'))
print(is_in_category(instring,'consonants'))
print(is_in_category(instring,'ants'))

def string2list(letters):
    i = 0
    comma_letters = '' 
    while i < len(letters):        
        comma_letters = comma_letters +  ',' + letters[i]         
        i += 1
    comma_letters = comma_letters[1:]      # omit initial comma 
    letter_list = comma_letters.split(',')   
    return letter_list

letters = 'abcdefg'
print(string2list(letters))


def string2pairs(string):
    if len(string)%2 != 0: string = string + ' ' 
    string_list = string2list(string)
    
    #print(4567,string_list)   # ok

    pair_list = []
    for i in range(0,len(string)-1):
        if string_list[i+1] != ' ':
            pair = string_list[i]+string_list[i+1]
            pair_list.append(pair)

    
    #print(666,pair_list)        # ok

    #double_pair_list = []        
    #for i in range(len(pair_list)):
    #    double_pair_list.append(pair_list[i])
    #    double_pair_list.append(reversepairs(pair_list[i]))
    #return double_pair_list
    return pair_list


