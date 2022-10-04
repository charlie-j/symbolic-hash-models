import subprocess, sys, re, os, argparse, logging, datetime, shutil




def iterFolder(folder):
	""" Yields all files in the folder that have a .spthy ending. """
	for dname, dirs, files in os.walk(folder):
		for fname in files:
			fpath = os.path.join(dname, fname)
			if not fpath.endswith(".spthy"):
				continue
			yield fpath



def parseFile(path):
	"""
	Parses a _analyzed.spthy file and returns their content in a tuple

	(lemmas([str]), results([bool]), steps([int]), time(float), proof)
	Note that time is not a list but a single value.
	If there is an error, the error message is returned as a string
	"""

	## open file ##
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
		parsed = re.findall(r"(\w+) (?:\(.*\))?:(?!  ) (.*) \((\d+) steps\)\n", summary)
		parsed = [(lemmas, res=="verified", int(steps)) for (lemmas, res, steps) in parsed]  # convert types
		#print(parsed)
		#parsed = list(zip(*parsed))             # transpose matrix
		#if (parsed == []): parsed = [[],[],[]]  #
		return parsed

	except Exception as ex:
		return f"Parse error - lemmas: {path}"






def main():
	startTime = datetime.datetime.now() 

	main_folder = ["original","distance_bounding","Tesla","ake"]
	subfolders = ["pre","new_pre"]
	
	outputL = {}
	sortMap = {}		
	for path1 in main_folder:
		for path2 in subfolders:
			if not(path2=="new_pre" and (path1=="ake" or path1=="csf-12")):
				sortMap[path1+'/'+path2] = set()
				for pathCom in iterFolder(path1+'/'+path2):
					sortMap[path1+'/'+path2].add(pathCom)
					process = subprocess.Popen("tamarin-prover --prove "+pathCom, shell=True, stdout=subprocess.PIPE)
					process_return = process.stdout.read()
					parsedLemmas = parseFile(process_return.decode("utf-8"))
					outputL[pathCom] = parsedLemmas
	

	main_folder_keys = sorted(main_folder)
	subfolders_keys = sorted(subfolders)
	output=""
	for mk in main_folder_keys:
		print(mk)
		output+=mk+"\n"
		print("    ")
		output+="    \n"
		for sk in subfolders_keys:
			if not(sk=="new_pre" and (mk=="ake" or mk=="csf-12")):
				print("    "+sk)
				output+="    "+sk+"\n"
				for value in sortMap[mk+"/"+sk]:
					print("        "+value)
					output+="        "+value+"\n"
					print("    ")
					output+="    \n"
					for tup in outputL[value]:
						print("            lemma "+str(tup[0])+": "+str(tup[1])+" in "+str(tup[2])+" steps")
						output+="            lemma "+str(tup[0])+": "+str(tup[1])+" in "+str(tup[2])+" steps\n"
					print("    ")
					output+="    \n"
		print("    ")
		output+="    \n"
		print("    ")
		output+="    \n"

	with open("results","w+") as f:
		f.write(output)
	## measure time ##
	print(f"\nTime elapsed: {str(datetime.datetime.now() - startTime).split('.')[0]}s")
	exit(0)

if __name__ == '__main__':
	main()
