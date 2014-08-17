#!/usr/bin/python

outFilename = "quotes.html"

header = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Really Simple Slideshow jQuery Plugin - HTML Captions Demo</title>
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <p align=center>
        Famous quotes translated in Greek by Bing. More information: 
        <a href="https://github.com/gmargari/bing-translated-quotes">
            https://github.com/gmargari/bing-translated-quotes
        </a>
    </p>      
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
    <script src="js/jquery-1.7.1.min.js"></script>
    <script src="js/jquery.rs.slideshow.min.js"></script>
    <script src="js/dynamic-controls-bootstrap.js"></script>
  </body>
</html>
"""

with open (outFilename, "w") as outFile:
    with open ("quotes.en.txt", "r") as enQuotes:
        file_lines = enQuotes.read().split("\n")
        num_quotes = len(file_lines) - 1 # -1: there is an empty line at the end
        outFile.write(header.format("images/quote-1.jpg", file_lines[0].split("#")[0]))
        for i in range(0, num_quotes):
            quote = file_lines[i].split("#")[0]
            imgurl = "images/quote-" + str(i+1) + ".jpg"
            slide_code = "            <li><a href=\"" + imgurl + "\" title=\"" + quote + "\" data-link-to=\""  + imgurl + "\"></a></li>\n"
            outFile.write(slide_code)
        outFile.write(footer)

