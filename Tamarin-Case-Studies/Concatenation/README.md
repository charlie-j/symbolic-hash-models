
This folder contains:
 * the hash library allowing for a fine grained modeling of hash functions, 
 * details on the associative concatenation operator,
 * the scripts to explore automatically all hash models on a given files.


# Systematic analysis

The script to generate the tables found in the paper is `auto_paper.py` (`./auto_paper.py --help` for usage). 

## Table from the paper

To completely reproduce all tables from the paper, first run:
`./check_case_studies.sh`
This shell scripts contains the list of all auto_paper commands needed, as well as in comments some timing indications. It will produce json files containing the results.
Those can be turned into latex tables with `make_latex_files.sh`.

## Custom usage

On complex examples, run the script a first time with default timeout. Even though the timeout is short, some long running example may be implied by examples solved very fast. We thus want to first explore everything with short timeout, and only then move to reloading the produced array, and retry over it with longer timeout, or with simplifcations.

## Example file

An example file allows to test the library against classical security property of hash functions, as a sanity checl.

Example file produced with (74 seconds):
./auto_paper.py Example_Hash_Library_usage.spthy -l TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance -j 30 -fs res-example


Then, latexfile produced with:
./auto_paper.py Example_Hash_Library_usage.spthy -l TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance -j 30 -fl res-example -lt -olt res-example.tex


# Concatenation and Hash Library

To use on new examples either the concatenation operator or the Hash Library, read `README_library.md` and `README_concatenation.md`.
