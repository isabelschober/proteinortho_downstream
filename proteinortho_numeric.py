#! /usr/bin/python

import sys
import os
import argparse

'''
By Isabel

proteinortho has to have been run with the -singles option!

Usage: python proteinortho_numeric.py <my_project.proteinortho> 
'''

def main(argv):
    
	parser=argparse.ArgumentParser()
	parser.add_argument('-p', '--proteinortho', required=True, help="<my_project.proteinortho> Proteinortho output calculated with -singles option")
	parser.add_argument('-m', '--mode', default='numeric', choices=['numeric','binary'], 
						help='numeric mode gives the number of paralogs present in a genome, binary mode gives out only 1 (gene family present)/ 0 (gene family not present)')

		
	args = parser.parse_args()
	
	proteinortho=open(args.proteinortho)
	if args.mode=="numeric":
		proteinortho_num=open(args.proteinortho+"_numeric.txt","w")
	elif args.mode=="binary":
		proteinortho_num=open(args.proteinortho+"_binary.txt","w")
	n=0
	
	for line in proteinortho:
		if line.startswith("#"):
			proteinortho_num.write("FAM_ID"+"\t"+"\t".join(line.replace(".faa","").split("\t")[3:]))
			n=n+1
		else:
			proteinortho_num.write("group"+str(n))
			lsplit=line.split("\t")
			for i in range(3,len(lsplit)):
				if lsplit[i]=="*" or lsplit[i]=="*\n":
					proteinortho_num.write("\t0")
				elif args.mode=="numeric":
					proteinortho_num.write("\t"+str(len(lsplit[i].split(","))))
				elif args.mode=="binary":
					proteinortho_num.write("\t1")
			proteinortho_num.write("\n")
			n=n+1
	
    
if __name__ == "__main__":
   main(sys.argv)
