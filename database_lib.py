import mysql.connector

class DBmanager:
    def __init__(self,restart=0):
        self.cnx = mysql.connector.connect(user='marco', password='password',
                                      host='127.0.0.1')
        self.mycursor = self.cnx.cursor()
        if restart:
            self.mycursor.execute("DROP DATABASE test")
            print("DROPPED")
            self.mycursor.execute("CREATE DATABASE test")
            print("RECREATED")
        self.mycursor.execute("USE test")
        if restart:
            self.create_db()
            self.create_armadio()

    def create_db(self):
        self.mycursor.execute("""CREATE OR REPLACE TABLE categorie (
                    id_cat INT KEY AUTO_INCREMENT,
                    descr VARCHAR(100)
                    ) """)

        print("created categorie")
        self.mycursor.execute("""CREATE OR REPLACE TABLE sottocategorie (
                id_sottocat INT KEY AUTO_INCREMENT,
                id_cat INT NOT NULL,
                descr VARCHAR(100),
                CONSTRAINT `fk_sottocat`
                  FOREIGN KEY(id_cat) REFERENCES categorie(id)
                  ON UPDATE CASCADE
                  ON DELETE CASCADE
                ) """)

        print("created subcat")


        self.mycursor.execute("""CREATE OR REPLACE TABLE armadi (
                id_armadio INT KEY AUTO_INCREMENT,
                descr VARCHAR(100)
                ) """)
    
        print("created armadi")
        
        self.mycursor.execute("""CREATE OR REPLACE TABLE cassetti (
                id_cassetto INT KEY AUTO_INCREMENT,
                id_cat INT,
                id_guida INT,
                posizione INT,
                altezza INT
                ) """)

        print("created cassetti")

        self.mycursor.execute("""CREATE OR REPLACE TABLE guide (
                id_guida INT KEY AUTO_INCREMENT,
                id_armadio INT,
                n_slot INT,
                pos_x INT,
                pos_y INT,
                pos_z INT,
                interasse INT
                ) """)
        print("created guide")
        
        self.mycursor.execute("""CREATE OR REPLACE TABLE forme (
                id_forma INT KEY AUTO_INCREMENT,
                descr VARCHAR(100)
                ) """)
        print("created forme")

        self.mycursor.execute("""CREATE OR REPLACE TABLE slots (
                id_slot INT KEY AUTO_INCREMENT,
                id_cassetto INT,
                id_forma INT
                ) """)
        print("created slots")


        
        #self.mycursor.execute("""CREATE TABLE packages (
        #        id_package INT KEY AUTO_INCREMENT,
        #        descrizione VARCHAR(100)
        #        ) """)
        #print("created prodotti")



        self.mycursor.execute("""CREATE OR REPLACE TABLE prodotti (
                id_prodotto INT KEY AUTO_INCREMENT,
                id_cat INT,
                id_sottocat INT,
                codice_fornitore INT,
                valore VARCHAR(100),
                package VARCHAR(100),
                id_buco INT,
                descrizione VARCHAR(100),
                datasheet VARCHAR(500)                ) """)

        print("created prodotti")


        #i can use this to have one component in multpile slots
        self.mycursor.execute("""CREATE OR REPLACE TABLE magazzino (
                id_prodotto INT,
                id_slot INT KEY,
                amount INT
                ) """)
        print("created magazzino")

    def create_armadio(self):
        print("filling base data")
        self.mycursor.execute("""INSERT INTO armadi ( descr ) VALUES( 'armadio per componenti elettroniche' )""")
        self.mycursor.execute("""INSERT INTO guide ( id_armadio, n_slot, interasse, pos_x, pos_y, pos_z ) VALUES( '1' , '20' , '10' ,0,0,0  )""")
        self.mycursor.execute("""INSERT INTO guide ( id_armadio, n_slot, interasse, pos_x, pos_y, pos_z ) VALUES( '1' , '10' , '10' ,0,50,0  )""")
        self.mycursor.execute("""INSERT INTO guide ( id_armadio, n_slot, interasse, pos_x, pos_y, pos_z ) VALUES( '1' , '5' , '10' ,0,50,130  )""")
        self.mycursor.execute("""INSERT INTO forme ( descr ) VALUES( '10x70'  )""")
        self.mycursor.execute("""INSERT INTO cassetti ( id_guida , posizione ) VALUES( '1' , '0' )""")
        self.mycursor.execute("""INSERT INTO slots ( id_cassetto , id_forma ) VALUES( '1' , '1' )""")
        self.mycursor.execute("""INSERT INTO slots ( id_cassetto , id_forma ) VALUES( '1' , '1' )""")
        self.mycursor.execute("""INSERT INTO slots ( id_cassetto , id_forma ) VALUES( '1' , '1' )""")
        self.mycursor.execute("""INSERT INTO categorie ( descr ) VALUES( 'Componenti elettroniche')""")
        self.mycursor.execute("""INSERT INTO sotto_categorie ( id_cat, descr ) VALUES( '1', 'Condensatori')""")
        self.mycursor.execute("""INSERT INTO sotto_categorie ( id_cat, descr ) VALUES( '1', 'Resistenze')""")
        

        self.cnx.commit()

    def add_product(self, id_fornitore, descr, value, package, datasheet ):
        #generate id product
        self.mycursor.execute("""INSERT INTO prodotti (
                    codice_fornitore, valore, package, datasheet)
                     VALUES('%s', '%s', '%s', '%s' )
                    """%(str(id_fornitore), str(value), str(package), str(datasheet)))




    def search_product(self, id_fornitore, id_interno, id_cat, id_sottocat):
        #restituisco linea tabella prodotti, da cui posso sapere slot e cassetto.
        #se non c'e' un id, ma solo parametri restituiso una lista
        pass


    def query_invoicex_and_get_new_products(self):
        pass

    def search_cassetto(self, cat=None, sottocat=None, forma=None, id_interno=None):
        if id_interno is not None:
            self.mycursor.execute("""
                SELECT id_cassetto 
                FROM
                (
                    SELECT id_slot 
                    FROM magazzino
                    WHERE id_prod = %s
                ) m INNER JOIN slots s 
                    ON m.id_slot = s.id_slot  
                """%(str(id_interno)))
            cassetti = []
            for val in self.mycursor:
                cassetti.append(val)
            return cassetti
        else:
            if cat is not None and sottocat is not None and forma is not None: 
                self.mycursor.execute("""
                    SELECT id_cassetto 
                    FROM
                    ( 
                        SELECT id_slot, id_cassetto
                        FROM slots
                        WHERE id_forma = %s
                    ) m INNER JOIN cassetti c 
                        ON m.id_cassetto = c.id_cassetto
                    WHERE
                        c.id_cat = %s AND c.id_sottocat = %s
                    """%(str(forma, cat, sottocat)))
                cassetti = []
                for val in self.mycursor:
                    cassetti.append(val)
                return cassetti
            else:
                self.mycursor.execute("""
                    SELECT id_slot, c.id_cassetto 
                    FROM
                    ( 
                        SELECT slots.id_slot, slots.id_cassetto
                        FROM slots
                        WHERE id_forma = %s
                    ) m INNER JOIN cassetti c 
                        ON m.id_cassetto = c.id_cassetto
                    """%(str(forma)))

                cassetti = []
                for val in self.mycursor:
                    print(val)
                    cassetti.append(val)
                return cassetti

    def remove_product_from_slot(self, slot):
        #slot should be empty
        pass


    def place_component(self, product, slot, quantity):
        #check if slot is free
        #while going in the storage update height
        pass

    def add_cassetto(self, slots, theme):
        #check that slots have known shapes
        pass

    def place_cassetto(self, cassetto):
        #search for location big enough to place given cassetto
        pass
   
    def get_armadio_shape():
        #inner join armadio guide cassetti slot
        #restituire la tabella cosi per come e', python non e' tipato
        #aggiungendo left join con prodotti viene armadio state
        pass


    def close(self):
        self.cnx.close()
