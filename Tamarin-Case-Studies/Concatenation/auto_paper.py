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
import time
import os
import sys
import signal
import subprocess
import argparse
import smtplib
import json
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from multiprocessing import Pool
import multiprocessing.pool
from functools import partial


from multiprocessing.managers import BaseManager
from multiprocessing import Manager


def scen_of_string(st):
    return st.split("_")

def string_of_scen(scen):
    scen.sort()
    return '_'.join(scen)


class Data:
    def __init__(self,data=None, length=0):
        self.data = data
        self.length = length

    def get(self):
        return self.data

    def set(self,data):
        self.data = data

    def set_lemma_scen(self,lemma,scen,value):
        self.data[lemma][string_of_scen(scen)] = value

    def get_lemma_scen(self,lemma,scen,value):
        self.data[lemma][string_of_scen(scen)] = value

    def set_length(self,length):
        self.length = length

    def length_minus(self,):
        self.length -= 1

    def get_length(self):
        return self.length



BaseManager.register("myresult",Data)



# We define our different base scenarios, from the naming conventions of the paper
# from left to right, stronger threat model to weaker
output=  ["ACT", "ACN", "RO"] # ! t^To^ND cannot be implemented
collisions_1 = ["AllCol", "PI1", "PI2", "Ex", ""]
collisions_2 = ["AllCol", "CP", "IP", ""] # add "IP" ??
length_ext = ["Adv", ""]
length_col = ["Clo", ""]
input_leak = ["i", ""]

# scenarios that if absent we add the CR macro parameter
all_collisions =  list(filter(lambda x : x!="",  set(collisions_1 + collisions_2)))

# We will build all the scenarios with cross products
# But first, we define which scenarios are redundant

# the presence of the key in the scenario implies that we should remove the scenario on the right handside, as it is implied by the one on the lhs.
redundancy = {
    "CP" : ["Ex"],  # ("CP" => "Ex")
    "IP": ["Ex"],   # ("IP" => "Ex")
    "ACT" : ["Adv"], #  ("ACT" => "Adv")
    "ACN" : ["Adv"], #  ("ACN" => "Adv")
    "i" : ["Adv"],
    "AllCol" : ["CP", "IP", "PI1", "PI2", "Ex", "Clo"], # ("AllCol" => all colisions...), and we say that AllCol has priority over CR
    }

def apply_redundancy(scen):
    res = list(scen)
    for key in redundancy:
        if key in res:
            for dropped in redundancy[key]:
                try:
                    res.remove(dropped)
                except: ()
    res.sort()
    return res

# next, the redundancy for scenario formatting
redundancy_col = {
    "CP" : ["Ex"],  # ("CP" => "Ex")
    "IP": ["Ex"],   # ("IP" => "Ex")
    "AllCol" : ["CP", "IP", "PI1", "PI2", "Ex"], # ("AllCol" => all colisions...), and we say that AllCol has priority over CR
    }


def apply_redundancy_col(scen):
    res = list(scen)
    for key in redundancy_col:
        if key in res:
            for dropped in redundancy_col[key]:
                try:
                    res.remove(dropped)
                except: ()
    res.sort()
    return res



# We check if sc1 is a stronger threat model than sc2 for a given dimensions
# This means that an attack (or a trace) in sc2 implies an attack (or a trace) in sc1.
# This is actually a stronger or equal relation.
def is_stronger_threat_model_dim(sc1, sc2, dim):
    dimsc1 = [dim.index(x) for x in dim if x in sc1]
    dimsc2 = [dim.index(x) for x in dim if x in sc2]
    return len(dimsc2) == 0 or (len(dimsc1) != 0 and dimsc1[0] <= dimsc2[0])



# We apply the normal form that removes redundancy, and we then check over all dimensions if the scenarios are comparable.
dimensions = [output, collisions_1, collisions_2, length_ext, input_leak, length_col]
def is_stronger_threat_model(sc1, sc2, use_redundant):
    if use_redundant:
        sc1 = apply_redundancy(sc1)
        sc2 = apply_redundancy(sc2)
    else:
        sc1 = apply_redundancy_col(sc1)
        sc2 = apply_redundancy_col(sc2)
    return all(is_stronger_threat_model_dim(sc1, sc2, d)  for d in dimensions)

