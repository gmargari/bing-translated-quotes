#!/bin/bash

function get_quotes_1() {
    wget -qO- https://raw.githubusercontent.com/wp-plugins/famous-quotes/master/quotes.xml | \
        awk '
        /<author>/ {
            gsub("<[^>]*>", "", $0)     # remove html tags
            gsub("^[ \t]*", "", $0)     # remove trailing white space
            author = $0
        }
        /<text>/ {
            gsub("<[^>]*>", "", $0)     # remove html tags
            gsub("^[ \t]*", "", $0)     # remove trailing white space
            gsub("\"", "", $0)          # remove quotes
            text = $0
            printf "%s#%s\n", text, author 
        }
        '
}

function get_quotes_2() {
    wget -qO- http://www-public.rz.uni-duesseldorf.de/~puschman/MySig/data/famousquotes.txt |
        awk -F "<br>- " ' NR > 2 {
            text = $1
            author = $2
            gsub("<br>", " ", text)     # replace <br>s inside text with spaces    
            gsub("#", " ", text)        # remove #s from text    
            gsub("\"", "", text)        # remove quotes
            gsub("<br>", " ", author)   # replace <br>s inside author with spaces    
            printf "%s#%s\n", text, author
        }'
}

outfile="quotes.en.txt"
get_quotes_1 >  $outfile
get_quotes_2 >> $outfile

tmp=`mktemp`
# https://github.com/gmargari/scripts/blob/master/unique-lines.py
cat $outfile | unique-lines.py > $tmp
mv $tmp $outfile

