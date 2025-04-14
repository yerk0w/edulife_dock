import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Создаем директорию для шаблонов, если она не существует
TEMPLATES_DIR = os.path.join(os.getcwd(), "app", "static", "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Регистрируем шрифт для поддержки кириллицы
# Замените путь к шрифту на актуальный для вашей системы
try:
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    font_name = 'DejaVuSerif'
except:
    # Если шрифт не установлен, используем стандартный
    font_name = 'Helvetica'

def create_application_template():
    """Создает шаблон заявления"""
    file_path = os.path.join(TEMPLATES_DIR, "application_form.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont(font_name, 14)
    c.drawString(30*mm, 280*mm, "ЗАЯВЛЕНИЕ")
    
    # Шапка
    c.setFont(font_name, 12)
    c.drawString(130*mm, 270*mm, "Директору ВУЗа")
    c.drawString(130*mm, 265*mm, "Иванову И.И.")
    c.drawString(130*mm, 260*mm, "от студента группы _________")
    c.drawString(130*mm, 255*mm, "_________________________")
    c.drawString(130*mm, 250*mm, "(ФИО)")
    
    # Линии для текста заявления
    c.setFont(font_name, 12)
    for i in range(8):
        y_pos = 230*mm - i*10*mm
        c.line(30*mm, y_pos, 180*mm, y_pos)
    
    # Место для подписи
    c.drawString(30*mm, 140*mm, "Дата: ________________")
    c.drawString(130*mm, 140*mm, "Подпись: ________________")
    
    c.save()
    return file_path

def create_reference_template():
    """Создает шаблон справки"""
    file_path = os.path.join(TEMPLATES_DIR, "reference_form.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont(font_name, 14)
    c.drawString(80*mm, 280*mm, "СПРАВКА")
    
    # Содержание
    c.setFont(font_name, 12)
    c.drawString(30*mm, 260*mm, "Настоящая справка выдана _________________________________")
    c.drawString(30*mm, 250*mm, "в том, что он/она действительно является студентом(кой) _________ курса")
    c.drawString(30*mm, 240*mm, "группы _____________ факультета _________________________")
    c.drawString(30*mm, 230*mm, "________________________________________________.")
    
    # Дополнительная информация
    c.drawString(30*mm, 210*mm, "Справка выдана для предъявления по месту требования.")
    
    # Место для подписи и печати
    c.drawString(30*mm, 180*mm, "Дата выдачи: ________________")
    c.drawString(30*mm, 170*mm, "Декан факультета: ________________")
    c.drawString(30*mm, 160*mm, "Секретарь: ________________")
    
    # Место для печати
    c.drawString(130*mm, 160*mm, "М.П.")
    c.circle(140*mm, 150*mm, 15*mm, stroke=1, fill=0)
    
    c.save()
    return file_path

def create_permission_slip_template():
    """Создает шаблон заявления на отпуск"""
    file_path = os.path.join(TEMPLATES_DIR, "permission_slip.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont(font_name, 14)
    c.drawString(30*mm, 280*mm, "ЗАЯВЛЕНИЕ НА ОТПУСК")
    
    # Шапка
    c.setFont(font_name, 12)
    c.drawString(130*mm, 270*mm, "Директору ВУЗа")
    c.drawString(130*mm, 265*mm, "Иванову И.И.")
    c.drawString(130*mm, 260*mm, "от _____________________")
    c.drawString(130*mm, 255*mm, "_________________________")
    c.drawString(130*mm, 250*mm, "(ФИО)")
    
    # Текст заявления
    c.drawString(30*mm, 230*mm, "Прошу предоставить мне отпуск с _____________ по _____________")
    c.drawString(30*mm, 220*mm, "в связи с _________________________________________________")
    c.drawString(30*mm, 210*mm, "____________________________________________________________")
    
    # Место для подписи
    c.drawString(30*mm, 180*mm, "Дата: ________________")
    c.drawString(130*mm, 180*mm, "Подпись: ________________")
    
    c.save()
    return file_path

def main():
    """Создает все шаблоны"""
    application_path = create_application_template()
    reference_path = create_reference_template()
    permission_slip_path = create_permission_slip_template()
    
    print(f"Созданы шаблоны:")
    print(f"1. Заявление: {application_path}")
    print(f"2. Справка: {reference_path}")
    print(f"3. Заявление на отпуск: {permission_slip_path}")

if __name__ == "__main__":
    main()