#print(is_stronger_threat_model(["AllCol","i", "ACN"], ["i", "ACN", "Adv", "AllCol"], True))

# And to speed up the verification process, we prioritize some scenarios.
# The idea is that we never explore all three output possibilities, and decide early which one is suited for the protocol.
# To do so, we simply have to priorize a few of the scenarios, in a heuristic like fashion.
# We actually prioritize all the scenarios that correspond to minimal proof or attacks on the atomic definitions.
first_scenarios = list(map(apply_redundancy,
                           [['ACN'],
                            ['ACT'],
                            ['Adv', 'RO'],
                            ['AllCol', 'RO'],
                            ['CP', 'RO'],
                            ['Ex', 'RO'],
                            ['IP', 'RO'],
                            ['PI2', 'RO'],
                            ['RO', 'PI1'],
                            ['RO', 'i'],
                            ['Ex', 'RO', 'Clo'],
                            ['IP', 'Clo', 'RO'],
                            ['PI2', 'i', 'RO'],
                            ['ACT', 'Adv', 'Clo', 'AllCol'],
                            ['ACT', 'Adv', 'i', 'Clo'],
                            ['CP', 'RO', 'Clo', 'PI1'],
                            ['Adv', 'AllCol', 'i', 'Clo', 'ACN'],
                            ['Adv', 'PI2', 'Clo', 'CP', 'ACT'],
                            ['Adv', 'i', 'Clo', 'CP', 'ACT'],
                            ['Adv', 'i', 'Clo', 'Ex', 'ACT'],
                            ['Adv', 'i', 'PI1', 'CP', 'ACT'],
                            ['Adv', 'i', 'PI1', 'Clo', 'ACT'],
                            ['Adv', 'RO', 'i', 'PI1', 'Clo', 'CP'],
                            ['Adv', 'i', 'PI1', 'IP', 'Clo', 'ACT']]
                           ))

scenarios = first_scenarios + []
# then, we build all with cross producst
for i in output:
    for j in collisions_1:
        for k in collisions_2:
            for l1 in length_ext:
                for l2 in length_col:
                    for m in input_leak:
                        aux = list(filter(lambda x : x!="",  set([i,j,k,l1,l2,m])))
                        aux = apply_redundancy_col(aux)
                        if aux not in scenarios: # we only add it once
                            scenarios.append(aux)



# The following script only work for universall quantified lemmas, i.e. true implies that the property hold for all traces.
def is_already_explored_scenario_for_universal_lemma(results,lemma, scen, use_redundant, allow_same):
    impliers_false = [ sc2 for sc2 in  (results[lemma]).keys() if is_stronger_threat_model(scen, scen_of_string(sc2), use_redundant)
                       and (allow_same or  set(scen) != set(scen_of_string(sc2)))
                       and results[lemma][sc2] == "false" ]
    impliers_true = [ sc2 for sc2 in  (results[lemma]).keys() if is_stronger_threat_model(scen_of_string(sc2),scen, use_redundant)
                      and (allow_same or set(scen) != set(scen_of_string(sc2)))
                      and results[lemma][sc2] == "true" ]

    impliers_true_simpl = [ sc2 for sc2 in  (results[lemma]).keys() if is_stronger_threat_model(scen_of_string(sc2),scen, use_redundant)
                      and (allow_same or set(scen) != set(scen_of_string(sc2)))
                      and results[lemma][sc2] == "truesimpl" ]


    if impliers_false:
        # if there exists a scenario such that scen is a stronger threat model than sc2, and sc2 already has an attack, we know that sc1 does too
        #print("Implied attack scenario %s by %s" % (scen, impliers_false[0] ) )

        return "false"
    elif impliers_true:
        # if there exists a scenario sc2 which is a stronger threat model than scen and which is secure, then lemma also holds for scen
        #print("Implied secure scenario %s by %s" % (scen, impliers_true[0]))
        return "true"
    elif impliers_true_simpl:
        # if there exists a scenario sc2 which is a stronger threat model than scen and which is secure, then lemma also holds for scen
        #print("Implied simplified secure scenario %s by %s" % (scen, impliers_true_simpl[0]))
        return "truesimpl"
    else:
        return None

