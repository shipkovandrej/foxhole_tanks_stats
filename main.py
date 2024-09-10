import requests
from bs4 import BeautifulSoup
import re

from config import headers, translation

health_table = requests.get("https://foxhole.wiki.gg/wiki/Vehicle_Health", headers)
health_table = BeautifulSoup(health_table.text, "html.parser").body


def get_vehicle_stats(url):
    req = requests.get(url, headers)
    src = req.text
    soup = BeautifulSoup(src, "html.parser").body

    # Название

    name = soup.find("h2", {"data-source": "name"}).get_text()

    # Здоровье
    hp = soup.find("div", {"data-source": "vehicle_hp"}).contents[3].string
    # children = hp.findChildren("div" , recursive=False)

    # Выведено из строя при
    disable = soup.find("div", {"data-source": "disable"}).contents[3].string
    pattern = r'\d+(?=%)'
    matches = re.findall(pattern, disable)
    disable = int(matches[0])

    # армор мин-макс шанс пробития
    armor_vars = soup.find("div", {"data-source": "min_pen_chance"}).contents[3].getText()

    pattern = r'(\d+),.?(\d+)-(\d+)'
    matches = re.findall(pattern, armor_vars)

    armor = matches[0][0]
    min_pin_chance = matches[0][1]
    max_pin_chance = matches[0][2]

    # % подбития под систем

    sub_vars = soup.find_all("div", {"data-source": "min_pen_chance"})[1].div.get_text()[1:].replace('%', '').split(' ')

    subsytems_dict = {}
    subsytems_dict.update({'Гусеницы': sub_vars[0]})
    if len(sub_vars) > 1:
        subsytems_dict.update({'Топливный бак': sub_vars[1]})
        if len(sub_vars) > 2:
            subsytems_dict.update({'Орудие': sub_vars[2]})
            if len(sub_vars) > 3:
                subsytems_dict.update({'Вторичное оружие': sub_vars[3]})

    # Стоимость ремонта
    repair_cost = soup.find("div", {"data-source": "repair"}).contents[3].getText().rstrip()

    tab_panels = soup.find_all("article", {"class": "tabber__panel"})

    tab_crew = tab_panels[0]
    tab_inventory = tab_panels[1]
    tab_engine = tab_panels[2]

    # Скорость
    pattern = r'Speed: (\d+[.]?(\d+)?) m\/s on road, (\d+[.]?(\d+)?) m\/s off-road'
    matches = re.findall(pattern, tab_engine.ul.get_text())

    speed1 = matches[0][0]
    speed2 = matches[0][2]

    # Объем бака расход и длительность
    fuelcap = soup.find("div", {"data-source": "fuelcap"}).contents[3].a.getText()[:-1]

    pattern = r'(\d).+(\d{2}[:]\d{2}).+'
    matches = re.findall(pattern, tab_engine.ul.contents[2].get_text())

    fuel_per_min = matches[0][0]
    fuel_autonomy = matches[0][1]

    # используемое вооружение
    guns = soup.find_all("div", {"data-source": "armament"})[0].contents[3].get_text().replace(', ', '#').split('#')
    translated_guns = []
    for i in guns:
        translated_guns.append(translation[i]) if i in translation else translated_guns.append(i)

    # перезарядка и длительность стрельбы и дальность
    reload_dict = {}
    range_dict = {}
    for i in tab_inventory.find('ul').findChildren("li", recursive=False):
        gun_name = i.contents[0].rstrip()
        gun_name = translation[gun_name] if gun_name in translation else gun_name
        text = i.get_text()

        pattern = r'Reload Duration: (\d+[.]?(\d+)?) seconds'
        matches = re.findall(pattern, text)
        reload_duration = matches[0][0]

        var_dict = {
            'Скорость перезарядки': reload_duration,
        }

        pattern = r'Firing Duration: (\d+[.]?(\d+)?) seconds'
        matches = re.findall(pattern, text)
        if matches:
            var_dict.update({'Время стрельбы': matches[0][0]})

        reload_dict.update({gun_name: var_dict})

        pattern = r'Range: ((\d+)([.]\d+)?(-\d+)?) meters'
        matches = re.findall(pattern, text)

        var_dict = {
            'Дальность': matches[0][0],
        }

        range_dict.update({gun_name: var_dict})

    # Экипаж
    crew_arr = []
    for i in tab_crew.ul.find_all('b'):
        crew_arr.append(i.get_text())

    translated_crew = []
    for i in crew_arr:
        translated_crew.append(translation[i]) if i in translation else translated_crew.append(i)

    # Инвентарь снаряды
    inventory_arr = []
    for i in soup.find_all("div", {"data-source": "armament"})[1].contents[3].find_all('a'):
        inventory_arr.append(i.get_text())

    # инвентарь пустой
    # pattern = r'(\d) inventory slot'
    # matches = re.findall(pattern, tab_inventory.contents[-4])
    # free_inventory = matches[0] if matches else None

    # Инвентарь итоговый

    # Место постройки
    # build_location = soup.find_all("div", {"data-source": "build_location"})[0].contents[3].getText()

    # Стоимость постройки
    # build_cost = soup.find_all("div", {"data-source": "build_location"})[1].contents[3].getText()

    # таблица здоровья и принимаемого урона
    table = health_table.find("table", {"class": "wikitable"}).tbody
    trs = table.find_all("tr")[1:]

    # print(trs[0].td.get_text())
    row = ''
    for tr in trs:
        if name in tr.td.get_text():
            row = tr
            break

    # print(row.contents[9])

    assign_dict = {
        '20мм': 9,
        'фласки': 47,
        'липкие бомбы': 49,
        'рпг': 17,
        '40мм': 19,
        'нкг': 43,
        '68мм': 41,
        'мины': 51,
        '75мм': 21,
        '94.5мм': 45,
    }
    table_dict = {}

    for i in assign_dict:
        val1 = row.contents[assign_dict[i]].find('font').string
        val2 = row.contents[assign_dict[i]].contents[2].string.rstrip()
        table_dict[i] = f'{val1}/{val2}'

    return {
        'ХП': hp,
        'Подбит при': disable,
        'П.П/У': table_dict,
        'Броня': armor,
        'Базовый шанс пробития': min_pin_chance,
        'Максимальная степень износа танковой брони': max_pin_chance,
        'Шанс подбития подсистем': subsytems_dict,
        'Стоимость полной починки': repair_cost,
        'Скорость': {
            'дорога': speed1,
            'бездорожье': speed2
        },
        'Объём бака': fuelcap,
        'Потребление': fuel_per_min,
        'Время хода': fuel_autonomy,
        'Вооружение': translated_guns,
        'Перезарядка': reload_dict,
        'Экипаж': translated_crew,
        'Дальность': range_dict
    }

