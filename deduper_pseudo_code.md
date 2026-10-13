deduper_pseudo_code
Bi624 


The problem: 
A PCR step is added to improve the yeild of cDNA libraries so that sequencing of the entire sample is possible. However this runs the risk of introducing PCR induced sequence variation as well as sequencing/recording dupilicate sequences. This can inflate sequencing read deapths and disproproationally represent read frequences when looking at transcription abunaces. To correct for this duplicates need to be removed from the data set after aligning to a genome. 

What is a duplicate? 
* same sequence (obiv)
* same chromosome 
* same starting posiont ^*
* same strand 
* Mate position (if paired)
* par orientation (if paired)
* same unique molecular identifier (UMI) or molecular bacode 

<small>^* must consider soft cliping when comparing starting positions </small>


## Functions: 

```py 
def smokenmirror (position, cigar, strand (+)): 
    ''' parses the sam file to find the cigar string, checks for soft clippings, adjusts start sites accordingly''' 
    clip = regex '(value)S' #check for soft clipping maybe raise a flag 
    if clip == true : 
        clip = false 
        return new start site = math (start site - int(soft clip num)) 
    else position 
```
input (50, 5S20M, +)
expected out: 45 
```py 
def rrorimnekoms (position, cigar, strand (-)): 
    ''' when strand is reverse compliment this function will do the math to place the start site at the rightmost postion '''
    len  = count SEQ field 
    if (check the last entry in the cigar string for soft clipping - perhaps with regex): 
        start = postion + lenght + soft clipping
    else: 
        start = postion + lenght 
```
input (50, 5M20S, -) (count is 30 ig)
expected out: 100 


## Pseudocode 
```
1) Use bash to sort the sam files 


2) Checking for correct UMIs and stranded-ness

known_umis = import UMIs 

## header 
for each line in input_sam: 
    If line starts with "@": 
        continue 
    else: 
    count += 1
    fields = line.strip .split 
    assign-- CURRENT:  qname, flag, chrom, pos, cigar, mate_pos 

    if ((flag & 4) == 4)  #unmapped 
        continue 
    
    #umi check 

    umi = regex for last item on qname 
    if umi not in known_umis 
        count_incorrect_umis +=1 
        continue 

    #strand check 
    if ((flag & 16) == 16)
        strand  = "-"
    else: 
        strand = "+"
    
    ####
    I want to use the function I wrote here but, hmmm. 
    I am confused on the best way tempoarily store reverse reads but maybe I wont worry about that! 
    ####

## check for soft clipping update start position 

    if strand == + 
        start = smokenmirror( )

## check for duplicates by creating an empty list 

    if chrom != current chrom : 
        seen = empty list 
        current chrom = chrom 

    key = list of chrom, strand, start, umi (maybe mate pos?)
    if key in seen: 
        dup_count +=1 
        continue 
    
    add key to seen 
    write line to output 
    kept_count += 1 
    
    



