#!/usr/bin/python
# -*- coding: utf-8 -*-
import ImageFont
import Image
import ImageDraw
import textwrap
import os

quoteTextFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Oblique.ttf", 22)
quoteAuthorFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 22)
quoteLeftMargin = 25       # space from left side, in pixels
textWrapWidth = 50         # Max width of wrapped lines, in characters
quoteTextColor = "#eeeeee"
quoteAuthorColor = "#eeeeee"
bgImage = './images/bg.jpg'
outFolder = "./images/"     # Will be created if it does not exis
outImagePrefix = "quote-"
outImageExtension = ".jpg"

#==============================================================================
# lineHeight()
#==============================================================================
def lineHeight(font):
    (width, height) = font.getsize("αβγδεξζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")
    return height * 1.1

#==============================================================================
# topMargin()
#==============================================================================
def topMargin(text, text_font, author, author_font, draw, img):
    (imgW, imgH) = img.size
    text_lines = len(textwrap.wrap(text, width = textWrapWidth))
    # +1 for empty line between text and author
    author_lines = len(textwrap.wrap(author, width = textWrapWidth)) + 1
    total_text_height = text_lines * lineHeight(text_font) + author_lines * lineHeight(author_font)
    return (imgH - total_text_height)/2

#==============================================================================
# addText()
#==============================================================================
def addText(draw, x, y, text, textFont, textColor):
    draw.text((x, y), text, font = textFont, fill = textColor)

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
    offset = topMargin(quoteText, quoteTextFont, quoteAuthor, quoteAuthorFont, draw, img)
    for line in textwrap.wrap(quoteText, width = textWrapWidth):
        addText(draw, margin, offset, line, quoteTextFont, quoteTextColor)
        offset += lineHeight(quoteTextFont)
    offset += lineHeight(quoteTextFont) # one empty line before author
    for line in textwrap.wrap(quoteAuthor, width = textWrapWidth):
        addText(draw, margin, offset, line, quoteAuthorFont, quoteAuthorColor)
        offset += lineHeight(quoteAuthorFont)
    del draw

    # Save result image
    img.save(outFilename, optimize = 1, quality = 90)

#==============================================================================
# main()
#==============================================================================
def main():
    with open ("quotes.el.txt", "r") as myfile:
        # Create output folder, if it does not exist
        if not os.path.exists(outFolder):
            os.makedirs(outFolder)

        line = myfile.read().split("\n")
        for i in range(0, len(line)):   # last line is empty
            # Each line is a pair of: <quote text> # <author name>
            quote = line[i].split("#")
            if (len(quote) > 1):
                text = quote[0].strip()
                author = quote[1].strip()
                outputFile = outFolder + "/" + outImagePrefix + str(i) + outImageExtension
                print "Creating image " + outputFile + " ..."
                createQuoteImage(text, author, bgImage, outputFile)

if __name__ == "__main__":
    main()

