#!/bin/bash

#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 8
#SBATCH --constraint=turin                # puts me on the new nodes and kicks off non-bgmp 😈
#SBATCH --job-name=sort_it             # optional: job name
#SBATCH --output=slurm_out/sort_slurm.%j.out

/usr/bin/time -v pixi run samtools sort -@ 16 /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam \
    -o /projects/bgmp/swahlen/bioinfo/Bi624/deduper/Deduper-Sarahwahlen/C1_SE_uniqAlign.sorted.sam