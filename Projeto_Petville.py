import sqlite3 
import tkinter as tk
from tkinter import ttk

dono=None
def conectar_db():
    conectar= sqlite3.connect('teste.db')
    return conectar
conectar=conectar_db() 
cursor=conectar.cursor()


def verificar(coisa1,coisa2):
    if coisa1==coisa2:
        return True
    else:
        return False

def abrir_erro():
  
    janela_erro=tk.Toplevel()
    mensagem_erro=tk.Label(janela_erro,text="ocorreu um erro tente novamente", font=("arial",12))
    mensagem_erro.grid(row=1,column=1)



def pesquisar(pesquisar,janela):
    pesquisar=pesquisar.get()+'%'
    c=20
    i=0
    #while c>0:
        #botao.destroy()
        #botao.grid(row=9+i,column=0)
        #i+=1
    
    cursor.execute('SELECT * FROM usuario WHERE nome LIKE ? AND tipo=?',(pesquisar,"cliente",))
    clientes=cursor.fetchall()
    i=0
    for cliente in clientes:
        cliente_id, nome_cliente,telefone_cliente,endereço_cliente,email_cliente,cpf_cliente,funcao_cliente, = cliente
        # Criando o botão para abrir a nova janela com os dados do cliente
        botao5 = tk.Button(janela, text=f"nome:{nome_cliente} telefone{telefone_cliente} endereço:{endereço_cliente} email:{email_cliente} cpf:{cpf_cliente} tipo:{funcao_cliente}",
                          command=lambda c_id=cliente_id: ver_cliente(c_id))
        botao5.grid(row=9+i,column=0)
        i+=1


def alterar_estatus(estatus,procedimento):
    cursor.execute('''
    UPDATE procedimento
    SET estatos=? WHERE id=?
    ''',(estatus,procedimento,))
    conectar.commit()








def validar_estatus(estatus,procedimento):
    if estatus==nada:
        a=abrir_erro()
    else:
        c=alterar_estatus(estatus,procedimento)






def detales_ob(cliente,procedimento):
    janela_visualisar=tk.Toplevel()
    cursor.execute('SELECT * FROM usuario WHERE id=?',(cliente,))
    clientes=cursor.fetchone()
    mensagem_visualisar=tk.Label(janela_visualisar,text=f'cliente:{clientes[1]}\n telefone:{clientes[2]}\n endereço:{clientes[3]}\n email:{clientes[4]}\n cpf:{clientes[5]}\n')
    mensagem_visualisar.grid(row=0,column=0)
    cursor.execute('SELECT * FROM procedimento WHERE id=?',(procedimento,))
    ob=cursor.fetchone()
    mensagem_visualisar2=tk.Label(janela_visualisar,text=f'veterinario:{ob[1]}\n animal:{ob[3]}\n dia:{ob[4]}\n mes:{ob[5]}\n ano:{ob[6]}\n horario:{ob[7]}-{ob[8]}\n estatus:{ob[9]}\n')
    mensagem_visualisar2.grid(row=5,column=0)
    estatus="Aberto","Terminado","Cancelado"
    estatus_ver=ttk.Combobox(janela_visualisar,values=estatus)
    estatus_ver.grid(row=14,column=1)
    mostrar_mes=tk.Label(janela_visualisar,text='mudar estatus')
    mostrar_mes.grid(row=14,column=0)
    botao_estatus=tk.Button(janela_visualisar,text='alterar estatus',command=lambda:validar_estatus(estatus_ver.get(),procedimento))
    botao_estatus.grid(row=14,column=2)




def cadastrar():
    janela_cadastro=tk.Toplevel()
    mensagem_nome=tk.Label(janela_cadastro,text="nome", font=("ariel", 15))
    mensagem_nome.grid(row=1,column=0)
    nome=tk.Entry(janela_cadastro)
    nome.grid(row=1,column=1)

    mensagem_telefone=tk.Label(janela_cadastro,text="telefone", font=("ariel", 15))
    mensagem_telefone.grid(row=2,column=0)
    telefone=tk.Entry(janela_cadastro)
    telefone.grid(row=2,column=1)

    mensagem_endereço=tk.Label(janela_cadastro,text="endereço", font=("ariel", 15))
    mensagem_endereço.grid(row=3,column=0)
    endereço=tk.Entry(janela_cadastro)
    endereço.grid(row=3,column=1)

    mensagem_email=tk.Label(janela_cadastro,text="email", font=("ariel", 15))
    mensagem_email.grid(row=5,column=0)
    email=tk.Entry(janela_cadastro)
    email.grid(row=5,column=1)

    mensagem_cpf=tk.Label(janela_cadastro,text="cpf", font=("ariel", 15))
    mensagem_cpf.grid(row=6,column=0)
    cpf=tk.Entry(janela_cadastro)
    cpf.grid(row=6,column=1)

    mensagem_funcao=tk.Label(janela_cadastro,text="tipo de cadastro", font=("ariel", 15))
    mensagem_funcao.grid(row=7,column=0)
    funcao=ttk.Combobox(janela_cadastro,values=funcaoes)
    funcao.grid(row=7,column=1)



    botao1=tk.Button(janela_cadastro,text="cadastro",command=lambda:validar_cadastro(nome,telefone,endereço,email,cpf,funcao))
    botao1.grid(row=8,column=0)


