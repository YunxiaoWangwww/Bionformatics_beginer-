#To rescale a collection of probabilities (the sides of the die) so that these probabilities sum to 1, we will write a function called Normalize(Probabilities). This function takes a dictionary Probabilities whose keys are k-mers and whose values are the probabilities of these k-mers (which do not necessarily sum to 1). The function should divide each value in Probabilities by the sum of all values in  Probabilities, then return the resulting dictionary.
def Normalize(Probabilities):
    Nomralized_probabilities = {}
    sum_probabilities = sum(Probabilities.values())
    for kmer in Probabilities:
        Nomralized_probabilities[kmer] = Probabilities[kmer]/sum_probabilities
    return Nomralized_probabilities

#To simulate rolling a die so that "ccgG" has probability 4/80, "cgGC" has probability 8/80, and so on. We will do so by generating a random number p between 0 and 1. If p is between 0 and 4/80, then it corresponds to "ccgG". If p is between 4/80 and 4/80 + 8/80, then it corresponds to "cgGC", etc.
#This is a cumulative way, as 4/80 < 8/80, cgGC is biased (there is more chance for a random number to lie in a bigger fraction (4/80+8/80 – 4/80) than a smaller fraction (4/80 – 0)
def WeightedDie(Probabilities):
    import random
    random_probabilities = random.uniform(0,1)
    p = 0
    for sequence in Probabilities:
        if p <= random_probabilities <= (Probabilities[sequence]+p):
            return sequence
        else:
            p += Probabilities[sequence]
    
#random.choices will throw the biased die according to the weights of the listed elements (Probabilities.keys() in this case)
def WeightedDie_simple(Probabilities):
    import random
    random_motif = random.choices(list(Probabilities.keys()), weights = list(Probabilities.values()),k = 1)
    return random_motif

#Gibbs sampling, rolling the dice according to the weights of the k-mer 
def Pr(Text,Profile):
    p = 1
    for i in range(len(Text)):
        p = Profile[Text[i]][i]*p 
    return p
def ProfileGeneratedString(Text,profile,k):
    n = len(Text)
    probabilities = {}
    for i in range(0,n-k+1):
        probabilities[Text[i:i+k]] = Pr(Text[i:i+k],profile)
    probabilities = Normalize(probabilities)
    return WeightedDie(probabilities)

#generate a random motif combinations for calculating the random profile frequency
import random
def RandomMotifs(Dna, k, t):
    Dna_length = len(Dna[0])
    random_motif = []
    for i in range(t):
        random_index = random.randint(0,Dna_length - k)
        random_motif.append(Dna[i][random_index:random_index+k])
    return random_motif
#Gibbs sampling -> k is k-mer, t is length of Dna or how many strings in the Dna array, N is how many times this iteration will repeat
def GibbsSampler(Dna,k,t,N):
    Motifs = RandomMotifs(Dna,k,t)
    BestMotifs = Motifs
    for j in range(1,N):
        i = random.randint(0,t-1)
        del Motifs[i]
        profiles = Profile(Motifs)
        Motifs.insert(i, ProfileGeneratedString(Dna[i], profiles,k))
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs
    

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

def Score(Motifs):
    score = 0
    consensus = Consensus(Motifs)
    for j in range(len(consensus)):
        for k in range(len(Motifs)):
            if consensus[j] != Motifs[k][j]:
                score += 1
    return score

Dna = []
with open("TB_DosR.txt", 'r') as f:
    for line in f:
        Dna.append(line[0:len(line)-1]) #the last position in each line is /n and we want to exclude it by minus 1
f.close()
print(Score(GibbsSampler(Dna,15,10,100)))
