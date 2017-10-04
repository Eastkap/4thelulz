# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def refait_nombre(s,element):
    once=0
    res=''
    for nombre in s:
        if(nombre==element):
            if(once==0):
                once=1
            else:
                res+=str(nombre)
        else:
            res+=str(nombre)
    return int(res)

def solve():
    dico=dict()
    for i in range(1,100):
        for j in range(1,100):
            f=i/j
            if f<1 and (i%10!=0 and j%10!=0):
                for a in str(i):
                    for b in str(j):
                        if a==b and (len(str(i))>1) and len(str(j))>1:
                            #print(i," ",j)
                            #inew=int(str([nombre for nombre in str(i) if(nombre!=a)]))
                            #jnew=int(str([nombre for nombre in str(j) if(nombre!=a)]))
                            inew=refait_nombre(str(i),a)
                            jnew=refait_nombre(str(j),a)
                           # print(i,"  ", inew, " ", j, " ",jnew)
                            #z=input()
                            if i*jnew==j*inew:
                                dico[i]=j
    return dico

def pgcd(a,b) :  
   while a%b != 0 : 
      a, b = b, a%b 
   return b

def main():
    res=solve()
    den=1
    num=1
    for i in res.keys():
        num*=i
        den*=res[i]
    print(den/pgcd(num,den))
