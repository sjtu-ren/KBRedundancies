# Numerated KB Format

The concept "KB" here refers only to the facts that are taken into account in this project.
Raw KB data contains long and repeated strings for relations, entities, and possibly, their domain prefixes.
The numerated KB format map the above strings into integers to save the storage space and improve the process performance.
A numerated KB is composed of the following parts:

1. Numeration Mapping
   - There may be multiple mapping files, each of which is a `.tsv` file. The files are named by `map<#num>.tsv`. `#num` is the order of the files, starting from 1.
   - The file contains two columns separated by the tabular char (`'\t'`):
     - The 1st column is the string for relation/entity names;
     - The 2nd column is an integer (in Hexadecimal) that is assigned as the identifier for the string;
     - Each row denotes a mapping between the name and the integer;
     - The mapping should be bijective, and the integers are continuous starting from 1.
   - Each of the files contains no more than 1M lines.
2. Numerated Records
   - There may be multiple numerated record files, each of which contains records in one relation.
   - The name of the files should be `<relation name>_<arity>_<#records>.rel`.
   - The files are binary files, each of which only contains `arity`x`#records` integers.
   - The integers stored in one `.rel` file is column oriented, each column corresponds to one argument in the relation. The columns are stored in the file in order, i.e., in the order of: 1st col 1st row, 1st col 2nd row, ..., ith col jth row, ith col (j+1)th row, ...
3. Meta Info
   - There may be multiple files with extension `.meta` to store arbitrary meta information of the KB.
   - The files are customized by other utilities and are not in a fixed format.

All of above files should be in one directory without nested sub-directories, and the name of the directory should be the same as the KB.

For example, the following KB with 3 relations is converted to 4 data files in a directory:

```
family/3
--------
alice	bob	catherine
diana	erick	frederick
gabby	harry	isaac
jenna	kyle	lily

mother/2
--------
alice	catherine
diana	frederick
gabby	isaac
jenna	lily

father/2
--------
bob	catherine
erick	frederick
harry	isaac
marvin	nataly
```

- `map.tsv`
```
family	1
mother	2
father	3
alice	4
bob	5
catherine	6
diana	7
erick	8
frederick	9
gabby	a
harry	b
isaac	c
jena	d
kyle	e
lily	f
marvin	10
nataly	11
```

- `family_3_4.rel` (numbers are separated by space for demonstration, the actual files are in binary format)
```
4 7 a d 5 8 b e 6 9 c f
```

- `mother_2_4.rel`
```
4 7 a d 6 9 c f
```

- `father_2_4.rel`
```
5 8 b e 6 9 10 11
```