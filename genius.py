from bs4 import BeautifulSoup
import requests
import socks
import json
def findLyrics(url):
    response = requests.get(url)
    # You May Receive 403 Error if you are running this on a server
    # you can use Cloudflare warp proxy as request proxy or use CloudScraper Module to make this request wihtout any problem 
    soup = BeautifulSoup(response.text, 'html.parser')
    lyricsDivs = soup.find_all(attrs={'data-lyrics-container':"true"})
    lyrics = ""
    for lyricsDiv in lyricsDivs:
        brs = lyricsDiv.find_all('br')
        for br in brs:
            br.replaceWith('\n')
        for child in lyricsDiv.children:
            lyrics+=child.text
    
    return lyrics

def findSong(search_term):
    access_token = 'your_access_token_for_genius'
    url = f'https://api.genius.com/search?q={search_term}'
    headers = {'Authorization': f'Bearer {access_token}'}
    result = {}
    data = requests.get(url, headers=headers).json()
    for song in data['response']['hits']:
        try:
            song_id = song['result']['id']
            song_url = song['result']['url']
            title = song['result']['title']
            artist = song['result']['artist_names']
            result["{} - {}".format(title,artist)] = song_url;
        except Exception as e:print(e)
    return result
