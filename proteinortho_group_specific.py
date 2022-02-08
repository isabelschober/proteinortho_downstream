#! /usr/bin/python
import sys
from Bio import SeqIO
import textwrap
import argparse

'''

For two groups of genomes in a proteinortho analysis, find all group-specific core sequences 
(sequences that are present in all genomes of one group, but in none of the other)
Define one group, all others are in the other group


Usage:

python proteinortho_parser3.py -p <my_project>.proteinortho -f <faa_folder> -o <output_string> 
-a <strainA1.faa,strainA2.faa,strainA3.faa,...> 

<my_project>.proteinortho: proteinortho output calculated with --singles option

<faa_folder>: path to folder containing the files that were used as input for proteinortho (faa or ffn)

<output_string>: a strain denoting the output fasta file of this script.

<strainA1.faa,strainA2.faa,strainA3.faa,...>: faa file names of all genomes in the first group. Comma separated without spaces.

'''


def main(argv):
    
    #initialize
    
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--proteinortho', required=True, help='<my_project>.proteinortho Proteinortho output calculated with --singles option')
	parser.add_argument('-f', '--folder', required=True, help='Path to folder containing the files that were used as input for proteinortho (faa or ffn)')
	parser.add_argument('-a', '--groupA', required=True, help='<strainA1.faa,strainA2.faa,strainA3.faa,...>: faa/ffn file names of all genomes in "groupA". Comma separated without spaces.')
	parser.add_argument('-o', '--output', default="Group_specific_proteinortho", help='A string denoting the output fasta file of this script.')
	args = parser.parse_args()
    
	proteinortho=open(args.proteinortho)
	faa_folder=args.folder
	out_string=args.output
	setA_strains=args.groupA.split(",")

	out={"setA":[],"setB":[]}
	
	setA_cols=[]
	setB_cols=[]
    
    
    #collect locus_tags of the sequences to be printed to output
    
    #go through proteinortho output
	for line in proteinortho:
		lsplit=line.split("\t")
		#header line -> find the columns that contain the set strains and intitialize dictionary for results
		if line.startswith("#"):
			for n in range(3,len(lsplit)):
				if lsplit[n].strip() in setA_strains:
					#print lsplit[n].strip()
					setA_cols.append(n)
				else:
					setB_cols.append(n)
				
				if setA_strains[0]==lsplit[n].strip():
					setA_ref=n
			print()
			print(len(setA_cols))
			#check if all strains named in input are present in the proteinortho output		
			if len(setA_strains)!=len(setA_cols):
				#print setA_cols
				print("\nError in strain names!\n")		
		
		#all other lines	
		else:
			#collect the row's entry for the set strains
			set_lineA=[]
			for n in setA_cols:
				set_lineA.append(lsplit[n].strip())
			set_lineB=[]	
			for n in setB_cols:
				set_lineB.append(lsplit[n].strip())
				

			#if sequence is not present in any of the set strains
			if (set(set_lineB)==set(["*"]) and "*" not in set_lineA):
				print(line)
				#go through all the cells in the row
				for n in range(3,len(lsplit)):
					#if there is a sequence in the strain and the strain is setA reference
					if lsplit[n].strip()!="*" and n==setA_ref:
						out["setA"].append(lsplit[n].strip())


	

	strainA_faa=SeqIO.index(faa_folder+"/"+setA_strains[0],"fasta")
	out_faa_A=open(out_string+".fasta","w")

		
	#write all genes in the strain's dictionary list to new faa file
	for gene in sorted(out["setA"]):
		out_faa_A.write(">"+strainA_faa[gene.split(",")[0]].id+" "+strainA_faa[gene.split(",")[0]].description+"\n")
		for line in textwrap.wrap(str(strainA_faa[gene.split(",")[0]].seq)+"\n",60):
			out_faa_A.write(line+"\n")

     
if __name__ == '__main__':   
    main(sys.argv)
