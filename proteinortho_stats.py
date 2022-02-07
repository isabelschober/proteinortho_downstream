#! /usr/bin/python

import sys
import os
import argparse

'''
By Isabel

proteinortho has to have been run wit the -singles option!

Usage: python proteinortho_stats.py <my_project.proteinortho> 
'''

def main(argv):
	
	parser=argparse.ArgumentParser()
	parser.add_argument('-p', '--proteinortho', required=True, help="<my_project.proteinortho> Proteinortho output calculated with -singles option")
	parser.add_argument('-m', '--mode', default='basic', choices=['basic','input','unique','all'], 
						help='What information should the script return? basic: Number of input sequences, sequence type, pan- and core-genome counts. input: Number of input sequences per strain. unique: Number of unique sequences per strain. all: all of the above. Default: basic ')
	args = parser.parse_args()
	
	proteinortho=open(args.proteinortho)
	mode=args.mode
	
	count_pan=0
	count_core=0
	genomes={}
	
	for line in proteinortho:
		lsplit=line.split("\t")
		
		if line.startswith("#"):
			number_genomes=len(lsplit)-3
			n=3
			for split in lsplit[3:]:
				genomes[str(n)+"_"+split.strip()]=[0,0]
				n+=1
			if ".faa" in lsplit[-1]:
				seqtype="protein sequences"
			elif ".ffn" in lsplit[-1]:
				seqtype="nucleotide sequences"
			else:
				seqtype="unknown"
				
		else:
			count_pan+=1
			if lsplit[0]==str(number_genomes):
				count_core+=1
			elif lsplit[0]=="1":
				n=3
				for split in lsplit[3:]:
					if split.strip()!="*":
						for key in genomes.keys():
							if key.split("_")[0]==str(n):
								genomes[key][1]+=1
						n+=1
					else:
						n+=1
			n=3
			for split in lsplit[3:]:
				if split.strip()!="*":
					for key in genomes.keys():
						if key.split("_")[0]==str(n):
							genomes[key][0]+=len(split.split(","))
				n+=1
				
	for key in list(genomes.keys()):
		genomes["_".join(key.split("_")[1:])]=genomes[key]
		del genomes[key]

	print("\n"+args.proteinortho+"\n")
	if mode=="basic" or mode=="all":
		print("Number of genomes: "+str(number_genomes))
		print("Sequence type: "+seqtype)
		print("Pan-genome count: "+str(count_pan))
		print("Core-genome count: "+str(count_core)+"\n")
	if mode=="input" or mode=="all":
		print("Number of input sequences per strain")
		for key in sorted(genomes.keys()):
			print(key+": "+str(genomes[key][0]))
	if mode=="unique" or mode=="all":
		print("\n"+"Number of unique sequences per strain")
		for key in sorted(genomes.keys()):
			print(key+": "+str(genomes[key][1]))

	
	
if __name__ == "__main__":
   main(sys.argv)

