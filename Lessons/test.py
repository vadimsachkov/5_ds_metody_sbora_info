# этот вариант почему то не прокатил - зараза столько времени на него потратил. а ведь было счастье так близко
#       parent_hits_obj = driver.find_element_by_xpath('//div[@class="gallery-layout" and descendant::div[contains(text(), "Хиты продаж")]]//ul[@data-init="galleryCarousel"]')
parents_hits_obj = driver.find_elements_by_xpath('//div[@class="indexGoods"]')
# ищем родителя у которого класс gallery-layout
hits_obj = None
myparent_hit = None
# ищем именного того предка (myparent_hit) у которго потомок hits_obj содержит  "Хиты продаж"
#
for parent_hit in parents_hits_obj:
    try:
        # print(parent_hit.get_attribute('class'))
        # print(parent_hit)
        # print(parent_hit.find_element_by_xpath('./child::*').get_attribute('class'))
        hits_obj = parent_hit.find_element_by_xpath('.//h2[contains(text(), "Хиты продаж")]')
        myparent_hit = parent_hit
    except:
        # print(hits_obj)
        pass

if not myparent_hit:
    # мы не нашли контейнер Хиты продаж . выходим
    print('Мы не нашли контейнер Хиты продаж . выходим')
    exit(1)

# мы нашли контейнер Хиты продаж . продолжаем
# ищем кнопку следующие