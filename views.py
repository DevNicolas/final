from flask import request, redirect, render_template, url_for, Flask
from app import app
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/', methods=["GET"])
def index():

    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result_search():
    query = request.form['search']
    query_search = query.replace(" ","+")
    #url = requests.get("https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q={}&btnG=&oq=".format(query_search))
    url = requests.get("https://scholar.google.com/citations?view_op=search_authors&mauthors="+query_search)
    sou = BeautifulSoup(url.content, "html.parser")
    lists = sou.find_all("div", class_="gs_ai")

    articles = []
    content = []
    for list in lists:
        title = list.find("h3").getText() #encuentra perfiles de cientificos
        universidad = list.find("div", {'class': 'gs_ai_aff'}).getText()
        cargo = list.find("div", {'class': 'gs_ai_eml'}).getText()
        url = list.find("a", href=True).attrs['href']
        #area = list.find("div", {'class': 'gs_ai_int'}).getText()
        article = title+"$"+universidad+"$"+cargo #+ "$" + content + "$" + profile + "$" + book_url + "$" + cite + "$" + url_article
        articles.append(article)
        content.append(url)

    return render_template('result_search.html', lists=articles, query=query, content = url )



@app.route('/profile', methods=["GET"])
def profile():
    complement = request.args.get('title' )

    page = requests.get("https://scholar.google.com/"+complement)
    bsObj = BeautifulSoup(page.content, "html.parser")
    perfil = bsObj.findAll("div", {"id": "gsc_prf_i"})
    contenido = bsObj.findAll("table", {"id": "gsc_a_t"})
    grafica = bsObj.findAll("table", {"id": "gsc_rsb_st"})
    datos = bsObj.findAll("div",{"class":"gsc_md_hist_b"})
    profile = []
    guardar = []
    estadistica = []
    url = complement
    for info in perfil:
        nombre = info.findAll("div")
        name = nombre[0].get_text()
        universidad = nombre[1].get_text()
        rama = nombre[3].get_text()
    profile.append(name+"$"+universidad+"$"+rama)

    for texto in contenido:
        todo = []
        titulo = texto.findAll("tr",{"class":"gsc_a_tr"})
        title = titulo
        todo.append(title[0].get_text()+"$"+title[1].get_text()+"$"+title[2].get_text()+"$"+title[3].get_text()+"$"+title[4].get_text()+"$"+title[5].get_text()+"$"+title[6].get_text()+"$"+title[7].get_text())

    for indice in grafica:

        cont = indice.findAll("td",{"class":"gsc_rsb_sc1"})
        cont1 = indice.findAll("td",{"class":"gsc_rsb_std"})
        guardar.append(cont[0].get_text()+"$"+cont1[0].get_text()+"$"+cont1[1].get_text()+"$"+cont[1].get_text()+"$"+cont1[2].get_text()+"$"+cont1[3].get_text()+"$"+cont[2].get_text()+"$"+cont1[4].get_text()+"$"+cont1[5].get_text())
    for data in datos:

        año = data.findAll("span",{"class":"gsc_g_t"})
        valor = data.findAll("span",{"class":"gsc_g_al"})
        estadistica.append(año[0].get_text()+"$"+valor[0].get_text()+"$"+año[1].get_text()+"$"+valor[1].get_text()+"$"+año[2].get_text()+"$"+valor[2].get_text()+"$"+año[3].get_text()+"$"+valor[3].get_text()+"$"+año[4].get_text()+"$"+valor[4].get_text()+"$"+año[5].get_text()+"$"+valor[5].get_text())
    return render_template('profile.html', perfil = profile, contenido = todo, grafica=guardar, datos=estadistica, url = url)


@app.route('/descarga', methods=["GET"])
def descarga():
    complement = request.args.get('url')
    page = requests.get("https://scholar.google.com/"+complement)
    bsObj = BeautifulSoup(page.content, "html.parser")
    perfil = bsObj.findAll("div", {"id": "gsc_prf_i"})
    contenido = bsObj.findAll("table", {"id": "gsc_a_t"})
    grafica = bsObj.findAll("table", {"id": "gsc_rsb_st"})
    datos = bsObj.findAll("div", {"class": "gsc_md_hist_b"})
    filename = "informacion_perfil.csv"
    f = open(filename, "w", newline='', encoding="utf-8" )

    profile = []
    guardar = []
    estadistica = []
    for info in perfil:
        nombre = info.findAll("div")
        name = nombre[0].get_text()
        universidad = nombre[1].get_text()
        rama = nombre[3].get_text()
    profile.append(name + "," + universidad + "," + rama)

    for texto in contenido:
        todo = []
        titulo = texto.findAll("tr", {"class": "gsc_a_tr"})
        title = titulo
        todo.append(
            title[0].get_text() + "," + title[1].get_text() + "," + title[2].get_text() + "," + title[
                3].get_text() + "," +
            title[4].get_text() + "," + title[5].get_text() + "," + title[6].get_text() + "," + title[
                7].get_text() )

    for indice in grafica:
        cont = indice.findAll("td", {"class": "gsc_rsb_sc1"})
        cont1 = indice.findAll("td", {"class": "gsc_rsb_std"})
        guardar.append(cont[0].get_text() + "," + cont1[0].get_text() + "," + cont1[1].get_text() + "," + cont[
            1].get_text() + "," + cont1[2].get_text() + "," + cont1[3].get_text() + "," + cont[2].get_text() + "," +
                       cont1[4].get_text() + "," + cont1[5].get_text())

    for data in datos:
        año = data.findAll("span", {"class": "gsc_g_t"})
        valor = data.findAll("span", {"class": "gsc_g_al"})
        estadistica.append(
            año[0].get_text() + "," + valor[0].get_text() + "," + año[1].get_text() + "," + valor[1].get_text() + "," +
            año[2].get_text() + "," + valor[2].get_text() + "," + año[3].get_text() + "," + valor[3].get_text() + "," +
            año[4].get_text() + "," + valor[4].get_text() + "," + año[5].get_text() + "," + valor[5].get_text())

        f.write('\ufeff'+str(profile) + "," + "\n" + str(todo) + " ," + "\n" + str(guardar) + "\n" + str(estadistica))

        f.close()

        return render_template('descarga.html')

    if __name__ == '__main__':
        app.run()
