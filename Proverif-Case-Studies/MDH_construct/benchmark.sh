# Commands to repoduce all results obtained with ProVerif and our hash axiomatization
# All computations on a 64 core server
# Total run time is ??TODO??

# 9s
echo "SIGMA no assoc, no col: running..."
time make sigma=1 > LOG_sigma_no.txt
grep RESULT LOG_sigma_no.txt

# 15s
echo "\nSIGMA with assoc, no col: running..."
time make sigma=1 assoc=1 > LOG_sigma_assoc.txt
grep RESULT LOG_sigma_assoc.txt

# 10s
echo "\nSIGMA with assoc, with col: running..."
time make sigma=1 col=1 > LOG_sigma_col.txt
grep RESULT LOG_sigma_col.txt

# --------------

# 4s
echo "\nSimplified IKE no assoc, no col: running..."
time make ike_s=1 > LOG_ikeS_no.txt
grep RESULT LOG_ikeS_no.txt

# 4s
echo "\nSimplified IKE with assoc, no col: running..."
time make ike_s=1 assoc=1 > LOG_ikeS_assoc.txt
grep RESULT LOG_ikeS_assoc.txt

# 137s
echo "\nSimplified IKE with assoc, with col: running..."
time make ike_s=1 col=1 > LOG_ikeS_col.txt
grep RESULT LOG_ikeS_col.txt

# --------------

# 8s
echo "\nIKE no assoc, no col: running..."
time make ike=1 > LOG_ike_no.txt
grep RESULT LOG_ike_no.txt

# 12s
echo "\nIKE with assoc, no col: running..."
time make ike=1 assoc=1 > LOG_ike_assoc.txt
grep RESULT LOG_ike_assoc.txt

# 112s
echo "\nIKE with assoc, with col: running..."
time make ike=1 col=1 > LOG_ike_col.txt
grep RESULT LOG_ike_col.txt

# 
echo "\nAll log files:"
ls LOG_*.txt

