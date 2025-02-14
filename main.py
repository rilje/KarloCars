from flask import Flask,render_template,redirect,request,url_for,session
from user import User
from automobil import Automobil
import secrets


app = Flask(__name__)


app.config['SECRET_KEY'] = secrets.token_hex(32)

@app.route("/")
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("landing.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        greska = User.uloguj_korisnika(username,password)
        if greska != "":
            return render_template("login.html",greska=greska)
        session['username'] = username
        return redirect(url_for('landing'))
    
@app.route("/registracija",methods=["POST","GET"])
def registracija():
    if request.method == "GET":
        return render_template("registracija.html")
    elif request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        privilegija = request.form['privilegija']
        greska = User.registruj_korisnika(username,email,password,repassword,privilegija)
        if greska != "":
            return render_template("registracija.html",greska=greska)
        session['username'] = username
        return redirect(url_for("landing"))


@app.route("/landing")
def landing():
    if 'username' in session:
        username = session['username']
        user = User.dohvati_korisnika_po_username(username)
        print(username)
        print(user)
        return render_template("landing.html",username=username,user=user)
    return redirect(url_for('login'))
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
   
@app.route("/admin")
def admin():
    if 'username' in session:
        username = session['username']
        user = User.dohvati_korisnika_po_username(username)
        broj_admina = User.vrati_broj_admina()
        broj_editora = User.vrati_broj_editora()
        broj_usera = User.vrati_broj_usera()
        return render_template("admin.html",user=user,broj_admina=broj_admina,broj_editora=broj_editora,broj_usera=broj_usera)
    return "404: ERROR ADMIN NOT FOUND"

@app.route("/svi_korisnici")
def svi_korisnici():
    if 'username' in session:
        username = session['username']
        user = User.dohvati_korisnika_po_username(username)
        korisnici = User.dohvati_sve_korisnike()
        print(korisnici)
        
        return render_template("svi_korisnici.html",korisnici=korisnici,user=user)
    return redirect(url_for('login'))

@app.route("/obrisi/<id>")
def obrisi(id):
    id_za_brisanje = id
    User.obrisi_korisnika(id_za_brisanje)
    return redirect(url_for('svi_korisnici'))

@app.route("/dodaj_korisnika", methods=["POST","GET"])
def dodaj_korisnika():
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    if request.method == "GET":
        return render_template("dodaj_korisnika.html",user=user)
    elif request.method == "POST":
        username = session['username']
        user = User.dohvati_korisnika_po_username(username)
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        privilegija = request.form['privilegija']
        greska = User.registruj_korisnika(username,email,password,repassword,privilegija)
        if greska != "":
            return render_template("dodaj_korisnika.html", greska=greska,user=user)
        return redirect(url_for('svi_korisnici'))


@app.route("/update/<id>",methods=["POST","GET"])
def update(id):
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    id_za_update = id
    korisnik = User.dohvati_korisnika_po_id(id_za_update)
    if request.method == "GET":
        return render_template("update.html",korisnik=korisnik,user=user)
    elif request.method == "POST": 
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        privilegija = request.form['privilegija']
        User.update_korisnika(email,username,password,privilegija,id_za_update)
        return redirect(url_for("svi_korisnici"))
    
    
@app.route("/pretraga", methods=['POST',"GET"])
def pretraga():
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    if request.method == "POST":
        upit = request.form['upit']
        korisnici1 = User.dohvati_sve_korisnike()
        korisnici = User.pretrazi_korisnike(upit)
        if korisnici == None:
            return render_template("svi_korisnici.html",korisnici=korisnici1,user=user)    
        return render_template("svi_korisnici.html", korisnici=korisnici,user=user)
        
    elif request.method == "GET":
        return "404! ERROR"


@app.route("/sortiraj/<id>")
def sortitaj(id):
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    id_za_sort = id
    if id_za_sort == "1":
        sortirani_korisnici = User.sortiraj_po_imenu_opadajuce()
        print(sortirani_korisnici)
        return render_template("svi_korisnici.html",korisnici=sortirani_korisnici,user=user)
    elif id_za_sort == "2":
        sortirani_korisnici = User.sortiraj_po_emailu_opadajuce()
        print(sortirani_korisnici)
        return render_template("svi_korisnici.html",korisnici=sortirani_korisnici,user=user)
    elif id_za_sort == "3":
        sortirani_korisnici = User.sortiraj_po_privilegiji_opadajuce()
        print(sortirani_korisnici)
        return render_template("svi_korisnici.html",korisnici=sortirani_korisnici,user=user)
    return "Greska 800"
    

@app.route("/filtriraj/<id>")
def filtriraj(id):
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    id_za_filter = id
    id_za_filter = int(id_za_filter)
    filtrirani_korisnici = User.filtriraj_po_privilegiji(id_za_filter)
    print(filtrirani_korisnici)
    return render_template("filter.html",user=user,korisnici=filtrirani_korisnici)
    

    
@app.route("/dodaj_automobil", methods=["POST","GET"])
def dodaj_automobil():
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    if request.method == "GET":
        return render_template("dodaj_automobil.html",user=user)
    elif request.method == "POST":
        
        stanje = request.form['stanje']
        marka = request.form['marka']
        model = request.form['model']
        godiste = request.form['godiste']
        kilometraza = request.form['kilometraza']
        karoserija = request.form['karoserija']
        gorivo = request.form['gorivo']
        kubikaza = request.form['kubikaza']
        snaga = request.form['snaga']
        fiksna_cena = request.form['fiksna_cena']
        zamena = request.form['zamena']
        broj_sasije = request.form['broj_sasije']
        klasa_motora = request.form['klasa_motora']
        pogon = request.form['pogon']
        menjac = request.form['menjac']
        broj_vrata = request.form['broj_vrata']
        broj_sedista = request.form['broj_sedista']
        strana_volana = request.form['strana_volana']
        klima = request.form['klima']
        lizing = request.form['lizing']
        boja = request.form['boja']
        materijal_enterijera = request.form['materijal_enterijera']
        boja_enterijera = request.form['boja_enterijera']
        rigistrovan_do = request.form['registrovan_do']
        poreklo_vozila = request.form['poreklo_vozila']
        vlasnistvo = request.form['vlasnistvo']
        ostecenje = request.form['ostecenje']
        kredit = request.form['kredit']
        sigurnost = request.form['sigurnost']
        oprema = request.form['oprema']
        opis = request.form['opis']
        cena = request.form['cena']

        Automobil.dodaj_automobil(stanje,marka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,rigistrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena)
        
        return redirect(url_for("svi_automobili"))
        
       
@app.route("/svi_automobili")
def svi_automobili():
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    automobili = Automobil.dohvati_sve_automobile()
    for automobil in automobili:
        print(automobil)
    return render_template("svi_automobili.html",user=user,automobili=automobili)
    
@app.route("/prikazi_automobil/<id>")
def prikazi_automobil(id):
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    automobil = Automobil.dohvati_auto_po_id(id)
    atributi = vars(automobil)
    return render_template("automobil.html",user=user,atributi=atributi,automobil=automobil)

@app.route("/obrisi_automobil/<id>")
def obrisi_automobil(id):
    Automobil.obiris_automobil(id)
    return redirect(url_for("svi_automobili"))

@app.route("/azuriraj_automobil/<id>", methods=["POST","GET"])
def azuriraj_automobil(id):
    username = session['username']
    user = User.dohvati_korisnika_po_username(username)
    if request.method == "GET":
        print(id)
        automobil = Automobil.dohvati_auto_po_id(id)
        return render_template("azuriraj_automobil.html", automobil=automobil,user=user)
    elif request.method == "POST":
        stanje = request.form['stanje']
        marka = request.form['marka']
        model = request.form['model']
        godiste = request.form['godiste']
        kilometraza = request.form['kilometraza']
        karoserija = request.form['karoserija']
        gorivo = request.form['gorivo']
        kubikaza = request.form['kubikaza']
        snaga = request.form['snaga']
        fiksna_cena = request.form['fiksna_cena']
        zamena = request.form['zamena']
        broj_sasije = request.form['broj_sasije']
        klasa_motora = request.form['klasa_motora']
        pogon = request.form['pogon']
        menjac = request.form['menjac']
        broj_vrata = request.form['broj_vrata']
        broj_sedista = request.form['broj_sedista']
        strana_volana = request.form['strana_volana']
        klima = request.form['klima']
        lizing = request.form['lizing']
        boja = request.form['boja']
        materijal_enterijera = request.form['materijal_enterijera']
        boja_enterijera = request.form['boja_enterijera']
        rigistrovan_do = request.form['registrovan_do']
        poreklo_vozila = request.form['poreklo_vozila']
        vlasnistvo = request.form['vlasnistvo']
        ostecenje = request.form['ostecenje']
        kredit = request.form['kredit']
        sigurnost = request.form['sigurnost']
        oprema = request.form['oprema']
        opis = request.form['opis']
        cena = request.form['cena']

        Automobil.azuriraj_automobil(stanje, marka,model, godiste, kilometraza,karoserija,gorivo,kubikaza,snaga,fiksna_cena,zamena,broj_sasije,klasa_motora,pogon,menjac,broj_vrata,broj_sedista,strana_volana,klima,lizing,boja,materijal_enterijera,boja_enterijera,rigistrovan_do,poreklo_vozila,vlasnistvo,ostecenje,kredit,sigurnost,oprema,opis,cena,id)
        
        return redirect(url_for("svi_automobili"))


app.run(debug=True)


