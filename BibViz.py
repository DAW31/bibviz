#!/usr/bin/env python3

import sys
import bibtexparser
#import unicodecsv as csv

from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from tinydb import TinyDB, Query

titleid=0
authorid=0

# There is no bibtex file to read
if len(sys.argv) == 1:
    print("Usage: ", sys.argv[0], " bibtex_file_1.bib bibtex_file_2.bib ... bibtex_file_N.bib");
# There is at least one bibtex file to read
else:

        # Create an empty list
        bib_database_set = [];

        # Process every bibtex file
        for i in range(1, len(sys.argv)):

            # Open the file is read it into a string
            with open(sys.argv[i]) as bibtex_file:
                bibtex_str = bibtex_file.read()

            # Create a bibtex parser
            parser = BibTexParser()
            parser.customization = convert_to_unicode

            # Process the string and add the corresponding BibDatabase into the list
            bib_database_set.append(bibtexparser.loads(bibtex_str, parser=parser));

        # Print the number of BibDatabase objects in bib_database_set
        print(len(bib_database_set))

        # Record the max number of authors
        max_number_of_authors = 1;

        # Process all the BibDatabase of the list
        for j in range(len(bib_database_set)):

            # Find the number of authors
            for entry_key in bib_database_set[j].entries_dict:
                # Get the authors
                authors = bib_database_set[j].entries_dict[entry_key]['author'];

                # Get the number of authors
                number_of_authors = authors.count(' and ') + 1;

                # Update the max number of authors
                max_number_of_authors = max(number_of_authors, max_number_of_authors);


        # Process all the BibDatabase of the list
        for j in range(len(bib_database_set)):
            print("Process ", sys.argv[j + 1])
            # Print the bibtex entry key, author and title of the corresponding BibDatabase object
            for entry_key in bib_database_set[j].entries_dict:

                # This is a paper in a conference:
                pub_venue="";
                if bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'] == "inproceedings":
                    pub_venue = bib_database_set[j].entries_dict[entry_key]['booktitle'];
                elif bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'] == "article":
                    pub_venue = bib_database_set[j].entries_dict[entry_key]['journal'];
                else:
                    pub_venue = "Unknown, ask Franck what ";
                    pub_venue += bib_database_set[j].entries_dict[entry_key]['ENTRYTYPE'];
                    pub_venue += " is.";

                # Get the year
                year = bib_database_set[j].entries_dict[entry_key]['year'];

                # Get the booktitle
                booktitle = bib_database_set[j].entries_dict[entry_key]['booktitle'];

                # Get the title
                title = bib_database_set[j].entries_dict[entry_key]['title'];

                # Get the authors
                authors = bib_database_set[j].entries_dict[entry_key]['author'];

                # Get the number of authors
                number_of_authors = authors.count(' and ') + 1;

                db = TinyDB('db.json')
                authors_table = db.table('authors')
                titles_table = db.table('titles')
                connections_table = db.table('connections')
                titleid=titleid+1

                titles_table.insert({'TitleID': titleid,'Title': title,'Booktitle': booktitle,'Year': year})
                
                # Find all the authors
                authors_split = authors.split(' and ');
                for author in authors_split:
                    name_components = author.split(', ');
                    authorid=authorid+1
                    connections_table.insert({'TitleID': titleid,'AuthorID': authorid})
                    G.add_edge(authorid, titleid)
                    if len(name_components) == 1:
                        authors_table.insert({'AuthorID': authorid,'Author': author})
                    else:
                        firstnames = name_components[1].split(' ');
                        short_name = "";
                        for firstname in firstnames:
                            short_name += firstname[0];
                            short_name += ". ";
                        short_name += name_components[0];
                        authors_table.insert({'AuthorID': authorid,'Author': short_name})

                #print("Entry key: ", entry_key)  

                print(db);
                print("Author(s): ", authors);
                print("Booktitle: ", booktitle);
                print("Title: ", title);
                print("Year: ", year);
                print();
