from sympy import *
import numpy as np
import json



def getJSON():
    with open('data.json') as json_file:
        data = json.load(json_file)
        return data["equation"], data["type"], data["bounds"]

eq, type, bounds = getJSON()

#change some of the chars


eq = eq.replace("**", "^")

#replace every letter with x

l = ["b", "d", "f", "g", "h", "j", "k", "m", "u", "w", "v", "z"]

for letter in l:
    eq = eq.replace(letter, "x")


#add in * in correct place, in case user didn't

def gettype(val):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    special = ['p']
    special2 = ["e"]
    if val in nums:
        return "num"
    elif val in letters:
        return "letters"
    elif val in special:
        return "special"
    elif val in special2:
        return "special2"
    else:
        return "none"

def checksec(str, pos):
    return str[pos-1:pos+2] == "sec"



s = 0
while s < len(eq) - 1:

    #sec case: if if current letter is e, then continue
    if checksec(eq, s) or checksec(eq, s+1):
        s += 1
        continue


    type1 = gettype(eq[s])
    type2 = gettype(eq[s+1])

    if (type1 != type2 and type1 != "none" and type2 != "none"):
        eq = eq[0:s+1] + "*" + eq[s+1:]
        s -= 1
    s += 1

eq = eq.replace("p", "pi") #switch back

print(eq)


x, y, z = symbols('x y z')

val = -1

if type == "derivative":
    val = diff(eq, x)
elif type == "integral":
    val = integrate(eq, x)
    val = str(val)
    val += " + C"
elif type == "limit":
    val = limit(eq, x, bounds)
elif type == "definite integral":
    lower = bounds[0:bounds.find(",")]
    upper = bounds[bounds.find(",") + 1:]
    val = integrate(eq, (x, lower, upper))
    val = N(val)
elif type == "summation":
    lower = bounds[0:bounds.find(",")]
    upper = bounds[bounds.find(",")+1:]
    val = Sum(eq, (x, lower, upper)).doit()
    val = N(val)
elif type == "product":
    lower = bounds[0:bounds.find(",")]
    upper = bounds[bounds.find(",")+1:]
    val = Product(eq, (x, lower, upper)).doit()
    val = N(val)

#formatting

print(val)

val = str(val)

val = val.replace("**", "^")

data = {}
data["equation"] = str(val)

with open('answer.json', 'w') as outfile:
    json.dump(data, outfile)
