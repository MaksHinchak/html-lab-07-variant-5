from pathlib import Path
from shutil import copy2
from html import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Preformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report/lab7-javascript-variant5.pdf'
DESKTOP=Path('/Users/maksimginchak/Desktop/Лабораторні/HTML/Лаба 7 JavaScript варіант 5.pdf')
pdfmetrics.registerFont(TTFont('ArialUA','/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('ArialUA',normal='ArialUA',bold='ArialBold')
pdfmetrics.registerFont(TTFont('CourierUA','/System/Library/Fonts/Supplemental/Courier New.ttf'))
BLUE=colors.HexColor('#174a7e'); LINE=colors.HexColor('#c9d8e2'); PALE=colors.HexColor('#f2f8fb')
body=ParagraphStyle('body',fontName='ArialUA',fontSize=10.5,leading=16,spaceAfter=8)
heading=ParagraphStyle('heading',fontName='ArialBold',fontSize=13,leading=18,textColor=BLUE,spaceBefore=5,spaceAfter=9)
example=ParagraphStyle('example',parent=heading,fontSize=14,leading=19,spaceAfter=11)
small=ParagraphStyle('small',parent=body,fontSize=10,leading=14)
cell=ParagraphStyle('cell',parent=body,fontSize=9,leading=13,spaceAfter=0)
white=ParagraphStyle('white',parent=cell,fontName='ArialBold',textColor=colors.white)
code=ParagraphStyle('code',fontName='CourierUA',fontSize=8,leading=10)
WIDTH=470.5512
story=[]
def p(s,style=body): return Paragraph(s,style)
def h(s): story.append(p(s,heading))
def paragraph(s,style=body): story.append(p(s,style))
def screenshot(name):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 story.append(Image(str(path),width=WIDTH,height=ht*WIDTH/w))
 story.append(Spacer(1,10))
def source(text):
 block=Preformatted(text.strip(),code)
 t=Table([[block]],colWidths=[WIDTH],hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
 story.append(t);story.append(Spacer(1,10))
def page(): story.append(PageBreak())
def example_start(title):
 story.append(p(title,example))
 story.append(p('Сторінка: javascript.html. Скріншот реального сайту у Chrome, ширина вікна 1280 px.',small))


import json
results=json.loads((ROOT/'report/check-results.json').read_text())
def grid(rows,widths):
 t=Table([[p(escape(str(s)),white if i==0 else cell) for s in row] for i,row in enumerate(rows)],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story.append(t);story.append(Spacer(1,10))
def image_fit(name,max_height):
 path=ROOT/'report'/name
 w,ht=PILImage.open(path).size
 width=min(WIDTH,max_height*w/ht)
 story.append(Image(str(path),width=width,height=ht*width/w,hAlign='LEFT'));story.append(Spacer(1,10))

story.append(Spacer(1,680));page()
h('Завдання та варіант №5')
paragraph('Розробити динамічні елементи навчального сайту ByteMarket за допомогою JavaScript. За основу взято поточні сторінки лабораторної №6. Результати сценаріїв виводяться безпосередньо на сторінці, у текстові поля textarea та журнал подій.')
grid([
 ['Пункт методички','Реалізація'],
 ['1. Спільне завдання','Обробники подій BODY на головній сторінці: завантаження, фокус, розмір вікна, друк, стан мережі, зміна якоря та вихід.'],
 ['2. Спільне завдання','Наведення, клік, подвійний клік, натискання й відпускання кнопки миші на заголовках, b та i; зміна оформлення і повідомлення.'],
 ['3.5. Варіант 5','Кнопка Run Task виводить доступні властивості об’єкта document.'],
 ['4. Додаткове','Події миші для кількох зображень: насиченість, масштаб, рамка та повідомлення.'],
 ['5.2.5. Варіант 5','Регулярними виразами знайти слова, які починаються літерою «п» і закінчуються літерою «я».'],
 ['6.5. Додаткове, варіант 5','Кнопка Array Task створює масив B із масиву A без нульових елементів.']
],[118,WIDTH-118])
h('Файли та зміни порівняно з №6')
for text in ['javascript.html - нова сторінка з трьома задачами та зображеннями.','assets/js/tasks.js - властивості document, пошук та масиви.','assets/js/events.js - події тексту й зображень, повідомлення та журнал.','assets/css/javascript.css - оформлення нових блоків і станів елементів.','index.html - обробники BODY; усі 9 сторінок отримали навігацію JavaScript і журнал.','Зміни_порівняно_з_лаб6.md та report/Захист.md - пояснення і порядок показу.']:
 story.append(p('• '+escape(text),small))
paragraph('Використано зовнішні сценарії з defer: вони запускаються після розбору HTML. Власний локальний проєкт має Git-історію етапів роботи й окремий публічний репозиторій. Сценарії цієї роботи виконуються в браузері.',small)
page()
story.append(p('Приклад 1. Події вікна, тексту та зображень',example))
story.append(p('Сторінки: index.html і javascript.html. Реальні скриншоти у Chrome.',small))
paragraph('На головній сторінці обробники записано в атрибутах BODY. Повідомлення містять час, сторінку, назву події та опис. Останні 40 записів зберігаються в sessionStorage, тому перехід на іншу сторінку не стирає журнал.')
image_fit('window-events.png',185)
source('''<body
  onload="LabEvents.record('load', 'Завантажено.')"
  onresize="LabEvents.record('resize', 'Новий розмір.')"
  onbeforeprint="LabEvents.record('beforeprint', 'Друк.')">
...
</body>''')
paragraph('Наведення підсвічує заголовки й виділений текст; клік перемикає підкреслення, подвійний клік змінює колір і нахил. Для зображень клік змінює масштаб та рамку. Клавіші Enter і пробіл дублюють дію кліку.')
image_fit('image-events.png',190)
paragraph('Використано коректну назву hashchange. Для виходу зі сторінки - pagehide: браузер не гарантує unload. Перелік подій у методичці є набором прикладів; за умовою потрібно обробити декілька подій.',small)
page()
example_start('Приклад 2. Властивості об’єкта document')
screenshot('document-task.png')
paragraph(f'У перевіреному Chrome знайдено {results["documentPropertyCount"]} властивостей. Кількість залежить від браузера. Виводяться назви й короткі представлення значень: URL, title, forms, images, методи та успадковані властивості. Довгі рядки скорочуються до 160 символів, функції й об’єкти показуються описово.')
source('''const names = new Set();
for (const name in document) names.add(name);
for (let object = document; object !== null;
     object = Object.getPrototypeOf(object)) {
  for (const name of Reflect.ownKeys(object)) {
    names.add(name);
  }
}''')
paragraph('Цикл for...in збирає перелічувані властивості. Reflect.ownKeys доповнює їх неперелічуваними і символьними ключами на кожному рівні прототипів. Set прибирає повтори. Значення читаються через Reflect.get у try...catch: недоступна властивість не перериває весь сценарій.')
paragraph('Обробник submit викликає preventDefault, щоб браузер не перезавантажував сторінку. Результат записується у value поля textarea. document.write не використано, оскільки після завантаження він може замінити поточний документ.',small)
page()
example_start('Приклад 3. Слова на «п…я»')
screenshot('search-task.png')
source(r'''const words = text.match(
  /\p{L}[\p{L}\p{M}]*(?:['’ʼ-]\p{L}[\p{L}\p{M}]*)*/gu
) || [];
const matches = words.filter(word => /^п[\s\S]*я$/iu.test(word));''')
paragraph('Перший вираз виділяє слова: літери Unicode, комбіновані знаки, внутрішній апостроф або дефіс. Другий перевіряє ціле слово: ^ - початок, п - перша літера, * - довільна кількість символів, я - остання літера, $ - кінець. Прапорець i вимикає залежність від регістру, u додає підтримку Unicode, g збирає всі слова.')
paragraph('У прикладі знайдено 6 слів: Паляниця, пісня, подія, Плаття, полум’я, пір\'я. Слова сім\'я, яблуня та поле відкидаються. Повтори зберігаються, оскільки шукаються всі входження. Якщо збігів немає, виводиться кількість 0 і пояснення.')
page()
example_start('Приклад 4. Масив без нульових елементів')
screenshot('array-task.png')
source(r'''const tokens = field.value.trim().split(/[\s,;]+/u).filter(Boolean);
const a = tokens.map(Number);
const b = a.filter(value => value !== 0);''')
paragraph('Перед перетворенням перевіряються формат кожного числа та Number.isFinite. Підтримуються від’ємні числа, десяткові дроби з крапкою та експоненційний запис. Некоректний текст позначається через setCustomValidity і reportValidity. Фрагмент вище показує основний алгоритм після перевірки введення.')
paragraph('Для A = [0, 5, -3, 0, 8, 0, -2] отримано B = [5, -3, 8, -2]. N = 7, розмір B = 4, вилучено 3 нулі. Метод filter створює новий масив і зберігає порядок решти елементів. Записи -0 та 0.0 також дорівнюють нулю. Для масиву з одних нулів B буде порожнім: [].')
h('Основні елементи форми')
paragraph('form об’єднує поля; label пов’язує підпис із полем; input приймає числа як текст; textarea містить вхідний текст або результат; button запускає дію. Атрибут readonly дозволяє копіювати результат і забороняє змінювати його. Кнопки вимкнені, доки сценарій не завантажиться; без JavaScript показано пояснення.')
page()
h('Тестові приклади та перевірка')
grid([
 ['Перевірка','Очікуваний і отриманий результат'],
 ['Run Task',f'{results["documentPropertyCount"]} властивостей; наявні URL, title, forms, images, getElementById та символьні ключі.'],
 ['Пошук у початковому тексті','6 слів: Паляниця, пісня, подія, Плаття, полум’я, пір\'я.'],
 ['Регістр, апостроф, відсутність збігів','Великі літери та три форми апострофа обробляються; за відсутності слів кількість дорівнює 0.'],
 ['A: 0, 5, -3, 0, 8, 0, -2','B: 5, -3, 8, -2; вилучено 3 нулі.'],
 ['A: 0 -0 0.0 +0','B = []; розмір 0.'],
 ['A: -2, 3.5; 0 4e1 0.01','B = [-2, 3.5, 40, 0.01].'],
 ['Некоректні числа та порожнє поле','abc, Infinity, 1e999, 0x10, 1..2 і порожнє введення відхилено.'],
 ['Події та клавіатура','Завантаження, перехід, розмір, мережа, якір і друк заносяться в журнал; текст і зображення змінюють стиль.'],
 ['390 px; JavaScript / сховище вимкнені','Нова сторінка без горизонтального виходу; без JS дії вимкнені; блокування сховища не ламає задачі.'],
 ['Навігація і локальні файли',f'Перевірено {results["checkedPages"]} HTML-сторінок та {results["checkedLocalLinks"]} локальних посилань. Помилок виконання у браузері немає.']
],[130,WIDTH-130])
paragraph('Перевірку виконано у Chrome за допомогою Playwright. Число властивостей document та їхні значення залежать від браузера й поточного стану сторінки. Детальні результати збережено у report/check-results.json.',small)
story.append(KeepTogether([
 p('Висновки',heading),
 p('Розроблено динамічні елементи сайту засобами JavaScript: обробку подій, перегляд властивостей документа, пошук слів регулярними виразами та фільтрування масиву. Для варіанта №5 реалізовано пункти 3.5, 5.2.5 і 6.5, а також спільні завдання й обробку зображень. Порівняно з лабораторною №6 додано інтерактивну сторінку та сценарії роботи з DOM і даними.'),
 p('Репозиторій',heading),
 p('<link href="https://github.com/MaksHinchak/html-lab-07-variant-5" color="#174a7e">https://github.com/MaksHinchak/html-lab-07-variant-5</link>')
]))

def decorate(c,doc):
 c.setFont('ArialUA',9); c.setFillColor(colors.HexColor('#587083'))
 c.drawRightString(538.9134,34,str(doc.page))
 if doc.page==1:
  c.setFillColor(colors.black);c.setFont('ArialUA',12)
  for y,line in [(688.89,'Чернівецький національний університет'),(669.89,'імені Юрія Федьковича'),(650.89,'Навчально-науковий інститут фізико-технічних'),(631.89,'та комп’ютерних наук')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',17)
  for y,line in [(495.89,'ЗВІТ'),(470.89,'про виконання лабораторної роботи №7'),(445.89,'з дисципліни «Веб-програмування»')]: c.drawCentredString(A4[0]/2,y,line)
  c.setFont('ArialUA',12);c.drawCentredString(A4[0]/2,423.89,'Тема: JavaScript-сценарії. Динамічні елементи')
  author_lines=[(303.39,'Виконав: студент групи 241-А'),(284.39,'Гінчак Максим Богданович'),(265.39,'Перевірив:'),(246.39,'асистент Нестеренко Володимир Васильович')]
  for y,line in author_lines: c.drawRightString(538.9134,y,line)
  c.drawCentredString(A4[0]/2,48,'Чернівці · 2026')

SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=62.3622,rightMargin=50.3622,topMargin=56,bottomMargin=46,title='Лабораторна робота №7. JavaScript. Варіант 5',author='Гінчак Максим Богданович').build(story,onFirstPage=decorate,onLaterPages=decorate)
r=PdfReader(OUT)
assert len(r.pages)==7,len(r.pages)
assert 'Висновки' in r.pages[-1].extract_text()
assert 'Репозиторій' in r.pages[-1].extract_text()
assert all('Висновки' not in p.extract_text() and 'Репозиторій' not in p.extract_text() for p in r.pages[:-1])
for index,page_obj in enumerate(r.pages):
 assert len(page_obj.extract_text())>50
 assert abs(float(page_obj.mediabox.width)-A4[0])<1
links=[a.get_object().get('/A',{}).get('/URI') for pg in r.pages for a in pg.get('/Annots',[])]
assert 'https://github.com/MaksHinchak/html-lab-07-variant-5' in links
copy2(OUT,DESKTOP)
assert OUT.read_bytes()==DESKTOP.read_bytes()
print(f'Created {len(r.pages)}-page A4 report:',DESKTOP)
