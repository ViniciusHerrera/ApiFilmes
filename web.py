from flask import Flask, jsonify, request   # Importação do s módulos
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

app = Flask(__name__)       # Cria a aplicação App web e atribui a uma variavel
#app.config['JSON_AS_ASCII'] = False         # Configura o Flask para trabalhar com caracteres unicode
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/api/v1/filmes', methods=['GET'])   # Define a rota para chamar a função
def filmes():
    # url = 'http://www.adorocinema.com/filmes/numero-cinemas/'
    url = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/"

    htmlDoc = urlopen(url).read()
    soup = BeautifulSoup(htmlDoc,'html.parser')    # Converte a página e atribui em uma variável

    data = []   # Define array vazio

    for dataBox in soup.findAll('div',class_='data_box'):
        titleobj = dataBox.find('a',class_='no_underline')
        imgObj = dataBox.find(class_='img_side_content').find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find('div',class_='content').find_all('p')[0]
        dateObj = dataBox.find('div', class_='content').find('div',class_='oflow_a')
        generoObj = dataBox.find('div',class_='content').find_all('li')[3].find('div',class_="oflow_a")
        movieLinkObj = dataBox.find(class_='img_side_content').find_all('a')[0]
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']
    
        # Load full sinopse

        htmlDocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmlDocMovieDetail,'html.parser')
        fullSinopse = soupMovieDetail.find(class_='content-txt')
        fullImgObj = soupMovieDetail.find("meta", property="og:image")

        data.append({
            'titulo':titleobj.text.strip(),
            'genero':generoObj.text.replace('\n','').strip(),
            'poster':fullImgObj['content'],
            'sinopse':sinopseObj.text.replace('\n','').strip(),
            'data':dateObj.text[0:11].strip(),
            'link' : detailsLink,
            'sinopseFull':fullSinopse.text.replace('\n','')
        })

    return jsonify({'filmes':data})

if __name__ == '__main__':      #Setando algumas configurações de porta e IP
    port = int(os.environ.get('PORT',5000))
    app.run(host='127.0.0.1',port=port)
