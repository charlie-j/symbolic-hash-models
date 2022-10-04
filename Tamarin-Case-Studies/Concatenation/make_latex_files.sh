# If check_case_studies was executed, allows to produce all the tex files for paper.

# Example file
./auto_paper.py Example_Hash_Library_usage.spthy -l TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance -fl res-example -lt -olt res-example.tex


# Sigma protocol
./auto_paper.py Sigma/sigma.spthy -l target_secA target_secB target_agree_B_to_A target_agree_A_to_B_or_Bbis -fl res-sigma -lt -olt res-sigma.tex

# Telegram
./auto_paper.py Telegram/telegram_with_HEB.spthy -l t_auth t_secC -fl res-telegram -lt -olt res-telegram.tex

#Flickr
./auto_paper.py Flickr/Flickr.spthy -l authenticate authenticatePermissions -fl res-flickr -lt -olt res-flickr.tex

# SSH
./auto_paper.py SSH/sshV2_HEB_A.spthy -l secrecy_key_A secrecy_key_B trans_auth agree_keys_all  -j 20 -fl res-ssh -lt -olt res-ssh.tex

#IKE (without neutral DH element)
./auto_paper.py IKE/IKE_Cookie/ikeV2_HEB_A.spthy -l  trans_auth secrecy_key_A secrecy_key_B  -fl res-ike -lt -olt res-ike.tex


#IKE (with neutral DH element)
./auto_paper.py IKE/IKE_Cookie/ikeV2_HEB_A.spthy -l  trans_auth secrecy_key_A secrecy_key_B  -fl res-ike-neutral -j 30 -p "tamarin-prover -D=neutral" -lt -olt res-ike-neutral.tex


#IKE No Cookie (with neutral DH element)
./auto_paper.py IKE/IKE_NoCookie/ikeV2_HEB_A.spthy -l  trans_auth secrecy_key_A secrecy_key_B  -fl res-ike-nocookie-neutral -j 30 -p "tamarin-prover -D=neutral" -lt -olt res-ike-nocookie-neutral.tex