def pesquisar_ob(dia,mes,ano,janela):

    
    cursor.execute('SELECT * FROM procedimento WHERE  dia LIKE ? AND mes LIKE ? AND ano LIKE ?',('%'+dia+'%','%'+mes+'%','%'+ano+'%',))
    obs=cursor.fetchall()
    i=0
    aberto=0
    terminado=0
    cancelado=0
    id_procedimento=[]
    cliente_id=[]
    
    for linha in obs:
        cursor.execute('SELECT * FROM usuario WHERE id=?',(linha[2],))
        cliente=cursor.fetchone()
        cliente=cursor.fetchone()
        id_procedimento.append(int(linha[0]))
        cliente_id.append(int(cliente[0]))
        botao_ob=tk.Button(janela,text=f"veterinario:{linha[1]},cliente:{cliente[1]},animal:{linha[3]},data:{linha[4]}/{linha[5]}/{linha[6]}, horario: {linha[7]}-{linha[8]}, estatus:{linha[9]}",command=lambda id_c=cliente_id[i],id_p=id_procedimento[i]:detales_ob(id_c,id_p))
        botao_ob.grid(row=1+i,column=0)
       
        i+=1
        if linha[9]=='Aberto':
            aberto+=1
        if linha[9]=='Terminado':
            terminado+=1
        if linha[9]=='Cancelado':
            cancelado+=1
    mensagem_completa=tk.Label(janela,text=f"abertos:{aberto} terminados:{terminado} cancelado:{cancelado}")
    mensagem_completa.grid(row=25,column=0)







def mostrar_obs():

    janela_mostrar=tk.Toplevel()
    mostrar_dia=tk.Label(janela_mostrar,text='dia', font=("arial", 12))
    mostrar_dia.grid(row=0,column=0)
    dia_ver=ttk.Combobox(janela_mostrar,values=list(dic_dia))
    dia_ver.grid(row=0,column=1)
    mostrar_mes=tk.Label(janela_mostrar,text='mes', font=("arial", 12))
    mostrar_mes.grid(row=0,column=2)
    mes_ver=ttk.Combobox(janela_mostrar,values=list(dic_mes))
    mes_ver.grid(row=0,column=3)
    mostrar_ano=tk.Label(janela_mostrar,text='ano', font=("arial", 12))
    mostrar_ano.grid(row=0,column=4)
    ano_ver=ttk.Combobox(janela_mostrar,values=list(dic_ano))
    ano_ver.grid(row=0,column=5)
    botao_mostrar_ob=tk.Button(janela_mostrar,text='aplicar pesquisa',command=lambda:pesquisar_ob(dia_ver.get(),mes_ver.get(),ano_ver.get(),janela_mostrar))
    botao_mostrar_ob.grid(row=0,column=6)
    botao_clientes=tk.Button(janela_mostrar,text="cadastrados",command=lambda:mostrar_clientes())
    botao_clientes.grid(row=0,column=7)




   
    janela_mostrar.geometry("1680x900")





    cursor.execute('SELECT * FROM procedimento' )
    obs=cursor.fetchall()
    i=0
    aberto=0  
    terminado=0
    cancelado=0
    id_procedimento=[]
    cliente_id=[]









    for linha in obs:
        cursor.execute('SELECT * FROM usuario WHERE id=?',(linha[2],))
        cliente=cursor.fetchone()
        id_procedimento.append(int(linha[0]))
        cliente_id.append(int(cliente[0]))
        botao_ob=tk.Button(janela_mostrar,text=f"veterinario:{linha[1]},cliente:{cliente[1]},animal:{linha[3]},data:{linha[4]}/{linha[5]}/{linha[6]}, horario: {linha[7]}-{linha[8]}, estatus:{linha[9]}",command=lambda id_c=cliente_id[i],id_p=id_procedimento[i]:detales_ob(id_c,id_p), width=150)
        botao_ob.grid(row=3+i,column=0,columnspan=6)
        if linha[9]=='Aberto':
            aberto+=1
        if linha[9]=='Terminado':
            terminado+=1
        if linha[9]=='Cancelado':
            cancelado+=1
        i+=1
    mensagem_completa=tk.Label(janela_mostrar,text=f"abertos:{aberto} terminados:{terminado} cancelado:{cancelado}", font=("arial", 12))
    mensagem_completa.grid(row=25,column=0)