def get_value(results,lemma,scen):
    r1 = is_already_explored_scenario_for_universal_lemma(results,lemma,scen, True, True)
    if r1 in ["true", "false", "truesimpl"]:
        return r1
    else:
        return is_already_explored_scenario_for_universal_lemma(results,lemma,scen, False, True)


library_params = {
    "ACT" : ["AttackerDomain"],
    "ACN" : ["AttackerDomainFresh"],
    "RO" : ["FreshDomain"],
    "PI1" : ["PreImage"],
    "PI2" : ["SndPreImage"],
    "CP" : ["CPcol"],
    "IP" : ["IPcol"],
    "Adv" : ["LengthExtension"],
    "Clo" : ["LEcol"],
    "CloAdv" : ["LengthExtension", "LEcol"],
    "AllCol" : [],
    "CR" : ["CR"],
    "i" : ["iLeak"], # TODO in Library!
    "Ex" : ["ExCol"],
    "SingleHash" : ["SingleHash"],
    "FixedLength" : ["FixedLength"]
#    "IP" : [] # TODO in Library!
    }
# there are the extra param of FixedLength & SingleHash , that we will try to use automatically in case of timeout
# And the extra param CR that needs to be handled specifically

def make_params_for_scen(scen):
    params=[param for cap in scen for param in library_params[cap]]
    if all(x not in scen for x in all_collisions): # if no collision scen is defined, it means CR
        params += ["CR"]
    params = ["-D=%s" % param for param in params]
    return ' '.join(params)


tex_mapper = {
    "ACT" : "\\otT",
    "ACN" : "\\otN",
    "RO" : "\\otF",
    "AllCol" : "\\topt",
    "PI1" : "\\colPIf",
    "PI2" : "\\colPIs",
    "Ex" : "\\colExists",
    "CP" : "\\colCP",
    "IP" : "\\colIP",
    "CloAdv" : "\\topt",
    "Clo" : "\\leClo",
    "Adv" : "\\leAdv",
    "i" : "\\topt"
}

def scen_to_tex(scen):
    tex = ""
    [O] = [tex_mapper[x] for x in scen if x in output]
    tex += "%s &" % O
    if "AllCol" in scen:
        tex += "\\topt &"
    else:
        col1 = [tex_mapper[x] for x in scen if x in collisions_1]
        col2 = [tex_mapper[x] for x in scen if x in collisions_2]
        cols = list(dict.fromkeys(col1+col2))
        if cols:
            tex += "%s&" % ( ",".join(cols))
        else:
            tex += " &"
    le = [tex_mapper[x] for x in scen if x=="Adv" or x=="Clo"]
    if len(le)==2:
        tex += "\\topt &"
    elif len(le)==1:
        [le] = le
        tex += "%s &" % le
    else:
        tex += " &"
    i = [tex_mapper[x] for x in scen if x=="i"]
    if i:
        [i]=i
        tex += "%s " % i
    else:
        tex += " "
    return tex



