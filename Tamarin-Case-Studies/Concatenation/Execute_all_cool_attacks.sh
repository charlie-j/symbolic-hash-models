
#Sigma

# S1
# 27.78s
(timeout 1000 time tamarin-concat --prove=target_secA Sigma/sigma.spthy +RTS -N8 -RTS -D=FreshDomain -D=CPcol -D=LEcol) &> Attacks/Sigma-FreshDomain_CPcol_LEcol-target_secA;

# S2 second attack needs to found in the interactive prover
#time tamarin-concat --prove Sigma/sigma.spthy +RTS -N8 -RTS -D=FreshDomain -D=CPcol -D=LEcol


# S3
# 54.87s
(timeout 1000 time tamarin-concat --prove=target_secA Sigma/sigma.spthy +RTS -N8 -RTS -D=FreshDomain -D=CPcol -D=noRole) &> Attacks/Sigma-FreshDomain_CPcol-target_secA;


#SSH

# SSH1
# 3.14s
(timeout 1000 time tamarin-concat --prove=agree_keys_all SSH/sshV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=CR -D=FixedLength) &> Attacks/SSH-FreshDomain_CR-agree_keys_all;

# SSH2
# 27.85s
(timeout 1000 time tamarin-concat --prove=trans_auth SSH/sshV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=IPcol -D=LEcol -D=FixedLength -D=SingleHash) &> Attacks/SSH-FreshDomain_IPcol_LEcol-trans_auth;

# SSH 3
# 40.52
(timeout 1000 time tamarin-concat --prove=trans_auth SSH/sshV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=SndPreImage -D=LEcol -D=FixedLength -D=SingleHash) &> Attacks/SSH-FreshDomain_SndPreImage_LEcol-trans_auth;


#IKE

# IKE1
# 5.87s
(timeout 1000 time tamarin-concat --prove=secrecy_key_B IKE/IKE_Cookie/ikeV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=CR) &> Attacks/IKE-FreshDomain_CR-secrecy_key_B;

# IKE2
# 20.48s
(timeout 1000 time tamarin-concat --prove=trans_auth IKE/IKE_Cookie/ikeV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=IPcol -D=LEcol -D=neutral) &> Attacks/IKE-FreshDomain_IPcol_LEcol_neutral-trans_auth;

#IKE3
# 8.85s
(timeout 1000 time tamarin-concat --prove=trans_auth IKE/IKE_Cookie/ikeV2_HEB_A.spthy +RTS -N8 -RTS -D=FreshDomain -D=ExCol -D=LEcol -D=neutral) &> Attacks/IKE-FreshDomain_ExCol_LEcol_neutral-trans_auth;


#Flickr

# F
# 0.95s
(timeout 1000 time tamarin-concat --prove=authenticatePermissions Flickr/Flickr.spthy +RTS -N8 -RTS -D=SingleHash -D=FreshDomain -D=CR -D=LengthExtension) &> Attacks/Flickr-FreshDomain_CR_LengthExtension-authenticatePermissions-SH;





