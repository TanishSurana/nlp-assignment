import nltk
import sys
import re

from nltk.tokenize import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

'''
I had a country walk on Thursday 

N V det Adj N P N

came home in a dreadful mess.

V N P det Adj N



'''

NONTERMINALS = """
S -> S Conj S | NP VP | S Conj VP
VP -> VP NP | V | VP NP PP | Adv VP | VP PP Adv | VP Adv
NP -> Det N | N | AP N | PP N | Det N AP
NP -> Det N | Det NP | AP NP | PP NP | NP PP
AP -> Adj | AP Adj
PP -> P NP | P 

"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    nltk.download('punkt')
    words = word_tokenize(sentence)

    litt = []
    for w in words:
        ww = w.lower()
        if ww.islower():
            litt.append(ww)
    return litt


def np_check_sub(tree):
    count = 0
    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and count != 0:
            return False
        count += 1
    return True

def np_parser(tree):
    litt = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # tree has label 
            if np_check_sub(subtree):
                litt.append(subtree)

    return litt


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    return np_parser(tree)
            


if __name__ == "__main__":
    main()
