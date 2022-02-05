import subprocess
import os
import matplotlib.pyplot as plt
from Bio import SeqIO

cmd = [
    "abyss",
    "-k",
    str(96),
    "-o",
    "_abyss_screen_out.fa",
    #two input files
    os.path.join("paired_dat1.fq"),
    os.path.join("paired_dat2.fq")
]
proc = subprocess.Popen(cmd)
proc.communicate()

# Make an empty list to contain contig lengths
lengths = []
max_contig_len = 0
max_contig_seq = ''
#find the longest contig
max_conting_len = 0
for record in SeqIO.parse("_abyss_screen_out.fa", "fasta"):
    lengths.append(len(record.seq))
    if lengths[-1] > max_contig_len:
        max_contig_len = lengths[-1]
        max_contig_seq = record.seq 
        max_contig_id = record.name
print(max_contig_id, max_contig_len)
plt.hist(lengths)
plt.xlabel('contig length')
plt.ylabel('frequency')
plt.show()
print(max(set(lengths), key=lengths.count))