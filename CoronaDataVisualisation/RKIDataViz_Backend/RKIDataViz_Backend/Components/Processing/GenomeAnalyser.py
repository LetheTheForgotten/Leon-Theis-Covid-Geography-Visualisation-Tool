import itertools
import subprocess
import numpy as np

from Bio import Align
from Bio import AlignIO

from ..Enviroment_Variables import enviroment as env


"""functions for genomic analysis"""

# preforms pairwise sequence alignment on given sequences
def two_sequence_alignment(ids, sequences, matchScore, mistmatchPenalty, gapPenalty, extensionPenalty):
    seq1 = sequences[0]
    seq2 = sequences[1]
    
    # exception raised if penalties are not numbers
    if not isinstance(matchScore, int) or not isinstance(gapPenalty, int) or not isinstance(extensionPenalty, int) or not isinstance(mistmatchPenalty, int):
        raise ValueError("match scores must be integers")
    
    # exception raised if penalties are positive
    if gapPenalty > 0 or extensionPenalty > 0:
        raise ValueError("penalty scores must be negative or zero")
    
    # exception raised if match score is not positive
    if matchScore <= 0:
        raise ValueError("match score must be positive")
    
    # exception raised if sequence are not strings
    if not isinstance(seq1,str) or not isinstance(seq2,str):
        raise ValueError("sequences must be handed over as string")
    
    # set values of alignment solver
    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.mismatch_score = mistmatchPenalty
    aligner.match_score = matchScore
    if(mistmatchPenalty!=0):
        aligner.open_gap_score = gapPenalty
        aligner.extend_gap_score = extensionPenalty
    else:
        aligner.gap_score = gapPenalty
    #print(gapPenalty)
    #print(aligner.algorithm)
    
    # solve
    align = aligner.align(seq1,seq2)
    #print(align[0])
    
    result = []
    
    # must be returned as a string 
    result.append("target: " + ids[0] + "\n" 
                  + "query: " + ids[1] + " \n" 
                  + "Score: " + str(align[0].score)
                  )
    
    result.append("Alignment: \n" + str(align[0]))
    
    # formats aligned indexes matrix properly
    alignedIndexes=np.array_str(align[0].aligned)
    alignedIndexes= '\t\t' + alignedIndexes.replace('\n','\n\t\t') + '\n'

    result.append({"score" : align[0].score, "aligned indexes" : alignedIndexes})

    return result

# preforms pairwise sequence alignment on given sequences
def pairwise_sequence_alignment_multiple(SeqList, matchScore, mismatchPenalty, gapPenalty, extensionPenalty, idList):
    finalSeqList = []
    
    SeqMatchedToIdList = []
    for i in range(0,len(SeqList)):
        SeqMatchedToIdList.append([SeqList[i], idList[i]])
        
    for p in itertools.combinations(SeqMatchedToIdList, 2):
        finalSeqList.append(
            two_sequence_alignment( 
                [p[0][1], p[1][1]], [p[0][0], p[1][0]], 
                matchScore, 
                mismatchPenalty, 
                gapPenalty, 
                extensionPenalty
            )
        )
    
    return finalSeqList
    
# preforms MSA using muscle CLI
def multiple_sequence_alignment(muscle_path_in, timeout, stdoutList):
    # muscle command line format:
    # file path of exe
    # -in
    # file path of first fasta file
    # -out
    # file path of output file
    
    if(timeout>=0):
        muscle_command_line = (r"" + env.MUSCLE_EXE + 
                               " -in " + muscle_path_in + 
                               " -out " + env.MUSCLE_OUT_FILE_PATH + 
                               " -maxiters 2 -diags"
                               )
    else:
        muscle_command_line=(r"" + env.MUSCLE_EXE + 
                             " -in " + muscle_path_in + 
                             " -out " + env.MUSCLE_OUT_FILE_PATH + 
                             " -maxhours " + timeout + 
                             " -maxiters 2 -diags"
                             )
    
    stdoutList.append("running on CMD: \n")
    stdoutList.append(muscle_command_line + "\n")
    
    stdoutList.append("MUSCLE Parsing Started... \n")

    with subprocess.Popen(muscle_command_line,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE,
                          shell = True,
                          bufsize = 1,
                          universal_newlines = True) as p:
        while True:
            line = p.stderr.readline()
            if line == "" and (p.poll() is not None):
                break

            stdoutList.append(line + "")
    if (p.returncode != 0):
        stdoutList.append("MUSCLE Parsing Finished... \n")
        stdoutList.append("Generating MSA Graph...\n")
        return None
    
    return True

# returns indexes of gaps in given MSA fasta file
def find_gap_indexes():
        
        Sequences = AlignIO.read(env.MUSCLE_OUT_FILE_PATH, "fasta")
        
        # every sequence row gets its own list - making this a plotly table
        MSAdata = []
        gapindexes = []
        names = []
        
        inc = 0
        for i in Sequences:
            names.append(i.id)
            MSAdata.append([])
            for j in i.seq:
                MSAdata[inc].append(j)
            inc += 1
        # save every index +- 8 , then preform merge operation to get list of indexes
        for i in range(0,len(MSAdata[0])):
             for j in range(0,len(MSAdata)):
                 if(MSAdata[j][i] == "-"):
                     if(i <= 7):
                         gapindexes.append((i, i + 8))
                     if(i >= len(MSAdata[0])):
                         gapindexes.append((i - 8, i))
                     else:
                         gapindexes.append((i - 8, i + 8))

        mergedIndexes = []
        for i in sorted(gapindexes):
            mergedIndexes = mergedIndexes or [i]
            if i[0] > mergedIndexes[-1][1]:
                mergedIndexes.append(i)
            else:
                old = mergedIndexes[-1]
                mergedIndexes[-1] = (old[0], max(old[1], i[1]))
        return mergedIndexes
                     