def gen_tex(data, filename):
    """Generates the tex array for the given list of protocols"""
    # need to escape \t, \n, \b \a
    header_tex_template =  u"""\documentclass[compsoc, conference, letterpaper, 10pt, times, table]{standalone}

\\usepackage[svgnames,dvipsnames]{xcolor}
\\usepackage{pifont}
\\usepackage{multicol}

\\newcommand{\cmark}{\\textcolor{Lime}{\ding{51}}}
\\newcommand{\cannot}{?}
\\newcommand{\\bigcmark}{\\textcolor{Lime}{\ding{52}}}
\\newcommand{\\bluecmark}{\\textcolor{Blue}{\ding{51}}}
\\newcommand{\\bigbluecmark}{\\textcolor{Blue}{\ding{52}}}
\\newcommand{\greycmark}{\\textcolor{Grey}{\ding{51}}}
\\newcommand{\\biggreycmark}{\\textcolor{Grey}{\ding{52}}}
\\newcommand{\qmark}{\\textcolor{Grey}{\ding{51}}}
\\newcommand{\\xmark}{\\textcolor{Red}{\ding{55}}}
\\newcommand{\\bigxmark}{\\textcolor{Red}{\ding{54}}}
\\newcommand{\greyxmark}{\\textcolor{Grey}{\ding{55}}}
\\newcommand{\\biggreyxmark}{\\textcolor{Grey}{\ding{54}}}

\definecolor{darkgreen}{rgb}{0.0, 0.2, 0.13}
\definecolor{darkred}{rgb}{0.55, 0.0, 0.0}
\definecolor{cadmiumgreen}{rgb}{0.0, 0.42, 0.24}
\definecolor{darkblue}{rgb}{0.0, 0.0, 0.55}


%%%%%%%%%%%%% ATOMIC CAPABILITIES AND LATTICE %%%%%%%%%%%%%%%
%%% DO NOT USE THOSE COMMANDS (RESERVED FOR INTERNAL USE)
\\newcommand{\sep}{}
\\newcommand{\DONTUSEatomscen}[2]{\ensuremath{\\textsf{#1}^{\\texttt{#2}}}}
\\newcommand{\otColor}{\color{darkred}}
\\newcommand{\colColor}{\color{orange}}
\\newcommand{\leColor}{\color{darkgreen}}
\\newcommand{\ilColor}{\color{darkblue}}

%%% USE INSTEAD THE COMMANDS BELOW (USER COMMANDS)
\\newcommand{\\bott}{\ensuremath{\\bot}}
\\newcommand{\\topt}{\ensuremath{\\top}}
% OT: Output Type dimension
\\newcommand{\\atomOT}[1]{{\otColor\DONTUSEatomscen{OT}{#1}}}
\\newcommand{\otT}{{\otColor{}advTerm}}
\\newcommand{\otN}{{\otColor{}advName}}
\\newcommand{\otF}{{\otColor{}frshName}}
% COL: Collision dimension
\\newcommand{\\atomCOL}[1]{{\colColor\DONTUSEatomscen{COL}{#1}}}
\\newcommand{\colPIf}{{\colColor{}fstPreImg}}
\\newcommand{\colPIs}{{\colColor{}sndPreImg}}
\\newcommand{\colExists}{{\colColor{}\ensuremath{\exists}}}
\\newcommand{\colCP}{{\colColor{}chsnPrfx}}
\\newcommand{\colIP}{{\colColor{}idtclPrfx}}
% \topp
% \bott
% LE: Length-Extension dimension
\\newcommand{\\atomLE}[1]{{\leColor\DONTUSEatomscen{LE}{#1}}}
\\newcommand{\leClo}{{\leColor{}closure}}
\\newcommand{\leAdv}{{\leColor{}advExtsn}}
% \topp
% \bott
% IL: Input Leak dimension
\\newcommand{\\atomIL}[1]{{\ilColor\DONTUSEatomscen{IL}{#1}}}


\\begin{document}

"""
    table_template = """
\\rowcolors{1}{Gray!30}{}
\\begin{tabular}{ccccc""" + "".join([ "c" for p in LEMMAS]) + """}
"""

    if TABLE_ONLY:
        tex_template =  table_template
        end_tex_template="""\end{tabular}"""
    else:
        tex_template = header_tex_template + table_template
        end_tex_template="""\end{tabular}
\end{document}
"""

    results = data.get()
    tex_template += """\\multicolumn{4}{c}{Threat Scenarios} & \\multicolumn{""" + str(len(LEMMAS)) + """}{c}{Lemmas} \\\\ """
    tex_template += """ \\atomOT{} & \\atomCOL{} & \\atomLE{}  & \\atomIL{} """
    # we compute the set of pertinent scenarios and display the protocols
    scens = set([])
    for lemma in LEMMAS:
        tex_template += """ & %s """ % lemma.replace("_", "\_")
        scens = scens | set(results[lemma].keys())
    tex_template += """\\\\
"""
    scens = list(scens)
    #print(scens)
    for scen in scens:
        tex_template += scen_to_tex(scen_of_string(scen))


        for lemma in LEMMAS:
            try:
                result = results[lemma][scen]
                tex_template += """& """
                if "truesimpl" in result:
                    tex_template += """\cmark$^*$ """
                elif "true" in result:
                    tex_template += """\cmark """
                elif "false" in result:
                    tex_template += """\\xmark """
                else:
                    tex_template += """- """
            except KeyError:  # this scen was added by another lemma, but not populated for the current one, thus it is implied
                tex_template += """& """
                value = get_value(results, lemma,scen_of_string(scen))
                if value == "true":
                    tex_template += """\greycmark """
                elif value == "false":
                    tex_template += """\greyxmark """
                elif value == "truesimpl":
                    tex_template += """\greycmark$^*$ """
                else:
                    tex_template += """ - """

        tex_template += """\\\\
"""
    tex_template += end_tex_template
    with open(filename, 'w') as res_file:
        res_file.write(tex_template)

