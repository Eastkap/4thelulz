#Code
import random



def c2vid(caches, endpoints):
    cpy= caches
    for key in cpy.keys():
        taillevid =0 
        for i in cpy[key]:
            taillevid += vidSize[cpy[key][i]]
        while (taillevid>CacheSize):
            a=random.randint(0,len(cpy[key]))
            taillevid-= vidSize[cpy[key][a]]
            cpy[key].remove(a)
    return cpy
        
    
        
    

filename='/Users/Jacobo/Downloads/test.in'
with open(filename, 'r') as cat:
    fichier=cat.readlines()
    ligneun=fichier[0].split()
    Nbvid=int(ligneun[0])
    Nbend=int(ligneun[1])
    NbReq=int(ligneun[2])
    NbCache=int(ligneun[3])
    CacheSize=int(ligneun[4])
    vidSize=[ int(x) for x in fichier[1].split()]
    endpoints=list()
    indice=2
    endpointsvides=set()
    caches=dict()
    for i in range(Nbend):
        endpoint=dict()
        ligne=[int(x) for x in fichier[indice].split()]
        #print(ligne)
        #a=input()
        endpoint['latence']=dict()
        endpoint['latence']['dc']=ligne[0]
        endpoint['latence']['ncache']=ligne[1]
        if (endpoint['latence']['ncache'] ==0):
            endpoints.append(endpoint)
            endpointsvides.add(i)
            indice+=1
            continue
        #print(endpoint['latence']['ncache'])
        indice+=1
        for j in range(0,endpoint['latence']['ncache']):
            ligne=[int(x) for x in fichier[indice].split()]
            if (ligne[0] not in caches.keys()):
                caches[ligne[0]]=[]
            endpoint['latence'][ligne[0]]=ligne[1]
        #ne pas oublier incrementer indice
            indice+=1
        endpoint['videos']=dict()
        endpoints.append(endpoint)
    #print(endpoints)
    ligne=[int(x) for x in fichier[indice].split()]
    taille=len(fichier)
    while(indice<taille):
        ligne=[int(x) for x in fichier[indice].split()]
        if not (ligne[1] in endpointsvides):
            endpoints[ligne[1]]['videos'][ligne[0]]=ligne[2]
        indice+=1
        for key in endpoints[ligne[1]]['latence'].keys():
            if(key!='dc' and key!='ncache'):
                if(vidSize[ligne[0]]<=CacheSize):
                    caches[key].append(ligne[0])
    resultat=genereConfig(caches)
    print(resultat)