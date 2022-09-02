from random import *
from tkinter import *

#FONCTION RELATIVE AU TKINTER

#fonction tkinter pour le choix
def Resultat():
    global msg2
    msg = entree1.get()
    msg2="" 
    choix = choixvalue.get()
    
    if choix == '1':    
        label1['text'] = codage(msg,clePublique)
        msg2=codage(msg,clePublique)
        
    else:
        label1['text'] = decodage(msg,clePrive)
        msg2=decodage(msg,clePrive)
    button1 = Button(text='Copier ce message', command=copy)
    res.create_window(400, 500, window=button1,width=100)
    
    

 #Refresh l'image pour créer le gif 
def update(delay=200):
    global ind
    ind += 1
    if ind == 27: ind = 0
    print (ind)
    photo.configure(format="gif -index " + str(ind))
    res.after(delay, update)
#fonction pour copier le message dans l'acquisition
def copy():
    global msg2
    msg=str(msg2)
    texte_de_base.set(msg)




#FONCTION CODAGE/DECODAGE
# fonction qui calcule le PGCD de deux entiers (algorithme d’Euclide)
def PGCD(nb1,nb2):
    r=0
    while nb2 != 0:
        r=nb1%nb2
        nb1=nb2
        nb2=r
    return(nb1)

# fonction qui cree un grand nombre
def creaGrand():
    nb=0
    for i in range (3):
        nb+=10**i*randint(1,9)
    return(nb)

# test de premier
def testPrem(nbprem):
    rep=True
    for i in range (2,nbprem):
        if nbprem%i==0:
            rep=False
    return(rep)


# fonction qui cree un grand premier 
def creaPrem():
    nb=creaGrand()
    while testPrem(nb)==False:
        nb=creaGrand()
    if testPrem(nb)==True:
        return(nb)

# fonction coef de Bezout avec a > b

def coefBezout(a, b):
    r=1
    u=1
    v=0
    x=0
    y=1
    while r>0:
        q=a//b
        r=a%b
        a,b=b,r
        x,u=u-q*x,x
        y,v=v-q*y,y
    return(u,v)


#Fonction qui code la puissance d'un nombre x par n modulo p 
def nxmodp (x,n,p):
    y=1
    while n!=0:
        if n%2==1:
            y=(x*y)%p
            n=n-1
        elif n%2==0:
            x=(x**2)%p
            n=n//2
    return(y)

