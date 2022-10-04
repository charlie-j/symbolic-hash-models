# Commands to repoduce all reuslts from paper
# All computations on a 64 core server
# Total run time is 150 minutes

# Example file
# 1m
time ./auto_paper.py Example_Hash_Library_usage.spthy -l TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance -c 2 -fs res-example > TIMED_RESULTS/example.results;

#Flickr
# 41s
time ./auto_paper.py Flickr/Flickr.spthy -l authenticate authenticatePermissions -c 2 -fs res-flickr > TIMED_RESULTS/Flickr.results;

# Sigma protocol
# 4min49
time ./auto_paper.py Sigma/sigma.spthy -l target_secA target_secB target_agree_B_to_A target_agree_A_to_B_or_Bbis -fs res-sigma -c 2 > TIMED_RESULTS/Sigma_quick.results;
# 25m14
time ./auto_paper.py Sigma/sigma.spthy -l target_secA target_secB target_agree_B_to_A target_agree_A_to_B_or_Bbis -fl res-sigma -fs res-sigma -c 2 -t 600 -rt > TIMED_RESULTS/Sigma.results;

# Telegram
# 1m55
time ./auto_paper.py Telegram/telegram_with_HEB.spthy -c 2 -l t_auth t_secC -fs res-telegram -t 60 > TIMED_RESULTS/TELEGRAM.results;

# SSH
# 8m01
time ./auto_paper.py SSH/sshV2_HEB_A.spthy -l secrecy_key_A secrecy_key_B trans_auth agree_keys_all -c 2 -fs res-ssh > TIMED_RESULTS/SSH_quick.results;
# 43m20
time ./auto_paper.py SSH/sshV2_HEB_A.spthy -l secrecy_key_A secrecy_key_B trans_auth agree_keys_all -c 8 -fl res-ssh -fs res-ssh -t 1200 -si -rt > TIMED_RESULTS/SSH.results;


#IKE (without neutral DH element)
# 4m55
time ./auto_paper.py IKE/IKE_Cookie/ikeV2_HEB_A.spthy -l trans_auth secrecy_key_A secrecy_key_B -fs res-ike -c 2 > TIMED_RESULTS/IKE_quick.results;
# 64m57
time ./auto_paper.py IKE/IKE_Cookie/ikeV2_HEB_A.spthy -l trans_auth secrecy_key_A secrecy_key_B -fl res-ike -fs res-ike -c 8 -t 1200 -rt -si > TIMED_RESULTS/IKE.results;


#IKE (with neutral DH element)
# 1m25
time ./auto_paper.py IKE/IKE_Cookie/ikeV2_HEB_A.spthy -l trans_auth secrecy_key_A secrecy_key_B -fs res-ike-neutral -c 2 -p "tamarin-concat -D=neutral" > TIMED_RESULTS/IKE_neutral.results;


# IKE (no cookie, with neutral)
# 2m12
time ./auto_paper.py IKE/IKE_NoCookie/ikeV2_HEB_A.spthy -l trans_auth secrecy_key_A secrecy_key_B -fs res-ike-nocookie-neutral -c 2 -p "tamarin-concat -D=neutral" > TIMED_RESULTS/IKE_neutral_nocookie.results;