def colocar_procedimento(cliente,animal,dia,mes,ano,horai,horaf,veterinario):
    cursor.execute('''
        INSERT INTO procedimento ( veterinario,cliente,animal,dia,mes,ano,data_inicial,data_final,estatos) VALUES(?,?,?,?,?,?,?,?,?)
    ''',(veterinario,cliente,animal,dia,mes,ano,horai,horaf,"Aberto",))
    conectar.commit()
    a=mostrar_obs()





def verificar_ob(cliente,animal,dia,mes,ano,horai,horaf,veterinario):
    
    td=True
    if dia==nada:
        f=abrir_erro()
    if mes==nada:
        f=abrir_erro()
    if ano==nada:
        f=abrir_erro()
    if horai==nada:
        f=abrir_erro()
    if horaf==nada:
        f=abrir_erro()
    if veterinario==nada:
        f=abrir_erro()
    else:
        v=colocar_procedimento(cliente,animal,dia,mes,ano,horai,horaf,veterinario)





dic_dia=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
dic_mes=("1","2","3","4","5","6","7","8","9","10","11","12")
dic_ano={"2024":1,"2025":2,"2026":3,"2027":4,"2028":5,"2029":6,"2030":7,"2031":8}

dic_final={"00:00":0,"00:30":1,"01:00":2,"01:30":3,"02:00":4,"02:30":5,"03:00":6,"03:30":7,"04:00":8,"04:30":9,"05:00":10,"05:30":11,"06:00":12,"06:30":13,"07:00":14,"07:30":15,"08:00":16,"08:30":17,"09:00":18,"09:30":19,"10:00":20,"10:30":21,"11:00":22,"11:30":23,"12:00":24,"12:30":25,"13:00":26,"13:30":27,"14:00":28,"14:30":29,"15:00":30,"15:30":31,"16:00":32,"16:30":33,"17:00":34,"17:30":35,"18:00":36,"18:30":37,"19:00":38,"19:30":39,"20:00":40,"20:30":41,"21:00":42,"21:30":43,"22:00":44,"22:30":45,"23:00":46,"23:30":47,}

