import sys
import pandas as pd
from io import StringIO

# Function to change chromosome notation in BED to match VCF
def change_chrom_notation(chrom, vcf_chrom):
    if chrom.startswith('chr') and not vcf_chrom.startswith('chr'):
        return chrom[3:]
    elif not chrom.startswith('chr') and vcf_chrom.startswith('chr'):
        return 'chr' + chrom
    else:
        return chrom

# Function to check if POS in [Start; End]
def check_within_range(bed, chrom, pos):
    matching = bed[(bed[0] == chrom) & (bed[1] <= pos) & (bed[2] >= pos)]
    return not matching.empty


def main():
    vcf_file = sys.argv[1]
    bed_file = sys.argv[2]

    # Read bed and vcf
    bed = pd.read_csv(bed_file, sep='\t', header=None)
    vcf_lines = []
    with open(vcf_file, 'r') as vcf_file:
        for line in vcf_file:
            if not line.startswith('##'):
                vcf_lines.append(line)
    vcf = pd.read_csv(StringIO('\n'.join(vcf_lines)), sep='\t')

    # Rename 'chr' if needed to match the format in VCF
    bed[0] = bed.apply(lambda row: change_chrom_notation(row[0], vcf['#CHROM'].iloc[0]), axis=1)
    vcf['within_range'] = vcf.apply(lambda row: check_within_range(bed, row['#CHROM'], row['POS']), axis=1)
    filtered_vcf = vcf[vcf['within_range']]
    # Drop tmp column
    filtered_vcf = filtered_vcf.drop('within_range', axis=1)
    filtered_vcf.to_csv('filtered_output.vcf', sep='\t', index=False)

if __name__ == '__main__':
    main()
