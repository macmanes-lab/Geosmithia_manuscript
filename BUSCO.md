### BUSCO (v1.1b1)

### Running BUSCO for genome assembly file
```
python3 BUSCO_v1.1b1.py -o g.morbida.busco \
-l /fungi -f -g g.morbida.scaffolds.fasta -c 10
```

### Running BUSCO for transcripts file
```
python3 BUSCO_v1.1b1.py -o g.morbida.transcripts.busco \
-l /fungi -f -g g.morbida.transcripts.fasta -c 10
```