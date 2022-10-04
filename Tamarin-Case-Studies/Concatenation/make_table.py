import re

folders = "TIMED_RESULTS_"
ext=".results"

prots = [
    ("example", 10),    
    ("Flickr", 2),
    ("SSH",4),         
    ("TELEGRAM",2),
# "IKE_NoCookie",
#"IKE_Cookie",
    ("Sigma",4),
    ("IKE",3),            
    ("IKE_neutral_nocookie",3),        
    ("IKE_neutral",3),
]

has_quick = ["SSH", "Sigma", "IKE"]

# Threat models imported from auto_paper.py

# We define our different base scenarios, from the naming conventions of the paper
# from left to right, stronger threat model to weaker
output=  ["ACT", "ACN", "RO"] # ! t^To^ND cannot be implemented
collisions_1 = ["PI1", "PI2", "Ex", ""]
collisions_2 = ["CP", "IP", ""] # add "IP" ??
length_ext = ["Adv", ""]
length_col = ["Clo", ""]
input_leak = ["i", ""]

colls=["AllCol"] + [(c1,c2) for c1 in collisions_1 for c2 in collisions_2]

th_per_dim = ([len(x) for x in [output,colls, length_ext, length_col, input_leak]])
spl = 1
for i in th_per_dim:
    spl = spl*i


default_timeout=30 # in seconds
long_timeout=1200 # in seconds

fullrt = 0
for prot in prots:
    calls = 0
    time = 0
    timeouts = 0
    for run in range(1,5):
        filename=folders + str(run) + "/" + prot[0] + ext
        with open(filename,"r") as file:
            for line in file:
                if re.search("TOTAL Tam", line):
                    calls+=int(line.split(" ")[-1])
                if re.search("TOTAL ex", line):
                    time+=float(line.split(" ")[-1])
                if re.search(".*timeout.*", line):
                    timeouts+=1
    hasq = prot[0] in has_quick
    ncalls=0
    ntime=0
    ntimeouts=0
    if hasq:
        for run in range(1,5):
            filename=folders + str(run) + "/" + prot[0] + "_quick" + ext
            with open(filename,"r") as file:
                for line in file:
                    if re.search("TOTAL Tam", line):
                        ncalls+=int(line.split(" ")[-1])
                    if re.search("TOTAL ex", line):
                        ntime+=float(line.split(" ")[-1])
                    if re.search("timeout", line) or re.search("missing", line):
                        ntimeouts+=1
    if hasq:
        calls, ncalls = ncalls, calls
        time, ntime = ntime, time
        timeouts, ntimeouts = ntimeouts, timeouts
    avgcall = calls/4
    avgtime = time/4
    navgcall = ncalls/4
    navgtime = ntime/4
    timeouts = timeouts /2 /4
    ntimeouts = ntimeouts /2 /4    
    avoidedcall = spl*prot[1] - int(avgcall) 
    navoidedcall =  timeouts - int(navgcall)
    totalavoidedcall = spl*prot[1] - int(avgcall) - int(navgcall)
    if hasq:
        snavgcall = str(int(navgcall))
        snavgtime = "{:.1f}".format(navgtime)
        snavoidedcall = str(int(navoidedcall))
    else:
        snavgcall = "-"
        snavgtime = "-"
        snavoidedcall = "-"        
    fullrt += avgtime + navgtime
    print( prot[0] + " & "                  # prot name
           + str(prot[1]) + " & "   # prot nb of lemmas
           
           +  "{:.1f}".format(avgtime)  + " & " # prot averages of main call
           +  str(int(avgcall))  + " & " #
           +  str(avoidedcall)   + " & "           
           +  str(int(timeouts))  + " & "

           
           +  snavgtime + " & " # prot averages of potential second call
           +  snavgcall  + " & "           
           + snavoidedcall
           #+ " & "
           
#           + str(int(totalavoidedcall*100/(spl*prot[1])))   

           
           + "\\\\" )
print(fullrt/60)
