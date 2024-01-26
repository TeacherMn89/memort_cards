from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout

app = QApplication([])
notes = []

'''Інтерфейс програми'''
# параметри вікна програми
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

# віджети вікна програми
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

button_note_create = QPushButton('Створити замітку')  # з'являється вікно з полем "Введіть ім'я замітки"
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

# розташування віджетів по лейаутах
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

'''Функціонал програми'''


def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])


def add_note():
    # Викликається діалогове вікно для введення назви замітки
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки: ")
    # Перевірка, чи користувач ввів назву та чи натиснув "OK" у діалоговому вікні
    if ok and note_name != "":
        # Створюється новий об'єкт замітки у вигляді списку
        note = [note_name, '', []]
        # Додається замітка до загального списку
        notes.append(note)
        # Додається назва замітки до віджету списку
        list_notes.addItem(note[0])
        # Додається список тегів до віджету тегів
        list_tags.addItems(note[2])
        # Виводиться вміст заміток у консоль (для дебагу)
        print(notes)
        # Записується назва замітки у текстовий файл з ім'ям, що відповідає індексу замітки
        with open(str(len(notes) - 1) + ".txt", "w") as file:
            file.write(note[0] + '\n')


def save_note():
    # Перевірка, чи обрано якусь замітку
    if list_notes.selectedItems():
        # Отримання тексту (назви) обраної замітки
        key = list_notes.selectedItems()[0].text()
        # Ініціалізація змінної для відстеження індексу обраної замітки
        index = 0
        # Проходження по списку заміток
        for note in notes:
            # Знаходження замітки за її назвою
            if note[0] == key:
                # Оновлення тексту замітки з вмістом текстового поля
                note[1] = field_text.toPlainText()
                # Записування змін до файлу за відповідним індексом
                with open(str(index) + ".txt", "w") as file:
                    file.write(note[0] + '\n')
                    file.write(note[1] + '\n')
                   # Записування тегів замітки
                    for tag in note[2]:
                        file.write(tag + ' ')
                    file.write('\n')
            # Збільшення індексу для наступної замітки
            index += 1
        # Виведення вмісту заміток після змін для дебагу
        print(notes)
    else:
        # Виведення повідомлення, якщо замітка для збереження не вибрана
        print("Замітка для збереження не вибрана!")


# обробка подій
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)

# запуск програми
notes_win.show()

name = 0
note = []
# Ініціалізація змінних
while True:
    # Формування імені файлу
    filename = str(name) + ".txt"
    try:
        # Відкриття файлу для читання
        with open(filename, "r") as file:
            # Читання кожного рядка файлу
            for line in file:
                # Видалення символу нового рядка
                line = line.replace('\n', '')
                # Додавання рядка до змінної note
                note.append(line)
        # Розбивання рядка тегів на окремі теги
        tags = note[2].split(' ')
        note[2] = tags
        # Додавання створеної замітки до списку заміток
        notes.append(note)
        # Очищення змінної note для наступної ітерації
        note = []
        # Збільшення числа для формування наступного імені файлу
        name += 1
    except IOError:
        # Обрив циклу, якщо сталася помилка відкриття файлу (зазвичай, коли всі файли були зчитані)
        break

print(notes)
for note in notes:
    list_notes.addItem(note[0])

app.exec_()
