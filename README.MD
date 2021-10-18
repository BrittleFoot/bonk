# BONK

Tool, which takes for input fasta file and some nucleotide/aminoacid substring (`ATGCGCTTA` for example) and outputs all positions of the substring in genome in a tab-separated file.


## Usage example:

```sh
genome_substring.py -a /path/to/genome.fasta -s ATGCGCTTA -o /path/to/output.bed
```

Output example ([bed](https://m.ensembl.org/info/website/upload/bed.html) format) :

```
#chr #start_position #stop_position #strand #subsring_seq
1   236     245     -   ATGCGCTTA
32  4567    4576    +   ATGCGCTTA
```

## Installation

### Conda

```
conda create --name bonk --file requirements.txt
conda activate bonk

# To test script
pip install pytest
```
