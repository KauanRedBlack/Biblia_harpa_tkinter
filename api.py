import json
import requests
import keyboard
import time
import os

count_ver = 1
count_cap = 1
# BIBLE_LINK = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_nvi.json"
BIBLE_LINK = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_aa.json"
# BIBLE_LINK = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/pt_acf.json"

def fetch_bible_data():
    """
    Busca os dados da Bíblia a partir do link fornecido.
    """
    try:
        response = requests.get(BIBLE_LINK)
        response.raise_for_status()
        return json.loads(response.text.encode())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bible data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding Bible data: {e}")
        return None


class Bible:
    """
    Classe que encapsula os dados da Bíblia e fornece métodos para busca.
    """

    def __init__(self):
        self.data = fetch_bible_data()
        self.count_ver = 1
        self.count_cap = 1
        self.f =[]

    def get_book_name(self, search="all"):
        """
        Retorna o número do livro procurado ou imprime a lista de todos os livros.
        """
        if not self.data:
            return "Error: Bible data not available"
        for index, book in enumerate(self.data):
            # for iten in self.data:
            #     self.f.append(f'''{iten['name']}''')
            # # print(self.f)
            if search == "all":
                pass
                return f"{index + 1}: {book.get('name')}"
            elif search == book.get("name"):
                return index + 1
        return None

    def get_words(self, book_name: str, chapter: int=None, verse: int=None, book_number=None):
        """
        Retorna o versículo desejado ou imprime uma mensagem de erro se o versículo não existe.
        """
        if not self.data:
            return "Error: Bible data not available"
        if not book_number:
            book_number = self.get_book_name(book_name)
            if book_number is None:
                return f"Error: book '{book_name}' not found"
        try:
            if verse == len(self.data[book_number]['chapters']):
                len(self.data[book_number]['chapters'][0])
                chapter += 1
            return self.data[book_number - 1]["chapters"][chapter - 1][verse - 1]
        except (IndexError, TypeError):
            book = self.data[book_number - 1].get('name')

            return f"Error: invalid chapter or verse for book '{book}'"

    def get_book_chapters(self, search:str):
        for index, book in enumerate(self.data):

            if search == book.get("name"):
                list_of_chapters = []
                c = 0
                book['chapters'][0]
                for cap in book['chapters']:
                    c += 1
                    list_of_chapters.append(c)
                return list_of_chapters
        return None
                #len(book['chapters'])

    def next_verse (self, choice_verse, chapter_selected):
        self.count_cap = int(chapter_selected)
        _ = f'{self.count_cap}.{self.count_ver} - {self.get_words(choice_verse, self.count_cap, self.count_ver)}'
        self.count_ver += 1
        return _

    def previous_verse (self, choice_verse, chapter_selected):
        self.count_cap = int(chapter_selected)
        self.count_ver -= 1
        if self.count_ver == 1:
            pass
        else:
            _ = f'{self.count_cap}.{self.count_ver} - {self.get_words(choice_verse, self.count_cap, self.count_ver)}'
            return _
        
    def next_chapter (self, choose_chapter, chapter_selected):
        self.count_cap = int(chapter_selected) + 1
        self.count_ver = 1
        _ = f'{self.count_cap}.{self.count_ver} - {self.get_words(choose_chapter, self.count_cap, self.count_ver)}'
        return _

    def previous_chapter (self, choose_chapter, chapter_selected):
        self.count_cap = int(chapter_selected) - 1
        self.count_ver = 1
        _ = f'{self.count_cap}.{self.count_ver} - {self.get_words(choose_chapter, self.count_cap, self.count_ver)}'
        return _
