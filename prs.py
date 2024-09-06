from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt

from main import get_vehicle_stats
from pprint import pprint

# result = {'vehicles': {}}
#
# for i in links.values():
#     result['vehicles'].update(get_vehicle_stats(i))
# pprint(result['vehicles']['T12 “Actaeon” Tankette']['П.П/У'], sort_dicts=False)

result = {'vehicles': {'T12 “Actaeon” Tankette': {'ХП': '1150',
                                                  'Подбит при': 30,
                                                  'П.П/У': {'20мм': '4-6/6-8',
                                                            'фласки': '3/4',
                                                            'липкие бомбы': '2/3',
                                                            'рпг': '2/3',
                                                            '40мм': '2/3',
                                                            'нкг': '2/2',
                                                            '68мм': '2/2',
                                                            'мины': '1/2',
                                                            '75мм': '1/1',
                                                            '94.5мм': '1/1'},
                                                  'Броня': '7200',
                                                  'Базовый шанс пробития': '60',
                                                  'Максимальная степень износа танковой брони': '90',
                                                  'Шанс подбития подсистем': {'Гусеницы': '30'},
                                                  'Стоимость полной починки': '120',
                                                  'Скорость': {'дорога': '5.40',
                                                               'бездорожье': '4.59'},
                                                  'Объём бака': '150',
                                                  'Потребление': '6',
                                                  'Время хода': '25:00',
                                                  'Вооружение': ['12,7-мм пулемет'],
                                                  'Перезарядка': {'12,7-мм пулемет': {'Скорость перезарядки': '3.5'}},
                                                  'Экипаж': ['Мехвод',
                                                             'Наводчик пулемета',
                                                             'Пассажиры'],
                                                  'Дальность': {'12,7-мм пулемет': {'Дальность': '40'}}}}}

# pprint(result['vehicles']['T12 “Actaeon” Tankette']['П.П/У'], sort_dicts=False)

prs = Presentation('test.pptx')

title_slide_layout = prs.slide_layouts[5]
# slide = prs.slides.add_slide(title_slide_layout)
slide = prs.slides[1]
title = slide.shapes.title.text
# subtitle = slide.placeholders[1]

# subtitle.text = "python-pptx was here!"

block = slide.shapes[1].text_frame
block.clear()
# block.text = (f"1\n"
#               f"2"
#               f"{title}")
block.text = f"ХП - {result['vehicles']['T12 “Actaeon” Tankette']['ХП']} ед"

p = block.add_paragraph()
p.text = f"Броня - {result['vehicles']['T12 “Actaeon” Tankette']['Броня']} ед"

p = block.add_paragraph()
p.text = f"Подбит при - <{result['vehicles']['T12 “Actaeon” Tankette']['Подбит при']}% ХП"

p = block.add_paragraph()
p.text = "П.П/У:"

p = block.add_paragraph()
p.text = f"20мм - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['20мм']}"
p.level = 1

p = block.add_paragraph()
p.text = f"фласки - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['фласки']}"
p.level = 1

p = block.add_paragraph()
p.text = f"липкие бомбы - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['липкие бомбы']}"
p.level = 1

p = block.add_paragraph()
p.text = f"РПГ - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['рпг']}"
p.level = 1

p = block.add_paragraph()
p.text = f"40мм - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['40мм']}"
p.level = 1

p = block.add_paragraph()
p.text = f"НКГ - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['нкг']}"
p.level = 1

p = block.add_paragraph()
p.text = f"68мм - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['68мм']}"
p.level = 1

p = block.add_paragraph()
p.text = f"мины - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['мины']}"
p.level = 1

p = block.add_paragraph()
p.text = f"75мм - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['75мм']}"
p.level = 1

p = block.add_paragraph()
p.text = f"94.5мм - {result['vehicles']['T12 “Actaeon” Tankette']['П.П/У']['94.5мм']}"
p.level = 1

p = block.add_paragraph()
p.text = f"Базовый шанс пробития - {result['vehicles']['T12 “Actaeon” Tankette']['Базовый шанс пробития']}%"

p = block.add_paragraph()
p.text = f"Максимальная степень износа танковой брони - {result['vehicles']['T12 “Actaeon” Tankette']['Максимальная степень износа танковой брони']}%"

p = block.add_paragraph()
p.text = f"Шанс подбития подсистем:"

for key, value in result['vehicles']['T12 “Actaeon” Tankette']['Шанс подбития подсистем'].items():
    p = block.add_paragraph()
    p.text = f"{key} - {value}%"
    p.level = 1

# p.level = 1
for i in block.paragraphs:
    i.runs[0].font.size = Pt(15)
    i.runs[0].font.name = "Bahnschrift Condensed"
prs.save('test.pptx')

# for shape in slide.shapes:
#     print("id: %s, type: %s" % (shape.type))
# print(slide.shapes[1].text)
