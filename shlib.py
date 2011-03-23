# -*- coding: UTF-8 -*-
'''
Created on 23.11.2010

@author: bmw

@todo: make class
'''

import sys
import random
import fractions


'Big prime number'
#p = 43213164901794279093007345412155723871258766965842189343642824674226586671278421048786750725767410848957676770032275974151870568841788467334437884551843640059833735118402230479078863266439732769361991
prime = 203956878356401977405765866929034577280193993314348263094772646453283062722701277632936616063144088173312372882677123879538709400158306567338328279154499698366071906766440037074217117805690872792848149112022286332144876183376326512083574821647933992961249917319836219304274280243803104015000563790123

def s2i(s,enc=sys.getdefaultencoding()):
    "Implement conversion from string to integer representation"
    rez = 0
    #for c in s:
    #    print(ord(c), end=' ');
    for c in s.encode(enc):
        rez <<= 8
        rez |= c
    return(rez)

def i2s(b,enc=sys.getdefaultencoding()):
    "Implement conversion from integer to string representation"
    try:
        b = int(b)
    except:
        raise Exception('Error: input not integer')
    rez = bytearray()
    while b:
        rez.insert(0, b&0xFF)
        b >>= 8
    return rez.decode(enc)


def getshadows(k,n,s,p=None,debug=False):
    '''Create shadow: 
    @param s: secret message
    @param k: - threshold (k,n) threshold scheme
    @param n: - shadows number
    @param p: - prime number 
    
    @todo: generate (p>s)
    Currently used by defined prime number
    '''
    
    #For save x, use hash
    shadows = {}
    
    #Range of coefficients
    range_min = 10**100
    range_max = 10**150
    
    #Prime number. len(p)~200 при длине строки в 100 символов количесвто цифр числового представления строки~ 240 цифр
    if(p==None):
        p = prime
    
    if(p <= s):
        raise Exception('Error: P<=S')
    
    #Generate a coefficients
    a = [random.randint(range_min,range_max) for i in range(k)]

    if(debug):
        a[3] = 9
        a[2] = 7
        a[1] = 8
        a[0] = 5
    
    #Generate Polynomial
    x = 1
    while(len(shadows)<n):
        str = ''
        shadow = 0;
        #generate polynomial for each x
        for i in range(k-1,0,-1):
            shadow += a[i]*x**i
            if(debug):
                str += 'a%s*%s^%s +'%(i,x,i)
        #Add secret component(a0)
        shadow += s
        shadow %= p
        
        #Check same element
        if(shadow not in shadows.values()):
            shadows[x] = shadow;
            
        x += 1
        
        if(debug):
            print(str + ' s')
            
    return(shadows)
    #print([((random.randint(1,10)*x**2 + random.randint(1,10)*x + s)%p) for x in range(1,k+1)]);
    
    
def reconstruction(shadows, p=None):
    '''Secret reconstruction algorithm, based on Lagrange polynomial algorithm
    @param shadow: Dictionaries of x is a key and y is a value
    @param p: Prime number  
    '''
    
    '@todo: hack, rewrite with class'
    if(p==None):
        p = prime
    
    #Lagrange polynomial
    s = 0
    l = {}
    for x in shadows.keys():
        #print({j:a[j] for j in shadows if j != x})
        #print('x: '+str(x))
        l[x] = 1
        for j in shadows:
            if(j!= x):
                #print(j,end='')
                #@todo: change [] on Fraction()
                #l[x][0] *= -j   #Numerator
                #l[x][1] *= x-j  #Denominator
                l[x] *= fractions.Fraction(-j,x-j)
        #print()
        #print(l[x])
        s += l[x] * shadows[x]
        #print()
    #print(i2s(s%p))
    return(s%p)

#int = s2i('i'*50)       
#print("int",len(str(int)))
#int = s2i('g'*50)
#print("int",len(str(int)))
#Многочлен размерности k - 1 где к- кол-во участников. (теней)
#F(x) = (a1*x^2 + a2*x + a0) % 13 Где а0 - секрет, 13 - простое число, ai - случайные числа
#Вычислим значения для 5 различных точек
#a = [((7*x**2 + 8*x + 11)%13) for x in range(1,6)]
#print(a);

shadows = getshadows(3,5,s2i('a'*50))
print(i2s(reconstruction(shadows)))

