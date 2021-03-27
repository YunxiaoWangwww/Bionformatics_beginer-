#forward strand (5' -> 3') #G-#C increases/positive, reverse strand (3' -> 5') #G-#C decreases/negative -> the position where #G-#C decreases and the increases reveals the replication origin
#At position i of Genome, if we encounter an A or a T, we set Skew[i+1] equal to Skew[i]; if we encounter a G, we set Skew[i+1] equal to Skew[i]+1; if we encounter a C, we set Skew[i+1] equal to Skew[i]-1
import matplotlib.pyplot as plt
file_name = input("Enter your genome txt file name: ")
file = open(file_name, "r")
file_copy = file.read()
def SkewArray(Genome):
    Skew = [None]*(len(Genome)+1)
    Skew[0] = int(0)
    for i in range(len(Genome)):
        if Genome[i] == "G":
            Skew[i+1] = Skew[i] + int(1)                  
        elif Genome[i] == "C":
            Skew[i+1] = Skew[i] - int(1)
        elif Genome[i] == "A" or Genome[i] == "T":
            Skew[i+1] = Skew[i]
    return Skew
result = SkewArray(file_copy)
min_GC = min(result)
summary = []
for i in range(len(result)):
    if result[i] == min_GC:
        summary.append(i)
print(f"{summary}")
plt.plot(result[:])
plt.xlabel('genome position')
plt.ylabel('GC skew')
plt.title('GC skew for Vibrio_cholerae')
plt.show()        
