#generate a random motif combinations for calculating the random profile frequency -> use this random motif as a start to generate a random profile -> use this random profile to find motifs in each string of the Dna -> repeat this process until the Score of the motifs is no longer improving 
#However, the probability extracted from the randomly chosen k-mers, is not uniform (i.e., is not 0.25 for each nucleotide), but biased towards the implanted k-mer. Thus, when iterating loops, the found k-mers will be closer to the regulatory regions wanted to be found (but it is not very acurate)

#generate a random motif combinations for calculating the random profile frequency
import random
def RandomMotifs(Dna, k, t):
    Dna_length = len(Dna[0])
    random_motif = []
    for i in range(t):
        random_index = random.randint(0,Dna_length - k)
        random_motif.append(Dna[i][random_index:random_index+k])
    return random_motif

#output the k-mer in each string of the Dna based on the Profile generated randomly
def Motifs(Profile, Dna):
    motifs = []
    k = len(Profile['A'])
    for i in range(len(Dna)):
        motifs.append(ProfileMostProbableKmer(Dna[i],k,Profile))
    return motifs

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

def ProfileMostProbableKmer(text, k, profile):
    pr = {}
    for i in range(len(text)-k+1):
        sequence = text[i:i+k]
        pr[i] = Pr(sequence,profile)
    indice = max(pr, key=pr.get)
    output = text[indice:indice+k]
    return output    

def Score(Motifs):
    score = 0
    consensus = Consensus(Motifs)
    for j in range(len(consensus)):
        for k in range(len(Motifs)):
            if consensus[j] != Motifs[k][j]:
                score += 1
    return score
#iterate this profile finds k-mer and k-mer used to generate profile until the score of k-mer is no longer improved by this algorithm, starting from a random motif collection/random profile
def RandomizedMotifSearch(Dna,k,t):
    M = RandomMotifs(Dna,k,t)
    BestMotifs = M
    N = 0
    while True:
        profile = Profile(BestMotifs)
        M = Motifs(profile,Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
            N += 1
        else:
            return BestMotifs, N+1

print(RandomizedMotifSearch(["GGCGTTCAGGCA","AAGAATCAGTCA","CAAGGAGTTCGC","CACGTCAATCAC","CAATAATATTCG"],3,5))



