plink --bfile mdd_gwas --logistic --covar covariates.txt --covar-name age,sex,PC1,PC2,PC3,PC4,PC5 --out mdd_gwas_logistic       
plink --bfile mdd_gwas --assoc --adjust --out mdd_gwas_assoc_adjusted  