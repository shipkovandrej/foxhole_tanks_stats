from pptx import Presentation
from pptx.util import Pt

from main import get_vehicle_stats
from config import links

prs = Presentation('test.pptx')

# text_frames index testing

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
