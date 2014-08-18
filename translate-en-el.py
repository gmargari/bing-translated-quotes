#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests # pip install requests
import urllib
import re

# For getting your ClientID and ClientSecret, see: http://blogs.msdn.com/b/translation/p/gettingstarted1.aspx
clientID = 'tmpCliendId909090' # your client id here
clientSecret = 'qCOecPI1gXjqNnlJ1lxxIcCx0WwYYgqg2uCA9VmfIjs=' # your azure secret here
inLanguage = "en"
outLanguage = "el"
inFilename = "quotes.en.txt"
outFilename = "quotes.el.txt"
delimiter = ".NONEXISTINGWORD."

#==============================================================================
# translateText()
#==============================================================================
def translateText(text):
    print "Translating buffer..."

    # Helping Bing translation a bit...
    text = text.replace("'cause", "because")
    text = text.replace("'em", "them")
    text = text.replace("'tis", "it is")
    text = text.replace("'Tis", "It is")
    # Add space after "..."
    # (Explanation: match "..." followed by any letter. The ( ) used will store
    # in variable \1 anything that matches the pattern within the parentheses.
    # Then, replace this matched pattern with "..." followed by a
    # space followed by the contents of variable \1.
    text = re.sub(r'\.\.\.([a-zA-Z])', '... \\1', text)
    text = re.sub(r'([a-zA-Z])\.\.\.', '\\1 ...', text)

    # Source: http://stackoverflow.com/a/12149985
    args = {
        'client_id': clientID,
        'client_secret': clientSecret,
        'scope': 'http://api.microsofttranslator.com',
        'grant_type': 'client_credentials'
    }
    oauth_url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)
    headers = { 'Authorization': 'Bearer ' + oauth_junk['access_token'] }
    translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
    translation_args = {
        'from': inLanguage,
        'to': outLanguage
    }

    translation_args['text'] = text
    result = requests.get(translation_url + urllib.urlencode(translation_args),
                          headers = headers)
    trans_text = result.content

    # Remove the first 4 bytes, <feff>, defining the Byte Order Marker
    trans_text = trans_text[3:]

    # Remove the trailing and leading quotes added by Bing
    trans_text = trans_text[1:-1]

    # Symbol ";" is translated by Bing into "?", instead of the greek semi-colon
    trans_text = trans_text.replace("?", "·")

    # Replace remove unnecessary space from word "ό, τι"
    trans_text = trans_text.replace(" ό, τι ", " ό,τι ")
    trans_text = trans_text.replace("Ό, τι ", "Ό,τι ")

    # Replace more than one space with a single space
    text = re.sub(r' +', ' ', text)

    # Bing often inserts a "\/" instead of "/"
    trans_text = trans_text.replace("\\/", "/")

    return trans_text

#==============================================================================
# main()
#==============================================================================
def main():
    with open (inFilename, "r") as inFile:

        # To avoid translating the file line-by-line (i.e. quote-by-quote),
        # create a buffer that contains the text of multiple quotes and send
        # this buffer for translation.
        text_buffer = ""
        whole_translated_text = ""
        for line in inFile:

            # Each line of input file is a pair of: <quote text> # <author name>
            quote = line.split("#")
            if (len(quote) > 1):
                text = quote[0].strip()
                author = quote[1].strip()
                # Separate different quotes by delimiter
                text_buffer = text_buffer + text + ' ' + delimiter + ' '

                # If buffer is long enough, translate it and add it to the
                # buffer containg the translated text
                if (len(text_buffer) > 8192):
                    translated_text = translateText(text_buffer)
                    whole_translated_text = whole_translated_text + translated_text
                    text_buffer = ""

        # Translate any remaining text in buffer
        if (len(text_buffer) > 0):
            translated_text = translateText(text_buffer)
            whole_translated_text = whole_translated_text + translated_text

        # Combine the translated quotes with their respective authors and
        # write them in output file
        with open (outFilename, "w") as outFile:

            # Split lines by '#'
            translated_text_lines = whole_translated_text.split(delimiter)

            inFile.seek(0)
            i = 0
            for line in inFile:
                quote = line.split("#")
                if (len(quote) > 1):
                    text = quote[0].strip()
                    author = quote[1].strip()
                    translated_text = translated_text_lines[i].strip()
                    outFile.write("{:s}#{:s}\n".format(translated_text, author))
                    i = i + 1

if __name__ == "__main__":
    main()

