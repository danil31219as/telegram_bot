from bs4 import BeautifulSoup
from telegraph.api import Telegraph
import requests
import telebot


def make_telegraph(token, title, photo, photo_text, main_text):
    session = Telegraph(token)
    content = [{'children': [{'tag': 'br'}], 'tag': 'p'},
               {'children': [{'attrs': {'src': photo},
                              'tag': 'img'},
                             {'children': [photo_text],
                              'tag': 'figcaption'}],
                'tag': 'figure'},
               {'children': [{'tag': 'br'}], 'tag': 'p'},
               {'children': [{'tag': 'br'}], 'tag': 'p'},
               {'tag': 'p', 'children': [main_text]},
               {'children': [{'tag': 'br'}], 'tag': 'p'},
               {'children': [{'attrs': {
                   'href': 'https://t.me/joinchat/JTVAx0pTnkjvH75UTArwTg',
                   'target': '_blank'},
                              'children': [
                                  'Наш чат - https://t.me/joinchat/JTVAx0pTnkjvH75UTArwTg'],
                              'tag': 'a'}],
                'tag': 'blockquote'},
               {'children': ['Telegram-канал',
                             {'children': [' '], 'tag': 'strong'},
                             {'attrs': {'href': 'https://t.me/muzhik_zdorov',
                                        'target': '_blank'},
                              'children': [{'children': ['Мужское здоровье - ',
                                                         {'children': ['@'],
                                                          'tag': 'em'},
                                                         'muzhik_zdorov'],
                                            'tag': 'strong'}],
                              'tag': 'a'}],
                'tag': 'blockquote'},
               {'children': [{'tag': 'br'}], 'tag': 'p'}]
    href = session.create_page(title=title, author_name='@muzhik_zdorov',
                               content=content)
    return href


bot = telebot.TeleBot('1106884691:AAHxW_QkU1PT3hlZfcuuUBuDwo-esplvWx4')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, кинь мне ссылку')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.id == 236831339:
        url = message.text
        token = 'e05180aaf37d7293ad9bfc1e3df510b7b6adc642e685da38f8068a222d8d'
        soup = BeautifulSoup(
            requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text,
            'html.parser')
        title = soup.find_all('h1')[0].text
        desc_tlg = soup.find('div', class_='detail-anons').text
        photo = 'https://www.menslife.com' + \
                soup.find('div', class_='detail-image').find('img')['src']
        photo_text = soup.find('div', class_='detail-image').find('img')['alt']
        main_text = soup.find('div', class_='detail-text').text
        href = make_telegraph(token, title, photo, photo_text, main_text)
        bot.send_message(-1001107192388,
                         "<strong>" + title + "</strong>\n\n" + desc_tlg.strip() + "\n\n" + str(href['url']),
                         parse_mode='HTML')


if __name__ == '__main__':
    bot.polling()
