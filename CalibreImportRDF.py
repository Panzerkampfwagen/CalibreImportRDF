# Prerequisites: python2-rdflib, python2-rdfextras

import rdflib
import pprint
#Couple of handy namespaces to use later
RDF    = rdflib.namespace.RDF
RDFN   = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
BIB    = rdflib.Namespace("http://purl.org/net/biblio#")
FOAF   = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
ZOTERO = rdflib.Namespace("http://www.zotero.org/namespaces/export#")
DC     = rdflib.Namespace("http://purl.org/dc/elements/1.1/")

File="ZoteroBibliography.rdf"
g = rdflib.Graph()
g.parse(File) 
#So that we are sure we get something back
print "Number of triples",len(g)


# List all books
Book_List=[k for k in g.subjects(RDF.type,BIB["Book"])]
#Article for wich we want the list of authors
for Book in Book_List:
    for Title in g.triples((Book,DC["title"],None)):
        print "Title: ", Title[2]
    #print Book
    #First loop filters is equivalent to "get all authors for article x" 
    for triple in g.triples((Book,BIB["authors"],None)):
        #print "Triple: ",triple,"\n"
        #This expresions removes the rdf:type predicate cause we only want the bnodes
        # of the form http://www.w3.org/1999/02/22-rdf-syntax-ns#_SEQ_NUMBER
        # where SEQ_NUMBER is the index of the element in the rdf:Seq
        list_triples = filter(lambda y: RDF['type'] != y[1], g.triples((triple[2],None,None)))
        #We sort the authors by the predicate of the triple - order in sequences do matter ;-)
        # so "http://www.w3.org/1999/02/22-rdf-syntax-ns#_435"[44:] returns 435
        # and since we want numberic order we do int(x[1][44:]) - (BTW x[1] is the predicate)
        authors_sorted =  sorted(list_triples,key=lambda x: int(x[1][44:]))
        #We iterate the authors bNodes and we get surname and givenname
        i=0
        for author_bnode in authors_sorted:
            for x in g.triples((author_bnode[2],FOAF['surname'],None)):
                author_surname = x[2]
                #Author counter to print at the bottom		  
	        for y in g.triples((author_bnode[2],FOAF['givenname'],None)):
                    author_name = y[2]
                    print "\tauthor(%s): %s %s"%(i,author_name,author_surname)
                    i += 1
    print "\n"
