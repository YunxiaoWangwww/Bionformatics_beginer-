#count for the profile, but this time each count will start from 1 instead of 0, becuase we know it can be this base before we count the profile (so probability should add 1 according to Laplace’s rule of succession)
def CountWithPseudocounts (Motifs):
    count = {}
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
             count[symbol].append(1)
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1 
    return count

def Profile(Motifs):
    profile = CountWithPseudocounts(Motifs)
    t = len(Motifs)
    k = len(Motifs[0])
    for symbol in profile:
        for i in range(k):
            profile[symbol][i] = profile[symbol][i]/(t+4)
    return profile

def Consensus(Motifs):
    k = len(Motifs[0])
    count = Profile(Motifs)
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if count[symbol][j] > m:
                m = count[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus

def Pr(Text,Profile):
    p = 1
    for i in range(len(Text)):
        p = Profile[Text[i]][i]*p 
    return p

def Score(Motifs):
    score = 0
    consensus = Consensus(Motifs)
    for j in range(len(consensus)):
        for k in range(len(Motifs)):
            if consensus[j] != Motifs[k][j]:
                score += 1
    return score

def ProfileMostProbableKmer(text, k, profile):
    pr = {}
    for i in range(len(text)-k+1):
        sequence = text[i:i+k]
        pr[i] = Pr(sequence,profile)
    indice = max(pr, key=pr.get)
    output = text[indice:indice+k]
    return output    

def GreedyMotifSearchWithPseudocounts(Dna,k,t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k])
    n = len(Dna[0])
    for m in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][m:m+k])
        for j in range(1, t):
            P = Profile(Motifs[0:j])
            Motifs.append(ProfileMostProbableKmer(Dna[j], k, P))
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs
Dna = []
with open("TB_DosR.txt", 'r') as f:
    for line in f:
        Dna.append(line[0:len(line)-1]) #the last position in each line is /n and we want to exclude it by minus 1
f.close()
results = GreedyMotifSearchWithPseudocounts(Dna,15,10)