#fonction TRANSFORME LA LETTRE EN CHIFFRE DE CA PLACE DANS L'ALPHABET
def toCodeX(mes):
    if len(mes)%3==1:
        mes+="__"
    if len(mes)%3==2:
        mes+="_"
    
    for loop in range (len(mes)):
        if mes[loop-1]==" ":
            mes[loop-1]="_"
    messageTabChiffre=[]
    r=0
    for a in range (len(mes)//3):
        codeX=0
        a=4
        for i in range(3): 
            codeX+=10**a*(ord(mes[r])-65)
            r+=1
            a-=2
        messageTabChiffre.append(codeX)
    return(messageTabChiffre)

#creation d'un cle publique
# e est un nombre entre 2 et N et dont le PGCD avec Nprim est 1
def creaClePublque(N,Nprim):
    e=randint(2,N)
    while PGCD(e,Nprim)!= 1:
        e=randint(2,N)
    clePublique=[N,e]
    return(clePublique)                                                         

#creation d'une clé privé
# d et k sont les coef de bezout entre 2 et Nprim
def creaClePrive(N,Nprim,e):
    d=coefBezout(e,Nprim)[0]
        #k=coefBezout(e,Nprim)[1]
    #partie qui permet de creer un d entre 2 et Nprim
    a=1
    while d < 2 or d > Nprim:
        d+=Nprim*a
            #k-=e*a
        a+=1
    clePrive=[N,d]
    return(clePrive)

#FONCTION codage
def codage(message,clePublique):
    nbCrypteAttache=""
    nbCrypte=[]
    messageCodeX=toCodeX(message)
    for e in range(len(messageCodeX)):
        #ajoute des 0 pour faire tjrs 8 chiffres
        if nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 10:
            nbCrypteAttache+="0000000"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        elif nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 100:
            nbCrypteAttache+="000000"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        elif nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 1000:
            nbCrypteAttache+="00000"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        elif nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 10000:
            nbCrypteAttache+="0000"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        elif nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 100000:
            nbCrypteAttache+="000"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        elif nxmodp(messageCodeX[e],clePublique[1],clePublique[0]) < 10000000:
            nbCrypteAttache+="0"
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
        else:
            nbCrypte.append(nxmodp(messageCodeX[e],clePublique[1],clePublique[0]))
            nbCrypteAttache+=str(nbCrypte[e])
    return(nbCrypteAttache)

#FONCTION decodage
def decodage(message,clePrive):
    nbDecryptAttache=[]
    nbDecryptAttacheVraimentcettefois=""
    indice=0
    for a in range(len(message)//8):
        Troislettre=""
        for i in range(8):
            Troislettre+=message[indice]
            indice+=1
        nbDecryptAttache.append(int(Troislettre))
    for n in range(len(nbDecryptAttache)):
        nbDecryptAttache[n]=nxmodp(nbDecryptAttache[n],clePrive[1],clePrive[0])
    #TRANSFOME LES CHIFRE DECOD2 EN LETTRES.
    for k in range(len(nbDecryptAttache)):
        nbDecryptAttacheVraimentcettefois+=chr((nbDecryptAttache[k]//10000)+65)
        nbDecryptAttache[k]-=10000*(nbDecryptAttache[k]//10000)
        nbDecryptAttacheVraimentcettefois+=chr((nbDecryptAttache[k]//100)+65)
        nbDecryptAttache[k]-=100*(nbDecryptAttache[k]//100)
        nbDecryptAttacheVraimentcettefois+=chr((nbDecryptAttache[k]//1)+65)
        nbDecryptAttache[k]-=1*(nbDecryptAttache[k]//1)
        nbDecryptAttacheVraimentcettefois = nbDecryptAttacheVraimentcettefois.replace("_","")
    return(nbDecryptAttacheVraimentcettefois)





#p et q sont des grands premiers


"""
p=creaPrem() 
q=creaPrem()
"""

p=12473 
q=5741
N=p*q
Nprim=(q-1)*(p-1)
ind=0


#CREATION DES CLEFS
clePublique=creaClePublque(N,Nprim)
clePrive=creaClePrive(N,Nprim,clePublique[1])
"""
#codage
messageClaire1=input()
messageCrypt1=codage(messageClaire1,clePublique)
print(messageCrypt1)

#decodage
messageCrypt2=input()
messageClaire2=decodage(messageCrypt2,clePrive)
print(messageClaire2)
"""





fenetre = Tk()
fenetre.title('Outil de décodage')
fenetre.minsize(width=800, height=600)

choixvalue=StringVar()  
choixvalue.set("1")
texte_de_base=StringVar()
texte_de_base.set("")

res = Canvas(fenetre, width=800, height=600)
res.pack()
photo = PhotoImage(file="C:\\Users\\Ralph\\Desktop\\Nouveau dossier\\leschiffres.gif")
res.create_image(0,0,anchor='nw', image=photo)
photo2 = PhotoImage(file="C:\\Users\\Ralph\\Desktop\\Nouveau dossier\\cadena.png")
res.create_image(280,100,anchor='nw', image=photo2)
entree1 = Entry(fenetre,textvariable=texte_de_base)
res.create_window(400, 230, window=entree1,width=100)
label1 = Label()
res.create_window(400, 350, window=label1) 
button1 = Button(text='Valider', command=Resultat)
res.create_window(400, 470, window=button1,width=100)

#CHOIX cryptage ou decryptage
choix1 = Radiobutton(fenetre, text='Cryptage', variable=choixvalue, value='1')
res.create_window(400, 160, window=choix1,width=100)
choix2 = Radiobutton(fenetre, text='Decryptage', variable=choixvalue, value='0')
res.create_window(400, 180, window=choix2,width=100)

update()
fenetre.mainloop()