# base function which calls the subscript computing the results
def call_check(lemma,scen, simplifiers):
    cmd = "%s %s --prove=%s %s" % (PROVER, PROTOCOL, lemma, make_params_for_scen(scen+simplifiers))
    if CORES:
        cmd += " +RTS -N%i -RTS" % (CORES)
    else:
        cmd += " +RTS -N%i -RTS" % (CORES)
    #print("Executing: $%s" % cmd)
    process = subprocess.Popen(cmd.split(),cwd=os.path.dirname(os.path.realpath(__file__)),stderr=subprocess.STDOUT,stdout=subprocess.PIPE, start_new_session=True)
    v.counter += 1
    try:
        output, errors = process.communicate(timeout=TIMEOUT)
        if "Maude returned warning" in str(output):
            return "AssociativeFailure"
        elif "CallStack" in str(output) or "internal error" in str(output):
            return "TamarinError"

        proof_results = [line for line in str(output).split('\\n') if (" "+lemma+" " in line and "steps" in line)]
        if len(proof_results) == 1:
            line = proof_results[0]
            if "verified" in line and simplifiers != []:
                return "truesimpl"
            if "verified" in line and simplifiers == []:
                return "true"
            elif "falsified" in line:
                return "false"
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
        return "timeout"

def load_result_scen_lemma(data, args):
    (scen, lemma, simplifiers) = args
    results=data.get()
    aux = is_already_explored_scenario_for_universal_lemma(results,lemma, scen, True, True)
    if aux==None:
        data.set_lemma_scen(lemma,scen, call_check(lemma,scen, simplifiers))
    elif aux=="true":
        data.set_lemma_scen(lemma,scen, "true")
    elif aux=="false":
        data.set_lemma_scen(lemma,scen, "false")
    elif aux=="truesimpl":
        data.set_lemma_scen(lemma,scen, "truesimpl")
    data.length_minus()
    #print("%i scenarios remaining" % data.get_length())
    # uncomment bellow to compute the full graph
    # elif aux:
    #     data.set_lemma_scen(lemma,scen, "true")
    # elif not(aux):
    #     data.set_lemma_scen(lemma,scen, "false")



def load_results(data):

    pool = Pool(processes=JOBS)
    first_args = [(scen, lemma, SIMPLIFIERS) for lemma in LEMMAS for scen in COMPRESSED_SCENARIOS if scen in first_scenarios]
    next_args = [(scen, lemma, SIMPLIFIERS) for lemma in LEMMAS for scen in COMPRESSED_SCENARIOS if not(scen in first_scenarios)]
    data.set_length(len(first_args)+len(next_args))
    res = pool.map(partial(load_result_scen_lemma,data), first_args,chunksize=1)
    next_args.sort(reverse=False,key=lambda x: len(x[0]))
    res = pool.map(partial(load_result_scen_lemma,data), next_args,chunksize=1)
    pool.close()
    # remainder = []
    # for scen in scenarios:
    #     if any(scen in results[prot].keys() for prot in prots):
    #         for prot in prots:
    #             if not(scen in results[prot].keys()):
    #                 remainder.append((prot,scen))
    # pool = Pool()
    # res = pool.map(load_remainder_trivia,remainder)
    # for ((prot,scen),i) in zip(remainder,res):
    #     results[prot][scen] = i

