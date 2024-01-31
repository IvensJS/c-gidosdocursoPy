from tkinter import *
import sqlite3
from tkinter import messagebox

# inicio funções banco de dados

def criar_banco():
    conexao = sqlite3.connect('cadastro_alunos.db')

    cursor = conexao.cursor()

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS pessoas
                    (
                    nome TEXT,
                    cpf TEXT PRIMARY KEY,
                    telefone TEXT,
                    data_nasc TEXT
                    )
                   ''') 
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS enderecos_pessoas
                    (
                    id INTEGER PRIMARY KEY,
                    rua TEXT,
                    numero INT,
                    bairro  TEXT,
                    cidade TEXT,
                    uf TEXT,
                    pessoas_cpf TEXT,
                    FOREIGN KEY (pessoas_cpf) REFERENCES pessoas(cpf)
                    )
                    ''')

    conexao.commit()

    conexao.close()

def salvar_dados():

    cont = len(en_cpf.get())

    if cont > 0:

        conexao = sqlite3.connect('cadastro_alunos.db')

        cursor = conexao.cursor()

        cursor.execute('''
        INSERT INTO pessoas
        (nome, cpf, telefone, data_nasc)
        VALUES (?, ?, ?, ?)''',
        (en_nome.get(),
        en_cpf.get(),
        en_telefone.get(),
        en_data_nasc.get())
                       )

        cursor.execute('''
        INSERT INTO enderecos_pessoas
        (rua, numero, bairro, cidade, uf, pessoas_cpf)
        VALUES (?, ?, ?, ?, ?,?)''',
        (en_rua.get(),
        int(en_nrua.get()),
        en_bairro.get(),
        en_cidade.get(),
        en_uf.get(),
        en_cpf.get())
                       )

        conexao.commit()

        conexao.close()

        en_cpf.delete(0, END)
        en_nome.delete(0, END)
        en_telefone.delete(0, END)
        en_data_nasc.delete(0, END)
        en_rua.delete(0, END)
        en_nrua.delete(0, END)
        en_bairro.delete(0, END)
        en_cidade.delete(0, END)
        en_uf.delete(0, END)

    else:
        messagebox.showwarning('Cuidado','O campo CPF está vazio')


def ler_dados():
    
    global janela_ler, en_buscar, lb_pessoas,  lb_enderecos, en_deletar , en_atualizar

    janela_ler = Tk()
    janela_ler.title('Cadastro de Alunos')
    janela_ler.config(padx=10, pady=10)
    janela_ler.option_add('*Font', 'Verdana 12')

    # quadro de buscar dados pessoais por cpf
    fr_buscar = LabelFrame(janela_ler)
    fr_buscar.grid(row=0, column=0, sticky='we')

    lb_buscar = Label(fr_buscar, text='CPF:', anchor='e')
    lb_buscar.grid(row=0, column=0, sticky='we')

    en_buscar = Entry(fr_buscar)
    en_buscar.grid(row=0, column=1)

    bt_buscar = Button(fr_buscar, text='Buscar', command=buscar_cpf)
    bt_buscar.grid(row=0, column=2)

    # quadro de deletar dados pessoais por cpf
    fr_deletar = LabelFrame(janela_ler)
    fr_deletar.grid(row=1, column=0, sticky='we')

    lb_deletar = Label(fr_deletar, text='CPF:', anchor='e')
    lb_deletar.grid(row=0, column=0, sticky='we')

    en_deletar = Entry(fr_deletar)
    en_deletar.grid(row=0, column=1)

    bt_deletar = Button(fr_deletar, text='Excluir', command=deletar_cpf)
    bt_deletar.grid(row=0, column=2)

    # quadro para atualizar dados pessoais por cpf

    fr_atualizar = LabelFrame(janela_ler)
    fr_atualizar.grid(row=2, column=0, sticky='we')

    lb_atualizar = Label(fr_atualizar,text='CPF:', anchor='e')
    lb_atualizar.grid(row=0, column=0)

    en_atualizar = Entry(fr_atualizar)
    en_atualizar.grid(row=0, column=1)

    bt_atualizar = Button(fr_atualizar, text='Atualizar', command=janela_atualizar)
    bt_atualizar.grid(row=0, column=2)

    # quadro que lista os dados pessoais
    fr_pessoas = LabelFrame(janela_ler, text='Dados Pessoais')
    fr_pessoas.grid(row=3, column=0, sticky='we')

    lb_pessoas = Label(fr_pessoas, anchor='w')
    lb_pessoas.grid(row=0, column=0, sticky='we')

    # quadro que lista os endereços
    fr_enderecos = LabelFrame(janela_ler, text='Endereços')
    fr_enderecos.grid(row=4, column=0, sticky='we')

    lb_enderecos = Label(fr_enderecos, anchor='w')
    lb_enderecos.grid(row=1, column=0, sticky='we')

    conexao = sqlite3.connect('cadastro_alunos.db')

    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM pessoas')
    linhas = cursor.fetchall()
    for i in linhas:
        linha = str(i).replace("'", "").replace("(", "").replace(")", "")
        lb_pessoas['text'] += '\n' + str(linha)

    cursor.execute('SELECT * FROM enderecos_pessoas')
    linhas = cursor.fetchall()
    for i in linhas:
        linha = str(i).replace("'", "").replace("(", "").replace(")", "")
        lb_enderecos['text'] += '\n' + str(linha)

    conexao.close()

    janela_ler.mainloop()

