from flask import Flask, jsonify, request   # Importação do s módulos
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

app = Flask(__name__)       # Cria a aplicação App web e atribui a uma variavel
#app.config['JSON_AS_ASCII'] = False         # Configura o Flask para trabalhar com caracteres unicode
app.config['DEBUG'] = True

@app.route('/api/v1/filmes', methods=['GET'])   # Define a rota para chamar a função
def filmes():
    url = 'http://www.adorocinema.com/filmes/numero-cinemas/'
    #url = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/"

    htmlDoc = urlopen(url).read()
    soup = BeautifulSoup(htmlDoc,'html.parser')    # Converte a página e atribui em uma variável
    data = []

    for dataBox in soup.findAll('li',class_='mdl'):
        titleobj = dataBox.find('a',class_='meta-title-link').string
        #imgObj = dataBox.find(class_='thumbnail-img')['src']
        dateObj = dataBox.find('div',class_='meta-body-info').find('span',class_='date').string
        sinopseObj = dataBox.find('div',class_='content-txt').text.replace('\n','').strip()

        movieLinkObj = dataBox.find('a',class_='meta-title-link')['href']
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj
        
        generoObj = dataBox.find('div',class_='meta-body-info').find_all('span')[3:]

        generoList = []
        for genero in generoObj:
            generoList.append(genero.text.strip())

        # Load full sinopse
        htmlDocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmlDocMovieDetail,'html.parser')
        fullSinopse = soupMovieDetail.find('div',class_='content-txt').text.replace('\n','').strip()
        imgObj = soupMovieDetail.find(class_='thumbnail-img')['src']

        data.append({
            'titulo' : titleobj,
            'poster' : imgObj,
            'genero' : ', '.join(generoList),
            'data' : dateObj,
            'sinopse' : sinopseObj,
            'link' : detailsLink,
            'sinopseFull':fullSinopse
        })

    return jsonify({'filmes':data})

if __name__ == '__main__':      #Setando algumas configurações de porta e IP
    port = int(os.environ.get('PORT',5000))
    app.run(host='127.0.0.1',port=port)
