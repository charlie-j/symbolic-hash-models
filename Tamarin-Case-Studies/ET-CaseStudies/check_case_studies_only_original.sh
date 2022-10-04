# Commands to repoduce all reuslts from paper
# All computations on a 64 core server
# Total run time is

# Execute 4 times all files
time ./auto-orig.py;

mv original_results.json original_results_1.json;

time ./auto-orig.py;

mv original_results.json original_results_2.json;

time ./auto-orig.py;

mv original_results.json original_results_3.json;

time ./auto-orig.py;

