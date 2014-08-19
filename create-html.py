#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

quotesFilename = "quotes.en.txt"
outFilename = "index.html"
if (len(sys.argv) == 2 and sys.argv[1] == "--remote"):
    image_prefix = "https://raw.githubusercontent.com/gmargari/bing-translated-quotes/master/"
else:
    image_prefix = "."

header = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Famous quotes translated in Greek by Bing</title>
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <div class="main">
      <div class="rss-container">
        <div id="slideshow" class="rs-slideshow">
          <div class="slide-container">
            <img src="{:s}" /><span class="slide-caption">{:s}</span>
          </div>
          <ol class="slides">
"""

footer = """
          </ol>
        </div>
      </div>
    </div>
    <p style="text-align: center; margin: 10px">
        Famous quotes translated in Greek by Bing.
        <a href="https://github.com/gmargari/bing-translated-quotes/"><img style="vertical-align:middle" src="images/but.gif"></a>
    </p>
    <script src="js/jquery-1.7.1.min.js"></script>
    <script src="js/jquery.rs.slideshow.min.js"></script>
    <script src="js/dynamic-controls-bootstrap.js"></script>
  </body>
</html>
"""

with open (outFilename, "w") as outFile:
    with open (quotesFilename, "r") as enQuotes:
        file_lines = enQuotes.read().split("\n")
        num_quotes = len(file_lines) - 1 # -1: there is an empty line at the end
        outFile.write(header.format(image_prefix + "/images/quote-0.jpg", file_lines[0].split("#")[0]))
        for i in range(0, num_quotes):
            quote = file_lines[i].split("#")[0]
            imgurl = image_prefix + "/images/quote-" + str(i) + ".jpg"
            slide_code = "            <li><a href=\"" + imgurl + "\" title=\"" + quote + "\" data-link-to=\""  + imgurl + "\"></a></li>\n"
            outFile.write(slide_code)
        outFile.write(footer)

