#this is a summary for all of the techniques used when finding a replication origin within a genome
#each section code can be found individually in the same test.code folder
#k is k-mer, L is window length for finding the clump, t is the frequency of the k-mer within the window length of a genome
#the output text file will in the format of total number of sequences above the frequency threshold 
#followed by a dictionary including all the elements in the format of the sequence:frequency:start position of the window

file_name = input("Enter your genome txt file name: ")
file = open(file_name, "r")
file_copy = file.read()

def FrequencyMap(Text, k):
    freq = {}
    n = len(Text)
    for i in range(n-k+1):
        pattern = Text[i:i+k]
        if pattern in freq:
            freq[pattern] += 1 
        elif pattern not in freq:
            freq[pattern] = 1  
    return freq
def ClumpFinder(k,L,t):
    clump = {}
    for i in range(len(file_copy)-L+1):
        freq = FrequencyMap(file_copy[i:i+L],k)
        for key in freq:
            if freq[key] >= t:
                clump[key] = [freq[key],i]
    return clump 

clump = ClumpFinder(9,500,3)
length = len(clump)
f = open("replication_origin_Vibrio_cholerae.txt","a")
f.write(str(length))
f.write(str(clump))
f.close()