def retry_failures(data):
    results = data.get()
    pool = Pool(processes=JOBS)
    args = [(scen_of_string(scen), lemma, SIMPLIFIERS) for lemma in LEMMAS for scen in results[lemma].keys() if not(results[lemma][scen] in ["true","truesimpl","false"]) ]

    data.set_length(len(args))
    res = pool.map(partial(load_result_scen_lemma,data), args)
    pool.close()

# def check_failures():
#     for prot in prots:
#         for scen in results[prot].keys():
#             if 'failure' in results[prot][scen]:
#                 new = load_remainder([prot,scen])
#                 if new != results[prot][scen]:
#                     print([prot,results[prot][scen],new,scen])
#                     results[prot][scen] = new



def getManager():
    m = BaseManager()
    m.start()
    return m


default_cores = min(os.cpu_count(),8)

default_prover = "tamarin-concat"
default_timeout = 30 # in seconds

simplifier_params = ["SingleHash", "FixedLength"]

parser = argparse.ArgumentParser()
parser.add_argument('protocol', help='the tamarin file to inspect')
parser.add_argument('-l','--lemmas', nargs='+', required=True, help='List of lemmas to test')
parser.add_argument('-s','--scen', nargs='+',  help='A scenario to test, all by default')
parser.add_argument('-fs','--filesave', nargs='+', help='Save results into file')
parser.add_argument('-lt','--latex', action="store_true", help='Save results into a latex file')
parser.add_argument('-olt','--outputlatex', help='Latex file name')
parser.add_argument('-p','--prover', default=default_prover, help='Prover command nameto use, tamarin-prover by default')
parser.add_argument('-fl','--fileload', nargs='+', help='Load results from file')
parser.add_argument('-t','--timeout', default=default_timeout, type=int, help='Timeout for prover execution')
parser.add_argument('-c','--cores', type=int,  help='Number of core for one job, default = 8')
parser.add_argument('-j','--jobs', type=int, help='Number of parallel jobs, default = total cores/cores ')
parser.add_argument('-rt','--retry', action="store_true",  help='For timeout jobs, retry to prove them')
parser.add_argument('-si','--simp', action="store_true",  help='Enables the simplifiers')
parser.add_argument('-to','--tableonly', action="store_true",  help='Latex output only contains the table')
args = parser.parse_args()

if args.scen:
    SCENARIOS =[args.scen]
else:
    SCENARIOS = scenarios


def no_dup(lst):
    list_of_setscen = map(set,lst)
    deduplicated_list = list()
    for item in list_of_setscen:
        if item not in deduplicated_list:
            deduplicated_list.append(item)
    return list(map(list,deduplicated_list))

SCENARIOS = list(map(apply_redundancy_col,no_dup(SCENARIOS)))


COMPRESSED_SCENARIOS = list(map(apply_redundancy,SCENARIOS))

PROTOCOL = args.protocol
LEMMAS = args.lemmas
PROVER = args.prover

TABLE_ONLY = args.tableonly

if args.simp:
    SIMPLIFIERS = simplifier_params
else:
    SIMPLIFIERS = []

inittime = time.time()

mana = Manager()
v = mana.Namespace()
v.counter = 0

#print("Checking %i scenarios for %i lemmas" % (len(COMPRESSED_SCENARIOS), len(LEMMAS)))
#print(COMPRESSED_SCENARIOS)
if args.jobs and args.cores:
    JOBS = args.jobs
    CORES = args.cores
elif args.cores:
    JOBS = int(os.cpu_count() / args.cores)
    CORES = args.cores
elif args.jobs:
    CORES = min(int(os.cpu_count() / args.jobs),8)
    JOBS = args.jobs
else:
    CORES = min(os.cpu_count(),8)
    JOBS = int(os.cpu_count() / CORES)

TIMEOUT = args.timeout

manager = getManager()
data = manager.myresult(0)

