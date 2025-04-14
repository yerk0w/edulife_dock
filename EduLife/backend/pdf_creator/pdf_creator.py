# pdf_creator.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Путь для сохранения шаблонов
TEMPLATES_DIR = "output"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def create_application_template():
    """Создает шаблон заявления"""
    file_path = os.path.join(TEMPLATES_DIR, "application_form.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont("Helvetica", 14)
    c.drawString(30*mm, 280*mm, "ZAYAVLENIE")
    
    # Шапка
    c.setFont("Helvetica", 12)
    c.drawString(130*mm, 270*mm, "Direktoru VUZa")
    c.drawString(130*mm, 265*mm, "Ivanovu I.I.")
    c.drawString(130*mm, 260*mm, "ot studenta gruppy _________")
    c.drawString(130*mm, 255*mm, "_________________________")
    c.drawString(130*mm, 250*mm, "(FIO)")
    
    # Линии для текста заявления
    c.setFont("Helvetica", 12)
    for i in range(8):
        y_pos = 230*mm - i*10*mm
        c.line(30*mm, y_pos, 180*mm, y_pos)
    
    # Место для подписи
    c.drawString(30*mm, 140*mm, "Data: ________________")
    c.drawString(130*mm, 140*mm, "Podpis: ________________")
    
    c.save()
    return file_path

def create_reference_template():
    """Создает шаблон справки"""
    file_path = os.path.join(TEMPLATES_DIR, "reference_form.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont("Helvetica", 14)
    c.drawString(80*mm, 280*mm, "SPRAVKA")
    
    # Содержание
    c.setFont("Helvetica", 12)
    c.drawString(30*mm, 260*mm, "Nastoyashaya spravka vydana _________________________________")
    c.drawString(30*mm, 250*mm, "v tom, chto on/ona deystvitelno yavlyaetsya studentom(koy) _________ kursa")
    c.drawString(30*mm, 240*mm, "gruppy _____________ fakulteta _________________________")
    c.drawString(30*mm, 230*mm, "________________________________________________.")
    
    # Дополнительная информация
    c.drawString(30*mm, 210*mm, "Spravka vydana dlya predyavleniya po mestu trebovaniya.")
    
    # Место для подписи и печати
    c.drawString(30*mm, 180*mm, "Data vydachi: ________________")
    c.drawString(30*mm, 170*mm, "Dekan fakulteta: ________________")
    c.drawString(30*mm, 160*mm, "Sekretar: ________________")
    
    # Место для печати
    c.drawString(130*mm, 160*mm, "M.P.")
    c.circle(140*mm, 150*mm, 15*mm, stroke=1, fill=0)
    
    c.save()
    return file_path

def create_permission_slip_template():
    """Создает шаблон заявления на отпуск"""
    file_path = os.path.join(TEMPLATES_DIR, "permission_slip.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    
    # Заголовок
    c.setFont("Helvetica", 14)
    c.drawString(30*mm, 280*mm, "ZAYAVLENIE NA OTPUSK")
    
    # Шапка
    c.setFont("Helvetica", 12)
    c.drawString(130*mm, 270*mm, "Direktoru VUZa")
    c.drawString(130*mm, 265*mm, "Ivanovu I.I.")
    c.drawString(130*mm, 260*mm, "ot _____________________")
    c.drawString(130*mm, 255*mm, "_________________________")
    c.drawString(130*mm, 250*mm, "(FIO)")
    
    # Текст заявления
    c.drawString(30*mm, 230*mm, "Proshu predostavit mne otpusk s _____________ po _____________")
    c.drawString(30*mm, 220*mm, "v svyazi s _________________________________________________")
    c.drawString(30*mm, 210*mm, "____________________________________________________________")
    
    # Место для подписи
    c.drawString(30*mm, 180*mm, "Data: ________________")
    c.drawString(130*mm, 180*mm, "Podpis: ________________")
    
    c.save()
    return file_path

if __name__ == "__main__":
    print("Создание PDF-шаблонов...")
    application_path = create_application_template()
    reference_path = create_reference_template()
    permission_slip_path = create_permission_slip_template()
    
    print(f"Созданы шаблоны в директории {TEMPLATES_DIR}:")
    print(f"1. Заявление: {application_path}")
    print(f"2. Справка: {reference_path}")
    print(f"3. Заявление на отпуск: {permission_slip_path}")
    
    # Инструкция для копирования файлов
    print("\nТеперь скопируйте эти файлы в директорию app/static/templates/ вашего проекта")