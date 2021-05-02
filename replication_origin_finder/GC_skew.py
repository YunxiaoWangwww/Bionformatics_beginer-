#this code allows to find the origin of bacteria using GC skew
#the origin is where #C decreases and suddenly increases again
#forward strand (5’ -> 3’) experiences non-continuous replication -> spend time on waiting for the primer to be placed, so the forward strand has more time being single stranded -> more mutations than what reverse strand experienced (C -> T deamination -> T-A pairing with the new strand so the newly synthesized reverses strand (3’ -> 5’) will lack G) 
#reverse strand (3’ -> 5’) experiences continuous replication, spending more time on double stranded -> compared to the forward string (5’ -> 3’), it has more C -> the newly synthesized forward string according to this reverse strand will encounter with less mutations too, so it has more G than the newly synthesized reverse strand (3’ -> 5’) 
#while G is reduced in the reverse strand and C is reduced in the forward strand, A-T does not change that much because they are unfavoured by the natural selection 
import matplotlib.pyplot as plt
file_name = input("Enter your genome txt file name: ")
file = open(file_name, "r")
file_copy = file.read()
def SymbolArray(Genome, symbol):
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n//2]
    array[0] = PatternCount(symbol,Genome[0:n//2])
    for i in range(1, n):
        array[i] = array[i-1]
        if ExtendedGenome[i-1] == symbol:
            array[i] = array[i]-1
        if ExtendedGenome[i+(n//2)-1] == symbol:
            array[i]= array[i]+1
    return array

def PatternCount(Pattern,Text):
    count = 0
    for i in range(len(Text)-len(Pattern)+1):
        if Text[i:i+len(Pattern)] == Pattern:
            count = count+1
    return count 
result = SymbolArray(file_copy, "C")
plt.plot(*zip(*sorted(result.items())))
plt.title('C Skew for Virbio cholerae')
plt.ylabel("C frequency")
plt.xlabel("genome position")
plt.show()
f = open("C_count_Vibrio_cholerae.txt","w")
f.write(str(result))
f.close()