def fazer_ob(animal,clientes):

        janela_ob=tk.Toplevel()
        cursor.execute('SELECT * FROM usuario WHERE id = ? ',(clientes,))
        cliente=cursor.fetchone()
        if cliente:
        # Exibindo os dados do cliente na nova janela

            cliente_ver = tk.Label(janela_ob, text=f"Nome: {cliente[1]}\ntelefone: {cliente[2]}\nendereço: {cliente[3]}\nemail: {cliente[4]}\ncpf: {cliente[5]}\nfunção: {cliente[6]}", font=("arial", 12))
            cliente_ver.grid(row=0,column=0)
            animal_ver=tk.Label(janela_ob,text=animal)
            animal_ver.grid(row=7,column=0)

            cursor.execute('SELECT * FROM usuario WHERE tipo = ? ',("veterinario(a)",))
            resultados=cursor.fetchall()
            animais_dic={}
            i=1
            for linha in resultados:
                botar_animal=f"{linha[1]}"
                animais_dic[botar_animal]=int(linha[0])
                i=+1
            animais=list(animais_dic.keys())
            
            anos=list(dic_ano.keys())
            dic_inicial={"00:00":0,"00:30":1,"01:00":2,"01:30":3,"02:00":4,"02:30":5,"03:00":6,"03:30":7,"04:00":8,"04:30":9,"05:00":10,"05:30":11,"06:00":12,"06:30":13,"07:00":14,"07:30":15,"08:00":16,"08:30":17,"09:00":18,"09:30":19,"10:00":20,"10:30":21,"11:00":22,"11:30":23,"12:00":24,"12:30":25,"13:00":26,"13:30":27,"14:00":28,"14:30":29,"15:00":30,"15:30":31,"16:00":32,"16:30":33,"17:00":34,"17:30":35,"18:00":36,"18:30":37,"19:00":38,"19:30":39,"20:00":40,"20:30":41,"21:00":42,"21:30":43,"22:00":44,"22:30":45,"23:00":46,"23:30":47,}
            
            
            horaf=list(dic_final.keys())

            mensagem_veterinario=tk.Label(janela_ob,text="veterinario", font=("arial", 12))
            mensagem_veterinario.grid(row=8,column=0)
            veterinario_ver=ttk.Combobox(janela_ob,values=animais)
            veterinario_ver.grid(row=8,column=1)

            mensagem_dia=tk.Label(janela_ob,text="dia", font=("arial", 12))
            mensagem_dia.grid(row=9 ,column=0)
            dia=ttk.Combobox(janela_ob,values=dic_dia)
            dia.grid(row=9,column=1)

            mensagem_mes=tk.Label(janela_ob,text="mes", font=("arial", 12))
            mensagem_mes.grid(row=10,column=0)
            mes=ttk.Combobox(janela_ob,values=dic_mes)
            mes.grid(row=10,column=1)

            mensagem_ano=tk.Label(janela_ob,text="ano", font=("arial", 12))
            mensagem_ano.grid(row=11,column=0)
            ano=ttk.Combobox(janela_ob,values=anos)
            ano.grid(row=11,column=1)

            mensagem_hora_i=tk.Label(janela_ob,text="inicio do procedimento", font=("arial", 12))
            mensagem_hora_i.grid(row=12,column=0)
            hora_i=ttk.Combobox(janela_ob,values=list(dic_inicial.keys()))
            hora_i.grid(row=12,column=1)

            mensagem_hora_f=tk.Label(janela_ob,text="final do procedimento", font=("arial", 12))
            mensagem_hora_f.grid(row=13,column=0)
            hora_f=ttk.Combobox(janela_ob,values=list(dic_final.keys()))
            hora_f.grid(row=13,column=1)
            hora_ini=hora_i.get()
            horafin=hora_f.get()
            if hora_ini in dic_inicial:
                horaini= dic_inicial.values(hora_ini)
            
           


            botao_procedimento=tk.Button(janela_ob,text="fazer o procedimento",command=lambda:verificar_ob(clientes,animal,dia.get(),mes.get(),ano.get(),hora_i.get(),hora_f.get(),veterinario_ver.get()), font=("arial", 12))
            botao_procedimento.grid(row=14,column=0)


def validar_ob(animal,cliente):
    if animal==nada:
        c=abrir_erro()
    else:
        e=fazer_ob(animal,cliente)



def ver_cliente(animal):
    janela_cliente=tk.Toplevel()
    cursor.execute("SELECT * FROM usuario WHERE id = ?", (animal,))
    cliente = cursor.fetchone()  # Recuperando o cliente com o id fornecido

    botao4=tk.Button(janela_cliente,text="animais",command=lambda:cadastrar_animais(animal), font=("arial", 12))
    botao4.grid(row=8,column=2)

    if cliente:
        # Exibindo os dados do cliente na nova janela
        cliente_ver = tk.Label(janela_cliente, text=f"Nome: {cliente[1]}\ntelefone: {cliente[2]}\nendereço: {cliente[3]}\nemail: {cliente[4]}\ncpf:\nfunção: {cliente[6]}", font=("arial",12))
        cliente_ver.grid(row=0,column=0)

        cursor.execute('SELECT * FROM animal WHERE dono = ? ',(animal,))
        resultados=cursor.fetchall()
        animais_dic={}
        i=1
        for linha in resultados:

#
#
#
#
#
#
#
#
#
            botar_animal=f"nome: {linha[1]}-especie:{linha[2]}-raça:{linha[3]}"
        
            animais_dic[botar_animal]=i
            i=+1
        animais=list(animais_dic.keys())
        animais_ver=ttk.Combobox(janela_cliente,values=animais)
        animais_ver.grid(row=7,column=0)

        bootao_ob=tk.Button(janela_cliente,text="adicionar operação",command=lambda:validar_ob(animais_ver.get(),animal), font=("arial", 12))
        bootao_ob.grid(row=8,column=1)

    else:
        label = tk.Label(janela_cliente, text="Cliente não encontrado.", font=("arial", 12))
        label.pack(padx=20, pady=20)
    
   
