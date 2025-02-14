import mysql.connector

mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "",
database = "karlo_cars"
)

class Automobil:
    stanje : str
    marka : str
    model : str
    godiste : int
    kilometraza : int
    karoserija : str
    gorivo : str
    kubikaza : int
    snaga : int
    fiksna_cena : str
    zamena : str
    broj_sasije : str
    klasa_motora : str
    pogon : str
    menjac : str
    broj_vrata : int
    broj_sedista : int
    strana_volana : str
    klima : str
    lizing : str
    boja : str
    materijal_enterijera : str
    boja_enterijera : str
    registrovan_do : str
    poreklo_vozila : str
    vlasnistvo : str
    ostecenje : list
    kredit : str
    sigurnost : list
    oprema : list
    opis : str
    cena : int

    def __init__(self,id,stanje,marka,model,godiste,kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,registrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena):
        self.id = id
        self.stanje = stanje
        self.marka = marka
        self.model = model
        self.godiste = godiste
        self.kilometraza = kilometraza
        self.karoserija = karoserija
        self.gorivo = gorivo
        self.kubikaza = kubikaza
        self.snaga = snaga
        self.fiksna_cena = fiksna_cena
        self.zamena = zamena
        self.broj_sasije = broj_sasije
        self.klasa_motora = klasa_motora
        self.pogon = pogon
        self.menjac = menjac
        self.broj_vrata = broj_vrata
        self.broj_sedista = broj_sedista
        self.strana_volana = strana_volana
        self.klima = klima
        self.lizing = lizing
        self.boja = boja
        self.materijal_enterijera = materijal_enterijera
        self.boja_enterijera = boja_enterijera
        self.registrovan_do = registrovan_do
        self.poreklo_vozila = poreklo_vozila
        self.vlasnistvo = vlasnistvo
        self.ostecenje = ostecenje
        self.kredit = kredit
        self.sigurnost = sigurnost
        self.oprema = oprema
        self.opis = opis
        self.cena = cena
      

    def __str__(self):
        rez = f"ID: {self.id}\nStanje: {self.stanje}\nMarka: {self.marka}\nModel: {self.model}\nGodiste: {self.godiste}\nKilometraza: {self.kilometraza}\nKaroserija: {self.karoserija}\nGorivo: {self.gorivo}\nKubikaza: {self.kubikaza}\nSnaga: {self.snaga}\nFiksna cena: {self.fiksna_cena}\nZamena: {self.zamena}\nBroj sasije: {self.broj_sasije}\nKlasa motora: {self.klasa_motora}\nPogon: {self.pogon}\nMenjac: {self.menjac}\nBroj vrata: {self.broj_vrata}\nBroj sedista: {self.broj_sedista}\nStrana volana: {self.strana_volana}\nKlima: {self.klima}\nLizing: {self.lizing}\nBoja: {self.boja}\nMaterijal enterijera: {self.materijal_enterijera}\nBoja enterijera: {self.boja_enterijera}\nRegistrovan do: {self.registrovan_do}\nPoreklo vozila: {self.poreklo_vozila}\nVlasnistvo: {self.vlasnistvo}\nOstecenje: {self.ostecenje}\nKredit: {self.kredit}\nSigurnost: {self.sigurnost}\nOprema: {self.oprema}\nOpis: {self.opis}\nCena: {self.cena}\n"
        return rez

    @staticmethod
    def dodaj_automobil(stanje, mraka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,rigistrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena):
        sql_upit = "INSERT INTO automobili VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        parametri = (stanje, mraka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,rigistrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()

    @staticmethod
    def dohvati_sve_automobile():
        sql_upit = "SELECT * FROM automobili"
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit)
        automobili_taplovi = cursor.fetchall()
        automobili_lista = Automobil.napravi_listu_listi(automobili_taplovi)
        automobili_objekti = Automobil.napravi_listu_objekata(automobili_lista)
        print(automobili_objekti)
        return(automobili_objekti)
    
    @staticmethod
    def dekodiraj_tapl(tapl):
        tapl = list(tapl)
        n = len(tapl)
        for i in range(n):
            if isinstance(tapl[i],bytearray):
                tapl[i] = tapl[i].decode()
        return tapl
    
    @staticmethod
    def napravi_listu_listi(lista):
        n = len(lista)
        for i in range (n):
            lista[i] = Automobil.dekodiraj_tapl(lista[i])
        return lista
    
    @classmethod
    def napravi_objekat_od_liste(cls,list):
        return cls(list[0],list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10],list[11],list[12],list[13],list[14],list[15],list[16],list[17],list[18],list[19],list[20],list[21],list[22],list[23],list[24],list[25],list[26],list[27],list[28],list[29],list[30],list[31],list[32])
    
    @staticmethod
    def napravi_listu_objekata(lista):
        n = len(lista)
        for i in range(n):
            lista[i] = Automobil.napravi_objekat_od_liste(lista[i])
        return lista
    
    @staticmethod
    def dohvati_auto_po_id(id):
        sql_upit = "SELECT * FROM automobili WHERE id=?"
        paramteri = (id,)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,paramteri)
        automobil_tapl = cursor.fetchone()
        automobil_lista = Automobil.dekodiraj_tapl(automobil_tapl)
        automobil_objekat = Automobil.napravi_objekat_od_liste(automobil_lista)
        return automobil_objekat
    
    @staticmethod
    def obiris_automobil(id):
        sql_upit = "DELETE FROM automobili WHERE id=?"
        parametri = (id,)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
        

    @staticmethod 
    def azuriraj_automobil(stanje, marka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,registrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena,id):
        sql_upit = "UPDATE automobili SET stanje=?, marka=?,model=?, godiste=?, kilometraza=?,karoserija=?,gorivo=?,kubikaza=?,snaga=?,fiksna_cena=?,zamena=?,broj_sasije=?,klasa_motora=?,pogon=?,menjac=?,broj_vrata=?,broj_sedista=?,strana_volana=?,klima=?,lizing=?,boja=?,materijal_enterijera=?,boja_enterijera=?,registrovan_do=?,poreklo_vozila=?,vlasnistvo=?,ostecenje=?,kredit=?,sigurnost=?,oprema=?,opis=?,cena=? WHERE id=?"
        parametri = (stanje, marka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,registrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena,id)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
