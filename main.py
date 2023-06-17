import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Tk, Label, font
from api import Bible
import sqlite3
bible = Bible()

chapters = ['Gênesis', 'Êxodo', 'Levítico', 'Números', 'Deuteronômio', 'Josué', 'Juízes', 'Rute', '1 Samuel', '2 Samuel', '1 Reis', '2 Reis', '1 Crônicas', 
            '2 Crônicas', 'Esdras', 'Neemias', 'Ester', 'Jó', 'Salmos', 'Provérbios', 'Eclesiastes', 'Cânticos', 'Isaías', 'Jeremias', 'Lamentações de Jeremias', 
            'Ezequiel', 'Daniel', 'Oséias', 'Joel', 'Amós', 'Obadias', 'Jonas', 'Miquéias', 'Naum', 'Habacuque', 'Sofonias', 'Ageu', 'Zacarias', 'Malaquias', 
            'Mateus', 'Marcos', 'Lucas', 'João', 'Atos', 'Romanos', '1 Coríntios', '2 Coríntios', 'Gálatas', 'Efésios', 'Filipenses', 'Colossenses', 
            '1 Tessalonicenses', '2 Tessalonicenses', '1 Timóteo', '2 Timóteo', 'Tito', 'Filemom', 'Hebreus', 'Tiago', '1 Pedro', '2 Pedro', '1 João', 
            '2 João', '3 João', 'Judas', 'Apocalipse']

