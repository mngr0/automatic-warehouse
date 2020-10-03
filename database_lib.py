import mysql.connector
import csv


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
                    id_cat INT KEY,
                    descr VARCHAR(100)
                    ) """)

        print("created categorie")
        self.mycursor.execute("""CREATE OR REPLACE TABLE sotto_categorie (
                id_sottocat INT KEY,
                id_cat INT NOT NULL,
                descr VARCHAR(100),
                CONSTRAINT `fk_sottocat`
                  FOREIGN KEY(id_cat) REFERENCES categorie(id_cat)
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
                x1 INT,
                y1 INT,
                x2 INT,
                y2 INT
                
                ) """)
        print("created slots")


        
        self.mycursor.execute("""CREATE TABLE packages (
                id_package INT KEY AUTO_INCREMENT,
                descrizione VARCHAR(100),
                id_sottocat INT
                ) """)
        print("created packages")



        self.mycursor.execute("""CREATE OR REPLACE TABLE prodotti (
                id_prodotto INT KEY AUTO_INCREMENT,
                id_cat INT,
                id_sottocat INT,
                codice_fornitore VARCHAR(100),
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


    def read_cat_from_csv(self):
        tmpmem=[]
        with open('files/cat.csv') as catfile:
            cat_reader = csv.reader(catfile, delimiter=',')
            header = next(cat_reader)
            while "id" not in header:
                header = next(cat_reader)
            print(header)
            for row in cat_reader:
                tmpmem.append(row)
                self.mycursor.execute("""INSERT INTO categorie (id_cat, descr ) VALUES( '%s', '%s')"""%(str(row[header.index('id')]), str(row[header.index('categoria')] )   ))
                print(row)
        with open('files/sotto_cat.csv') as catfile:
            cat_reader = csv.reader(catfile, delimiter=';')
            header = next(cat_reader)
            while "id" not in header:
                header = next(cat_reader)
            for row in cat_reader:
                print(row)
                oid_cat = None
                for ocat in tmpmem:
                    if row[header.index('Categoria')]  in ocat:
                        oid_cat = ocat[0]
                self.mycursor.execute("""INSERT INTO sotto_categorie ( id_cat, id_sottocat, descr ) VALUES( "%s", "%s" , "%s")"""%( str(oid_cat),  str(row[header.index('id')]), str(row[header.index('Sottocategoria')])  ))
        self.cnx.commit()

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
        
        
        self.cnx.commit()


    def read_eeschema_bom(self, filename):
        with open('files/boms/'+filename) as bom:
            bom_reader = csv.reader(bom, delimiter=',')
            header = next(bom_reader)
            print(header)
            fails= []
            succ = []
            for row in bom_reader:
                try:
                    self.add_product(
                        row[header.index('Manufacturer_Part_Number')],
                        row[header.index('Description')],
                        row[header.index('Value')],
                        row[header.index('Footprint')],
                        row[header.index('Datasheet')]
                        )
                    succ.append(row)
                except Exception as e:
                    fails.append((row,e))
        return (succ,fails)

    def add_product(self, id_fornitore, descr, value, package, datasheet ):
        #generate id product
        self.mycursor.execute("""INSERT INTO prodotti (
                    codice_fornitore, valore, package, datasheet, id_cat)
                     VALUES('%s', '%s', '%s', '%s' , '12' )
                    """%(str(id_fornitore), str(value), str(package), str(datasheet)))
        self.cnx.commit()
   
   
    def get_categories(self):
        self.mycursor.execute("""
            SELECT *
            FROM categorie
            """)
        res = []
        for val in self.mycursor:
            res.append(val)
        return res


    def get_sottocategories(self, cat):
        self.mycursor.execute("""
            SELECT id_sottocat, descr
            FROM sotto_categorie
            WHERE id_cat = %s
            """%(str(cat)))
        res = []
        for val in self.mycursor:
            res.append(val)
        return res

    def search_product(self, id_fornitore=None, id_interno=None, id_cat=None, id_sottocat=None):
        self.mycursor.execute("""
            SELECT *
            FROM prodotti
            WHERE id_cat = %s
            """%(str(id_cat)))
        #restituisco linea tabella prodotti, da cui posso sapere slot e cassetto.
        #se non c'e' un id, ma solo parametri restituiso una lista
        res = []
        for val in self.mycursor:
            res.append(val)
        return res


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
