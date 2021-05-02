#conseus string -> output one string
def Consensus(Motifs):
    k = len(Motifs['A'])
    consensus = ""
    for j in range(k):
        m = 0
        frequentSymbol = ""
        for symbol in "ACGT":
            if Motifs[symbol][j] > m:
                m = Motifs[symbol][j]
                frequentSymbol = symbol
        consensus += frequentSymbol
    return consensus
motif = {'A': [0.4,0.3,0.0,0.1,0.0,0.9],'C': [0.2,0.3,0.0,0.4,0.0,0.1],'G': [0.1,0.3,1.0,0.1,0.5,0.0],'T': [0.3,0.1,0.0,0.4,0.5,0.0]}
#conseus string -> output all possible consesus strings 
def Consensus_final(Motifs):
    bestseqs = [[]]
    n = len(Motifs['A'])
    d = {}
    for i in range(n):
        for symbol in "ACGT":
            d[symbol] = Motifs[symbol][i]
        m = max(d.values())
        l = []
        for symbol in "ACGT":
            if d[symbol] == m:
                l.append(symbol)
        bestseqs = [ s+[N] for s in bestseqs for N in l]
    for i in range(len(bestseqs)):
        bestseqs[i] = ''.join(bestseqs[i])
    return bestseqs
print(Consensus_final(motif))
