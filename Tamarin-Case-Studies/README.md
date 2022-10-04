This folder contains:
 * in `ET-CaseStudies` the equational theory based case studies;
 * in `Concatenation` the event based hash with associative concatenation case-studies.


Each subfolder contains a dedicated README that explains how to reproduce the case studies.

The Tamarin version used here is renamed to 'tamarin-concat' to distinguish with the classical `tamarin-prover`, if you installed it yourself you need to rename the executable. Note that both `tamarin-prover` and `tamarin-concat` are used in the scripts.

# Benchmarking

Note: If you use the scripts outside of the docker image, there can be potential problems running the scripts on MacOS machines.
This is caused by the multiprocessing library used in our python files.

## ET-CaseStudies

To run the case studies using equational theory (ET) based hash models
in `ET-CaseStudies`, simply execute

```bash check_case_studies.sh```

It runs all the valid case studies in the following folders 4 times:

- `ake`
- `csf-12`
- `distance_bounding`
- `original`
- `Tesla`

It creates ALL_results.json files for each run and stores the analysis and the timing data
in them.
It also produces original_results.json  files which contain all the original
case studies in the ROM like ET model separetly.

In the case we only want the latter results, execute

```bash check_case_studies_only_original.sh```

## Concatenation

For the event based (EB) models, there are two different data points to compute.

With

```bash main.sh```

we run all EB models (4 times) on all our original case studies and save
the results in the TIMED_RESULTS folders. As we apply some smart computation
to minimize the calls to the tamarin prover, we, in addition to the timing and analysis data,
save the amount of tamarin calls per case study. 

Further, to just get data on the attacks mentioned on Table 3 in the main paper,
execute

```bash Execute_all_cool_attacks.sh```

The results are saved in the `Attacks` folder and are named according to the flags used to find the attack. 
