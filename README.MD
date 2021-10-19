# BONK 

![Tests](https://github.com/BrittleFoot/bonk/blob/master/.github/workflows/tests.yml/badge.svg)

Tool, which takes a fasta file and some nucleotide/aminoacid substring (`ATGCGCTTA` for example) as an input and outputs all positions of the substring in genome in a tab-separated file.

## Installation

### Install python>=3.10
I suggest to use conda virtual env
```sh
conda create -y --name bonk python=3.10
conda activate bonk
```

### Install package
```sh
pip install .
```

## Usage:
```sh
python -m bonk -a /path/to/genome.fasta -s ATGCGCTTA -o /path/to/output.bed
```

Output example ([bed](https://m.ensembl.org/info/website/upload/bed.html) format) :

```
#chr #start_position #stop_position #strand #subsring_seq
1   236     245     -   ATGCGCTTA
32  4567    4576    +   ATGCGCTTA
```
