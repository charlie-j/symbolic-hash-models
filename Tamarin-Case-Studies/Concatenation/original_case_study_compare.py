#!/usr/bin/env python3

"""
This script allows to automatically explore the hierarchy for an example relying on  the HashLibrary.

It only works on a universally quantified lemma.


To run the Example Hash Library file for all lemmas using 4 parallel job and  storing the result in the res-example file, run:

./auto_paper.py Example_Hash_Library_usage.spthy -l TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance -j 4 -fs res-example


This runs in on Intel® Core™ i7-10510U CPU @ 1.80GHz × 8


 TypeFlawAttack_Resistance GuessingHash_Resistance Collision_Resistance PreImage_Resistance SndPreImage_Resistance ChosenPrefixCollision_Resistance IdentiticalPrefixCollision_Resistance LengthExtensionCol_Resistance LengthExtensionAdv_Resistance iLeaks_Resistance



./auto_paper.py Sigma/SigmaCleanUP/sigma.spthy -l target_secA target_agree_B_to_A -t 6000 -fs res


"""

import os
import sys
import signal
import subprocess
import argparse
import smtplib
import json
import time
import re
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from multiprocessing import Pool
import multiprocessing.pool
from functools import partial


from multiprocessing.managers import BaseManager






# base function which calls the subscript computing the results
def call_check(lemma,PROTOCOL):
    cmd = "%s %s --prove=%s" % (PROVER, PROTOCOL, lemma)
    if CORES:
        cmd += " +RTS -N%i -RTS" % (CORES)
    else:
        cmd += " +RTS -N%i -RTS" % (CORES)
    cmd += " -D=FreshDomain -D=CR"
    print("Executing: $%s" % cmd)
    startTime = time.time()
    process = subprocess.Popen(cmd.split(),cwd=os.path.dirname(os.path.realpath(__file__)),stderr=subprocess.STDOUT,stdout=subprocess.PIPE, start_new_session=True)
    try:
        output, errors = process.communicate(timeout=TIMEOUT)
        TotalTime = time.time() - startTime
        if "Maude returned warning" in str(output):
            return "AssociativeFailure"
        elif "CallStack" in str(output) or "internal error" in str(output):
            return "TamarinError"

        proof_results = [line for line in str(output).split('\\n') if (" "+lemma+" " in line and "steps" in line)]
        if len(proof_results) == 1:
            line = proof_results[0]
            if "verified" in line:
                return ("true",TotalTime)
            elif "falsified" in line:
                return ("false",TotalTime)
            else:
                print("Scripting error")
                print(cmd)
                print(output)
                print(proof_results)
                raise ValueError
        else:
            print("Scripting error")
            print(cmd)
            print(output)
            print(proof_results)
            raise ValueError


    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return ("timeout",TIMEOUT)



# Here, we have populated a set of results over a compressed set of scenario.
# We first infer the full set of results
def results_per_case(lemmas,protocol):
    RESULTS[protocol] = list()
    for lemma in lemmas:
        res = call_check(lemma,protocol)
        if res[0]=="true":
            RESULTS[protocol].append((lemma,res))
        elif res[0]=="false":
            RESULTS[protocol].append((lemma,res))
        else:
            RESULTS[protocol].append((lemma,res))


default_cores = min(os.cpu_count(),8)

default_prover = "tamarin-concat"
default_timeout = 30 # in seconds




PROVER = default_prover


CORES = 8


TIMEOUT = 600


protocolsOrg = ['Flickr/Flickr.spthy',
'IKE/IKE_NoCookie/ikeV2_HEB_A.spthy',
'SSH/sshV2_HEB_A.spthy',
'Telegram/telegram_with_HEB.spthy',
'IKE/IKE_Cookie/ikeV2_HEB_A.spthy',                   
'Sigma/sigma.spthy',           
]


lemmasOrg = { 'Flickr/Flickr.spthy' : ['authenticate','authenticatePermissions','KeySecrecy'],
'IKE/IKE_NoCookie/ikeV2_HEB_A.spthy' : ['trans_auth', 'secrecy_key_A', 'secrecy_key_B'],
'SSH/sshV2_HEB_A.spthy' : ['secrecy_key_A', 'secrecy_key_B', 'trans_auth', 'agree_keys_all'],
'Telegram/telegram_with_HEB.spthy' : ['t_auth', 't_secC'],
'IKE/IKE_Cookie/ikeV2_HEB_A.spthy' : ['trans_auth', 'secrecy_key_A', 'secrecy_key_B'],                   
'Sigma/sigma.spthy' : ['target_secA', 'target_secB', 'target_agree_B_to_A', 'target_agree_A_to_B_or_Bbis'],           
}


original_cases = []

for proto in protocolsOrg:
    original_cases.append((proto,lemmasOrg[proto]))


# run 4 times
for i in ["","_1","_2","_3"]:
    full_results = {}
    RESULTS = full_results

    for (PROTOCOL,LEMMAS) in original_cases:
        results_per_case(LEMMAS,PROTOCOL)

    with open('original_results'+i+'.json','w') as f:
        f.write(json.dumps(RESULTS, indent=4))



