from func import *
from conditions import poor_suffix

def power(period,top,bottom):
    # Returns the top/bottom power of the word period
    p=len(period)
    rep=""
    while (len(rep)+1)*bottom <= p*top:
        rep+=period[len(rep)%p]
    return rep

# Forbidden Factors
# Entered as dictionaries, where the forbidden factors are keys, and the values are used to provide evidence that they are forbidden

F1={}
F1["00"]=(1,"01",5,2,[""],["0","1","2"])
F1["11"]=(1,"022",7,3,[""],["0","1","2"])
F1["212"]=(3,"2010201022010",31,13,[""],["0","1","2"])
F1["2222"]=(2,power("0102",2,1),5,2,[""],["0","1","2"])
F1["1222"]=(4,power("02010220102010220102",2,1),19,8,[""],["0","1"])
F1["2221"]=(4,power("20102010220102020102",2,1),19,8,["0","1"],["0","1","2"])
F1["1010"]=(1,"02201",12,5,[""],["1","2"])
F1["0101"]=(1,"20102",12,5,["2"],["2"])
F1["022022"]=(2,"2010220102010",31,13,["0","1","2"],["0","1","2"])
F1["220220"]=(2,"2010201020102",31,13,["0","1","2"],["0","1","2"])

F2={}
F2["202202"]=(2,"2010201022010",31,13,["0","1","2"],["0","1","2"])
F2["1022021"]=(3,"20102010220102020102201020102",67,29)
F2["1202201"]=(3,"20102010220102010220102020102",67,29)
F2["120102201021"]=(3,"20102010220102010220102020102201020102010220102020102",124,53)
F2[power("021012",13,6)]=(2,"020102201020102020102201020201",71,30,["1","2"],["1","2"])
F2[power("012021",13,6)]=(2,"020102201020201020102201020102",71,30,["1","2"],["1","2"])
F2[power("21012010",21,8)]=(0,"21012010",21,8)
F2[power("21012210120",27,11)]=(0,"21012210120",27,11)
F2[power("2101221012010",31,13)]=(0,"2101221012010",31,13)

F3={}
F3["2"+power("2101",17,4)+"2"]=(3,"20102010220102010220102010201022010202010220102010201022010201022010201020102201020201022010",211,92,["0","1"],["0","1"])
F3[power("2101210122101",31,13)]=(0,"2101210122101",31,13)

F4={}
F4[power("0222",17,4)+"1"]=(1,"2010202020102020",37,16,["1","2"],[""])
F4[power("22010",12,5)]=(1,"02020102201",27,11,[""],["0","1","2"])
F4[power("022201",29,6)]=(0,"022201022201",29,12)
F4[power("0222010222",12,5)]=(0,"0222010222",12,5)
F4[power("0222022201",12,5)]=(0,"0222022201",12,5)
F4[power("0222010222010222022201",5,2)]=(0,"0222010222010222022201",5,2)

def parikh(w):
    # Returns the Parikh vector of a word w over Sigma_3
    vector=[w.count(str(i)) for i in range(3)]
    return vector

def parikh_check(period,top,bottom):
    # Returns True if and only if every entry of the Parikh vector of period^{top/bottom} is at least 2/7 of the corresponding entry of the Parikh vector of period
    excess=power(period,top,bottom)
    return all(7*parikh(excess)[i]>=2*parikh(period)[i] for i in range(3))

def critical_exponent(w):
    # Returns the critical exponent of w
    N=len(w)
    top=1
    bottom=1
    word=""
    u=""
    for n in range(N):
        u+=w[n]
        p=1
        while n*bottom>=p*top:
            i=0
            while u[-1-i]==u[-1-i-p]:
                i+=1
                if i+p>=n+1:
                    break

            if i>=1 and (i+p)*bottom>p*top:
                bottom=p
                top=i+p

            p+=1
        
    return [top,bottom,word]

def has_suffix(w,s):
    n=len(w)
    m=len(s)
    if m<=n:
        if w[n-m:]==s:
            return True
    return False

def has_factor(w,s):
    prefix=""
    for a in w:
        prefix+=a
        if has_suffix(prefix,s):
            return True
    return False