def mostrar_clientes():
    janela_clientes=tk.Toplevel()
    janela_clientes.geometry("1680x900")
    mensagem_pesquisa=tk.Label(janela_clientes,text="pesquisa", font=("arial", 12))
    mensagem_pesquisa.grid(row=0,column=0)
    pesquisa=tk.Entry(janela_clientes)
    pesquisa.grid(row=0,column=1)

    botao6=tk.Button(janela_clientes,text="pesquisar",command=lambda:pesquisar(pesquisa,janela_clientes), font=("arial", 12))
    botao6.grid(row=0,column=2)
    botao7=tk.Button(janela_clientes,text="cadastrar",command=lambda:cadastrar(), font=("arial", 12))
    botao7.grid(row=0,column=3)

    

    cursor.execute('SELECT * FROM usuario WHERE tipo=?',("cliente",))
    clientes=cursor.fetchall()
    i=0
    for cliente in clientes:
        cliente_id, nome_cliente,telefone_cliente,endereço_cliente,email_cliente,cpf_cliente,funcao_cliente, = cliente
        # Criando o botão para abrir a nova janela com os dados do cliente
        botao5 = tk.Button(janela_clientes, text=f"nome:{nome_cliente} telefone{telefone_cliente} endereço:{endereço_cliente} email:{email_cliente} cpf:{cpf_cliente} tipo:{funcao_cliente}",
                          command=lambda c_id=cliente_id: ver_cliente(c_id), width=150)
        
        botao5.grid(row=9+i,column=0)
        i+=1



def colocar_tabela_login(nome,telefone,endereço,email,cpf,funcao):
    cursor.execute('''
        INSERT INTO usuario(nome,telefone,endereço,email,cpf,tipo) VALUES(?,?,?,?,?,?)
    ''',(nome.get(),telefone.get(),endereço.get(),email.get(),cpf.get(),funcao.get()))
    conectar.commit()

    
    

def validar_cadastro(nome,telefone,endereço,email,cpf,funcao):
    if nome.get()==nada:
        c=abrir_erro()
    elif telefone.get()==nada:
        c=abrir_erro()
    elif endereço.get()==nada:
        c=abrir_erro()
    elif email.get()==nada:
        c=abrir_erro()
    elif cpf.get()==nada:
        c=abrir_erro()
    elif funcao.get()==nada:
        c=abrir_erro()
    else:
        a=colocar_tabela_login(nome,telefone,endereço,email,cpf,funcao)



def confirmar_login():

    cursor.execute('SELECT * FROM usuario WHERE nome = ? AND email = ? AND telefone  = ? AND endereço = ? AND cpf = ?',(nome.get(),email.get(),telefone.get(),endereço.get(),cpf.get()))
    resultados=cursor.fetchone()
    if resultados:
        a=mostrar_obs()
        conectar.close
    else:
        b=abrir_erro()
    
def validar_login():
    if nome.get()==nada:
        c=abrir_erro()
    elif telefone.get()==nada:
        c=abrir_erro()
    elif endereço.get()==nada:
        c=abrir_erro()
    elif email.get()==nada:
        c=abrir_erro()
    elif cpf.get()==nada:
        c=abrir_erro()
    else:
        a=confirmar_login()

def validar_animal(nome,telefone,endereço,email,cpf,nome_animal,especie,raça,janela):
    if nome==nada:
        c=abrir_erro()
    elif telefone==nada:
        c=abrir_erro()
    elif endereço==nada:
        c=abrir_erro()
    elif email==nada:
        c=abrir_erro()
    elif cpf==nada:
        c=abrir_erro()
    elif nome_animal.get()==nada:
        c=abrir_erro()
    elif especie.get()==nada:
        c=abrir_erro()
    elif raça.get()==nada:
        c=abrir_erro()
    else:
        cursor.execute('SELECT * FROM usuario WHERE nome = ? AND email = ? AND telefone  = ? AND endereço = ? AND cpf = ?AND tipo = ?',(nome,email,telefone,endereço,cpf,"cliente"))
        data=cursor.fetchone()
        if data:
            dono=int(data[0])
            d=colocar_animais(nome_animal,especie,raça,dono)

def colocar_animais(nome_animal,especie,raça,dono):
    cursor.execute('''
        INSERT INTO animal(nome_animal,especie,raça,dono) VALUES(?,?,?,?)
    ''',(nome_animal.get(),especie.get(),raça.get(),dono))
    conectar.commit()
    

