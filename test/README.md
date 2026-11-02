`test_dups.sam` contains 8 reads:
 
| Read | Expected result |
|---|---|
| chr 2, forward, `71M` | kept |
| chr 2, same position and UMI | duplicate |
| chr 2, UMI containing an `N` | bad UMI |
| chr 2, `3S68M` at pos +3 | duplicate (soft clip correction) |
| chr 14, reverse, `71M` | kept |
| chr 14, same position and UMI | duplicate |
| chr 14, same position and UMI soft clip changes 5' position `71M5S`| kept |
| chr 14, reverse, `68M3S` | duplicate (trailing soft clip correction) |
| unmapped (flag 4) | skipped |
| chr 18, forward, 71M, unique umi | kept |
| chr 18, same position different umi, more complex cigar | kept| 
 
Expected counts: **total 11, bad UMI 1, unmapped 1, duplicates 4, 1 changed start site, 2 only differ in umis, kept 5.**