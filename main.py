# import json
import requests
from bs4 import BeautifulSoup
import re
# from pprint import pprint
from pprint import pformat

st_accept = "text/html"
st_useragent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/15.4 Safari/605.1.15")

headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
}

health_table = requests.get("https://foxhole.wiki.gg/wiki/Vehicle_Health", headers)
health_table = BeautifulSoup(health_table.text, "html.parser").body

links = {
    'T12 “Actaeon” Tankette': 'https://foxhole.wiki.gg/wiki/T12_“Actaeon”_Tankette',
    'H-5 “Hatchet”': 'https://foxhole.wiki.gg/wiki/H-5_“Hatchet”',
    'H-8 “Kranesca”': 'https://foxhole.wiki.gg/wiki/H-8_“Kranesca”',
    'H-10 “Pelekys”': 'https://foxhole.wiki.gg/wiki/H-10_“Pelekys”',
    'HC-2 “Scorpion”': 'https://foxhole.wiki.gg/wiki/Light_Infantry_Tank',
    'HC-7 “Ballista”': 'https://foxhole.wiki.gg/wiki/Siege_Tank',
    '85K-b “Falchion”': 'https://foxhole.wiki.gg/wiki/85K-b_“Falchion”',
    '85K-a_“Spatha”': 'https://foxhole.wiki.gg/wiki/85K-a_“Spatha”',
    '86K-a “Bardiche”': 'https://foxhole.wiki.gg/wiki/86K-a_“Bardiche”',
    '85V-g “Talos”': 'https://foxhole.wiki.gg/wiki/85V-g_“Talos”',
    'Lance-36': 'https://foxhole.wiki.gg/wiki/Lance-36',
    'Lance-25 “Hasta”': 'https://foxhole.wiki.gg/wiki/Lance-25_“Hasta”',
    'O-75b “Ares”': 'https://foxhole.wiki.gg/wiki/O-75b_“Ares”',
    'Cullen Predator Mk. III': 'https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III',
    'Gallagher_Outlaw_Mk._II': 'https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II',
    'Silverhand - Mk. IV': 'https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV',
    'King Spire Mk. I': 'https://foxhole.wiki.gg/wiki/King_Spire_Mk._I',
    'King Gallant Mk. II': 'https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II',
    'Devitt Mk. III': 'https://foxhole.wiki.gg/wiki/Devitt_Mk._III',
    'Devitt Ironhide Mk. IV': 'https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV',
    'Gallagher Highwayman Mk. III': 'https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III',
    'Silverhand Chieftain - Mk. VI': 'https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI',
    'Silverhand Lordscar - Mk. X': 'https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X',
    'Noble Widow MK. XIV': 'https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV',
    'Flood Mk. I': 'https://foxhole.wiki.gg/wiki/Flood_Mk._I',
    'Flood Juggernaut Mk. VII': 'https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII',
}
translation = {
    '40mm Long Barrel Cannon': '40-мм длинноствольная пушка',
    '7.92mm Hull Machine Gun': '7,92-мм корпусный пулемет',
    '40mm Cannon': '40-мм пушка',
    '68mm Cannon': '68-мм пушка',
    '7.92mm Machine Gun': '7,92-мм пулемет',
    'Bonesaw Mortar Launchers': 'минометные установки Bonesaw',
    '12.7mm Machine Gun': '12,7-мм пулемет',
    '2x 12.7mm Machine Gun': 'Два 12,7-мм пулемета',
    'Dual 20mm Cannon': 'Сдвоенная 20-мм пушка',
    '94.5mm Cannon': '94,5-мм пушка',
    '250mm Mortar': '250-мм миномет',
    '12.7mm Twin Barrel Machine Gun': '12,7-мм двухствольный пулемет',
    '2x Quad Grenade Launcher': '2 четырехствольных гранатомета',
    'Heavy Flamethrower': 'Тяжелый огнемет',
    '75mm Cannon': '75-мм пушка',
    'Double-Barrelled 75mm Cannon': 'Двуствольная 75-мм пушка',
    'Commander': 'Командир',
    'Driver': 'Мехвод',
    'Turret Gunner': 'Наводчик башни',
    'AT Gunner': 'Наводчик ПТ пушки',
    'Passenger(s)': 'Пассажиры',
    'MG Gunner': 'Наводчик пулемета',
    'Cannoneer (Gunner)': 'Наводчик',
    'Engineer': 'Инженер',
    'Middle Secondary Gunner': 'Средний вспомогательный стрелок',
    'Back Secondary Gunner': 'Задний вспомогательный стрелок',
    'Right Engineer': 'Правый инженер',
    'Left Engineer': 'Левый инженер',
    'Gunner': 'Наводчик',
    'Passenger/Commander': 'Пассажир/командир',
    'Secondary Gunner': 'Второй наводчик',
    'Gunner (Right)': 'Наводчик (Правый)',
    'Commander/Gunner (Left)': 'Командик/наводчик (левый)',
    'Commander/Machine Gunner': 'Командир/Наводчик пулемета',
    '12.7mm Coaxial Machine Gun': 'Спаренный 12,7-мм пулемет',
    '68mm Short-Barrel Cannon': '68-мм короткоствольная пушка',
}


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

    for i in assign_dict.keys():
        val1 = row.contents[assign_dict[i]].find('font').string
        val2 = row.contents[assign_dict[i]].contents[2].string.rstrip()
        table_dict[i] = f'{val1}/{val2}'

    return {name: {
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
    }}


result = {'vehicles': {}}

for i in links.values():
    result['vehicles'].update(get_vehicle_stats(i))

# pprint(result, sort_dicts=False)
f = open('output.txt', 'w+', encoding='windows-1251')
f.write(pformat(result, sort_dicts=False))
f.close()
