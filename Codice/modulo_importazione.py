%modulo per importare file .GT

f=open('IMG_0030.gt',encoding='utf-8')
n=f.read()

l=[]
s=n.split()
for t in n.split():
    l.append(float(t))
g=int(len(l)/7)

m=[]
for i in range(g):
    m.append(l[i*7:i*7+7])
    


