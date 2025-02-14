import mysql.connector

mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "",
database = "karlo_cars"
)

class User:
    __id : int
    __username : str
    __email : str
    __password : str
    __privilegija : str

    def __init__(self,id,username,email,password,privilegija):
        self.__id = id
        self.__username = username
        self.__email = email
        self.__password = password
        self.__privilegija = privilegija

    def __str__(self):
        rez = f"ID: {self.__id}\nUsername: {self.__username}\nEmail: {self.__email}\nPassword: {self.__password}\nPrivilegija: {self.__privilegija}"
        return rez
        
   
    def get_id(self):
        return self.__id
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_password(self):
        return self.__password
    def get_privilegija(self):
        return self.__privilegija
    
    @staticmethod
    def registruj_korisnika(username,email,password,repassword,privilegija):
        greska = ""
        # Validacija podataka iz forme
        if email == "" or username == "" or password == "" or repassword == "" or privilegija == "":
            greska = "Sva polja moraju biti popunjena!"
            return greska
        if "@" not in email and "." not in email:
            greska = "Unesite validnu e-mail adresu!"
            return greska
        if len(username) < 4:
            greska = "Username mora imati makar 4 karaktera!"
            return greska
        if password != repassword:
            greska = "Sifre se ne poklapaju!"
            return greska
        if User.proveri_da_li_email_postoji(email):
            greska = "Email adresa je vec u upotrebi!"
            return greska
        if User.proveri_da_li_username_postoji(username):
            greska = "Username vec u upotrebi!"
            return greska
        # Ako je sve proslo kako treba
        sql_upit = "INSERT INTO users VALUES (null,?,?,?,?)"
        parametri = (username,email,password,privilegija)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()


        return greska
    
    @staticmethod
    def proveri_da_li_email_postoji(email):
        sql_upit = "SELECT * FROM users WHERE email = ?"
        parametri = (email, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        dohvaceni_email = cursor.fetchone()
        if dohvaceni_email:
            return True
        return False
    
    @staticmethod
    def proveri_da_li_username_postoji(username):
        sql_upit = "SELECT * FROM users WHERE username = ?"
        parametri = (username, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        dohvaceni_username = cursor.fetchone()
        if dohvaceni_username:
            return True
        return False
    
    @staticmethod 
    def uloguj_korisnika(username,password):
        greska = ""
        #Validacija
        if username == "" or password == "":
            greska = "Unesite sve podatke!"
            return greska
        korisnik = User.dohvati_korisnika_po_username(username)
        if not korisnik:
            greska = "Username ne postoji!"
            return greska
        if password != korisnik.get_password():
            greska = "Netacna sifra!"
            return greska
        return greska
        
        
    @staticmethod
    def dohvati_korisnika_po_username(username):
        sql_upit = "SELECT * FROM users WHERE username = ?"
        parametri = (username, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone() # tapl
        if korisnik:
            korisnik_list = User.dekodiraj_tapl(korisnik)
            korisnik_objekat = User.napravi_objekat_od_liste(korisnik_list)
            print(korisnik_objekat)
            return korisnik_objekat
    
    @staticmethod
    def dohvati_korisnika_po_id(id):
        sql_upit = "SELECT * FROM users WHERE id = ?"
        parametri = (id, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone() # tapl
        if korisnik:
            korisnik_list = User.dekodiraj_tapl(korisnik)
            korisnik_objekat = User.napravi_objekat_od_liste(korisnik_list)
            print(korisnik_objekat)
            return korisnik_objekat
        return False
        
    
    @staticmethod
    def dohvati_korisnika_po_username(username):
        sql_upit = "SELECT * FROM users WHERE username = ?"
        parametri = (username, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone() # tapl
        if korisnik:
            korisnik_list = User.dekodiraj_tapl(korisnik)
            korisnik_objekat = User.napravi_objekat_od_liste(korisnik_list)
            print(korisnik_objekat)
            return korisnik_objekat
        return False

    @staticmethod
    def dekodiraj_tapl(tapl):
        tapl = list(tapl)
        n = len(tapl)
        for i in range (n):
            if isinstance(tapl[i],bytearray):
                tapl[i] = tapl[i].decode()
        return tapl
    
    @classmethod
    def napravi_objekat_od_liste(cls,lista):
        return cls(lista[0],lista[1],lista[2],lista[3],lista[4])
        
    @staticmethod
    def dohvati_sve_korisnike():
        sql_upit = "SELECT * FROM users"
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit)
        korisnici_taplovi = cursor.fetchall()
        korisnici_lista = User.napravi_listu_listi(korisnici_taplovi)
        korisnici_objekti = User.napravi_listu_objekata(korisnici_lista)
        print(korisnici_objekti)
        return korisnici_objekti
        
    @staticmethod
    def napravi_listu_listi(lista):
        n = len(lista)
        for i in range (n):
            lista[i] = User.dekodiraj_tapl(lista[i])
        return lista
    
    @staticmethod
    def napravi_listu_objekata(lista):
        n = len(lista)
        for i in range (n):
            lista[i] = User.napravi_objekat_od_liste(lista[i])
        return lista
        

    @staticmethod
    def obrisi_korisnika(id):
        id_za_brisanje = id
        sql_upit = "DELETE FROM users WHERE id = ?"
        parametri = (id_za_brisanje, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()

    @staticmethod
    def update_korisnika(email,username,password,privilegija,id):
        sql_upit = "UPDATE users SET email=?,username=?,password=?,privilegija=? WHERE id=?"
        parametri = (email,username,password,privilegija,id)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()


    @staticmethod
    def pretrazi_korisnike(upit):
        sql_upit = "SELECT * FROM users WHERE username LIKE ?"
        parametri = (f'%{upit}%', )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        takmicari = cursor.fetchall()
        takmicari_lista = User.napravi_listu_listi(takmicari)
        takmicari_objekti = User.napravi_listu_objekata(takmicari_lista)
        if takmicari_objekti:
            return takmicari_objekti
        return None



    @staticmethod
    def sortiraj_po_imenu_opadajuce():
        sql_upit = "SELECT * FROM users ORDER BY username ASC"
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit)
        korisnici_taplovi = cursor.fetchall()
        korisnici_lista = User.napravi_listu_listi(korisnici_taplovi)
        korisnici_objekti = User.napravi_listu_objekata(korisnici_lista)
        
        return korisnici_objekti
    
    @staticmethod
    def sortiraj_po_emailu_opadajuce():
        sql_upit = "SELECT * FROM users ORDER BY email ASC"
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit)
        korisnici_taplovi = cursor.fetchall()
        korisnici_lista = User.napravi_listu_listi(korisnici_taplovi)
        korisnici_objekti = User.napravi_listu_objekata(korisnici_lista)
        
        return korisnici_objekti
    
    @staticmethod
    def sortiraj_po_privilegiji_opadajuce():
        sql_upit = "SELECT * FROM users ORDER BY privilegija ASC"
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit)
        korisnici_taplovi = cursor.fetchall()
        korisnici_lista = User.napravi_listu_listi(korisnici_taplovi)
        korisnici_objekti = User.napravi_listu_objekata(korisnici_lista)
        
        return korisnici_objekti
    
    @staticmethod
    def filtriraj_po_privilegiji(id):
        if id == 1:
            privilegija = "admin"
            sql_upit = "SELECT * FROM users WHERE privilegija=?"
            parametri = (privilegija, )
            cursor = mydb.cursor(prepared=True)
            cursor.execute(sql_upit,parametri)
            korisnici_tapl = cursor.fetchall()
            korisnici_lista = User.napravi_listu_listi(korisnici_tapl)
            korisnici_objekat = User.napravi_listu_objekata(korisnici_lista)
            return korisnici_objekat
        if id == 2:
            privilegija = "editor"
            sql_upit = "SELECT * FROM users WHERE privilegija=?"
            parametri = (privilegija, )
            cursor = mydb.cursor(prepared=True)
            cursor.execute(sql_upit,parametri)
            korisnici_tapl = cursor.fetchall()
            korisnici_lista = User.napravi_listu_listi(korisnici_tapl)
            korisnici_objekat = User.napravi_listu_objekata(korisnici_lista)
            return korisnici_objekat
        if id == 3:
            privilegija = "user"
            sql_upit = "SELECT * FROM users WHERE privilegija=?"
            parametri = (privilegija, )
            cursor = mydb.cursor(prepared=True)
            cursor.execute(sql_upit,parametri)
            korisnici_tapl = cursor.fetchall()
            korisnici_lista = User.napravi_listu_listi(korisnici_tapl)
            korisnici_objekat = User.napravi_listu_objekata(korisnici_lista)
            return korisnici_objekat
        
    @staticmethod
    def vrati_broj_admina():
        privilegija = "admin"
        sql_upit = "SELECT * FROM users WHERE privilegija=?"
        parametri = (privilegija, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnici_tapl = cursor.fetchall()
        broj_admina = len(korisnici_tapl)
        return broj_admina
    @staticmethod
    def vrati_broj_usera():
        privilegija = "user"
        sql_upit = "SELECT * FROM users WHERE privilegija=?"
        parametri = (privilegija, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnici_tapl = cursor.fetchall()
        broj_usera = len(korisnici_tapl)
        return broj_usera
    @staticmethod
    def vrati_broj_editora():
        privilegija = "editor"
        sql_upit = "SELECT * FROM users WHERE privilegija=?"
        parametri = (privilegija, )
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        korisnici_tapl = cursor.fetchall()
        broj_editora = len(korisnici_tapl)
        return broj_editora