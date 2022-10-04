# Commands to repoduce all reuslts from paper
# All computations on a 64 core server
# Total run time is

# Execute 4 times all files
time ./check_case_studies.sh;

mv TIMED_RESULTS TIMED_RESULTS_1
mkdir TIMED_RESULTS
time ./check_case_studies.sh;

mv TIMED_RESULTS TIMED_RESULTS_2
mkdir TIMED_RESULTS
time ./check_case_studies.sh;

mv TIMED_RESULTS TIMED_RESULTS_3
mkdir TIMED_RESULTS
time ./check_case_studies.sh;

mv TIMED_RESULTS TIMED_RESULTS_4
mkdir TIMED_RESULTS
