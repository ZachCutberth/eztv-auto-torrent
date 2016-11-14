#! python3

import bs4, requests, re, os, shelve
from twilio.rest import TwilioRestClient
# URL to scrape.
url = 'https://eztv.it'
# List of shows to torrent
shows = ['Anthony Bourdain', 'Westworld', 'American Dad', 'Archer', 'Better Call Saul', 'Black Sails', 'The Expanse', 'Family Guy', 'Halt and Catch Fire', 'House of Cards', "It's Always Sunny in Philadelphia", 'Maron', 'Mr. Robot', 'Narcos', 'Shameless', 'Sherlock', 'Silicon Valley', 'The Strain', 'True Detective', 'Workaholics']
# Get the raw source code
sauce = requests.get(url)
# Feed the source code to BeautifulSoup for parsing
soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
# Open database for persistant storage of torrent urls already downloaded
shelfFile = shelve.open('torrents')

# Create key for database if it hasn't already been created.
if shelfFile['torrenturls'] == False:
    torrentUrls = []
    shelfFile['torrenturls'] = torrentUrls

# Twilio configuration for sending text messages
accountSID = os.environ['twilioAccountSid']
authToken = os.environ['twilioAuthToken']
twilioCli = TwilioRestClient(accountSID, authToken)
myTwilioNumber = os.environ['twilioMyTwilioNumber']
myCellPhone = os.environ['twilioMyCellPhone']

# Seach for shows in our list to download. Check to make sure we haven't already downloaded them. If they are new, download the torrent and send a text message.
print('Looking for new shows to torrent...')
for show in shows:
    for url in soup.find_all('a', class_='magnet', title=re.compile(show)):
        if '720' in url.get('title'):
            pass
        elif '1080' in url.get('title'):
            pass
        elif url.get('href') in shelfFile['torrenturls']:
            pass
        else:
            os.startfile(url.get('href'))
            tempTorrentUrls = shelfFile['torrenturls']
            tempTorrentUrls.append(url.get('href'))
            shelfFile['torrenturls'] = tempTorrentUrls
            print('Torrenting >>> ' + url.get('title'))
            message = twilioCli.messages.create(body=('Torrenting >>> ' + url.get('title')), from_=myTwilioNumber, to=myCellPhone)

shelfFile.close()
