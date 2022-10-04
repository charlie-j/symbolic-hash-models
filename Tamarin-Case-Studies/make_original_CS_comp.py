import json
  
# Opening JSON file
ET_original = {}
for suffix in ["","_1","_2","_3"]:
	f = open('ET-CaseStudies/original_results'+suffix+'.json')
  
	# returns JSON object as 
	# a dictionary
	data = json.load(f)
	for k in data.keys():
		try:
			test = ET_original[k]
		except Exception:
			ET_original[k] = {}	
		for [lem,res] in data[k]:
			#print(k,lem,res)
			try:
				ET_original[k][lem].append(res)
			except Exception:			
				ET_original[k][lem] = list()
				ET_original[k][lem].append(res)
	# Closing file
	f.close()

#print(json.dumps(ET_original))
  
  
CONC_original = {}
for suffix in ["","_1","_2","_3"]:
	f = open('Concatenation/original_results'+suffix+'.json')
  
	# returns JSON object as 
	# a dictionary
	data = json.load(f)
	for k in data.keys():
		try:
			test = CONC_original[k]
		except Exception:
			CONC_original[k] = {}	
		for [lem,res] in data[k]:
			#print(k,lem,res)
			try:
				CONC_original[k][lem].append(res)
			except Exception:			
				CONC_original[k][lem] = list()
				CONC_original[k][lem].append(res)
	# Closing file
	f.close()

#print(json.dumps(CONC_original))

ComparisionMap = [ ("Flickr/Flickr.spthy","original/Flickr.spthy","Flickr"),
("IKE/IKE_NoCookie/ikeV2_HEB_A.spthy","original/ikeV2_HF_EC_nocookie.spthy","IKE_NoCookie"),
("SSH/sshV2_HEB_A.spthy","original/sshV2_HF_EC.spthy","SSH"),
("Telegram/telegram_with_HEB.spthy","original/telegram_with_HEB.spthy","Telegram"),
("IKE/IKE_Cookie/ikeV2_HEB_A.spthy","original/ikeV2_HF_EC.spthy","IKE_Cookie"),
("Sigma/sigma.spthy","original/sigma.spthy","Sigma"),
]

ComparisionJSON = {}
for (k,k1,k2) in ComparisionMap:
	ComparisionJSON[k2+"_ET"] = ET_original[k1]
	ComparisionJSON[k2+"_CONC"] = CONC_original[k]

print(json.dumps(ComparisionJSON, indent=4))