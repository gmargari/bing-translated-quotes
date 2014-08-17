1. get-en-quotes.sh
-------------------

Gathers english quotes from various sources and creates the file `quotes.en.txt`. Each line of this file contains a quote in the form: quote text # quote author.

2. translate-en-el.py
---------------------

Translates quotes from english to greek using the Bing API. Reads file `quotes.en.txt` and creates file `quotes.el.txt`.

3. create-images.py
-------------------

For each quote, it creates an image that contains the quote's text in greek (as translated by Bing) and the quote’s author in english: it reads `quotes.el.txt` for quote's text and `quotes.en.txt` for quote's author and produces an image in folder `images/`

4. create-html.py
-----------------

Creates a simple html page with an image slider that shows all images produced in previous step. You can see this page live here: [http://gmargari.github.io/quotes/](http://gmargari.github.io/quotes/)
