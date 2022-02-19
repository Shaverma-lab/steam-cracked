from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


class ParseGameInfo:
    def __init__(self, game):
        self.user = UserAgent().random
        symbol = '+'
        self.url = f'https://steamcrackedgames.com/search/?q={symbol.join(game)}'

    def parse_info(self):
        resp = requests.get(self.url, headers={
            'user-agent': self.user,
            'accept': '*/*'
        })

        soup = BeautifulSoup(resp.text, 'lxml')
        tbody = soup.select('#tbody_games > tr')

        games = []

        for i in tbody:
            game_info = [x for x in i.get_text().splitlines() if x]
            game_info.append(i.find('img').get('data-src'))

            games.append(game_info)

        return games

    def start(self):
        games = self.parse_info()

        return games

if __name__ == '__main__':
    parse_info = ParseGameInfo(input().lower().split())
    print(parse_info.start())