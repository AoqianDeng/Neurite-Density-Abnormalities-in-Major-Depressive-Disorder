
#!/bin/bash

# Define the output merged VCF file
MERGED_VCF="merged_filtered.vcf"

# Initialize the merged VCF flie header
echo -n "" > $MERGED_VCF

for i in {1..22}; do
  VCF_FILE="chr${i}.dose.vcf"
  INFO_FILE="chr${i}.info"
  SNP_LIST_FILE="chr${i}_snplist.txt"
  OUTPUT_PREFIX="chr${i}_filtered"

  # Filter the info file and count the number of SNPs
  TOTAL_SNPS=$(awk 'NR > 1 {print $1}' $INFO_FILE | wc -l)
  echo "Number of SNPs before QC on chromosome $i: $TOTAL_SNPS"

  # Filter the info file based on QC criteria
  awk 'BEGIN {FS="\t"; OFS="\t"}
       NR == 1 || ($6 > 0.99 && $5 > 0.01 && $7 > 0.8) {print $1}' $INFO_FILE > $SNP_LIST_FILE

  FILTERED_SNPS=$(wc -l < $SNP_LIST_FILE)
  FILTERED_SNPS=$((FILTERED_SNPS - 1))  # Subtract the header line
  echo "Number of SNPs after QC on chromosome $i: $FILTERED_SNPS"

  # Use plink1.9 to filter the VCF file
  plink1.9 --vcf $VCF_FILE --extract $SNP_LIST_FILE --make-bed --out $OUTPUT_PREFIX --double-id

  # Convert the filtered BED file back to VCF
  plink1.9 --bfile $OUTPUT_PREFIX --recode vcf --out $OUTPUT_PREFIX

  # Append the filtered VCF file to the merged VCF file
  if [ $i -eq 1 ]; then
    # For the first file, include the header
    cat ${OUTPUT_PREFIX}.vcf >> $MERGED_VCF
  else
    # For other files, skip the header (lines starting with #)
    grep -v '^#' ${OUTPUT_PREFIX}.vcf >> $MERGED_VCF
  fi
done

# The final merged file is merged_filtered.vcf
echo "Merged VCF file: $MERGED_VCF"

