import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser
import json 
import re
import pandas as pd
import sys

def url_to_parse(url="") -> BeautifulSoup:
    response = requests.get(url, timeout=2)
    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        return soup
    else:
        raise requests.exceptions.HTTPError(response.status_code, response.reason)

def parse_to_data(soup_list=[]) -> dict:
    # Creation d"un dictionnaire 
    film_number = 0
    films_dico = {"films_number" : film_number, "films" : []}
    
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

                try: # Certains films n'ont pas de realisateur
                    film_data["director"] = film.find("div", {"class": "meta-body-item meta-body-direction"}).text.replace("\n"," ").strip()[3:]
                except:
                    film_data["director"] = ""

                try: # Certains films n'ont pas d'acteurs
                    actors = film.find("div", {"class": "meta-body-item meta-body-actor"}).text.replace("\n"," ").strip()[5:].split(",")
                    film_data["actors"] = [x.strip() for x in actors]
                except:
                    film_data["actors"] = []
                
                film_data["synopsis"] = film.find("div", {"class": "synopsis"}).text.replace("\n"," ").strip()



                # Nombre de sceances
                seance = film.find("a", {"class": "button button-sm button-inverse-full"}).text.replace("\n"," ").strip()
                film_data["sessions"] = int(''.join(re.findall(r'\d', seance)))



                # Notes : ['Presse 3,3', 'Spectateurs 3,9', 'Mes amis --']
                ratings = film.findAll("div", {"class": "rating-item"})

                # Nettoyage de la liste puis concaténation
                ratings = [rate.text.replace("\n"," ").strip() for rate in ratings[:-1]]
                ratings = " ".join(ratings)
                
                # Transformation des notes de str -> float si le champ Presse/Spectateur est présent 
                # Ex:    Presse 3,3 Spectateurs 3,9 -> 3.3  3.9      |     Spectateurs 3,9 -> N/A  3.9
                film_data["rating"] = {
                    "critics": float(r) if (r := re.sub(r'Presse\s*(\d*),(\d*).*', r'\1.\2', ratings)) != ratings else 'N/A',
                    "audience": float(r) if (r := re.sub(r'.*Spectateurs\s*(\d*),(\d*).*', r'\1.\2', ratings)) != ratings else 'N/A'
                }
                
                film_number += 1
                films_dico["films"].append(film_data)
            except Exception as e:
                pass
    
    films_dico["films_number"] = film_number
    return films_dico
    

 
def data_to_json(data=None, filename="data.json") -> None:
    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def data_to_csv(data: dict = None, filename="data.csv") -> None:
    data_frame = {
        "title" : [film["title"] for film in data["films"]],
        "release_date" : [film["release_date"] for film in data["films"]],
        "length" : [film["length"] for film in data["films"]],
        "type" : [film["type"] for film in data["films"]],
        "director" : [film["director"] for film in data["films"]],
        "actors" : [film["actors"] for film in data["films"]],
        "synopsis" : [film["synopsis"] for film in data["films"]],
        "sessions" : [film["sessions"] for film in data["films"]],
        'rating' : [film["rating"] for film in data["films"]],
    }
    data_frame = pd.DataFrame.from_dict(data_frame)
    with open(filename, 'w', encoding='utf8') as csv_file:
        data_frame.to_csv(csv_file, index=False, header=True)



def main():
        # Lecture du fichier config.ini
        parser = ConfigParser()
        parser.read("config.ini")

        soup_list = []
        for i in range(1, int(parser['Url']['page_number'])+1):
            try:
                # print(f"{parser['Url']['page_url']}{i}")
                url = f"{parser['Url']['page_url']}{i}"
                soup = url_to_parse(url)
                soup_list.append(soup)
            except:
                print(f'failed to parse : {url}')
                pass

        data = parse_to_data(soup_list)
        output_file = parser['Files']['output_file']
        
        match sys.argv[1]:
            case 'json':
                data_to_json(data, output_file)
            case 'csv':
                data_to_csv(data, output_file)
            case _:
                data_to_csv(data, output_file)
                data_to_json(data, output_file)


if __name__ == "__main__":
    main()