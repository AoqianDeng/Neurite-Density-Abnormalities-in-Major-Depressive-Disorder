import pandas as pd
import requests
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read GWAS results file
try:
    gwas_results = pd.read_csv(r'G:\11.23noddi\step3\PRS\gwas_results.assoc', delim_whitespace=True)
except Exception as e:
    logging.error(f"Failed to read GWAS results file: {e}")
    raise

# Set significance threshold
threshold = 1e-5

# Filter significant SNPs
if 'P' in gwas_results.columns:
    significant_snps = gwas_results[gwas_results['P'] < threshold]
else:
    logging.error("Column 'P' not found in GWAS results.")
    raise KeyError("Column 'P' not found in GWAS results.")

# Function: Annotate SNP using Ensembl VEP API
def annotate_snp_vep(snp):
    server = "https://rest.ensembl.org"
    ext = f"/vep/human/id/{snp}?content-type=application/json"
    
    try:
        r = requests.get(server + ext, headers={ "Content-Type" : "application/json"})
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for SNP {snp}: {e}")
        return snp, 'NA', 'NA', 'NA'

    decoded = r.json()
    if decoded:
        most_severe_consequence = decoded[0].get('most_severe_consequence', 'NA')
        gene = decoded[0].get('transcript_consequences', [{}])[0].get('gene_symbol', 'NA')
        location = f"{decoded[0].get('seq_region_name', 'NA')}:{decoded[0].get('start', 'NA')}-{decoded[0].get('end', 'NA')}"
        return snp, gene, location, most_severe_consequence
    else:
        return snp, 'NA', 'NA', 'NA'

# Annotate significant SNPs using parallel processing
annotated_snps = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(annotate_snp_vep, significant_snps['SNP'])
    for result in results:
        annotated_snps.append(result)

# Convert annotation results to DataFrame
annotated_df = pd.DataFrame(annotated_snps, columns=['SNP', 'Gene', 'Location', 'Consequence'])

# Merge original significant SNP data with annotation information
final_results = significant_snps.merge(annotated_df, on='SNP', how='left')

# Save results
try:
    final_results.to_csv(r'G:\11.23noddi\step3\PRS\annotated_gwas_results.csv', index=False)
    logging.info("Annotation completed, results saved to annotated_gwas_results.csv")
except Exception as e:
    logging.error(f"Failed to save annotated results: {e}")
    raise
