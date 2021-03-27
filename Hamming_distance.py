#count the mismatch bewteen two strings of the same length
def Hamming_Distance (p,q):
    count = 0
    i = 0
    if len(p) == len(q):
        while i < len(p):
            if p[i] != q[i]:
                count = count + 1
            i = i+1
    else:
        print("two strings do not have the same length")
    return count
result = Hamming_Distance("TGACCCGTTATGCTCGAGTTCGGTCAGAGCGTCATTGCGAGTAGTCGTTTGCTTTCTCAAACTCC","GAGCGATTAAGCGTGACAGCCCCAGGGAACCCACAAAACGTGATCGCAGTCCATCCGATCATACA")
print(f"{result}")
def ApproximatePatternMatching(Pattern,Text, d):
    positions = []
    occurance = 0
    for i in range(len(Text)-len(Pattern)+1):
        p = Text[i:i+len(Pattern)]
        counts = Hamming_Distance(p,Pattern)
        if counts <= d:
            positions.append(i)  
            occurance = occurance+1 
    return occurance, positions
results = ApproximatePatternMatching("GAGG","TTTAGAGCCTTCAGAGG",2)
print(f"{results}")
