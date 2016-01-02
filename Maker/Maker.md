### Maker (version 2.31.8)
#### Required files:
1. Assembly file called ```g.morbida.scaffolds.fasta```.
2. ```makerPrep.py```. This script is provided in the github repo.
3. ***Fusarium solani*** (version v2.0.26) cdna and proteins files.
4. CEGMA generated ```gff``` output. This file is provided in the github repo. 
5. SNAP trained ```hmm``` output.   

#### A. Fix headers if final assembly is produced with ALLPaths-LG.
```
python3 makerPrep.py --fasta g.morbida.scaffolds.fasta \
--output g.morbida.scaffolds.fixed.fasta
```
```
mv g.morbida.scaffolds.fasta old.g.morbida.scaffolds.fasta
mv g.morbida.scaffolds.fixed.fasta g.morbida.scaffolds.fasta
```

#### B. Train SNAP with CEGMA generated ```gff``` output

```
mkdir snap_1
cd snap_1
/maker/bin/cegma2zff -n g.morbida.output.cegma.gff g.morbida.scaffolds.fasta
/snap/fathom -categorize 1000 genome.ann genome.dna
/snap/fathom -export 1000 -plus uni.ann uni.dna
/snap/forge export.ann export.dna
/snap/hmm-assembler.pl g.morbida . > ../g.morbida_1.hmm
cd ..
```
#### C. Generate control files
```
maker -CTL
```

#### D. Prepare ```maker_opts.ctl``` by changing the following lines in the file

```
#-----Genome (these are always required)
genome=~/g.morbida.scaffolds.fasta #genome sequence (fasta file or fasta embeded in GFF3 file)
.
.
.
#-----EST Evidence (for best results provide a file for at least one)
est= #set of ESTs or assembled mRNA-seq in fasta format
altest=~/Fusarium_solani.v2.0.26.cdna.all.fa #EST/cDNA sequence file in fasta format from an alternate organism
est_gff= #aligned ESTs or mRNA-seq from an external GFF3 file
altest_gff= #aligned ESTs from a closly relate species in GFF3 format

#-----Protein Homology Evidence (for best results provide a file for at least one)
protein=~/Fusarium_solani.v2.0.26.pep.all.fa #protein sequence file in fasta format (i.e. from mutiple oransisms)
protein_gff=  #aligned protein homology evidence from an external GFF3 file
.
.
.
#-----Gene Prediction
snaphmm=~/g.morbida_1.hmm #SNAP HMM file
gmhmm= #GeneMark HMM file
augustus_species=fusarium #Augustus gene prediction species model
fgenesh_par_file= #FGENESH parameter file
pred_gff= #ab-initio predictions from an external GFF3 file
model_gff= #annotated gene models from an external GFF3 file (annotation pass-through)
est2genome=1 #infer gene predictions directly from ESTs, 1 = yes, 0 = no
protein2genome=1 #infer predictions from protein homology, 1 = yes, 0 = no
trna=0 #find tRNAs with tRNAscan, 1 = yes, 0 = no
snoscan_rrna= #rRNA file to have Snoscan find snoRNAs
unmask=0 #also run ab-initio prediction programs on unmasked sequence, 1 = yes, 0 = no
.
.
.
#-----MAKER Behavior Options
max_dna_len=3000000 #length for dividing up contigs into chunks (increases/decreases memory usage)
min_contig=10000 #skip genome contigs below this length (under 10kb are often useless)
.
.
.
```

#### E. First Maker run (run1) in the same directory as the control files
```
maker
```

#### F. Train SNAP using Maker generated ```gff``` output 
```
maker/bin/fasta_merge -d g.morbida.scaffolds.maker.output/g.morbida.scaffolds_master_datastore_index.log
maker/bin/gff3_merge -d g.morbida.scaffolds.maker.output/g.morbida.scaffolds_master_datastore_index.log
cd ../
mkdir snap_2
cd snap_2
maker2zff ~/g.morbida.scaffolds.maker.output/g.morbida.scaffolds.all.gff
/snap/fathom -categorize 1000 genome.ann genome.dna
/snap/fathom -export 1000 -plus uni.ann uni.dna
/snap/forge export.ann export.dna
/snap/hmm-assembler.pl g.morbida.scaffolds . > ../g.morbida_2.hmm
cd ../
```
#### G. Copy the ```maker_opts.ctl``` to a different file and move ```g.morbida.scaffolds.maker.output``` to a different directory
```
scp maker_opts.ctl run1_maker_opts.ctl
mv g.morbida.scaffolds.maker.output run1_g.morbida.scaffolds.maker.output
```
#### H. Prepare ```maker_opts.ctl``` again by changing the following lines in the file. Note only one line is edited this time. 

```
.
.
.
#-----Gene Prediction
snaphmm=~/g.morbida_2.hmm #SNAP HMM file
gmhmm= #GeneMark HMM file
augustus_species=fusarium #Augustus gene prediction species model
fgenesh_par_file= #FGENESH parameter file
pred_gff= #ab-initio predictions from an external GFF3 file
model_gff= #annotated gene models from an external GFF3 file (annotation pass-through)
est2genome=1 #infer gene predictions directly from ESTs, 1 = yes, 0 = no
protein2genome=1 #infer predictions from protein homology, 1 = yes, 0 = no
trna=0 #find tRNAs with tRNAscan, 1 = yes, 0 = no
snoscan_rrna= #rRNA file to have Snoscan find snoRNAs
unmask=0 #also run ab-initio prediction programs on unmasked sequence, 1 = yes, 0 = no
.
.
.
```


#### I. Run Maker (run2) in the same directory as the control files
```
maker
```
#### J. Repeat F-I for a third Maker run and merge all the fastas and gffs one last time.

#### K. Convert structural fastas and gffs into functional files using a database of choice.

```
/maker/bin/maker_functional_fasta uniprot.sprot.fasta output.txt g.morbida.scaffolds.all.maker.transcripts.fasta > g.morbida.transcripts.fasta
```

```
/maker/bin/maker_functional_fasta uniprot.sprot.fasta output.txt g.morbida.scaffolds.all.maker.proteins.fasta > g.morbida.proteins.fasta
```
```
/maker/bin/maker_functional_gff uniprot.sprot.fasta output.txt g.morbida.scaffolds.all.gff > g.morbida.gff
```