class ExibidorDeTexto:
    def __init__(self):
        # height = altura
        # width = largura
        self.bible_passage = ''
        self.chapter_selected = ''
        self.chapter_biblical_passage  =''
        self.janela = tk.Tk()
        self.janela.configure(bg="black")  # Define o fundo preto
        # self.janela.title = "Concerto com Deus"
        largura = 800
        altura = 710
        pos_x = (self.janela.winfo_screenwidth() - largura) // 2
        pos_y = (self.janela.winfo_screenheight() - altura) // 2
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        fonte_negrito = font.Font(family="Arial", size=15, weight="bold")

        frame1 = tk.Frame(self.janela, bg="black", highlightbackground="LightGrey", highlightthickness=2)
        frame1.pack(side="bottom", fill="y", ipadx=15)

        frame2 = tk.Frame(frame1, bg="black", highlightbackground="LightGrey", highlightthickness=2)
        frame2.pack(side="right", fill="y", ipadx=15)

        frame3 = tk.Frame(frame2, bg="black",)
        frame3.pack(side="bottom", fill="y", ipadx=15)

        frame4 = tk.Frame(frame1, bg="black",)
        frame4.pack(side="top", fill="y", ipadx=15)

        self.scrolled_text = scrolledtext.ScrolledText(self.janela, font=(font.Font(family="Arial", size=60, weight="bold")), wrap=tk.WORD, width=65, 
        height=35 , fg="white", bg="black")
        self.scrolled_text.pack(pady=10)

        self.aling_text('Biblia')

        self.botao = tk.Button(frame1, text="<", command=self.previous_verse) #Versiculo Anterior
        self.botao.pack(ipadx=11, ipady=3, padx=28, pady=3, side="left")

        self.botao1 = tk.Button(frame1, text=">", command=self.next_verse) #Próximo versiculo
        self.botao1.pack(ipadx=11, ipady=3, padx=28, pady=3,side="right")

        self.chosen_book = ttk.Combobox(frame4, values=chapters, state="readonly", justify='center', height=1, width=15, font=fonte_negrito)
        self.chosen_book.current(0)
        self.chosen_book.pack(ipady=2, ipadx=2,side="top")
        self.chosen_book.bind("<<ComboboxSelected>>", self.atualizar_valor)

        self.combo_itens = ttk.Combobox(frame4, state="readonly", justify='center', height=1, width=15, font=fonte_negrito)
        self.combo_itens.pack(ipady=2, ipadx=2,side="bottom")

        conn = sqlite3.connect('database_new.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [tabela[0] for tabela in cursor.fetchall()]

        self.combo = ttk.Combobox(frame3, state="readonly", justify='center', height=1, width=20, font=fonte_negrito)
        self.combo["values"] = tabelas
        self.combo.current(0)  # Seleciona a primeira tabela por padrão
        self.combo.pack(ipady=2, ipadx=2,side="top")

        exibir_botao = tk.Button(frame3, text="Exibir", command=self.exibir_conteudo)
        exibir_botao.pack(side="bottom")

        self.praise_christian_harp = tk.Label(frame2, text="Harpa Cristã", justify='center', font=fonte_negrito, fg="white", bg="black")
        self.praise_christian_harp.pack(side="top")

    def exibir_conteudo(self,):
        tabela_selecionada = self.combo.get()
        
        if tabela_selecionada:
            # Obter o conteúdo da tabela selecionada
            conn = sqlite3.connect('database_new.db')
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM {tabela_selecionada}')
            resultado = cursor.fetchall() ######
            
            nova_janela = tk.Toplevel(self.janela)
            nova_janela.title(f'{tabela_selecionada}')
            nova_janela.configure(bg="black")  # Define o fundo preto
            largura = 800
            altura = 710
            pos_x = (nova_janela.winfo_screenwidth() - largura) // 2
            pos_y = (nova_janela.winfo_screenheight() - altura) // 2
            nova_janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
            
            scrolled_text = scrolledtext.ScrolledText(nova_janela, font=("Arial", 60), wrap=tk.WORD, width=65, 
            height=35 , fg="white", bg="black")
            scrolled_text.pack(pady=10)

            cursor.execute(f'PRAGMA table_info({tabela_selecionada})')
            colunas = [info[1] for info in cursor.fetchall()]
            praisen = 0
            chorus_praise = ''
            activate_chorus_praise = False
            for linha in resultado:
                praisen += 1 #linha[1]
                if praisen == 2 or praisen == 4 or praisen == 6 or praisen == 8 or praisen == 10:
                    if activate_chorus_praise == False:
                        chorus_praise = f'\n\n{linha[1]}'
                        activate_chorus_praise = True
                        scrolled_text.insert(tk.END, chorus_praise)
                        scrolled_text.tag_configure("center", justify='center')
                        scrolled_text.tag_add("center", "1.0", "end")
                    else:
                        scrolled_text.insert(tk.END, chorus_praise)
                        scrolled_text.tag_configure("center", justify='center')
                        scrolled_text.tag_add("center", "1.0", "end")
                else:
                    praise = f'\n\n{linha[1]}'
                    scrolled_text.insert(tk.END, praise)
                    scrolled_text.tag_configure("center", justify='center')
                    scrolled_text.tag_add("center", "1.0", "end")

    def atualizar_valor(self, event):
        _ =bible.get_book_chapters(self.chosen_book.get())
        self.combo_itens["values"] = _
        self.combo_itens.current(0)

    def formatar_texto(self, texto, palavras_por_linha=5):
        palavras = texto.split()  # Separa o texto em palavras
        linhas = []
        linha_atual = ""

        for i, palavra in enumerate(palavras, 1):
            palavra.replace("(","").replace(")","").replace("\n","")
            linha_atual += palavra + " "

            if i % palavras_por_linha == 0:
                linhas.append(linha_atual.strip())  # Remove espaços extras no final da linha
                linha_atual = ""

        if linha_atual:
            linhas.append(linha_atual.strip())

        texto_formatado = "\n".join(linhas)

        return texto_formatado

    def aling_text(self, text:str):
        self.scrolled_text.delete("1.0", tk.END)
        self.scrolled_text.insert(tk.END, f'\n{text}')
        self.scrolled_text.tag_configure("center", justify='center')
        self.scrolled_text.tag_add("center", "1.0", "end")

    def next_verse (self):
        self.bible_passage = self.chosen_book.get().replace("\n", "")
        self.chapter_selected = self.combo_itens.get()
        _ =bible.next_verse(self.bible_passage, self.chapter_selected)
        _ = str(_)
        ret = self.formatar_texto(_)
        texto = ret
        self.aling_text(texto)

    def previous_verse (self):
        self.bible_passage = self.chosen_book.get().replace("\n", "")
        self.chapter_selected = self.combo_itens.get()
        _ =bible.previous_verse(self.bible_passage, self.chapter_selected)
        _ = str(_)
        ret = self.formatar_texto(_)
        texto = ret
        self.aling_text(texto)

    def next_chapter (self):
        self.bible_passage = self.chosen_book.get().replace("\n", "")
        self.chapter_selected = self.combo_itens.get()
        _ =bible.next_chapter(self.bible_passage, self.chapter_selected)
        _ = str(_)
        ret = self.formatar_texto(_)
        texto = ret
        self.aling_text(texto)

    def previous_chapter (self):
        self.bible_passage = self.chosen_book.get().replace("\n", "")
        self.chapter_selected = self.combo_itens.get()
        _ =bible.previous_chapter(self.bible_passage, self.chapter_selected)
        _ = str(_)
        ret = self.formatar_texto(_)
        texto = ret
        self.aling_text(texto)

    def exibir_janela(self):
        self.janela.mainloop()

exibidor = ExibidorDeTexto()

exibidor.exibir_janela()