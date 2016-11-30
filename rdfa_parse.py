from rdflib import Graph

if __name__ == '__main__':
    g = Graph()

    g.parse('http://www.worldcat.org/title/library-of-babel/oclc/44089369', format='rdfa')

    print "Books found:"
    import ipdb; ipdb.set_trace()
    for row in g.query("""SELECT ?title ?author WHERE { 
       [ a schema:Book ; 
         schema:author [ rdfs:label ?author ] ;
         schema:name ?title ]
       FILTER (LANG(?title) = 'en') } """):

        print "%s by %s"%(row.title, row.author)
