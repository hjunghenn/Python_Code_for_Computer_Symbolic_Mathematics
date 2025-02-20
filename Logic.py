
import Tools as tl

############################# simple table ############################

def zero_one(i,j,ncols):
    # returns truth value at row i and col j of table 
    x = int((i-1)/2**(ncols-j))    # 1 <= i <= nrows, 1 <= j <= ncols
    y = int((1 + (-1)**x) / 2)    
    return y
  
def initial_table(numvars):
     # generates a table of 1"s,0"s in standard format    
    table = [] 
    ncols = numvars   
    nrows = 2**numvars             # no. of rows of variable values
    for i in range(1,nrows+1):                  # generate the rows   
        row = ''
        for j in range(1,ncols+1):        
            tval = zero_one(i,j,ncols) # truth val at position (i,j)
            row = row + str(tval)                   # append to row         
        table.append(row)
    return table                   

#tl.print_list(initial_table(4),'h')

############################# computations ############################

def eval_stmt(ps,mode):                
    ps = ps.replace("1'","0")
    ps = ps.replace("0'","1")   
    global idx
    while idx < len(ps):
        c = ps[idx]                        # character at index idx
        if c in "01":                
            p = c                              # c is a truth value
            idx += 1
        elif c == "+":
            if mode > 0: break     # wait for higher mode to finish
            idx += 1
            q = eval_stmt(ps,0)  # lowest mode; all other calcs 1st
            p = disjunction(p,q)                    # calculate p+q
        elif c == "*":
            idx += 1
            q =  eval_stmt(ps,2) # highest mode: conjunctions first
            p = conjunction(p,q)                   # calculate p*q
        elif c == "-":                                # conditional
            if mode > 1: break          # wait for conjunction calc
            idx += 2                                    # skip "->"
            q =  eval_stmt(ps,1)
            p =  conditional(p,q)                  # calculate p->q
        elif c == "<":                              # biconditional
            if mode > 1: break 
            idx += 3                                   # skip "<->"
            q =  eval_stmt(ps,1)
            p =  biconditional(p,q)             
        elif c == "(":
            idx += 1                                     # skip "("
            p =  eval_stmt(ps,0)         # evaluate stuff inside ()
            idx = idx + 1                                # skip ")"
            if idx < len(ps) and ps[idx] == "'":
                p = negation(p)           # negate paren expression
                idx += 1    
        elif c == ")":
            break 
    return p

def disjunction(p, q):
    return str(min(int(p) + int(q), 1))  

def conjunction(p, q):
    return str(int(p)*int(q))  

def negation(p):
    return str(1-int(p))  

def conditional(p,q):
    return disjunction(negation(p), q)
    
def biconditional(p,q):    
    return conjunction(conditional(p,q), conditional(q,p))


######################### statement to table ##########################

def statement2truthtable(stmt):
    # input: compound statement
    # output: truth table  
    global idx
    stmt = stmt.replace(" ","")               # remove white space 
    var_list,varstring  = tl.get_vars(stmt)
    itab = initial_table(len(varstring))     
    tableT = []                     # table with only true values attached   
    tableT.append(varstring + ' ' + stmt)
    tableF = []                        # table with only false values   
    tableF.append(varstring + ' ' + stmt)
    
    tableA = []                        # table with all values    
    tableA.append(varstring + ' ' + stmt)
    
    stmt = tl.insert_asterisks(stmt,var_list)
    for i in range(len(itab)):        # generate the truth values
       row = itab[i]
       ps = stmt                   # for populating with 0"s, 1"s
       #print("i:",i,', ',end = " ")
       for j in range(len(row)):         # insert 1"s, 0"s into ps 
           ps = ps.replace(varstring[j],row[j])
           #print(ps,end = " ")                # for observation
       idx = 0                  # points to position in string ps
       value = eval_stmt(ps,0)    # truth value of populated stmt
       #print(value,"\n")                      # for observation
       row = row  + value    # attach truth value of statement
       tableA.append(row) 
       if value == '1':      
          tableT.append(row) 
       if value == '0':      
          tableF.append(row)    
    return  tableA, tableT, tableF


