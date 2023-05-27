# Allocine Scrapper

Ce scrapper permet d'accéder à un nombre défini de page contenant les derniers films à l'affiche (classés par nombre de séances décroissant).

![à l'affiche](/assets/allocine.png)


### Pré-requis 
Pour que le scrapper fonctionne on utilise le module `requests` ainsi que le module `BeautifulSoup`. Le module `requests` étant déjà présent par défaut on doit installer `BeautifulSoup` et `Pandas` qui permet la sauvergarde au format `csv`.

Pour cela :
* `$ pip install bs4`
* `$ pip install pandas`

## Le projet
### Les modules
Comme vu précédemment on utilise les modules `requests` et `BeautifulSoup` mais aussi `Configparser`.
* `requests` : permet ici d'effectuer une requette **http** vers un site (ici **[allocine.fr](https://www.allocine.fr/)**).
* `BeautifulSoup` : permet de parser le code html de la page reçu via la requette.
* `Configparser` : permet d'accéder à un fichier config (**config.ini**) afin de structurer le projet. 
* `Sys` : qui permet de récupérer les argument lors de l'éxecution.
* `Pandas` : qui permet de transformer les données en dataframe et de les sauvegarder en `csv`

### Structure
Le projet est structuré en plusieures fonctions. Le but est d'aller chercher l'url et le nombre de page à scrapper dans le fichier config. Puis d'effectuer une requette pour chaque page et enfin de récupérer les informations importantes sur chaque film. 
Pour cela trois fonctions sont définies :
* `url_to_parse` : qui prend en entrée une url et qui renvoie le parser sur l'html.
* `parse_to_data` : qui récupère le parser afin d'extraire les données importantes (**cf: le fichier json de sortie**).
* `data_to_json`: qui écrit les données extraites dans un fichier `json`.
* `data_to_csv`: qui transforme les données en dataframe puis les écrit dans un fichier `csv`.

Ici les requettes sont effectuée vers la page **[FILMS À L'AFFICHE](https://www.allocine.fr/film/aucinema/?page=1)**



### Les données
Les données sont sous forme de dictionnaire dans le code afin de pouvoir les écrire au format json et pour les convetir en dataframe par la suite. Tout en haut du `.json` on retrouve le nombre de film dans la liste. Puis pour chaque film on retrouve nottament son **titre**, sa **date de parution**, sa **durée**, son/ses **genre(s)**, son **synopsis**, etc...

Le csv lui, possède les même attribut comme entête de colone 

*ici un exemple du `json` avec Les Gardiens de la Galaxie 3 :*

```json
"films_number": 15,
"films": [
        {
            "title": "Les Gardiens de la Galaxie 3",
            "release_date": "3 mai 2023",
            "length": "2h 30min",
            "type": "Action, Fantastique, Science Fiction",
            "director": "James Gunn",
            "actors": [
                "Chris Pratt",
                "Zoe Saldana",
                "Dave Bautista"
            ],
            "synopsis": "Notre bande de marginaux favorite a quelque peu changé. Peter Quill, qui pleure toujours la perte de Gamora, doit rassembler son équipe pour défendre l’univers et protéger l’un des siens. En cas d’échec, cette mission pourrait bien marquer la fin des Gardiens tels que nous les connaissons.",
            "sessions": 1127,
            "rating": {
                "critics": 3.6,
                "audience": 4.3
            }
        }
      ]
```
*ici un exemple du `csv` avec la première ligne*
|title                       |release_date|length  |type                                |director  |actors                                         |synopsis                                                                                                                                                                                                                                                                                          |sessions|rating                           |
|----------------------------|------------|--------|------------------------------------|----------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|---------------------------------|
|Les Gardiens de la Galaxie 3|3 mai 2023  |2h 30min|Action, Fantastique, Science Fiction|James Gunn|['Chris Pratt', 'Zoe Saldana', 'Dave Bautista']|Notre bande de marginaux favorite a quelque peu changé ...|1027    |{'critics': 3.6, 'audience': 4.3}|


