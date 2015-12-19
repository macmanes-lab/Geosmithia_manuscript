### SGA preqc (v0.10.13)
```
sga preprocess \
--pe-mode 1 g.morbida_pe_R1.fastq g.morbida_pe_R2.fastq > g.morbida.fastq
sga index -a ropebwt --no-reverse -t 8 g.morbida.fastq
sga preqc -t 8 g.morbida.fastq > g.morbida.preqc
sga-preqc-report.py g.morbida.preqc sga/src/examples/preqc/*.preqc
```
