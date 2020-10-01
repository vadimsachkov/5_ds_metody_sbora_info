# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instagramparser.items import InstagramParserItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from pprint import pprint






class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'insttest98'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1601366430:AedQALcCk9Jy8MyLIQqj+VPgAlvoG3In1nXy+EFeZPW6JY94D2woPMM/zRZEy5YNGkPyS1Qh57R1+wqOOd1Tta/iJ7JdTnbQqNBWRb0dO88zQrffdn0A1yt2TEqjX7LT6aXpvEiq4F7on7xrpHAY'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    # список пользователей, у которого собираем посты. Можно указать список
    parse_users = ['ostrov_salon','texaspizzeria', 'makcim123098']


    graphql_url = 'https://www.instagram.com/graphql/query/?'
    posts_hash1 = '18a7b935ab438c4514b1f742d8fa07a7'     #hash для получения данных по постах с главной страницы
    subscription_hash ='d04b0a864b4b54837c0d870b0e77e076'   # hash подписки
    subscriber_hash ='c76146de99bb02f6415203be841dd25a'     # hash подписчиков
    # gagara1987 подписчики c76146de99bb02f6415203be841dd25a
    # gagara1987 подписки   d04b0a864b4b54837c0d870b0e77e076

    subscriptions = {}  # словарь где ключ это id_пользователя а значение- список его подписок


    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.myuser_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def myuser_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        # можно использовать встроенную функцию scrapy j_body = response.json()
        # перtбираем всех пользоватлей чьи подписчикаи и подписки нас интересуют
        for parse_user in self.parse_users:
            if j_body['authenticated']:                 #Проверяем ответ после авторизации
                yield response.follow(                  #Переходим на желаемую страницу пользователя. Сделать цикл для кол-ва пользователей больше 2-ух
                    f'/{parse_user}',
                    callback= self.user_data_parse,
                    cb_kwargs={'person_name':parse_user}
                )
    # вход на страницу нужного пользователя
    def user_data_parse(self, response:HtmlResponse, person_name):
        person_id = self.fetch_person_id(response.text, person_name)       #Получаем id пользователя
        variables={"id":person_id,                                    #Формируем словарь для передачи даных в запрос
                   "first":25}                                      #12 постов. Можно больше (макс. 50)


        # Сначала обходим подписчиков
        #url_posts = f'{self.graphql_url}query_hash={self.subscriber_hash}&{urlencode(variables)}'
        url_posts=f'{self.graphql_url}query_hash={self.subscriber_hash}&variables='+json.dumps(variables,separators=(',', ':'))

        #Формируем ссылку для получения данных о подписчиках
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'person_name':person_name,
                       'person_id':person_id,
                       'followto_id':person_id,
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )


        # ТЕПЕРЬ  обходим на кого сам подписан пользователь
        #url_posts = f'{self.graphql_url}query_hash={self.subscriber_hash}&{urlencode(variables)}'
        # separators=(',', ':') в json.dumps убирает лишние пробелы в строке т.е. сделает так '{"id":"40942744149","first":12}' вместо '{"id": "40942744149", "first": 12}'
        url_posts = f'{self.graphql_url}query_hash={self.subscription_hash}&variables=' + json.dumps(variables,separators=(',', ':'))
        #Формируем ссылку для получения данных о подписках
        followto_id=None # id пользовтаеля на которого пописаны
        # инициализируем список подписок если он уже не иниацилизирован
        if person_id not in self.subscriptions:
            self.subscriptions[person_id] = []
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            cb_kwargs={'person_name':person_name,
                       'person_id':person_id,
                       'followto_id':None,
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )






    def user_posts_parse(self, response:HtmlResponse,person_name,person_id,followto_id,variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)

        if (followto_id):
            # если это подписчик
            user_info = j_data.get('data').get('user').get('edge_followed_by')
            posts_hash=self.subscriber_hash
        else:
            user_info = j_data.get('data').get('user').get('edge_follow')
            posts_hash = self.subscription_hash
        #page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')

        users = user_info.get('edges')     #Сами посты
        for user in users:                                                                      #Перебираем посты, собираем данные
            item = InstagramParserItem(
                user_id = user['node']['id'],
                photo = user['node']['profile_pic_url'],
                node = user['node'],
                fullname= user['node']['full_name'],
                username=user['node']['username'],
                subscriptions=[followto_id]  # присводить subscriptions=номер пользователя , так этот пользователь подписан
            )
            if not followto_id:

                self.subscriptions[person_id].append(user['node']['id'])

            yield item   #В пайплайн

        # ищем следующую порцию подписчиков (если followto_id) или подписки если followto_id is None
        if user_info.get('page_info').get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = user_info['page_info']['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={posts_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_posts_parse,
                cb_kwargs={'person_name': person_name,
                           'person_id': person_id,
                           'variables': deepcopy(variables),
                           'followto_id':followto_id}
            )
        else:
            # зкончились все подписки - пора создавать Персону
            # создаем iteм самого пользователя _Условно назовем его mainUser
            person_item = InstagramParserItem(
                user_id=person_id,
                photo=response.xpath('//div[@class="XjzKX"]//img/@src'),
                fullname=response.xpath('//h1/text()'),
                username=person_name,
                subscriptions=self.subscriptions[person_id]  # создаем пустое множество кужа потом будут добавляться на кого подписан пользователь
            )
            yield person_item







    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_person_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    #Получаем full_name желаемого пользователя
    def fetch_user_fullname(self, text, username):
        matched = re.search(
            '{\"full_name\":\"\\.+\",\"has_ar_effects\":}' , text
        ).group()
        return json.loads(matched).get('id')

   # "full_name": "Doutzen Kroes", "has_ar_effects"
   #re.search('{\"full_name\":\"\\.+\",\"has_ar_effects\":}' , response.text)