### HMMER (version 3.1b2)

#### hmmpress pfam database (v28.0)

```
hmmpress Pfam-A.hmm
```

#### hmmscan for *G. morbida* 
```
hmmscan \
--domtblout gm5_new.pfam \
--cpu 8 Pfam-A.hmm g.morbida.proteins.fasta
```

#### hmmscan for effector proteins. The effector proteins file is provided with the github repo
```
hmmscan --domtblout effector_prots.pfam --cpu 8 Pfam-A.hmm effector_prots.fasta
```
