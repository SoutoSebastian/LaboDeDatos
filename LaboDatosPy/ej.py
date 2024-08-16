

def palindromo (p):
    res = True
    for i in range (len(p)):
        if p[i] != p[len(p)-i-1]:
            res = False
    
    return res

#print(palindromo("nadan") == True) 

def divisibles13():
    i = 0
    while i<214:
        if i % 13 == 0:
            print(i)
        i += 1
            
#divisibles13()

def obelisco():
    i = 0
    res = 0
    cantidadBilletes = 1
    while i <= 67.5 * 1000:
        i += 0.11 * cantidadBilletes
        res += 1
        cantidadBilletes *= 2
    return res

print(obelisco())