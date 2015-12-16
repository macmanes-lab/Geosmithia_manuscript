#!/usr/bin/python3
# A program for trimming and error correcting raw MP and PE reads 
# USAGE: ./geosmithia_dataProcessing_TA.py 
# Author: Taruna Aggarwal
# Affiliation: University of New Hampshire, Durham, NH, USA
# Date: 11/10/2015
# Purpose is to trim and error correct raw reads (MP and PE)


import sys
import subprocess
import argparse



#  Set up input and output arguments
parser = argparse.ArgumentParser(description="This script generates a genome assembly with PE and MP reads as input files.")
parser.add_argument('PE_forward_fastq', help="Input PE forward fastq file")
parser.add_argument('PE_reverse_fastq', help="Input PE reverse fastq file")
parser.add_argument('MP_forward_fastq', help="Input MP forward fastq file")
parser.add_argument('MP_reverse_fastq', help="Input MP reverse fastq file")
args = parser.parse_args()

############################################# Mate-pair reads #############################################

#### Trimmed MP reads using Nextclip V1.3.1 ####

# nextclip -i /home/mcclintock/ta2007/scripts4Gen812/0_final_project/gm5_mp_R1_small.fastq \
#  -j /home/mcclintock/ta2007/scripts4Gen812/0_final_project/gm5_mp_R2_small.fastq \
#  -o /home/mcclintock/ta2007/scripts4Gen812/0_final_project/nextclip/gm5_mp_nxtclip -t 5 -e

# nextclip_logfile = open("nextclip_log.txt" , "w")

def runNextclip(MP_R1_file, MP_R2_file):
    nextclip_args = {}
    nextclip_args['read1'] = MP_R1_file
    nextclip_args['read2'] = MP_R2_file
    nextclip_command = "nextclip "
    nextclip_command += "-i /home/mcclintock/ta2007/scripts4Gen812/0_final_project/{read1} ".format(**nextclip_args)
    nextclip_command += "-j /home/mcclintock/ta2007/scripts4Gen812/0_final_project//{read2} ".format(**nextclip_args)
    nextclip_command += "-o /home/mcclintock/ta2007/scripts4Gen812/0_final_project/nextclip/gm5_mp_nxtclip -t 5 -e"
    # nextclip_output = subprocess.check_output(nextclip_command, stderr=subprocess.STDOUT)
    # nextclip_logfile.write(nextclip_output)
    subprocess.call(nextclip_command, shell=True)
    # print(nextclip_command)

############################################# Paired-end reads #############################################

#### error corrected using BLESS V:0.16 ####

# bless -read1 /fungi/taruna/shared/Geosmithia/raw_data/gm5_R1.fastq -read2 /fungi/taruna/shared/Geosmithia/raw_data/gm5_R2.fastq \
# -kmerlength 21 \
# -verify -notrim -prefix /fungi/taruna/geosmithia_old/bless_corr_data/gm5/gm5_bless_corr_k21

bless_logfile = open("bless_log.txt" , "w")
def runBless(PE_R1_file, PE_R2_file):
    bless_args = {}
    bless_args['read1'] = PE_R1_file
    bless_args['read2'] = PE_R2_file
    bless_command = "/home/mcclintock/ta2007/bin/bless/v0p17/bless -read1 {read1} -read2 {read2} -kmerlength 21 -verify -notrim -prefix gm5_bless_corr_k21".format(**bless_args)
    bless_output = subprocess.check_output(bless_command, stderr=subprocess.STDOUT)
    bless_logfile.write(bless_output)
    subprocess.call(bless_command, shell=True)
    # print(bless_command)


#### trimmed using Trimmomatic V0.32 ####

# java -jar /opt/Trimmomatic-0.32/trimmomatic-0.32.jar PE -threads 4 \
# -baseout gm5_k21corr_trim.Phred2 \
# /fungi/taruna/geosmithia_old/bless_corr_data/gm5/gm5_bless_corr_k21.1.corrected.fastq \
# /fungi/taruna/geosmithia_old/bless_corr_data/gm5/gm5_bless_corr_k21.2.corrected.fastq \
# ILLUMINACLIP:/opt/Trimmomatic-0.32/adapters/TruSeq3-PE-2.fa:2:30:10 \
# LEADING:2 TRAILING:2 SLIDINGWINDOW:4:2 MINLEN:30

def runTrim(R1_bless_corr_file, R2_bless_corr_file):
    trim_command = "java -jar /opt/Trimmomatic-0.32/trimmomatic-0.32.jar PE -threads 4 "
    trim_command += "-baseout gm5_k21corr_trim.Phred2 "
    trim_command += R1_bless_corr_file
    trim_command += R2_bless_corr_file
    trim_command += "ILLUMINACLIP:/opt/Trimmomatic-0.32/adapters/TruSeq3-PE-2.fa:2:30:10 "
    trim_command += "LEADING:2 TRAILING:2 SLIDINGWINDOW:4:2 MINLEN:30"
    subprocess.call(trim_command, shell=True)
    # print(trim_command)


#### Run the Preparation script ####

# /opt/allpathslg/bin/PrepareAllPathsInputs.pl \
# DATA_DIR=/fungi/taruna/Allpaths \
# GENOME_SIZE=26000000 OVERWRITE=True PLOIDY=1 \
# HOSTS=36 \
# JAVA_MEM_GB=200

# def allpathsPrep():
#     allpathsPrep_command = "perl /opt/allpathslg/bin/PrepareAllPathsInputs.pl "
#     allpathsPrep_command += "DATA_DIR=/home/mcclintock/ta2007/scripts4Gen812/0_final_project/allpaths "
#     allpathsPrep_command += "GENOME_SIZE=26000000 OVERWRITE=True PLOIDY=1 "
#     allpathsPrep_command += "HOSTS=36 "
#     allpathsPrep_command += "JAVA_MEM_GB=200"

#### Run the Assembly script ####

# def allpathsRun():
#     allpathsRun_command = "perl /opt/allpathslg/bin/RunAllPathsLG THREADS=24 FIX_ASSEMBLY_BASE_ERRORS=TRUE "
#     allpathsRun_command += "PRE=/home/mcclintock/ta2007/scripts4Gen812/0_final_project/ "
#     allpathsRun_command += "DATA_SUBDIR=Allpaths "

# Calling the functions
runNextclip(args.MP_forward_fastq, args.MP_reverse_fastq)

runBless(args.PE_forward_fastq, args.PE_reverse_fastq)

runTrim("gm5_bless_corr_k21.1.corrected.fastq ", "gm5_bless_corr_k21.2.corrected.fastq ")

# trim_output = subprocess.check_output(trim_command, stderr=subprocess.STDOUT)
# good_run = False
# for currentLine in trim_output:
#     if currentLine.startswith("TrimmomaticPE: Completed successfully"):
#         good_run = True
#         break
#     if not good_run:
#         sys.exit()




