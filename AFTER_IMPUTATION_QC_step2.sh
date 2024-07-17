#!/bin/bash

# Define the merged VCF file
MERGED_VCF="merged_filtered.vcf"
FINAL_PREFIX="final_filtered"

# Count the number of SNPs in the merged VCF file
TOTAL_SNPS=$(grep -v '^#' $MERGED_VCF | wc -l)
echo "Number of SNPs in the merged VCF file: $TOTAL_SNPS"

# Use plink1.9 for Hardy-Weinberg equilibrium test and Sample Call Rate QC

# Convert the merged VCF file to PLINK format
plink1.9 --vcf $MERGED_VCF --make-bed --out $FINAL_PREFIX --double-id

# Hardy-Weinberg equilibrium test
plink1.9 --bfile $FINAL_PREFIX --hardy --out $FINAL_PREFIX

# Extract SNPs with HWE p-value > 1×10^-6
awk '$9 > 1e-6' ${FINAL_PREFIX}.hwe | cut -f2 > ${FINAL_PREFIX}_hwe_snps.txt

# Count the number of SNPs after HWE filtering
HWE_FILTERED_SNPS=$(wc -l < ${FINAL_PREFIX}_hwe_snps.txt)
HWE_FILTERED_SNPS=$((HWE_FILTERED_SNPS - 1))  # Subtract the header line
echo "Number of SNPs remaining after HWE QC: $HWE_FILTERED_SNPS"
echo "Number of SNPs removed after HWE QC: $((TOTAL_SNPS - HWE_FILTERED_SNPS))"

# Filter SNPs that do not meet HWE criteria
plink1.9 --bfile $FINAL_PREFIX --extract ${FINAL_PREFIX}_hwe_snps.txt --make-bed --out ${FINAL_PREFIX}_hwe_filtered

# Sample Call Rate QC
plink1.9 --bfile ${FINAL_PREFIX}_hwe_filtered --mind 0.02 --make-bed --out ${FINAL_PREFIX}_final

# Count the number of SNPs and samples after Sample Call Rate QC
FINAL_SNPS=$(wc -l < ${FINAL_PREFIX}_final.bim)
FINAL_SAMPLES=$(wc -l < ${FINAL_PREFIX}_final.fam)
echo "Number of SNPs remaining after Sample Call Rate QC: $FINAL_SNPS"
echo "Number of SNPs removed after Sample Call Rate QC: $((HWE_FILTERED_SNPS - FINAL_SNPS))"
echo "Number of samples remaining after Sample Call Rate QC: $FINAL_SAMPLES"

# Count the final number of SNPs and samples after QC
FINAL_SNPS=$(wc -l < ${FINAL_PREFIX}_final.bim)
FINAL_SAMPLES=$(wc -l < ${FINAL_PREFIX}_final.fam)
echo "Final number of SNPs after QC: $FINAL_SNPS"
echo "Final number of samples after QC: $FINAL_SAMPLES"

