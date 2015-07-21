###About this project:

- **Project date**: 10/10/2013

- **Objective**: Write a program that retrieves information across health science databases based on a search query and use that information to create a biology-themed card game.

- **Outcome**: Wrote a program in Biopython that automates the use of a federated search engine, known as Entrez, to find proto-oncogenes found in humans. The program fetches information about each proto-oncogene and filters the analyzed results to obtain 30 proto-oncogenes deemed unique by the team’s defined criteria. The program then outputs the 30 proto-oncogenes and their information in a formatted text file, which is then used to create a card game.

- **Contribution**: Took the initiative of developing the program’s algorithm by learning Biopython and then teaching it to the rest of the team members. Wrote the majority of the structural code as well as its documentation and made sure team members understood how the program’s algorithm worked.

###How to use:

1. Install Biopython (http://biopython.org/wiki/Download)
2. Run *entrez_proto-oncogene.py* via command-line: ```python entrez_proto-oncogene.py```
3. Open *output.txt* to view the results. (Located in the same directory as entrez_proto-oncogene.py)

###Notes:
- This program was created and run using Biopython 1.62 and Python 2.7.5 in September/October 2013. Current updates to Biopython, Python, or the Entrez database may or may not be compatible with the final version of the code.
