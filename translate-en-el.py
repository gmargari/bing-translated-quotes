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
    return result.content

#==============================================================================
# main()
#==============================================================================
def main():
    outFile = open(outFilename, "w")
    with open (inFilename, "r") as myfile:
        quotes = 1
        for line in myfile:
            # Each line is a pair of: <quote text> # <author name>
            quote = line.split("#")
            if (len(quote) > 1):
                text = quote[0].strip()
                author = quote[1].strip()
                print "Translating quote " + str(quotes)
                translated_text = translateText(text)
                # [4:]: remove the first 4 bytes, <feff>, defining the Byte Order Marker
                outFile.write("{:s} # {:s}\n".format(translated_text[3:], author))
                quotes = quotes + 1
    outFile.close()

if __name__ == "__main__":
    main()

# Note: quotes.en.txt is the result of cleaning and processing:
# https://github.com/mjseaman/restful_crud/blob/master/db/litemind-quotes.csv

