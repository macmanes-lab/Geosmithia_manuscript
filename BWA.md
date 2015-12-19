### BWA 

### Index the *G. morbida* genome assembly

```
bwa index g.morbida.scaffolds.fasta
```

### Map paired-end reads to the indexed genome

```
bwa mem g.morbida.scaffolds.fasta \
g.morbida_pe_R1.fastq g.morbida_pe_R2.fastq > g.morbida.pe.sam 
```

### Sort PE sam file

```
samtools sort g.morbida.pe.sam g.morbida.pe.sorted
```

### Find mapping metrics
```
samtools flagstat g.morbida.pe.sorted.bam
```
### Map mate-pair reads to the indexed genome

```
bwa mem g.morbida.scaffolds.fasta \
g.morbida_mp_R1.fastq g.morbida_mp_R2.fastq > g.morbida.mp.sam 

```
### Sort MP sam file

```
samtools sort g.morbida.mp.sam g.morbida.mp.sorted
```

### Find mapping metrics
```
samtools flagstat g.morbida.mp.sorted.bam
```