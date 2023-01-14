import mysql.connector
import time

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

#Check if user can create database before
def create_database(dbcursor,database_name):
    dbcursor.execute("CREATE DATABASE "+ database_name)

    return

def create_table(dbcursor,table_name,lista_de_headers):
    if checkTableExists(mydb,table_name) == False:
        create_table_string="CREATE TABLE "+table_name +" ("
        for i in range (0,len(lista_de_headers)-1):
            create_table_string+= lista_de_headers[i] +" VARCHAR(255), "
        create_table_string+= lista_de_headers[-1] +" VARCHAR(255))"
        dbcursor.execute(create_table_string)
        
    else:
        print(table_name + " already exists")
    return

def read_from_table(dbcursor,table,headers):
    string_to_read=("SELECT ")
    for i in range(0,len(headers)-1):
        string_to_read+=headers[i]+","
    string_to_read+=headers[-1]+" FROM "+table
    dbcursor.execute(string_to_read)
    query= dbcursor.fetchall()
    for x in query:
        print(x)

def read_from_table_where(dbcursor,table,headers,where):
    string_to_read=("SELECT ")
    for i in range(0,len(headers)-1):
        string_to_read+=headers[i]+","
    string_to_read+=headers[-1]+" FROM "+table +" WHERE "+ where
    dbcursor.execute(string_to_read)
    query= dbcursor.fetchall()
    for x in query:
        print(x)

def insert_table(mydb,dbcursor,table_name,headers, valores):
    update_string_sql="INSERT INTO " + table_name + " ("
    for i in range (0,len(headers)-1):
        update_string_sql+=headers[i]+ ", "
    update_string_sql+=headers[-1]+ ") VALUES (%s, %s, %s)"
    dbcursor.execute(update_string_sql, valores)
    mydb.commit()
    return()

def multiple_insert_table(mydb,dbcursor,table_name,headers, valores):
    update_string_sql="INSERT INTO " + table_name + " ("
    for i in range (0,len(headers)-1):
        update_string_sql+=headers[i]+ ", "
    update_string_sql+=headers[-1]+ ") VALUES (%s, %s, %s)"
    dbcursor.executemany(update_string_sql, valores)
    mydb.commit()
    return()

def update_table(mydb,dbcursor,table_name,new_value, old_value):
    update_sql = "UPDATE "+table_name+ " SET " + new_value +" WHERE "+ old_value
    #print(update_sql)
    dbcursor.execute(update_sql)
    mydb.commit()
    print(dbcursor.rowcount, "record(s) affected")
    return()

def delete_from_table(mydb,dbcursor,table_to_delete,Delete_WHERE):
    delete_sql = "DELETE FROM " +table_to_delete+ " WHERE "+Delete_WHERE
    dbcursor.execute(delete_sql)
    mydb.commit()
    print(dbcursor.rowcount, "record(s) deleted")
    return()

def drop_table(dbcursor,table_name):
    drop_string="DROP TABLE " + table_name
    dbcursor.execute(drop_string)
    return() 

def mini_tour(mydb,dbcursor):
    print("Ola, bem vindo as minhas funcoes CRUD para MYSQL em Python")
    time.sleep(5)
    print("Coloquei esse tour aqui para caso sempre ter um guia das funcoes mais usadas em MYSQL sem ter que procurar")
    time.sleep(3)
    print("No inicio do Main, ja coloquei as informacoes de Login. Altere para sua necessidade")
    time.sleep(3)
    print("Vamos Comecar - Primeiro Criamos uma tabela")
    time.sleep(3)
    print("O comando eh 'create_table(dbcursor,table_name='NomedaTabela',lista_de_headers=[Header1,Header2,Header3]")
    time.sleep(3)
    print("E bem intuitivo, se voce souber MYSQL as substituicoes sao obvias")
    time.sleep(3)
    print("Criamos uma tabela chamada 'TabelaTeste' com headers 'Descricao', 'Quantidade' e 'Preco'")
    time.sleep(3)
    create_table(dbcursor,table_name='TabelaTeste',lista_de_headers=['Descricao','Quantidade','Preco'])
    time.sleep(3)
    print("Se a tabela ja existir, uma funcao e uma flag impede que criemos outra")
    time.sleep(3)
    print("Para comecar, adicionemos 10 tomates que custam 1,50")
    print("insert_table(mydb,dbcursor,table_name='TabelaTeste',headers=['Descricao','Quantidade','Preco'],valores=['Tomate','10','1,50'])")
    insert_table(mydb,dbcursor,table_name='TabelaTeste',headers=['Descricao','Quantidade','Preco'],valores=['Tomate','10','1,50'])
    time.sleep(3)
    print("Com a tabela criada, usamos a funcao read para ver se ela foi criada")
    print("read_from_table(dbcursor,table='TabelaTeste',headers=[*])")
    read_from_table(dbcursor,table='TabelaTeste',headers=['*'])
    time.sleep(3)
    print("Adicionamos tambem 12 batatas por 1,20 e 14 cebolas por 1,60")
    multiple_insert_table(mydb,dbcursor,table_name='TabelaTeste',headers=['Descricao','Quantidade','Preco'],valores=[('Batata','12','1,20'),('Cebola','14','1,60')])
    print("multiple_insert_table(mydb,dbcursor,table_name='TabelaTeste',headers=['Descricao','Quantidade','Preco'],valores=[('Batata','12','1,20'),('Cebola','14','1,60')])")
    time.sleep(3)
    print("Pensando bem, acho que a cebola deveria custar 2,10. Vamos alterar isso")
    print("update_table(mydb,dbcursor,table_name='TabelaTeste',new_value= 'Preco = '2,10'', old_value='Descricao = 'Cebola'')")
    update_table(mydb,dbcursor,table_name='TabelaTeste',new_value="Preco = '2,10'", old_value="Descricao = 'Cebola'")
    time.sleep(3)
    print("Vamos ver o novo preco da cebola")
    print("read_from_table_where(dbcursor,table='TabelaTeste',headers=['Preco'],where='Descricao = 'Cebola''")
    read_from_table_where(dbcursor,table='TabelaTeste',headers=["Preco"],where="Descricao = 'Cebola'")
    print("Agora vamos deletar o tomate da base")
    print("delete_from_table(mydb,dbcursor,table_to_delete='TabelaTeste',Delete_WHERE= 'Descricao = 'Tomate'')")
    delete_from_table(mydb,dbcursor,table_to_delete='TabelaTeste',Delete_WHERE="Descricao = 'Tomate'")
    read_from_table(dbcursor,table='TabelaTeste',headers=['*'])
    print("Isso e tudo. Para finalizar, essa tabela SQL ira se autodestruir em 5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("drop_table(dbcursor,table_name='TabelaTeste')")
    drop_table(dbcursor,table_name='TabelaTeste')
    print("Obrigado por vir. Olhe o codigo para entender melhor")
    return()

#main        
#information from database
#change as needed
mydb = mysql.connector.connect(
  host="localhost",
  user="userCRUD", 
  password="passwordCRUD!",
  database="NomedaBase"
 )

dbcursor=mydb.cursor()

mini_tour(mydb,dbcursor)

