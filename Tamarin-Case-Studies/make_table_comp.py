import json

f = open('compare.json')
data = json.load(f)

prots = ["Flickr",
"SSH",
"Telegram",
"IKE_NoCookie",
"IKE_Cookie",         
"Sigma"]

factlst=[]
for prot in prots:
    protET = prot + "_ET"
    protEB = prot + "_CONC"    
    for lemma in data[protET]:
        totalET=0
        for timing in data[protET][lemma]:
            totalET += timing[1]
        totalEB=0            
        for timing in data[protEB][lemma]:
            totalEB += timing[1]
        fact = totalEB/totalET
        factlst += [fact]
        print(prot + " & " + lemma + " & " + data[protET][lemma][0][0] + " & " + data[protEB][lemma][0][0] +" & " +  "{:.2f}".format(totalET/4) + " & " +  "{:.2f}".format(totalEB/4) + " & "+   "{:.0f}".format(fact) +
              "\\\\"  )

avg=0
for t in factlst:
    avg += t
    
print(avg/len(factlst))        
            

