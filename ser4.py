import math
import random
import socket
pu=[]
pr=[]
host="127.0.0.1"
port=2085
l1=[]
def primeNr(n): #storing prime no from 2 to n=50 in list l1
    print("Prime numbers from 2 to ",n)
    
    for i in range(100,n):
        ip= True
        for j in range(2,int(math.sqrt(i)) + 1):
            if i % j == 0:
                ip= False
                break
        if ip:
            l1.append(i)
    print(l1)
primeNr(200)
p=random.choice(l1)
q=random.choice(l1)
n=p*q
t=(p-1)*(q-1)
def publickey(b):
    for i in range(1,b):
        e1=random.randint(1,b)
        v=math.gcd(e1,b)
        if(v==1):
            return e1
e=publickey(t) # calculating e, part of a public key
print("e=",e)
def priv(p,q):
    b=[0,1]
    c=[q,p]
    k=[0,int(q/p)]
    i=2
    d1=0
    
    for i in range(q):
    	d1=(1+i*q)/p
    	j=int(d1)
    	if (d1-j==0):
    		#print(j)
    		#print(i)
    		break
    return j
d=priv(e,t) #calculating d ,part of a public key
print("d=",d)
pu=[e,n]
pr=[d,n]
print(pu,pr)

o=int(input("Select which type of communication you want\n1:Encrypted\n2:Digitally signatured\n3:both\n"))
print("Thank You! Now server is ready to connect")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
c,addr=s.accept()

c.send(str(o).encode())
ec=(c.recv(2048)).decode()
c.send(str(e).encode())
nc=(c.recv(2048)).decode()
c.send(str(n).encode())

print("Client connected and public keys are exchanged")
ec=int(ec)
nc=int(nc)




def encr(mes):
    m=[]
    c=[]
    cip=0
    for i in mes:
       m.append(ord(i))
    for i in m:
        if(o==1):
            cip=pow(i,ec)%nc
        elif(o==2):
            cip=pow(i,d)%n

        elif(o==3):
            cip=pow(i,d)%n
            if cip>nc:
                cip=i
            cip=pow(cip,ec)%nc           
        c.append(str(cip))
    string=' '.join(c)   #list will be converted to string with seperator ' '
    return string


def dec(j):
    mes=[]
    l=j.split(' ')    #string will be converted to list
    for i in l:
        if(o==1):
            mes.append(chr(pow(int(i),d)%n))
        elif(o==2):
            mes.append(chr(pow(int(i),ec)%nc))
        elif(o==3):
            a=pow(int(i),d)%n
            if(a not in range(32,127)):
                a=pow(a,ec)%nc
            a=chr(a)
            mes.append(a)
    
    mes=''.join(mes)  #list will be converted to string
    return mes
    

while True:
    j=(c.recv(2048)).decode()
    if not j:
        break
    print("(Encrypted) client --> "+j)
    print("(Decrypted) client --> "+dec(j))
    string=input("Server --> ")
    strl=encr(string)
    c.send(strl.encode())    
c.close()


