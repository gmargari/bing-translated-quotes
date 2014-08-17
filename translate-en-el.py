#!/usr/bin/python
import json
import requests # pip install requests
import urllib

# For getting your ClientID and ClientSecret, see: http://blogs.msdn.com/b/translation/p/gettingstarted1.aspx
clientID = 'tmpCliendId909090' # your client id here
clientSecret = 'qCOecPI1gXjqNnlJ1lxxIcCx0WwYYgqg2uCA9VmfIjs=' # your azure secret here
inLanguage = "en"
outLanguage = "el"
inFilename = "quotes.en.txt"
outFilename = "quotes.el.txt"

#==============================================================================
# translateText()
#==============================================================================
def translateText(text):
    print "Translating buffer..."

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
    text = result.content

    # Remove the first 4 bytes, <feff>, defining the Byte Order Marker
    text = text[3:]

    # Remove the trailing and leading quotes added by Bing
    text = text[1:-1]

    return text

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
                text_buffer = text_buffer + text + "\n"
                
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

            # Split lines by the unicode character \u000a (Line feed)
            translated_text_lines = whole_translated_text.split('\u000a')
            print "lines = ", len(translated_text_lines)

            inFile.seek(0)
            i = 0
            for line in inFile:
                print i,
                quote = line.split("#")
                if (len(quote) > 1):
                    text = quote[0].strip()
                    author = quote[1].strip()
                    translated_text = translated_text_lines[i]
                    outFile.write("{:s}#{:s}\n".format(translated_text, author))
                    i = i + 1

if __name__ == "__main__":
    main()