def buscar_cpf():
    conexao = sqlite3.connect('cadastro_alunos.db')

    cursor = conexao.cursor()

    cursor.execute(f"SELECT * FROM pessoas WHERE cpf ='{en_buscar.get()}'")

    linha = cursor.fetchone()

    lb_pessoas['text'] = ''
    if linha:
            lb_pessoas['text'] += '\n' + str(linha).replace("'", "").replace("(", "").replace(")", "")
    else:
        messagebox.showerror("Cadastro Alunos", "Digite um CPF valido.")


    cursor.execute(f"SELECT * FROM enderecos_pessoas WHERE pessoas_cpf ='{en_buscar.get()}'")

    linha = cursor.fetchone()

    lb_enderecos['text'] = ''
    if linha:
            lb_enderecos['text'] += '\n' + str(linha).replace("'", "").replace("(", "").replace(")", "")
    else:
        messagebox.showerror("Cadastro Alunos", "Digite um CPF valido.")

def deletar_cpf():
    conexao = sqlite3.connect('cadastro_alunos.db')

    cursor = conexao.cursor()

    cursor.execute(f'DELETE FROM pessoas WHERE cpf = "{en_deletar.get()}"')

    cursor.execute(f'DELETE FROM enderecos_pessoas WHERE pessoas_cpf = "{en_deletar.get()}"')

    conexao.commit()

    conexao.close()

def janela_atualizar():

    global en_nome_up, en_data_nasc_up, en_telefone_up, en_rua_up, en_nrua_up, en_bairro_up, en_cidade_up, en_uf_up

    janela2 = Tk()
    janela2.title('Atualizar Cadastro')
    janela2.config(padx=10, pady=10)
    janela2.option_add('*Font', 'Verdana 12')

    dados_pessoas = LabelFrame(janela2, text='Dados Pessoais', padx=10, pady=10)
    dados_pessoas.grid(row=0, column=0, sticky='we')

    dados_endereco = LabelFrame(janela2, text='Endereço', padx=10, pady=10)
    dados_endereco.grid(row=1, column=0, sticky='we')

    # Widgets LabelFrame 'dados_pessoas'
    lb_nome_up = Label(dados_pessoas, text='Nome:', anchor='e')
    lb_nome_up.grid(row=0, column=0, sticky='we')

    en_nome_up = Entry(dados_pessoas)
    en_nome_up.grid(row=0, column=1, columnspan=5, sticky='we')

    lb_cpf_up = Label(dados_pessoas, text='CPF:', anchor='e')
    lb_cpf_up.grid(row=1, column=0, sticky='we')

    en_cpf_up = Label(dados_pessoas, text=f'{en_atualizar.get()}', borderwidth=3, relief='groove')
    en_cpf_up.grid(row=1, column=1)

    lb_telefone_up = Label(dados_pessoas, text='Telefone:', anchor='e')
    lb_telefone_up.grid(row=1, column=2, sticky='we')

    en_telefone_up = Entry(dados_pessoas)
    en_telefone_up.grid(row=1, column=3)

    lb_data_nasc_up = Label(dados_pessoas, text='Data Nasc.:', anchor='e')
    lb_data_nasc_up.grid(row=1, column=4, sticky='we')

    en_data_nasc_up = Entry(dados_pessoas)
    en_data_nasc_up.grid(row=1, column=5)

    # Widgets LabelFrame 'dados_endereco'

    lb_rua_up = Label(dados_endereco, text='Rua:', anchor='e')
    lb_rua_up.grid(row=0, column=0, sticky='we')

    en_rua_up = Entry(dados_endereco)
    en_rua_up.grid(row=0, column=1, columnspan=3, sticky='we')

    lb_nrua_up = Label(dados_endereco, text='N°:', anchor='e')
    lb_nrua_up.grid(row=0, column=4, sticky='we')

    en_nrua_up = Entry(dados_endereco, width=6)
    en_nrua_up.grid(row=0, column=5)

    lb_bairro_up = Label(dados_endereco, text='Bairro:', anchor='e')
    lb_bairro_up.grid(row=1, column=0, sticky='we')

    en_bairro_up = Entry(dados_endereco, width=29)
    en_bairro_up.grid(row=1, column=1)

    lb_cidade_up = Label(dados_endereco, text='Cidade:', anchor='e')
    lb_cidade_up.grid(row=1, column=2, sticky='we')

    en_cidade_up = Entry(dados_endereco, width=33)
    en_cidade_up.grid(row=1, column=3)

    lb_uf_up = Label(dados_endereco, text='UF:', anchor='e')
    lb_uf_up.grid(row=1, column=4, sticky='we')

    en_uf_up = Entry(dados_endereco, width=6)
    en_uf_up.grid(row=1, column=5)

    # widgets Frame 'quadro_botoes'

    quadro_botoes = Frame(janela2, padx=10, pady=10)
    quadro_botoes.grid(row=2, column=0, sticky='e')

    bt_gravar = Button(quadro_botoes, text='Gravar', command=atualizar_cpf)
    bt_gravar.grid(row=0, column=0)



