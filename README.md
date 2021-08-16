# tiktok-scavanger
 Tiktok data scavanager that stores data in CSV files of predefined formats

## Dependencies
1. Python 3.9+
2. Node 10+

## Installation
1. Make sure that you've installed Python 3 and Node 10
2. Run in terminal/cmd/powershell:
`npm i -g tiktok-scraper`
3. Download/clone this project and open a terminal/cmd/powershell in the directory of this project and run: 
`pip install -r requirements.txt`
4. Before running for the first time, make sure you've the correct values in the `config.ini` file.

## Configuration (`config.ini`)
1. Set `chromepath` in the config.ini file to the location of your chrome browser replacing the existing one
2. Use `maxnumberofinfluencers` to set the max number of users you wanna scrape. Set to 0 for no limits
3. `apicacheenabled` and `authcacheenabled` are used to control caching of tiktok API calls and tiktok sign-in respectively. When set to "yes", you'll only need to sign in the first time and the data of the raw users you've scrapped so far will be saved locally even if scraping fails half way through for some reason so that you can restart a few hours later from where you left off when the network is stable again. If you're having trouble signing in, set `authcacheenabled` to "no" to force a fresh sign in. You can again set it to "yes" for subsequent attemts.
4. Tiktok limits API calls. So, you'll most likely need a proxy service. the one currently being used here is a free trial account of proxymesh.com. You can purchase one of their premium packages and enter your username password in the `PROXY-CONFIG` section and it will automatically pick up the proxy servers available for you. 
*NOTE: You can change proxy servers from a list signing in to your proxymesh account (even the free account) in case you're getting blocked*
5. The last param is `searchtopics`. Enter the categories you want to scrape comma separated, No spaces. Please pay attention to spelling and capitalization as you'll need to make sure that they are exactly the way presented in the creatormarketplace site. 
*NOTE: You can even use sub categories in the same way and it will still work. When you do that, skip the parent category and only name the subcategory e.g: Art, Pets* 

## Usage
1. Open a terminal/cmd/powershell 
2. Navigate to the project folder (tiktok-scavanger)
3. Run `python main.py`
