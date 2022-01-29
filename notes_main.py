import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget, QPushButton, QTextEdit, QVBoxLayout, QWidget

notes = {
    "Инструкция":
        {
            "текст": "т.к. инструкцию мне писать лень, разбирайтесь сами.\nЗато все работает стабильно.\nТолько смайлики не сохраняйте в заметках, крашнет и не сохранит.",
            "теги": ["ленивый разраб", "инструкция", "гайд"]
        },
}

try:
    with open("notes_data.json", "r") as f:
        notes = json.load(f)
except:
    with open("notes_data.json", "w") as f:
        json.dump(notes, f, sort_keys=True, ensure_ascii=False)

with open("notes_data.json", "r") as f:
        notes = json.load(f)
print(notes)


app = QApplication([])


# Главное окно
MainWindow = QWidget()
MainWindow.setWindowTitle("Умные заметки")
MainWindow.resize(900, 600)


# Виджеты
TextEdit = QTextEdit()

TextListNotes = QLabel('Список заметок')
ListNotes = QListWidget()

ButtonCreateNote = QPushButton('Создать заметку')
ButtonDeleteNote = QPushButton('Удалить заметку')
ButtonSaveNote = QPushButton('Сохранить заметку')

TextListTag = QLabel('Список тегов')
ListTag = QListWidget()

LineEditTag = QLineEdit()
LineEditTag.setPlaceholderText('Введите тег...')

ButtonSaveTag = QPushButton('Добавить к заметке')
ButtonDeleteTag = QPushButton('Открепить от заметки')
ButtonFindTag = QPushButton('Искать заметки по тегу')


# Лейауты
verticaLayout = QVBoxLayout()
verticaLayout.addWidget(TextListNotes)
verticaLayout.addWidget(ListNotes)
hor1 = QHBoxLayout()
hor1.addWidget(ButtonCreateNote)
hor1.addWidget(ButtonDeleteNote)
verticaLayout.addLayout(hor1)
verticaLayout.addWidget(ButtonSaveNote)

verticaLayout.addWidget(TextListTag)
verticaLayout.addWidget(ListTag)
verticaLayout.addWidget(LineEditTag)

hor2 = QHBoxLayout()
hor2.addWidget(ButtonSaveTag)
hor2.addWidget(ButtonDeleteTag)
verticaLayout.addLayout(hor2)
verticaLayout.addWidget(ButtonFindTag)


mainLayout = QHBoxLayout()
mainLayout.addWidget(TextEdit, stretch=2)
mainLayout.addLayout(verticaLayout, stretch=1)
mainLayout.setSpacing(15)

MainWindow.setLayout(mainLayout)
MainWindow.show()


def create_note():
    name, result = QInputDialog.getText(
        MainWindow, "Добавить заметку", "Название заметки:"
    )
    if result and name != '':
        notes[name] = {"текст": "", "теги": []}
        ListNotes.clear()
        ListNotes.addItems(notes.keys())
        TextEdit.clear()
        ListTag.clear()

def save_note():
    key = ListNotes.selectedItems()
    if key:
        key = key[0].text()
        notes[key]["текст"] = TextEdit.toPlainText()
        with open("notes_data.json", "w") as f:
            json.dump(notes, f, sort_keys=True, ensure_ascii=False)

def  delete_note():
    key = ListNotes.selectedItems()
    if key:
        key = key[0].text()
        del notes[key]
        ListNotes.clear()
        TextEdit.clear()
        ListTag.clear()
        ListNotes.addItems(notes.keys())
        with open("notes_data.json", "w") as f:
            json.dump(notes, f, sort_keys=True, ensure_ascii=False)

def show_info():
    key = ListNotes.selectedItems()[0].text()
    TextEdit.setText(notes[key]["текст"])
    ListTag.clear()
    ListTag.addItems(notes[key]["теги"])

def save_tag():
    key = ListNotes.selectedItems()
    if key:
        key = key[0].text()
        new_tags = LineEditTag.text().split(", ")
        notes[key]["теги"] += new_tags
        ListTag.addItems(new_tags)
        LineEditTag.clear()

def delete_tag():
    key = ListNotes.selectedItems()
    if key:
        key = key[0].text()
        tag = ListTag.selectedItems()
        if tag:
            tag = tag[0].text()
            notes[key]["теги"].remove(tag)
            ListTag.clear()
            ListTag.addItems(notes[key]["теги"])

def find_tag():
    global notes
    tag = LineEditTag.text()
    if tag:
        ListNotes.clear()
        TextEdit.clear()
        ListTag.clear()
        for note in notes:
            if tag in notes[note]["теги"]:
                ListNotes.addItem(note)

    else:
        with open("notes_data.json", "r") as f:
            notes = json.load(f)
        ListNotes.clear()
        TextEdit.clear()
        ListTag.clear()
        ListNotes.addItems(notes.keys())


ListNotes.itemClicked.connect(show_info)
ButtonCreateNote.clicked.connect(create_note)
ButtonSaveNote.clicked.connect(save_note)
ButtonDeleteNote.clicked.connect(delete_note)
ButtonSaveTag.clicked.connect(save_tag)
ButtonDeleteTag.clicked.connect(delete_tag)
ButtonFindTag.clicked.connect(find_tag)



ListNotes.addItems(notes.keys())

app.exec_()