def forbidden_factor_check(w,n,BadPeriod,BadTop,BadBottom,Prefixes=[""],Suffixes=[""],quiet=True):    
    # Performs a necessary check for the proof of Lemma 3.10
    
    if not quiet:
        print('--------------------')
        print(f'Let w={w}.')
    
    BadRep=power(BadPeriod,BadTop,BadBottom)
    
    if n > 0:
        for a in Prefixes:
            for b in Suffixes:
                word=a+w+b
                for i in range(n):
                    gword=apply(g,word)
                    taugword=apply(transducer,gword)
                    cetop,cebottom,cefactor=critical_exponent(taugword)
                    # print(cetop,cebottom,cefactor) # Uncomment to see the factor of exponent at least 16/7
                    if cetop*7<cebottom*16:
                        print(f'RED FLAG: The word tau(g(awb)), where w={w}, a={a}, b={b}, and n={i} has no factor of exponent at least 16/7.')
                        return False
                
                    word=apply(f_hat,word)
                    
                if not has_factor(word,BadRep):
                    print(f'RED FLAG: The word f^{n}(awb), where w={w}, a={a}, and b={b} does not contain the {BadTop}/{BadBottom}-power of {BadPeriod}.')
                    return False
        if not quiet:
            print(f'For all a in {Prefixes}, b in {Suffixes}, and n<={n-1}, the word tau(g(f^n(awb))) has a factor of exponent at least 16/7, and the word f^{n}(awb) contains the {BadTop}/{BadBottom}-power of p={BadPeriod}.')
    
    else:
        if not w==power(BadPeriod,BadTop,BadBottom):
            print(f'RED FLAG: The word w={w} is not equal to p^{BadTop}/{BadBottom}, where p={BadPeriod}.')
            return False
        if not quiet:
            print(f'Then we can write w=p^{BadTop}/{BadBottom}, where p={BadPeriod}.')
    
    if BadPeriod.count("2")%2==0:
        if not quiet:
            print(f'We check that p has an even number of 2s.')
    else:
        print(f'RED FLAG: The word p={BadPeriod} has an odd number of 2s.')
        return False

    if w in ["00","11","1010","0101"]:
        if not quiet:
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 7/3 for all n>={n}.')
    elif w==power("0222",17,4)+"1":
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3 p_4)^2 p_1, where p_1=20102, p_2=02020, p_3=10202, and p_4=20.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 16/7 for all n>={n}.')
    elif w=="220102201022":
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1=02020, p_2=102, and p_3=201.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(awb))) has a factor of exponent at least 7/3 for all n>={n}.')
    elif w==power("2101221012010",31,13):
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1=p_2=21012 and p_3=010.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.')
    elif w==power("022201",29,6):
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (q 1 q 1)^2 q, where q=02220.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.')
    elif w==power("0222010222",12,5):
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1=p_3=0222 and p_2=01.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.')
    elif w==power("0222022201",12,5):
        if not quiet:
            print(f'Further, we can write p^{BadTop}/{BadBottom} = (p_1 p_2 p_3)^2 p_1, where p_1=p_2=0222 and p_3=01.')
            print(f'It follows from Lemma 3.7 and Lemma 3.9 that tau(g(f^n(w))) has a factor of exponent at least 7/3 for all n>={n}.')
    else:
        if parikh_check(BadPeriod,BadTop-2*BadBottom,BadBottom):
            if not quiet:
                print(f'Further, we can write p^{BadTop}/{BadBottom} = p^2 q, where q={power(BadPeriod,BadTop-2*BadBottom,BadBottom)}.')
                print(f'We check that each entry in the Parikh vector of q is at least 2/7 of the corresponding entry in the Parikh vector of p.')
                print(f'Thus, we conclude that tau(g(f^n(awb))) has a factor of exponent at least 16/7 for all n>={n}.')
        else:
            print(f'RED FLAG: The Parikh check failed for {w}.')
            return False
    return True

def directed_edges_in_H():

    Edges=[]
    for i in range(8):
        Edges.append([])
        for j in range(8):
            w=f_hat("",i)+f_hat("",j)+"0"
            if poor_suffix(w)==None and all(has_factor(w,v)==False for v in F1.keys()):
                Edges[i].append(j)
    return Edges

def short_factor_check(w,claim,quiet):
    
    if claim=="3.18.1":
        image=apply(f_hat,"6"+w+"7")
        F=F2.keys()
    
    elif claim=="3.18.2":
        image=apply(f_hat,apply(phi,w+"0"))
        F=F2.keys()
    
    elif claim=="3.19":
        image="21"+apply(f_hat,w)+"012"
        F=F3.keys()
    
    elif claim=="3.20.1":
        image=apply(f_hat,w)
        F=F4.keys()

    elif claim=="3.20.2":
        image=apply(f_hat,apply(psi,w))
        if w=="3":
            image="22"+image+"01022"
        elif w=="21":
            image=image+"010222"
        else:
            image="0222"+image+"0102220"
        F=F4.keys()
        
    for v in F:
        if has_factor(image,v):
            if not quiet:
                
                if claim=="3.18.1":
                    print(f'When u={w}, the image of 6u7 under f_hat contains the forbidden factor {v} in F_2.')
                
                elif claim=="3.18.2":
                    print(f'When w={w}, the image of w0 under f_hat compose phi contains the forbidden factor {v} in F_2.')
                
                elif claim=="3.19":
                    print(f'When w={w}, the (slightly extended) image of w under f_hat contains the forbidden factor {v} in F_3.')
                
                elif claim=="3.20.1":
                    print(f'When w={w}, the image of w under f_hat contains the forbidden factor {v} in F_4.')
                
                elif claim=="3.20.2":
                    print(f'When w={w}, the (slightly extended) image of w under f_hat compose psi contains the forbidden factor {v} in F_4.')
            
            return True
    
    return False