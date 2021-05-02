import colorama
def colored(seq):
    """colour the amino acid"""
    bcolors = {
        'A': '\033[32m',
        'C': '\033[34m',
        'G': '\033[33m',
        'T': '\033[31m',
        'U': '\033[31m',
        'reset': '\033[0m'
    }
    tmpStr = ""
    for nuc in seq:
        if nuc in bcolors:
            tmpStr += bcolors[nuc] + nuc
        else:
            tmpStr += bcolors['reset'] + nuc
    return tmpStr + '\033[0m'
def readTextFile(filePath):
    with open(filePath,'r') as f:
        return "".join([l.strip() for l in f.readlines()]) #strip removes any blank spaces on either side of a string -> put every line in the file into a list and concatenate all the elements within that list
def writeTextFile(filePath, seq, mode = 'w'):
    with open(filePath, mode) as f:
        f.write(seq + '\n')
def read_FASTA(filePath):
    with open(filePath, 'r') as f:
        FASTAFile = [l.strip() for l in f.readlines()]
    FASTADict = {}
    FASTALabel = ""
    for line in FASTAFile:
        if '>' in line:
            FASTALabel = line
            FASTADict[FASTALabel] = ""
        else:
            FASTADict[FASTALabel] += line
    return FASTADict
