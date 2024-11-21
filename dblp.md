# Extract publications of ORCID members from DBLP

## Script
Don't forget to insert your orcids!

Create a code.sparql file with the following content, edited to your needs.

```sparql
PREFIX dblp: <https://dblp.org/rdf/schema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT DISTINCT ?orcid ?person ?name ?publ ?title ?type ?publicationDate ?doi ?venue (GROUP_CONCAT(DISTINCT ?coauthorName; separator=", ") AS ?coauthors)  WHERE {
  VALUES ?orcid {
    <https://orcid.org/0000-0002-0000-0000>
    <https://orcid.org/0000-0002-0000-0001>
    ...

  }

  ?person dblp:orcid ?orcid .
  ?person rdfs:label ?name .

  ?publ dblp:authoredBy ?person .
  ?publ dblp:title ?title .
  ?publ dblp:yearOfEvent ?publicationDate .
  ?publ dblp:doi ?doi .

  ?publ a ?type .
  OPTIONAL { ?publ dblp:publishedIn ?venue . }

  # Fetch coauthors
  ?publ dblp:authoredBy ?coauthor .
  ?coauthor rdfs:label ?coauthorName .
  FILTER(?coauthor != ?person).  # Exclude the main author
  FILTER(?publicationDate >= "2021"^^xsd:gYear && ?publicationDate <= "2023"^^xsd:gYear).

}
GROUP BY ?orcid ?person ?name ?publ ?title ?publicationDate ?doi ?type ?venue
ORDER BY ?publicationDate
LIMIT 1000
```

## Endpoint

Run this curl command to execute the content of the code.sparql file.

```bash
curl -v -o output.csv -H "Accept: text/csv" -H "Content-type: application/sparql-query" -d @code.sparql https://sparql.dblp.org/sparql
```
