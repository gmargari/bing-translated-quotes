#!/usr/bin/python
# -*- coding: utf-8 -*-
import ImageFont
import Image
import ImageDraw
import textwrap
import os

quoteTextFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Oblique.ttf", 26)
quoteAuthorFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 26)
quoteLeftMargin = 50
textTopMargin = 120
authorTopSpace = 40
quoteTextColor = "#eeeeee"
quoteAuthorColor = "#eeeeee"
bgImage = './bg.jpg'
outFolder = "./quotes"     # Will be created if it does not exis
outImagePrefix = "quote-"
outImageExtension = ".jpg"

#==============================================================================
# createQuoteImage()
#==============================================================================
def createQuoteImage(quoteText, quoteAuthor, bgImgFilename, outFilename):

    # Open background image
    img = Image.open(bgImgFilename)
    draw = ImageDraw.Draw(img)

    # Add text to image
    quoteText = unicode(quoteText, 'utf-8')
    quoteAuthor = unicode(quoteAuthor, 'utf-8')
    margin = quoteLeftMargin
    offset = textTopMargin
    for line in textwrap.wrap(quoteText, width=45):
        draw.text((margin, offset), line, font = quoteTextFont, fill = quoteTextColor)
        offset += quoteTextFont.getsize(line)[1]
    draw.text((margin, offset + authorTopSpace), quoteAuthor, font = quoteAuthorFont, fill = quoteAuthorColor)
    del draw

    # Save result image
    img.save(outFilename)

#==============================================================================
# main()
#==============================================================================
def main():
    with open ("quotes.el.txt", "r") as myfile:
        # Create output folder, if it does not exist
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)
        quotes = 1
        for line in myfile:
            # Each line is a pair of: <quote text> # <author name>
            quote = line.split("#")
            if (len(quote) > 1):
                text = quote[0].strip()
                author = quote[1].strip()
                outputFile = outFolder + "/" + outImagePrefix + str(quotes) + outImageExtension
                print "Creating image " + outputFile + " ..."
                createQuoteImage(text, author, bgImage, outputFile)
                quotes = quotes + 1

if __name__ == "__main__":
    main()