def cadastrar_animais(cliente):
    janela_animais=tk.Toplevel()
    cursor.execute('SELECT * FROM usuario WHERE id=?',(cliente,))
    resposta=cursor.fetchone()
    nome=resposta[1]
    telefone=resposta[2]
    endereço=resposta[3]
    email=resposta[4]
    cpf=resposta[5]
    
    mensagem_nome_animal=tk.Label(janela_animais,text="nome do animal", font=("arial", 12))
    mensagem_nome_animal.grid(row=7,column=0)
    nome_animal=tk.Entry(janela_animais)
    nome_animal.grid(row=7,column=1)
    
    mensagem_especie=tk.Label(janela_animais,text="qual a especie do animal?", font=("arial", 12))
    mensagem_especie.grid(row=8,column=0)
    especie=tk.Entry(janela_animais)
    especie.grid(row=8,column=1)
    
    mensagem_raça=tk.Label(janela_animais,text="qual a raça do animal?", font=("arial", 12))
    mensagem_raça.grid(row=9,column=0)
    raça=tk.Entry(janela_animais)
    raça.grid(row=9,column=1)
    
    
    

    botao3=tk.Button(janela_animais,text="login",command=lambda:validar_animal(nome,telefone,endereço,email,cpf,nome_animal,especie,raça,janela_animais), font=("arial",12))
    botao3.grid(row=10,column=1)
    
   





def criar_tabela():
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone INTEGER NOT NULL,
            endereço TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf INTEGER NOT NULL,
            tipo TEXT NOT NULL
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_animal TEXT NOT NULL,
            especie TEXT NOT NULL,
            raça TEXT NOT NULL,
            dono INTEGER NOT NULL
        )''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procedimento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            veterinario TEXT NOT NULL,
            cliente INTEGER NOT NULL,
            animal TEXT NOT NULL,
            dia INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            data_inicial TEXT NOT NULL,
            data_final TEXT NOT NULL,
            estatos TEXT NOT NULL
        )
    ''')
    
    








    
    #cursor.execute('''
    #    INSERT INTO cadastro(nome,email) VALUES(?,?)
    #''',(nome,email))
    #conectar.commit()
    
    #cursor.execute('SELECT * FROM cadastro')
    #resultados=cursor.fetchall()
    #i=0
    #for linha in resultados:
        #mensagem=tk.Label(janela,text=f'ID:{linha[0]},nome:{linha[1]},email:{linha[2]}')
        #mensagem.grid(row=2+i,column=0)
        #i+=1
    #conectar.close
funcaoes=("cliente","secretario(a)","veterinario(a)","gerente")
janela_login=tk.Tk()
nada=""

tamanho_tela_x = janela_login.winfo_screenwidth()
tamanho_tela_y = janela_login.winfo_screenheight()

# Definir a largura e altura da janela
largura = 300
altura = 250

# Calcular a posição x e y para centralizar a janela
posicao_x = (tamanho_tela_x // 2) - (largura // 2)
posicao_y = (tamanho_tela_y // 2) - (altura // 2)

# Configurar a geometria da janela
janela_login.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")



criartabela=criar_tabela()
mensagem_nome=tk.Label(text="nome", font=("arial", 15))
width=15
height=15
mensagem_nome.grid(row=1,column=0)
nome=tk.Entry()
nome.grid(row=1,column=1)

mensagem_telefone=tk.Label(text="telefone", font=("arial", 15))
width=15
height=15
mensagem_telefone.grid(row=2,column=0)
telefone=tk.Entry()
telefone.grid(row=2,column=1)

mensagem_endereço=tk.Label(text="endereço", font=("arial", 15))
width=15
height=15
mensagem_endereço.grid(row=3,column=0)
endereço=tk.Entry()
endereço.grid(row=3,column=1)

mensagem_email=tk.Label(text="email", font=("arial", 15))
width=15
height=15
mensagem_email.grid(row=5,column=0)
email=tk.Entry()
email.grid(row=5,column=1)

mensagem_cpf=tk.Label(text="cpf", font=("arial", 15))
width=15
height=15
mensagem_cpf.grid(row=6,column=0)
cpf=tk.Entry()
cpf.grid(row=6,column=1)


cursor.execute('''
        INSERT INTO usuario(nome,telefone,endereço,email,cpf,tipo) VALUES(?,?,?,?,?,?)
    ''',("silvio josé da silva pinto",5547912345678,"SC, joinville, jardim paraiso, rua aquarius, 123","silvio_j_pinto@estudante.sesisenai.org.br",1234565678910,"cliente",))
conectar.commit()


botao2=tk.Button(janela_login,text="login",command=validar_login, font=("arial", 15))
botao2.grid(row=8,column=1)




janela_login.mainloop()
