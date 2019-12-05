import pickle
import re
import requests
import json
import csv
import sys
import os
import logging
import time

apiUrl = 'https://api.jikan.moe/v3/anime/'  # base url for API

csv_columns = ['anime_id', 'title', 'title_english', 'title_japanese',
               'title_synonyms', 'image_url', 'type', 'source', 'episodes', 'status',
               'airing', 'aired', 'duration', 'synopsis', 'rating', 'score', 'scored_by',
               'rank', 'popularity', 'members', 'favorites', 'background', 'premiered',
               'broadcast', 'related', 'producers', 'licensors', 'studios', 'genres',
               'opening_themes', 'ending_themes']


def main():
    logging.basicConfig(filename='coleta.log')

    data_file = 'animes.csv'
    writeheader = False
    start = 1

    if not os.path.isfile(data_file):
        with open(data_file, 'w') as f:
            writeheader = True
            f.close()

    file = open(data_file, 'r', encoding="utf-16")
    if not writeheader:
        read = list(csv.reader(file))
        if len(read) > 1:
            start = int(read[-1][0]) + 1
        file.close()

    file = open(data_file, 'a', encoding="utf-16", newline='')
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    if writeheader:
        writer.writeheader()

    for anime_id in range(start, 41000):
        time.sleep(4)  # API demand this interval

        print('Reading anime with id {}'.format(anime_id))

        # API call
        page = requests.get(apiUrl + str(anime_id))

        # avoiding status code 429 (Too Many Requests)
        while page.status_code == 429:
            time.sleep(4)
            page = requests.get(apiUrl + str(anime_id))

        if page.status_code == 200 or page.status_code == 304:
            # Decoding JSON
            jsonData = json.loads(page.content)

            anime = {}
            anime['anime_id'] = anime_id
            anime['title'] = jsonData['title']
            anime['title_english'] = jsonData['title_english']
            anime['title_japanese'] = jsonData['title_japanese']
            anime['title_synonyms'] = jsonData['title_synonyms']
            anime['image_url'] = jsonData['image_url']
            anime['type'] = jsonData['type']
            anime['source'] = jsonData['source']
            anime['episodes'] = jsonData['episodes']
            anime['status'] = jsonData['status']
            anime['airing'] = jsonData['airing']
            anime['aired'] = {'from': jsonData['aired']['prop']['from'], 'to': jsonData['aired']['prop']['to']}
            anime['duration'] = jsonData['duration']
            anime['synopsis'] = jsonData['synopsis']
            anime['rating'] = jsonData['rating']
            anime['score'] = jsonData['score']
            anime['scored_by'] = jsonData['scored_by']
            anime['rank'] = jsonData['rank']
            anime['popularity'] = jsonData['popularity']
            anime['members'] = jsonData['members']
            anime['favorites'] = jsonData['favorites']
            anime['background'] = jsonData['background']
            anime['premiered'] = jsonData['premiered']
            anime['broadcast'] = jsonData['broadcast']
            anime['related'] = jsonData['related']
            anime['producers'] = [p['name'] for p in jsonData['producers']]
            anime['licensors'] = [p['name'] for p in jsonData['licensors']]
            anime['studios'] = [p['name'] for p in jsonData['studios']]
            anime['genres'] = [p['name'] for p in jsonData['genres']]
            anime['opening_themes'] = jsonData['opening_themes']
            anime['ending_themes'] = jsonData['ending_themes']

            writer.writerow(anime)
        elif page.status_code == 404:
            continue
        else:
            logging.error('anime_id: {}; status_code: {}'.format(anime_id, page.status_code))

if __name__ == '__main__':
    main()
