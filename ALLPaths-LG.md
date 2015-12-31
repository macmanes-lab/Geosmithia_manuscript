### ALLPaths-LG (v49414)
##### NOTE: add `.fastq` to the PE reads if that extension is not present


#### create a csv file called in_groups.csv

```
file_name, library_name, group_name
~/g.morbida_corrk21_trimphred2_*P.fastq, L1, frags1
~/g.morbida_ABC_mp_nxtclp_R*.fastq, L2, jump2
```

#### create a csv file called in_libs.csv
```
library_name, project_name, organism_name, type, paired, frag_size, frag_stddev, insert_size, insert_stddev, read_orientation, genomic_start, genomic_end
L1, g.morbida_ref_genome, geosmithia, fragment, 1, 300, 50, , , inward, 0, 0
L2, g.morbida_ref_genome, geosmithia, jump, 1, , , 3000, 500, outward, 0, 0
```

#### Run the Preparation script

```
./PrepareAllPathsInputs.pl \
DATA_DIR= ~/ \
GENOME_SIZE=26000000 OVERWRITE=True PLOIDY=1 \
HOSTS=36 \
JAVA_MEM_GB=200
```
#### Create the following directories and move files from the preparation step
```
mkdir g.morbida 
cd g.morbida
mkdir AllpathsPreparedInputs
cd ~/
mv frag* ~/g.morbida/AllpathsPreparedInputs
mv jump* ~/g.morbida/AllpathsPreparedInputs
mv ploidy ~/g.morbida/AllpathsPreparedInputs
cd ~/g.morbida/AllpathsPreparedInputs
```
#### Run the assembly pipeline in `~/g.morbida/AllpathsPreparedInputs`

```
RunAllPathsLG THREADS=24 FIX_ASSEMBLY_BASE_ERRORS=TRUE \
PRE= ~/ \
DATA_SUBDIR=AllpathsPreparedInputs \
RUN=geosmithia MAXPAR=2 \
REFERENCE_NAME=g.morbida \
TARGETS=standard OVERWRITE=True \
CONNECT_SCAFFOLDS=TRUE HAPLOIDIFY=TRUE
```

#### For a short summary of length-based stats

```
cd ~/g.morbida/AllpathsPreparedInputs/geosmithia/ASSEMBLIES/test
abyss-fac linear_scaffolds0.clean.remodel.applied.connected.tag.assembly.fasta
```




