def atualizar_cpf():
    conexao = sqlite3.connect('cadastro_alunos.db')

    cursor1 = conexao.cursor()

    cursor1.execute(f'UPDATE pessoas SET nome = "{en_nome_up.get()}",telefone = "{en_telefone_up.get()}",data_nasc = "{en_data_nasc_up.get()}" WHERE cpf = "{en_atualizar.get()}"')

    cursor2 = conexao.cursor()

    cursor2.execute(f'UPDATE enderecos_pessoas SET rua = "{en_rua_up.get()}",numero = "{en_nrua_up.get()}",bairro = "{en_bairro_up.get()}", cidade = "{en_cidade_up.get()}", uf = "{en_uf_up.get()}" WHERE pessoas_cpf = "{en_atualizar.get()}"')

    conexao.commit()

    conexao.close()


# fim funções banco de dados

# chamada da função 'criar_banco' antes da criação da GUI
criar_banco()

# inicio interface gráfica
janela = Tk()
janela.title('Cadastro de Alunos')
janela.config(padx=10, pady=10)
janela.option_add('*Font', 'Verdana 12')

# Labels Frame
dados_pessoas = LabelFrame(janela,  text= ('Dados Pessoais'), padx=10, pady=10)
dados_pessoas.grid(row=0, column=0, sticky='we')

dados_endereco = LabelFrame(janela, text='Endereço', padx=10, pady=10)
dados_endereco.grid(row=1, column=0, sticky='we')

quadro_botoes = Frame(janela, padx=10, pady=10)
quadro_botoes.grid(row=2, column=0, sticky='e')

# Widgets LabelFrame 'dados_pessoas'
lb_nome = Label(dados_pessoas, text='Nome:', anchor='e')
lb_nome.grid(row=0, column=0, sticky='we')

en_nome = Entry(dados_pessoas)
en_nome.grid(row=0, column=1, columnspan=5, sticky='we')

lb_cpf = Label(dados_pessoas, text='CPF:', anchor='e')
lb_cpf.grid(row=1, column=0, sticky='we')

en_cpf = Entry(dados_pessoas)
en_cpf.grid(row=1, column=1)

lb_telefone = Label(dados_pessoas, text='Telefone:', anchor='e')
lb_telefone.grid(row=1, column=2, sticky='we')

en_telefone = Entry(dados_pessoas)
en_telefone.grid(row=1, column=3)

lb_data_nasc = Label(dados_pessoas, text='Data Nasc.:', anchor='e')
lb_data_nasc.grid(row=1, column=4, sticky='we')

en_data_nasc = Entry(dados_pessoas)
en_data_nasc.grid(row=1, column=5)

# Widgets LabelFrame 'dados_endereco'
lb_rua = Label(dados_endereco, text='Rua:', anchor='e')
lb_rua.grid(row=0, column=0, sticky='we')

en_rua = Entry(dados_endereco)
en_rua.grid(row=0, column=1, columnspan=3, sticky='we')

lb_nrua = Label(dados_endereco, text='N°:', anchor='e')
lb_nrua.grid(row=0, column=4, sticky='we')

en_nrua = Entry(dados_endereco, width=6)
en_nrua.grid(row=0, column=5)

lb_bairro = Label(dados_endereco, text='Bairro:', anchor='e')
lb_bairro.grid(row=1, column=0, sticky='we')

en_bairro = Entry(dados_endereco, width=29)
en_bairro.grid(row=1, column=1)

lb_cidade = Label(dados_endereco, text='Cidade:', anchor='e')
lb_cidade.grid(row=1, column=2, sticky='we')

en_cidade = Entry(dados_endereco, width=33)
en_cidade.grid(row=1, column=3)

lb_uf = Label(dados_endereco, text='UF:', anchor='e')
lb_uf.grid(row=1, column=4, sticky='we')

en_uf = Entry(dados_endereco, width=6)
en_uf.grid(row=1, column=5)

# widgets Frame 'quadro_botoes'

bt_gravar = Button(quadro_botoes, text='Gravar', command=salvar_dados)
bt_gravar.grid(row=0, column=2)

bt_listar = Button(quadro_botoes, text='Listar', command=ler_dados)
bt_listar.grid(row=0, column=1)

janela.mainloop()
# fim interface gráfica