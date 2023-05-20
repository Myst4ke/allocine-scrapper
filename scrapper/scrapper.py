import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser
import json 
import re

def url_to_parse(url=""):
    response = requests.get(url, timeout=2)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    else:
        raise requests.exceptions.HTTPError(response.status_code, response.reason)

def parse_to_data(soup_list=[]):
    # Creation d"un dictionnaire 
    films_dico = {"films_number" : 0, "films" : []}
    film_number = 0
    for soup in soup_list:
        content = soup.find("main", {"id": "content-layout"}) # Contenu de la page
        films = content.findAll("li", {"class": "mdl"}) # Liste des films
        for film in films:
            try:
                film_data = {}

                # Titre
                film_data["title"] = film.find("h2").text.strip()

                # Description : Date / Duree / Type 
                # Ex: 26 avril 2023 / 1h 39min / Comédie dramatique 
                descritpion = film.find("div", {"class": "meta-body-item meta-body-info"}).text.replace("\n"," ").strip().split("/")
                film_data["release_date"] = descritpion[0].strip()
                film_data["length"] = descritpion[1].strip()
                film_data["type"] = descritpion[2].strip()

                # Realisateur, Acteurs, Synopsis
                film_data["director"] = film.find("div", {"class": "meta-body-item meta-body-direction"}).text.replace("\n"," ").strip()[3:]
                actors = film.find("div", {"class": "meta-body-item meta-body-actor"}).text.replace("\n"," ").strip()[5:].split(",")
                film_data["actors"] = [x.strip() for x in actors]
                film_data["synopsis"] = film.find("div", {"class": "synopsis"}).text.replace("\n"," ").strip()

                # Nombre de sceances
                seance = film.find("a", {"class": "button button-sm button-inverse-full"}).text.replace("\n"," ").strip()
                film_data["sessions"] = int(''.join(re.findall(r'\d', seance)))

                # Notes : ['Presse 3,3', 'Spectateurs 3,9', 'Mes amis --']
                ratings = film.findAll("div", {"class": "rating-item"})
                film_data["rating"] = {
                    "critics": float(re.sub(r'(\d*),(\d*)',r'\1.\2', ratings[0].text.replace("\n"," ").strip()[-3:])),
                    "audience": float(re.sub(r'(\d*),(\d*)',r'\1.\2', ratings[1].text.replace("\n"," ").strip()[-3:]))
                }
                film_number += 1
                films_dico["films"].append(film_data)
            except:
                pass
    films_dico["films_number"] = film_number
    return films_dico
    

 
def data_to_json(data=None, filename="data.json"):
    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)



def main():
        # Lecture du fichier config.ini
        parser = ConfigParser()
        parser.read("config.ini")

        soup_list = []
        for i in range(int(parser['Url']['page_number'])):
            try:
                url = f"{parser['Url']['page_url']}{i}"
                soup = url_to_parse(url)
                soup_list.append(soup)
            except:
                pass
        
        data = parse_to_data(soup_list)
        data_to_json(data, parser['Files']['output_file'])



if __name__ == "__main__":
    main()