def print_truth_table(table):
    print(table[0].replace('"',''))  # remove double quotes
    space = len(table[1])*' '   # space to separate truth value
    position = len(table[1])-1       # put space starting here
    for i in range(1,len(table)):
        row = tl.insert_string(table[i],space,position)[0] # insert space
        print(row.replace("'",'')) # remove single quotes

'''
s1 = "(p + q)'"
s2 = "pq"
s3 = "(p+r'+ q)-> p'q r'"
s4 = "((p+q+r)->qr')<->(pq)"
s5 = "pqr + pqr' + pq'r + pq'r' + p'qr + p'q'r"
stmt = s4

tableA,tableT,tableF = statement2truthtable(stmt)

print_truth_table(tableA);print('\n')
print_truth_table(tableT);print('\n')
print_truth_table(tableF)
'''


############################## equivalence ############################

def is_tautology(stmt):    
    TableA,TableT,TableF = statement2truthtable(stmt)     
    return len(TableT) == len(TableA)    

#stmt = "(p->q)(q->r)->(p->r)" # tautology
#print(is_tautology(stmt))

def is_contradiction(stmt):
    TableA,TableT,TableF = statement2truthtable(stmt)     
    return len(TableF) == len(TableA,)    

#stmt = "((p->q)(q->r)->(p->r))'"
#print(is_contradiction(stmt))

def are_equivalent(a,b):
    stmt = "(" + a + ")<->(" + b + ")"
    return is_tautology(stmt)

'''
print(are_equivalent("(p + q)'", "p'q'"))
print(are_equivalent("(pq)'","p' + q'"))
print(are_equivalent("p -> q", "q' -> p'"))
print(are_equivalent("p(q + r)", "pq + pr"))
print(are_equivalent("p + qr", "(p + q)(p + r)"))
print(are_equivalent("(p+q)+r","p+(q+r)"))
print(are_equivalent("(pq)r","p(qr)"))

# equivalent:
a = "(p+q)+r";  b = "p+q+r"
a = "p+(qr)";   b = "p+qr"
a = "p+(q->r)"; b = "p+q->r"   
a = "(pq)->r";  b = "pq->r"
a = "pqrs";     b = "(pq)(rs)"
a = "(p+q)+r";  b = "p+(q+r)"
a = "p+q+r+s";  b = "p+(q+(r)+s"
# not equivalent:
a = "(p+q)->r"; b = "p+q->r" 
print(are_equivalent(a,b))
'''


########################### valid arguments #######################

def isvalid(arg):   # list of premises and a conclusion
    L = len(arg)
    for i in range(L):
        arg[i] = "(" + arg[i] + ")"    
    premise = "".join(arg[:L-1])
    conclusion = arg[L-1]    
    stmt = premise + "->" + conclusion
    if is_tautology(stmt): 
        return "valid"
    return "not valid"

'''
arg1 = ["p->q","q->r","p->r"]   # hypothetical syllogism
arg2 = ["p+q","p'","q"]         # disjunctive syllogism
arg3 = ["p->q","p","q"]         # modus ponens
arg4 = ["p->q","q'","p'"]       # modus tollens (contrapositive)
arg5 = ["p->q","q","p"]
arg6 = ["p+q","q","p"]
arg7 = ["p->q","p'", "q"]
arg8 = ["p'->q","pq", "q'"]
args = [arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8]

for i in range(len(args)):  
   print('arg',i+1,isvalid(args[i]))
'''


################## disjunctive form ###################

def tvals2conj(varstring,valcombo):  
    # true precisely for valcombo
    conj = ''
    for i in range(len(varstring)):        
        conj = conj + varstring[i]
        if valcombo[i] == '0':               
            conj = conj + "'"                      
    return conj