if args.fileload:
    import numpy
    filename = args.fileload[0]
    results = numpy.load(filename+".npy", allow_pickle=True).item()
    data.set(results)
else:
    results = {}
    for lemma in LEMMAS:
        results[lemma] = {}

    data.set(results)
    load_results(data)

RESULTS = data.get()
#print("Uncompressed results")
#print(RESULTS)

# Here, we have populated a set of results over a compressed set of scenario.
# We first infer the full set of results
if not(args.fileload):
    full_results = {}
    for lemma in LEMMAS:
        full_results[lemma] = {}
        for sc in SCENARIOS:
            strsc = string_of_scen(sc)
            res = get_value(RESULTS, lemma, sc)
            if res=="true":
                full_results[lemma][strsc] = "true"
            elif res=="false":
                full_results[lemma][strsc] = "false"
            elif res=="truesimpl":
                full_results[lemma][strsc] = "truesimpl"
            else:
                try:
                    if not( RESULTS[lemma][strsc] in ["true", "truesimpl", "false"]):
                        full_results[lemma][strsc] = RESULTS[lemma][strsc]
                except:
                        full_results[lemma][strsc] = "missing"

                # We can now compress over this set of full_results
    compressed_results = {}
    for lemma in LEMMAS:
        compressed_results[lemma] = {}
        for sc in SCENARIOS:
            strsc = string_of_scen(sc)
            if is_already_explored_scenario_for_universal_lemma(full_results, lemma, sc, False, False)  == None:
                # if the scenario is maximal, we get its value
                compressed_results[lemma][strsc] = full_results[lemma][strsc]

            # else:
            #     try:
            #         if not( full_results[lemma][strsc] in ["true", "truesimpl", "false" ]):
            #             compressed_results[lemma][strsc] = full_results[lemma][sc]
            #     except: ()

    data.set(compressed_results)

if args.retry:
    retry_failures(data)

    RESULTS = data.get()
    compressed_results = {}
    for lemma in LEMMAS:
        compressed_results[lemma] = {}
        for sc in RESULTS[lemma].keys():
            if is_already_explored_scenario_for_universal_lemma(RESULTS, lemma, scen_of_string(sc), False,False) == None:
                compressed_results[lemma][sc] = RESULTS[lemma][sc]
            # elif not( RESULTS[lemma][sc] in ["true", "truesimpl", "false"] ):
            #     compressed_results[lemma][sc] = RESULTS[lemma][sc]
    data.set(compressed_results)

RESULTS = data.get()


if args.filesave:
    import numpy
    filename = args.filesave[0]
    numpy.save(filename,RESULTS)

print("Compressed Results")
print(json.dumps(RESULTS, indent=4))

print("TOTAL Tamarin calls: " + str(v.counter))

fulltime = time.time() - inittime
print("TOTAL execution time for"+ PROTOCOL+ ": " + str(fulltime) )
timed_results = {}
for lemma in LEMMAS:
    timed_results[lemma] = {}
    for sc in RESULTS[lemma].keys():
        if RESULTS[lemma][sc] == "timeout":
            timed_results[lemma][sc] = ("timeout", TIMEOUT)
        elif RESULTS[lemma][sc] in ["true","false","truesimpl"]:
            starttime = time.time()
            if RESULTS[lemma][sc]=="truesimpl":
                sim = SIMPLIFIERS
            else:
                sim = []
            value = call_check(lemma,scen_of_string(sc),sim)
            totaltime = time.time() - starttime
            if value == RESULTS[lemma][sc]:
                timed_results[lemma][sc] = (RESULTS[lemma][sc],totaltime)
            else:
                timed_results[lemma][sc] = (RESULTS[lemma][sc],"DOES NOT RUN, ONLY IMPLIED")
        else:
            timed_results[lemma][sc] = RESULTS[lemma][sc]
data.set(timed_results)

RESULTS = data.get()



print("Timed Results")
print(json.dumps(RESULTS, indent=4))


if args.outputlatex:
    filename = args.outputlatex
else:
    filename = PROTOCOL + "-".join(LEMMAS)+".tex"

if args.latex:
    gen_tex(data, filename)
