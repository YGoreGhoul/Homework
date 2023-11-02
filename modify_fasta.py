import sys


def read_vcf(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Skip header and comment lines
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                chrom = fields[0]
                pos = fields[1]
                alt = fields[4]
                if chrom not in data:
                    data[chrom] = {}
                if pos not in data[chrom]:
                    data[chrom][pos] = alt
                else:
                    data[chrom][pos] = [data[chrom][pos], alt]
    return data


def modify_fasta_with_vcf(fasta_path, vcf_data):
    output = ''
    with open(fasta_path, 'r') as fasta_file:
        chrom = None
        count = 0
        for line in fasta_file:
            if line.startswith(">"):
                chrom = line[1:].strip()  # Get name chr
                count = 0  # Reset the counter for the new chromosome
            elif chrom in vcf_data:
                positions = vcf_data[chrom]
                for pos, alt in positions.items():
                    pos = int(pos)
                    if pos >= count and pos < count + len(line):
                        relpos = pos - count
                        line = line[:relpos-1] + alt + line[relpos:]
                count += len(line) - 1  
            output += line
    return output


def main():
    # Read fasta and vcf 
    fasta_file = sys.argv[1]
    vcf_file = sys.argv[2]
    # Get and write modified fasta
    vcf_data = read_vcf(vcf_file)
    modified_fasta = modify_fasta_with_vcf(fasta_file, vcf_data)
    out_fasta = 'modified.fasta' 
    with open(out_fasta, 'w') as output_file:
        output_file.write(modified_fasta)

if __name__ == "__main__":
    main()