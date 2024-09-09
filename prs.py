from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt

from main import get_vehicle_stats
from pprint import pprint

# for slide in prs.slides:
#     text = slide.shapes.title.text
#     print(links[text] if text in links else None)
#
# quit()

# for i in links.values():
#     result['vehicles'].update(get_vehicle_stats(i))
# pprint(result['vehicles']['T12 “Actaeon”tank_name['П.П/У'], sort_dicts=False)

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
    'Gallagher Outlaw Mk. II': 'https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II',
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
    'Cullen Predator Mk. III': 'https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III',
}

# result = {'vehicles': {}}

prs = Presentation('test.pptx')
# slide = prs.slides[3]
# block = slide.shapes[1].text_frame.text
# print(block)
# quit()

for slide in prs.slides:
    text = slide.shapes.title.text
    if text in links:
        tank_name = text
        result = get_vehicle_stats(links[tank_name])


        block = slide.shapes[1].text_frame

        block.text = f"ХП - {result['ХП']} ед"

        p = block.add_paragraph()
        p.text = f"Броня - {result['Броня']} ед"

        p = block.add_paragraph()
        p.text = f"Подбит при - <{result['Подбит при']}% ХП"

        p = block.add_paragraph()
        p.text = "П.П/У: |"
        for key, value in result['П.П/У'].items():
            p.text += f" {key} - {value} |"

        p = block.add_paragraph()
        p.text = f"Базовый шанс пробития - {result['Базовый шанс пробития']}%"

        p = block.add_paragraph()
        p.text = f"Максимальная степень износа танковой брони - {result['Максимальная степень износа танковой брони']}%"

        p = block.add_paragraph()
        p.text = "Шанс подбития подсистем:"

        for key, value in result['Шанс подбития подсистем'].items():
            p = block.add_paragraph()
            p.text = f"{key} - {value}%"
            p.level = 1

        for i in block.paragraphs:
            i.runs[0].font.size = Pt(16)
            i.runs[0].font.name = "Bahnschrift Condensed"
        prs.save('test.pptx')

        block = slide.shapes[2].text_frame

        block.text = f"Стоимость полной починки - {result['Стоимость полной починки']} бматов"

        p = block.add_paragraph()
        p.text = (f"Скорость: по дороге - {result['Скорость']['дорога']} м/с, "
                  f"по внедорожью - {result['Скорость']['бездорожье']} м/с")

        p = block.add_paragraph()
        p.text = f"Объём бака: {result['Объём бака']} л"

        p = block.add_paragraph()
        p.text = f"Потребление: {result['Потребление']} л/мин"

        p = block.add_paragraph()
        p.text = f"Время хода: {result['Время хода']}"

        p = block.add_paragraph()
        p.text = "Вооружение:"

        for i in result['Вооружение']:
            weapon_name = i
            reload_dict = result['Перезарядка'][weapon_name]

            if 'Время стрельбы' in reload_dict:
                weapon_reload = f"{reload_dict['Время стрельбы']} + {reload_dict['Скорость перезарядки']}"
            else:
                weapon_reload = f"{reload_dict['Скорость перезарядки']}"

            weapon_range = result['Дальность'][weapon_name]['Дальность']

            p = block.add_paragraph()
            text = f"{weapon_name} | {weapon_reload} сек. | {weapon_range} метров"
            p.text = text
            p.level = 1

        p = block.add_paragraph()
        p.text = "Экипаж:"

        for i in result['Экипаж']:
            p = block.add_paragraph()
            p.text = i
            p.level = 1

        for i in block.paragraphs:
            i.runs[0].font.size = Pt(16)
            i.runs[0].font.name = "Bahnschrift Condensed"
        prs.save('test.pptx')
