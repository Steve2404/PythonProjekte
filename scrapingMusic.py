from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import json
import collections

"""
    This program allows you to scrape music lyrics using Genius API and 
    count the most used words in the music.
"""


def is_valid(word):
    """
    this method allows the selection of words that do not have an opening and closing bracket
    :param word:
    :return: bool
    """
    return "[" not in word and "]" not in word


def filter_lyrics(lyrics):
    """
    this method allows you to filter the lyrics by first removing the html tags,
    then the commas, then the full stops, then by putting in lower case
    and finally, by selecting only the valid words.
    :param lyrics:
    :return: list[string]
    """
    all_word = []
    if not lyrics:
        return []
    for sentence in lyrics.stripped_strings:
        sentence_word = [word.strip(",").strip(".").lower()
                         for word in sentence.split() if is_valid(word)]
        all_word.extend(sentence_word)
    return all_word


def extrat_lyrics(url):
    """
    this method makes a request on a url and with the help of the BeautifulSoup library,
     we select only the song lyrics and then we filter
    :param url:
    :return: list[string]
    """
    print(f"fetching lyrics {url}...")
    r = requests.get(url)
    if r.status_code != 200:
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    lyrics = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6")
    return filter_lyrics(lyrics)


def get_all_urls():
    """
    this method makes a query on the api containing all the song lyrics of the artist.
    it returns a json file in which we extract the link to the lyrics of the designated song
    :return: list[string]
    """
    page_number = 1
    next_page = 1
    links = []
    while next_page:
        r = requests.get(
            f"https://genius.com/api/artists/62583/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            print(f"fetching page {page_number} ...")
            response = r.json().get("response", {})
            next_page = response.get("next_page")
            page_number += 1
            songs = response.get("songs")
            url = [song.get("url") for song in songs]
            links.extend(url)
        if not next_page:
            print("No more page to fetch")
            break
    print(len(links))
    return links


def count_word(words, length_words=5):
    """
    this method allows us to restrict the length of the words we wish to obtain,
    and allows us to count the words that appear the most
    :param words:
    :param length_words:
    :return: list[tuple(_T, int)]
    """
    counter = collections.Counter([wd for wd in words if len(wd) > length_words])  # count the words
    most_counter_word = counter.most_common(20)  # find the 20 most common words
    return most_counter_word


def get_all_words():
    """
    This is the main method, it allows you to store all the song lyrics ( scraping, processing)
    in a file if it doesn't exist, but to open it if it does.
    :return: none
    """
    if Path("lyrics_nena.json").is_file():
        with open("lyrics_nena.json", "r", encoding="utf-8") as f:
            words = json.load(f)
    else:
        urls = get_all_urls()
        words = []
        for url in urls:
            lyrics = extrat_lyrics(url)
            words.extend(lyrics)
        with open("lyrics_nena.json", "w", encoding="utf-8") as f:
            json.dump(words, f, indent=4)

    most_counter_word = count_word(words, length_words=7)
    pprint(most_counter_word)


get_all_words()
