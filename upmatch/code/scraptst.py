import re, csv, requests, time, random, os.path
from bs4 import BeautifulSoup

#if sys.version_info[0] == 3:
#    from urllib.request import *
#else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    #from urllib import urlopen


# filename = '/Users/Jacobo/pr/upmatch/a.jpg'
# with open(filename, 'wb') as file:
#   file.write(urlopen('https://etu.math.upmc.fr/math/photos/3520121.jpg').read())


def wait():
    a = random.randint(250, 1000) / 1000
    #a = random.randint(1, 10) / 1000
    time.sleep(a)

def ask(adresse,hdr,payload):
    wait()
    while True:
            try:
                if(payload==0):
                    req = requests.get(adresse)
                else:
                    req = requests.post(adresse, data=payload, headers=hdr)
                if req.status_code == 200:
                    break
                else:
                    print(req.status_code)
                    time.sleep(30)
            except:
                print("error ",payload,adresse)
                time.sleep(30)
    if(payload==0):
        print("0 ",end='')
    print("good")
    return req


def get_infos(r,hdr):
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    infos=list()
    for o in soup.findAll("td", {'class': 'result'}):
        info=dict()
        info['name'] = o.text.strip()  # prenom NOM
        info['etu'] = str(o)[77:84]  # numETU
        if (int(info['etu'][0]) != 3 or int(info['etu'][1]) < 1):
            print(info['etu'])
            info=dict()
            continue
        adresse = 'https://www.annuaire.upmc.fr/upmc/list.upmc?method=list&dn=uidInterne=' + str(o)[re.search(r'Interne=',str(o)).span()[1]:re.search(r',ou=',str(o)).span()[0]] + ',ou=People&mode=display'
        print(adresse,' data request')
        req=ask(adresse,hdr,0)
        #can also get sex
        full = BeautifulSoup(req.text, 'html.parser')
        full = full.findAll("td", {'class': 'attributeDisplayer_value'})
        if(str(full[0])=='<td class="attributeDisplayer_value"><div>M.<br/></div></td>'):
            info['sexe']='H'
        else:
            info['sexe']='F'
        mail = str(full[5])
        try:
            info['mail'] = mail[re.search(r'@etu.upmc.fr">', mail).span()[1]:re.search(r'</a>', mail).span()[0]]
        except:
            info['mail']=0
        #print(info)
        #a=input()
        if(info!=dict()):
            infos.append(info)
    #print(infos)
    return infos

#make csv qu bug
def make_csv(infos, filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ("mail", "sexe", "etu",  "name")
        print(fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        #for infos in informations:
        writer.writerows(infos)
        #print('AAA')


def scrap(init, mid):
    random.seed()
    url = "https://www.annuaire.upmc.fr/upmc/simpleSearch.upmc"
    filedebut = "/Users/Jacobo/pr/upmatch/data/"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.95 Safari/537.36'}
    i=ord(init)
    j=ord(mid)
    infos = list()
    for k in range(ord('a'), ord('z') + 1):
        name = chr(i) + chr(j) + chr(k)
        payload = {
            'name': name,
            'name_query_type': 'NAME*',
            'surname': '',
            'surname_query_type': 'SURNAME*',
            'filter': 'objectClass=etudiant',
            'number': '2500',
            'bouton.x': '38',
            'bouton.y': '15',
            'inputPage': 'inputBadSearchWithoutFilters',
        }
        r = ask(url,hdr, payload)

        # call get info with r
        informations = get_infos(r,hdr)
        if(informations!=list()):
            infos+=informations
    print(infos)
    #a=input()
    filename = filedebut + chr(i) + chr(j) + '.csv'
    print(filename)
    if (infos!=list()):
        make_csv(infos, filename)

def merge():
    filedebut = "/Users/Jacobo/pr/upmatch/data/"
    final="/Users/Jacobo/pr/upmatch/data/users.csv"
    initial=True
    with open(final, 'w') as base:
        for i in range(ord('a'),ord('z')+1):
            for j in range(ord('a'), ord('z')+1):
                filename=filedebut+chr(i)+chr(j)+'.csv'
                if not ( os.path.exists(filename)):
                    print('nexiste pas',filename)
                    scrap(chr(i),chr(j))
                if(os.path.exists(filename) ):
                    print(filename)
                    with open(filename, 'r') as fichier:
                        lignes=fichier.readlines()
                        if not (initial):
                            try:
                                lignes.pop(0)
                            except:
                                continue
                        else:
                            initial=False
                        base.writelines(lignes)

                                          