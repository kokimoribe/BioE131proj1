#! /usr/bin/python

"""
Yi-hsuan Fu
Koki Moribe
Hye-In Son

Note:
We obtained our information for each card from the Entrez search engine using Biopython.
Instead of printing out the results as we find them, we decided to create a simple Python class called Card so that we have Card objects to store the information about each card.
We thought that having a Card class can leave the code open for additional features like converting each Card object to HTML (so that it visually looks like a card), or using these Card objects for a code-implementation of the actual game.

Our theme for our deck is proto-oncogenes found in humans.

Here's the general approach for our code:
1)define Card class
2)use Bio.Entrez to get a list of search results of proto-oncogenes in humans in the gene database.
3)get the IDs for the search results
4)look up the specific proto-oncogene using Bio.Entrez with the specific gene ID to obtain the necessary information
5)create a Card object using the information found
6)add the Card object to our list of Cards
7)repeat 4) to 7) until we build 30 cards
8)write the string represenation of the Card objects into an output file.

"""


#Card class to hold our information
class Card(object):

	def __init__(self, num, name, symbol, geneID, summary, chromosome, exon, weight, bp, variants, homologs, publications, domains):
		self.num = num #card number
		self.name = name #name of proto-oncogene
		self.symbol = symbol #symbol of proto-oncogene
		self.summary = summary #summary of proto-oncogene
		self.geneID = geneID
		self.chromosome = int(chromosome) #chromosome #
		self.exon = int(exon) #number of exons
		self.weight = int(weight) #gene weight
		self.bp = int(bp) #base pairs
		self.variants = int(variants) #related # of mRNA variants
		self.homologs = int(homologs)
		self.publications = int(publications)
		self.domains = int(domains)

	#define a string representation of the card
	#this will be what gets written to the output file at the end
	def __str__(self):
		return "CARD #{0}\nname: {1}\nsymbol: {2}\ngeneID: {3}\nchromosome #: {4}\n# of exons: {5}\ngene weight: {6}\nbp: {7}\n# of related mRNA variants: {8}\nhomologs: {9}\nRelated articles with homology group: {10}\n# of conserved domains: {11}\nsummary: {12}\n".format(self.num, self.name, self.symbol, self.geneID, self.chromosome, self.exon, self.weight, self.bp, self.variants, self.homologs, self.publications, self.domains, self.summary)

import sys
from Bio import Entrez
Entrez.email = "koki.moribe@gmail.com"

#the total number of cards we want in the deck
DECK_SIZE = 30

#name of file to output
OUTPUT_FILENAME = 'output.txt'

#search Entrez in gene database for proto-oncogenes in humans
#have retmax > DECK_SIZE so that we have more than DECK_SIZE search results in case we run into duplicate/unwanted entries
handle = Entrez.esearch(db= "gene", term='(proto-oncogene) AND "Homo sapiens"[porgn:__txid9606]', retmax=DECK_SIZE * 3)
record = Entrez.read(handle)

#oncIDlist will be a list of the gene ids retrieved from the search result
oncIDlist = record["IdList"]

#card will be the list of Card objects. The length of deck at the end will be DECK_SIZE.
deck = []

print("Finding {0} proto-oncogenes . . . ".format(DECK_SIZE))

#begin a while loop, stop when we get DECK_SIZE cards
i = 0
while (len(deck) < DECK_SIZE):
	#get the esummary in the gene database using the ID found at index i in oncIDlist
	handle = Entrez.esummary(db="gene", id=oncIDlist[i])
	record = Entrez.read(handle)

	#this boolean value will be set to True if it is decided that we need to skip the current entry for whatever reason
	skip = False

	#get the full proto-oncogene name
	name = record[0]['Description']

	#get the symbol
	symbol = record[0]['Name']

	#a description of the gene
	summary = record[0]['Summary']

	#the chromosome # this gene is located
	chromosome = record[0]['Chromosome']

	#exon count
	exon = record[0]['GenomicInfo'][0]['ExonCount']

	#gene weight
	weight = record[0]['GeneWeight']

	#find the # of base pairs this gene covers
	stop = record[0]['GenomicInfo'][0]['ChrStop']
	start = record[0]['GenomicInfo'][0]['ChrStart']
	bp = abs(int(stop) - int(start))


	#see how many mRNA transcript variants there are related to this gene
	handle = Entrez.esearch(db="nucleotide", term='{0}[Gene Name] AND mRNA[Filter] AND "Homo sapiens"[porgn:__txid9606] AND {1}[Title]'.format(symbol, symbol))
	record = Entrez.read(handle)
	variants = record['Count']


	handle = Entrez.esearch(db="homologene", term="{0}[Gene ID]".format(oncIDlist[i]))
	record = Entrez.read(handle)

	homologeneID = record['IdList'][0]

	handle = Entrez.efetch(db="homologene", id=homologeneID, rettype="homologene", retmode="text")

	linenum = 0

	homologs = 0

	pubstart = False
	publications = 0

	domainstart = False
	domains = 0

	import re

	for line in handle:
		if pubstart:
			if line.startswith(" See  all ("):
				publications = re.sub("[^0-9]", "", line)
				pubstart = False

		elif domainstart:
			if len(line) == 1:
				domainstart = False
			else:
				domains += 1


		elif line.startswith("&#160"):
			homologs += 1

		elif line.startswith("PublicationsArticles"):
			pubstart = True

		elif line.startswith("Conserved Domains"):
			domainstart = True


	#increment i
	i += 1

	#if skip is set to False, we will skip making a Card object and adding it to the deck if we have a problem with the current result
		#problems can include:
			#info is too similar to another proto-oncogene
			#missing results like no chromosome # or no mRNA transcript variants
	if skip:
		#fortunately, our code does not need to reach here because the first 30 results are fine
		skip = False

		continue

	else:
		#create a Card object with the information we found		
		myCard = Card(i, name, symbol, oncIDlist[i-1], summary, chromosome, exon, weight, bp, variants, homologs, publications, domains)

		#add the newly created object to our list of Cards
		deck.append(myCard)

print("Done.\n")

print("Writing to file {0}. . . ".format(OUTPUT_FILENAME))

#create writable file named OUTPUT_FILENAME
f = open(OUTPUT_FILENAME, 'w')
#iterate through our list of cards and write its string representation to the file
for card in deck:
	f.write(str(card) + "\n")

print("Done.\n")

print("Process completed. Check {0} for results.".format(OUTPUT_FILENAME))
