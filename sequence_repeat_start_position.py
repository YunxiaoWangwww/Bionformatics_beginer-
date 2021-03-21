#this code determines the start positions within a genome where the k-mer occurs
#k-mer is a pattern that will be repeated in the genomer, which may represent the origin of the replication
def PatternMatching(Pattern,Genome):
    positions = []
    for i in range(len(Genome)-len(Pattern)+1):
        if Genome[i:i+len(Pattern)] == Pattern:
            positions.append(i)
    return positions
print(PatternMatching("CTTGATCAT","GATATATGCATATACTT"))
 