'''
varstring = "pqr"
valcombo = "010"
varstring = "pqrstuvwxy"
valcombo = "1010101010"
print(varstring,'\n')
print(valcombo,'\n')
print(tvals2conj(varstring,valcombo))
'''

def disj_of_conj(varstring,valcombos):        
    disj = ''                 
    valcombos = valcombos.split(',')   
    for combo in valcombos:                   # run thru desired combos                    
        conj = tvals2conj(varstring,combo)                
        disj = disj + ' + ' + conj           # form the disjunction         
    return disj[3:]                          # remove first ' + '    

'''
varstring = "pqr"
valcombos = "100,111,101"
print(disj_of_conj(varstring,valcombos))
'''

def disjunctive_form(stmt):   
    stmt = stmt.replace(" ","")                 # remove white space
    varstring = tl.get_vars(stmt)[1]                    # string form    
    Ttable = statement2truthtable(stmt)[1][1:]       # true rows only  
    print('Ttable:    ',Ttable)
    truecombos = ','.join(Ttable)      
    print('truecombos:',truecombos)    
    return disj_of_conj(varstring,truecombos)

'''    
stmt = "p+q'(r+ p'+ q)" 
stmt = "((p+q+r)->qr')<->(pq)"   
#stmt = "p+qr"
disj = disjunctive_form(stmt)
#print(stmt)
#print(statement2truthtable(stmt)[0][1:])    # entire table without header
#print('\n')
print('disunctive form:',disj)
#print(statement2truthtable(disj)[0][1:])    
'''


####################  conjunctive form ###################  


def tvals2disj(varstring,valcombo):   ##ok
    #false precisely for valcombo   
    disj = ''
    for i in range(len(varstring)):
        if valcombo[i] == '1':               
            disj = disj + varstring[i] + "' + "   # negate      
        else:    
            disj = disj + varstring[i] + " + "  
    return disj[:len(disj)-3] # remove last padded '+'

'''
varstring = "pqrstuvwxy"
valcombo = "1010101010"
print(varstring)
print(valcombo)
print(tvals2disj(varstring,valcombo))
'''


def conj_of_disj(varstring,valcombos):        
    conj = ''                 
    valcombos = valcombos.split(',')           
    for combo in valcombos:                   # run thru desired combos                    
        disj = tvals2disj(varstring,combo)                       
        conj = conj + '(' + disj + ')'      # form the disjunction 
    
    return conj                          # remove first ' + '    

'''
varstring = "pqr"
valcombos = "100,111,101"
stmt = conj_of_disj(varstring,valcombos)
print(stmt)                       
'''

def conjunctive_form(stmt):   
    stmt = stmt.replace(" ","")               # remove white space
    varstring = tl.get_vars(stmt)[1]       
    Ftable = statement2truthtable(stmt)[2][1:] # false rows only        
    false_combos = ','.join(Ftable)          
    return conj_of_disj(varstring,false_combos)


'''
#stmt = "p+q'(r+ p'+ q)"    
#stmt = "p+q'"    
stmt = "((p+q+r)->qr')<->(pq)" 
conj = conjunctive_form(stmt)
print('conjunctive form',conj)
print(statement2truthtable(stmt)[0][1:])    
print(statement2truthtable(conj)[0][1:])
'''

# big test
'''
stmt = "((p+q+r)->qr')<->(pq)"
#stmt = "(p+q+r)->qr"
print(stmt)
print(statement2truthtable(stmt)[1:],"\n")

d = disjunctive_form(stmt)
print(d)
print(statement2truthtable(d)[1:],"\n")

c = conjunctive_form(stmt)
print(c,"\n")
print(statement2truthtable(c)[1:],"\n")

cd = conjunctive_form(d)
dcd = disjunctive_form(cd)
print(d)
print(dcd,'\n')
print(statement2truthtable(dcd)[1:],"\n")

dc = disjunctive_form(c)
cdc = conjunctive_form(dc)
print(c)
print(cdc,'\n')
print(statement2truthtable(cdc)[1:],"\n")
'''


