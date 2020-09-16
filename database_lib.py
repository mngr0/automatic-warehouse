import mysql.connector

cnx = mysql.connector.connect(user='marco', password='password',
                              host='127.0.0.1',
                              database='test')

mycursor = cnx.cursor()
try:
    mycursor.execute("""CREATE OR REPLACE TABLE categorie ( 
            id INT KEY AUTO_INCREMENT, 
            descr VARCHAR(100)  
            ) """)
except Exception as e:
    print(e)


mycursor.execute("""CREATE OR REPLACE TABLE sottocategorie (
        id INT KEY, 
        id_cat INT NOT NULL, 
        descr VARCHAR(100), 
        CONSTRAINT `fk_sottocat` 
          FOREIGN KEY(id_cat) REFERENCES categorie(id) 
          ON UPDATE SET NULL
          ON DELETE SET NULL
        ) """)

print("created subcat")


mycursor.execute("""CREATE OR REPLACE TABLE armadi (
        id INT KEY,
        descr VARCHAR(100)  
        ) """)

mycursor.execute("""CREATE OR REPLACE TABLE cassetti (
        id INT KEY, 
        id_cat INT,
        id_guida INT,
        posizione INT,
        altezza INT
        ) """)

mycursor.execute("""CREATE OR REPLACE TABLE guide ( 
        id INT KEY,
        id_armadio INT,
        n_slot INT,
        pos_x INT,
        pos_y INT,
        interasse INT
        ) """)

mycursor.execute("""CREATE OR REPLACE TABLE forme (
        id INT KEY, 
        descr VARCHAR(100)  
        ) """)

mycursor.execute("""CREATE OR REPLACE TABLE buchi (
        id INT KEY, 
        id_cassetto INT,
        id_forma INT
        ) """)


mycursor.execute("""CREATE OR REPLACE TABLE prodotti (
        id INT KEY AUTO_INCREMENT,
        id_cat INT,
        id_sottocat INT,
        codice_fornitore INT,
        valore VARCHAR(100),
        package VARCHAR(100),
        id_buco INT,
        descrizione VARCHAR(100),
        datasheet VARCHAR(100)
        ) """)



#i can use this to have one component in multpile slots
mycursor.execute("""CREATE OR REPLACE TABLE magazzino (
        id_prod INT,
        id_buco INT KEY,
        amount INT,
        ) """)



def add_product( id_fornitore, descr, value, package, datasheet ):
    #generate id product
    mycursor.execute("""INSERT INTO prodotti (
                id_prod, valore, package, datasheet)
            
            VALUES('%s', '%s', %s', %s' )
            """%(str(id_fornitore), str(value), str(package), str(datasheet)))




def search_product(id_fornitore, id_interno, parametrivari):
    #restituisco linea tabella prodotti, da cui posso sapere slot e cassetto.
    #se non c'e' un id, ma solo parametri restituiso una lista
    pass


def query_invoicex_and_get_new_products():
    pass

def search_cassetto(tema, forma, id_interno):
    #tema/forma da una lista di cassetti con slot validi
    #id_interno da una lista di cassetti con slot contenenti quell' id
    pass

def remove_product_from_slot(slot):
    #slot should be empty


def place_component(product, slot, quantity):
    #check if slot is free
    #while going in the storage update height
    pass

def add_cassetto(slots, theme):
    #check that slots have known shapes
    pass

def place_cassetto(cassetto):
    #search for location big enough to place given cassetto
    pass


cnx.close()
