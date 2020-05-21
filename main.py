from bs4 import BeautifulSoup
from telegraph.api import Telegraph
import requests
import telebot
import os

bot_token = os.environ.get('bot_token')
token = os.environ.get('token')


def add_src(code):
    while code.find('src="/uplo') > -1:
        x = code.find('src="/') + 5
        print(code[x - 5:x])
        code = code[:x] + 'https://www.menslife.com' + code[x:]
    return code


def del_tag(code, tag):
    while code.find(tag) > -1:
        x = code.find(tag)
        code = code[:x] + '<br><br>' + code[x + len(tag):]
    return code


def make_telegraph(token, title, photo, photo_text, main_text):
    session = Telegraph(token)

    tag = del_tag(del_tag('\n'.join(str(main_text).split('\n')[1:]), '<h2>'),
                  '</h2>')
    tag = str(photo) + '\n' + tag
    tag = del_tag(tag, '/div')
    tag = add_src(tag)
    return session.create_page(title=title, author_name='@muzhik_zdorov',
                               html_content=tag[:-3])


bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, кинь мне ссылку')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.id == 236831339:
        try:
            url = message.text
            soup = BeautifulSoup(
                requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text,
                'html.parser')
            title = soup.find_all('h1')[0].text
            desc_tlg = soup.find('div', class_='detail-anons').text
            photo = soup.find_all('img')[8]
            photo_text = soup.find_all('img')[8]['alt']
            main_text = soup.find('div', class_='detail-text')
            href = make_telegraph(token, title, photo, photo_text, main_text)
            bot.send_message(-1001107192388,
                             "<strong>" + title + "</strong>\n\n" + desc_tlg.strip() + "\n\n" + str(
                                 href['url']),
                             parse_mode='HTML')
        except Exception:
            bot.send_message(236831339, 'Что-то пошло не так')

    else:
        bot.send_message(message.chat.id, 'Не подчиняюсь')


if __name__ == '__main__':
    bot.polling()
