from flask import Flask, render_template, request, redirect, session
import pymongo

app = Flask(__name__)
app.secret_key = 'bizim cok zor gizli sozcugumuz'

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["obsdb"]
dersler_tablosu = mydb["dersler"]
kullanicilar_tablosu = mydb["kullanicilar"]
ogrenciler_tablosu = mydb["ogrenciler"]



@app.route('/')
def baslangic():
    return render_template("anasayfa.html")


@app.route('/giris', methods=['GET','POST'])
def giris():
    if request.method == 'POST':
        kullanici = request.form['kullanici']
        sifre = request.form['sifre']
        kayit = kullanicilar_tablosu.find_one({"_id" : kullanici})
        if kayit:
            if sifre == kayit['sifre']:
                del kayit['sifre']
                session['kullanici'] = kayit
                return redirect ('/', code=302)
            else:
                return 'sifre yanlis'
        else:
            return 'kullanici bulunamadi'
    else:
        return render_template('giris.html')


if __name__ == "__main__":
    app.run(debug=True)