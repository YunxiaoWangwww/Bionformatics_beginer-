from bio_struct import DNAtoProtein_table, NUCLEOTIDE_BASE, RNAtoProtein_table
import random
from collections import Counter
class bio_seq:
    """DNA sequence class or RNA sequence class, default value ATCG or AUCG, no label """
    def __init__(self, seq="ATCG", seq_type = "DNA", label = "No Label"):
        self.seq = seq.upper()
        self.label = label
        self.seq_type = seq_type
        self.is_valid = self.__validate_seq()
        assert self.is_valid, f"Provided data is not a correct {self.seq_type} sequence" #assert allows to print out an error message if the condition is not True
    def __validate_seq(self): #__ makes this function as a private function that will not be shown when calling the class in other files 
        """" to check whether the sequence is in the DNA nucleotide list, or ['A','T','C','G']"""
        return set(NUCLEOTIDE_BASE[self.seq_type]).issuperset(self.seq)
    def get_seq_biotype(self):
        """to return the type of input sequence"""
        return self.seq_type
    def get_seq_info(self):
        """to get all information including label, sequence, biotype and length of the input sequence"""
        return f"[Label]: {self.label}\n[Sequence]: {self.seq}\n[Biotype]: {self.seq_type}\n[Length]: {len(self.seq)} "
    def generate_rnd_seq(self, length = 10, seq_type = "DNA"):
        """to reintialize the sequence with a randomly generated sequence, default length is 10"""
        seq = ''.join([random.choice(NUCLEOTIDE_BASE[seq_type])
                        for x in range(length)])
        self.__init__(seq, seq_type,"Randomly generated sequence") #reinitialize the class with the randomly generated sequences 
    def nucleotide_frequency(self):
        """to return nucleotide frequency in a given sequence"""
        return dict(Counter(self.seq))
    def transcription(self):
        """conert a DNA sequence into a RNA sequence"""
        if self.seq_type == "DNA":
            return self.seq.replace("T", "U") #return a copy of string after transcription
        return "Not a DNA sequence"
    def reverse_complement(self):
        """output the reverse complement sequence of either a DNA or a RNA sequence"""
        if self.seq_type == "DNA":
            mapping = str.maketrans('ATCG','TAGC')
        elif self.seq_type == "RNA":
            mapping = str.maketrans('AUCG','UAGC')
        return self.seq.translate(mapping)[::-1]
    def gc_content(self):
        """output the gc percentage in a given DNA or RNA sequence"""
        return round((self.seq.count('C')+self.seq.count('G'))/len(self.seq)*100)
    def gc_count_subsec(self, k=20):
        """in a given window length (default is 20), output the gc content for each windown section of a given sequence"""
        res = []
        for i in range(0,len(self.seq)-k+1,k):
            subseq = self.seq[i:i+k]
            res.append(round((subseq.count('C')+subseq.count('G'))/len(subseq)*100))
        return res
    def translate_seq(self,init_pos = 0):
        """translation using a DNA or a RNA sequence"""
        if self.seq_type == "DNA":
            return ''.join([DNAtoProtein_table[self.seq[pos:pos+3]]for pos in range(init_pos,len(self.seq)-2,3)])
        elif self.seq_type == "RNA":
            return ''.join([RNAtoProtein_table[self.seq[pos:pos+3]]for pos in range(init_pos,len(self.seq)-2,3)])

    def codon_usage(self,aminoacid):
        """for a given amino acid, output the frequency of condon in a given input sequence coding for this amino acid"""
        tmpList = []
        if self.seq_type == "DNA":
            for i in range(0,len(self.seq)-2,3):
                if DNAtoProtein_table[self.seq[i:i+3]] == aminoacid:
                    tmpList.append(self.seq[i:i+3])
        elif self.seq_type == "RNA":
            for i in range(0,len(self.seq)-2,3):
                if RNAtoProtein_table[self.seq[i:i+3]] == aminoacid:
                    tmpList.append(self.seq[i:i+3])

        freqDict = dict(Counter(tmpList))
        totalWight = sum(freqDict.values())
        for seq in freqDict:
            freqDict[seq] = round(freqDict[seq]/totalWight,2)
        return freqDict 
    def gen_reading_frames(self):
        """generate all six possible ORF for a given sequence"""
        frames = []
        frames.append(self.translate_seq(0))
        frames.append(self.translate_seq(1))
        frames.append(self.translate_seq(2))
        tmp_seq = bio_seq(self.reverse_complement(), self.seq_type)
        frames.append(tmp_seq.translate_seq(0))
        frames.append(tmp_seq.translate_seq(1))
        frames.append(tmp_seq.translate_seq(2))
        del tmp_seq
        return frames
    #open reading frame from start codon to the stop codon -> to generate the real protein sequence
    def proteins_from_rf(self, aa_seq): #given the amino acid to find the ORF
        """return all the possible proteins from a given amino acid sequence"""
        current_prot = []
        proteins = []
        for aa in aa_seq:
            if aa == "_":
                if current_prot:
                    for p in current_prot:
                        proteins.append(p)
                    current_prot = []
            else:
                if aa == "M":
                    current_prot.append("") #ensure the list length is 1 when attaching the first M or the start codon into the list -> each time when it finds a M, it will create an empty list, and if there are two lists in the main list, both list will accumulate values in the same time
                for i in range(len(current_prot)):
                    current_prot[i] += aa #accumulating the list, since the list length is 1, the next amino acid will be added directly to the element in index 0 -> over time this list still contains one amino acid but the single element inside the list is accumulating
        return proteins
    def all_proteins_from_orfs(self, startReadPos = 0, endReadPos = 0, ordered = False):
        """output all the possible protein from all the possible six ORFs from a given sequence, protein should start from M and end with a stop condon_"""
        if endReadPos > startReadPos:
            tmp_seq = bio_seq(self.seq[startReadPos:endReadPos],self.seq_type)
            rfs = tmp_seq.gen_reading_frames()
        else:
            rfs = self.gen_reading_frames()
        res = []
        for rf in rfs:
            prots = self.proteins_from_rf(rf)
            for p in prots:
                res.append(p)
        if ordered:
            return sorted(res, key=len, reverse = True) #reverse makes sure the ordered list is from the longest to the shortest string
        return res
