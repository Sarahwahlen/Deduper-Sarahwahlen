#!/bin/bash

#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 8
#SBATCH --constraint=turin                # puts me on the new nodes and kicks off non-bgmp 😈
#SBATCH --job-name=Deduper             # optional: job name
#SBATCH --output=slurm_out/deduper_slurm.%j.out

dir="/projects/bgmp/swahlen/bioinfo/Bi624/deduper/Deduper-Sarahwahlen"
in="$dir/C1_SE_uniqAlign.sorted.sam"
out="$dir/C1_SE_deduped.sorted.sam"
umi="$dir/STL96.txt"



/usr/bin/time -v python3 "$dir/SW_Deduper.py" -f $in -o $out -u $umi 