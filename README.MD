# BONK 

![Tests](https://github.com/BrittleFoot/bonk/actions/workflows/tests.yml/badge.svg)

Tool, which takes a fasta file and some nucleotide/aminoacid substring (`ATGCGCTTA` for example) as an input and outputs all positions of the substring in genome in a tab-separated file.

## Installation

### Install python>=3.10
I suggest to use conda virtual env
```shell
conda create -y --name bonk python=3.10
conda activate bonk
```

### Install package
```sh
pip install .
```

### Testing

#### Using TOX

```sh
pip install tox
tox
```

#### Using pytest

```sh
pip install -r requirements_dev.txt
pytest
```

# Usage:
```sh
bonk --help
```
```sh
bonk -a /path/to/genome.fasta -s ATGCGCTTA -o /path/to/output.bed
```
note: you can specify `-` as an `-o` argument to perform output to stdout

Output example ([bed](https://m.ensembl.org/info/website/upload/bed.html) format) :

```
#chr #start_position #stop_position #strand #subsring_seq
1   236     245     -   ATGCGCTTA
32  4567    4576    +   ATGCGCTTA
```
