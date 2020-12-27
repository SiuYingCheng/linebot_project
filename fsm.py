from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message,send_image_message
from bs4 import BeautifulSoup
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import json
import numpy
import pandas as pd

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_choose(self, event):
        text = event.message.text
        if text == 'choose' or text.lower()=='back':
            return True
        return False

    def on_enter_choose(self, event):
        title = '主人您好，我是bot，很高興為您服務'
        text = '請選擇您想要的休閑活動'
        btn = [
            MessageTemplateAction(
                label = 'movie',
                text ='movie'
            ),
            MessageTemplateAction(
                label = 'restaurant',
                text = 'restaurant'
            ),
            MessageTemplateAction(
                label = 'picture',
                text = 'picture'
            ),
            MessageTemplateAction(
                label = 'show_fsm',
                text = 'show_fsm'
            ),
        ]
        url = 'https://i.imgur.com/LLTWOUr.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_show_fsm(self, event):
        text = event.message.text
        if text == 'show_fsm' or (self.state == 'show_fsm' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_show_fsm(self,event):
        url = 'https://i.imgur.com/tdBrIa7.png'
        send_image_message(event.reply_token, url)

    def is_going_to_picture(self, event):
        text = event.message.text
        if text == 'picture' or (self.state == 'picture' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_picture(self, event):
        title = '主人好，您想看的圖片已就位'
        text = '請選擇您想查看的圖片'
        btn = [
            MessageTemplateAction(
                label = 'hot_girl',
                text ='hot_girl'
            ),
            MessageTemplateAction(
                label = 'hot_boy',
                text = 'hot_boy'
            ),
            MessageTemplateAction(
                label = 'meaningful_quote',
                text = 'meaningful_quote'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://i.imgur.com/yT4x7LC.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def is_going_to_hot_boy(self, event):
        text = event.message.text
        if text == 'hot_boy' or (self.state == 'hot_boy' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_hot_boy(self,event):
        url = 'https://i.imgur.com/wkcQwFm.png'
        send_image_message(event.reply_token, url)
    
    def is_going_to_hot_girl(self, event):
        text = event.message.text
        if text == 'hot_girl' or (self.state == 'hot_girl' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_hot_girl(self,event):
        url = 'https://i.imgur.com/zrMWzp2.jpg'
        send_image_message(event.reply_token, url)
    
    def is_going_to_meaningful_quote(self, event):
        text = event.message.text
        if text == 'meaningful_quote' or (self.state == 'meaningful_quote' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_meaningful_quote(self,event):
        url = 'https://i.imgur.com/sC4RaQr.jpg'
        send_image_message(event.reply_token, url)

    def is_going_to_movie(self, event):
        text = event.message.text
        if text == 'movie' or (self.state=='movie' and text.lower()=='back'):
            return True
        return False
    
    def on_enter_movie(self, event):
        url = 'https://www.boxofficemojo.com/weekend/by-year/2020/?area=TW'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        url_list = []
        img_list = []
        for i in range(5):
            url_list.append(soup.select('td.mojo-cell-wide > a.a-link-normal')[i].getText())

        send_text_message(event.reply_token, str(url_list))

    def is_going_to_restaurant(self, event):
        text = event.message.text   
        if text == 'restaurant' or self.state == 'restaurant':
            return True
        return False
    
    def on_enter_restaurant(self,event):
        text = event.message.text
        if text == 'restaurant':
            send_text_message(event.reply_token, '輸入您想要查詢的地區（ex. 台南市）: ')
            return
        response = requests.get("https://ifoodie.tw/explore/" + event.message.text + "/list?sortby=popular&opening=true")
        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.find_all('div', {'class': 'jsx-2133253768 restaurant-item track-impression-ga'}, limit=5)
        content = ""
        for card in cards:
            title = card.find("a", {"class": "jsx-2133253768 title-text"}).getText()
            stars = card.find( "div", {"class": "jsx-1207467136 text"}).getText()
            address = card.find("div", {"class": "jsx-2133253768 address-row"}).getText()
            content += f"{title} \n{stars}顆星 \n{address} \n\n"
        
        send_text_message(event.reply_token, content)
