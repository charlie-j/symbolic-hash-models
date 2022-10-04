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

default_prover = "tamarin-prover"
default_timeout = 30 # in seconds




PROVER = default_prover


CORES = 8


TIMEOUT = 600


protocolsOrg = ['Flickr.spthy',
'ikeV2_HF_EC_nocookie.spthy',
'sshV2_HF_EC.spthy',
'telegram_with_HEB.spthy',
'ikeV2_HF_EC.spthy',                   
'sigma.spthy',           
'telegram_2HF.spthy'
]

foldersOrg = ['original/',
'original/pre/',
'original/new_pre/']

lemmasOrg = { 'Flickr.spthy' : ['authenticate','authenticatePermissions','KeySecrecy'],
'ikeV2_HF_EC_nocookie.spthy' : ['trans_auth', 'secrecy_key_A', 'secrecy_key_B'],
'sshV2_HF_EC.spthy' : ['secrecy_key_A', 'secrecy_key_B', 'trans_auth', 'agree_keys_all'],
'telegram_with_HEB.spthy' : ['t_auth', 't_secC'],
'ikeV2_HF_EC.spthy' : ['trans_auth', 'secrecy_key_A', 'secrecy_key_B'],                   
'sigma.spthy' : ['target_secA', 'target_secB', 'target_agree_B_to_A', 'target_agree_A_to_B_or_Bbis'],           
'telegram_2HF.spthy' : ['auth', 'secC']
}


original_cases = []

for fol in foldersOrg:
    for proto in protocolsOrg:
        original_cases.append((fol+proto,lemmasOrg[proto]))



full_results = {}
RESULTS = full_results

for (PROTOCOL,LEMMAS) in original_cases:
    results_per_case(LEMMAS,PROTOCOL)


with open('original_results.json','w') as f:
    f.write(json.dumps(RESULTS, indent=4))




'''
def iterFolder(folder):
    """ Yields all files in the folder that have a .spthy ending. """
    for file in os.listdir(folder):
        if file.endswith(".spthy"):
            fpath = os.path.join(folder, file)
            yield fpath


def parseFile(path):
    summary = ""
    try:
        # strip everything before the summary part
        allContent = path.split("summary of summaries")
        summary = allContent[-1]
        #proof = allContent[0].split("------------------------------------------------------------------------------")[0]
    except Exception:
        return "There was an error while reading"

    ## parse lemmas ##
    try:
        parsed = re.findall(r"(\w+) (?:\(all-traces\))?:(?!  ) (.*) \((\d+) steps\)\n", summary)
        parsed = [lemmas for (lemmas, res, steps) in parsed]  # convert types
        return parsed

    except Exception as ex:
        return f"Parse error - lemmas: {path}"


def get_lemmas(file):
    process = subprocess.Popen(["tamarin-prover",file], cwd=os.path.dirname(os.path.realpath(__file__)),stderr=subprocess.STDOUT,stdout=subprocess.PIPE, start_new_session=True)
    process_return = process.stdout.read()
    parsedLemmas = parseFile(process_return.decode("utf-8"))
    return parsedLemmas
    try:
        output, errors = process.communicate(timeout=TIMEOUT)
        return parseFile(output)

    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        return "timeout"



def get_spthy():
    main_folder = ["distance_bounding","Tesla","ake","csf-12"]
    subfolders = ["pre","new_pre",""]
    
    pairs = []       
    for path1 in main_folder:
        for path2 in subfolders:
            if path2=="":
                for pathCom in iterFolder(path1):
                    pairs.append((pathCom,get_lemmas(pathCom)))
            else:
                for pathCom in iterFolder(path1+'/'+path2):
                    pairs.append((pathCom,get_lemmas(pathCom)))
    print("Parsing Complete: " + str(len(pairs)))

    for keys, lemma in pairs:
        results_per_case(lemma,keys)

    print("Proving Complete: " + str(len(RESULTS.keys())))
    with open('others_results.json','w') as f:
        f.write(json.dumps(RESULTS, indent=4))       

full_results = {}
RESULTS = full_results
get_spthy()  
'''
'''
print("Compressed Results")
print(RESULTS)
print(json.dumps(RESULTS, indent=4))
'''
