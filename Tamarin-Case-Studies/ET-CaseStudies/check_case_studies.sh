# Commands to repoduce all reuslts from paper
# All computations on a 64 core server
# Total run time is

# Execute 4 times all files
time ./auto.py;

mv original_results.json original_results_1.json;
mv ALL_results.json ALL_results_1.json;

time ./auto.py;

mv original_results.json original_results_2.json;
mv ALL_results.json ALL_results_2.json;

time ./auto.py;

mv original_results.json original_results_3.json;
mv ALL_results.json ALL_results_3.json

time ./auto.py;

