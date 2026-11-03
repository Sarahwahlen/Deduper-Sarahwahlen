#!/usr/bin/env python

import argparse
import gzip
import re

def get_args():
	parser = argparse.ArgumentParser(description="setting global variables for deduper")
	parser.add_argument("-f", "--file", help="designates absolute file path to SORTED sam file", type=str)
	parser.add_argument("-o", "--outfile", help="designates absolute file path to sorted sam file", type=str)
	parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", type=str) 
	#parser.add_argument("-c", help="outputs a count file", type=str, required= False )
	return parser.parse_args()
args = get_args()
#print(f'the input file is {args.file},the output file is {args.outfile}, the list of known umis is {args.umi}')

indexes = args.umi
#indexes = "/projects/bgmp/swahlen/bioinfo/Bi624/deduper/Deduper-Sarahwahlen/STL96.txt"


# Create a seachable set for the known barcodes to refrence back to for each read
barcode_set= set()

with open (indexes,"r") as fh: 
    for line in fh: 
        umi = line.strip()
        barcode_set.add(umi)
#print(barcode_set)



#start counts for comparisons and analysis 
header = 0
count = 0 
incorrect_umi = 0
unmapped = 0 
duplicate_count = 0 
kept_reads = 0 




def open_reads(path):
     '''A all in one file opener to simplify opening statments regardless of zipped status'''
     if str(path).endswith(".gz"): 
          opener, mode = gzip.open, "rt"
     else: 
          opener, mode = (open, "r")
     return opener(path, mode)


def five_prime_start (curr_pos , cigar, strand): 
     '''This function considers strandedness and soft clipping and re-adjust start positions when necessary'''
     cigar_parts = re.findall(r'([0-9]+)([A-Z=])', cigar) #splits up the cigar and connects the letter to the value in a tuple, returns a list of tuples
     #print(cigar_parts)
     if strand == '+': 
          adj_start = curr_pos #default, no soft clipping
          if "S" in cigar_parts[0]: # 5' on the left most position
               anewstart= int(cigar_parts[0][0])
               adj_start  = curr_pos - anewstart
          return adj_start
     else: #strand is negative 
          adj_start = curr_pos -1 #default, no soft clipping
          for (number,letter) in cigar_parts: 
               if letter in "MDN": #find right most position (5' start site) by adding all of the values in the cigar string
                    adj_start = adj_start + int(number)

          if "S" in cigar_parts[-1]: # 5' on the right most postion check the last value in the list 
               #have to find the lenght to add 
               anewstart = int(cigar_parts[-1][0])
               adj_start = adj_start + anewstart
          return adj_start


with (
    open(args.outfile, "w") as out_file, 
    open_reads(args.file)as in_file ):
     seen = set ()
     chrom = None
     chrom_unique = 0
     chrom_dupes = 0

     for line in in_file:
          if line.startswith("@"):
               header += 1
               out_file.write(line) 
               continue
               #save the headers so the output is a correctly formatted SAM file
          
          count +=1 #every read matters 
          feilds = line.strip().split() 
          qname = feilds[0]
          curr_umi = qname.split(":")[-1]
          flag = int(feilds[1])
          curr_chrom = feilds[2]
          curr_pos = int(feilds[3])
          cigar = str(feilds[5])

#check mapped - not necessary for assignment but included in my test files 
          if ((flag & 4)==4): 
                 unmapped +=1 
                 continue
          if str(curr_umi) not in barcode_set : 
               incorrect_umi +=1 
               continue

     #check for stranded-ness 
          strand = 0 
          if ((flag & 16) == 16): 
               strand = "-"
          else: 
               strand = "+"
          ## update start position ## 
          adj_start = five_prime_start(curr_pos, cigar, strand)
          #print(strand, adj_start)

     #File is sorted by position and therefore chromosome, update chromosome, update key 
          if chrom != curr_chrom: 
               seen = set() #empty seen and start over
               if chrom is None: print(f"Chrom_name \t Count")
               if chrom is not None: print(f"{chrom}\t{chrom_unique}\n")
               chrom = curr_chrom
               chrom_unique = 0
          #ordered tuple to check seen set 
          key = (curr_chrom, strand, adj_start, curr_umi )
          if key in seen: 
               duplicate_count +=1  
               continue
          seen.add(key)
          out_file.write(line)
          kept_reads += 1 
          chrom_unique +=1
                
print(f"header lines: {header}\n" f"total reads: {count}\n" f"unmapped reads: {unmapped}\n" f"incorrect UMI reads: {incorrect_umi}\n" f"duplicate reads removed: {duplicate_count}\n" f"unique reads kept: {kept_reads}\n")

