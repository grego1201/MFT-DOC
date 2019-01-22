import requests
from bs4 import BeautifulSoup
import codecs
import time
import pandas as pd
import numpy as np

class Competitor:

    def __init__(self):
        self.test = ""


    def obtain_competitor_data(self, url):
        try:
            req = requests.get(url)
            if req.status_code == 200:
                html = BeautifulSoup(req.text, "html.parser")

                fie_ranking_container = html.find('div', {'class': 'jumbotron__ranking'})

                translation = {
                    10: "",
                    9: "",
                }
                if fie_ranking_container:
                    fie_ranking = str(html.find('div', {'class': 'jumbotron__ranking'}).text).translate(translation)
                else:
                    fie_ranking = None

                weapon_container = html.find('li', {'class': 'jumbotron__weapon'})
                if weapon_container:
                    weapon = str(html.find('li', {'class': 'jumbotron__weapon'}).text).translate(translation)
                else:
                    weapon = None

                age = str(html.find('div', {'class': 'jumbotron__age'}).text).translate(translation)
                handness = str(html.find('div', {'class': 'jumbotron__handness'}).text).translate(translation)
                nationality = str(html.find_all('div', {'class': 'jumbotron__table-cell-title'})[1].text).translate(translation)
                if nationality == "Age":
                    nationality = str(html.find_all('div', {'class': 'jumbotron__table-cell-title'})[0].text).translate(translation)

                fencer_id = str(url.split("/")[-2])

                return {
                        "fencer_id": fencer_id,
                        "nationality": nationality,
                        "handness": handness,
                        "age": age,
                        "weapon": weapon,
                        "fie_ranking": fie_ranking
                        }

            else:
                print("Conexión: Fallo en competidor --> " + url)
            return {}

        except Exception as e:
            print(e)
            print("\n")
            print("Excepción: Fallo en competidor --> " + url)
            return  {}

    def scrap_competitors(self):
        pages = []
        competitors = []
        wrong_competitors = []
        correct_competitors = []
        fieUrl = "http://fie.org"

        competitorHead = "ID, Edad, FieRanking, Nacionalidad, Mano, Arma\n"
        competitorsFile = codecs.open("../data/competidores.csv", "w+", encoding='utf-8')
        competitorsFile.write(competitorHead)

        a = time.clock()

        df = pd.read_csv("../data/eliminatoria - copia.csv")

        competitors1 = np.unique(df[" Competitor1"].values)
        competitors2 = np.unique(df[" Competitor2"].values)
        competitors = np.unique(np.concatenate((competitors1, competitors2)))
        competitors = np.delete(competitors, [0, 1])

        for competitor in competitors:
            base_url = fieUrl + competitor[1:]#  QUITAR [1:] CUANDO SE ESCRIBA BIEN EL FICHERO, SE USA PARA QUITAR EL ESPACIO EXTRA
            competitor_data = self.obtain_competitor_data(base_url)
            if not competitor_data:
                wrong_competitors.append(base_url)
                print("Error en competidor")
            else:
                correct_competitors.append(competitor_data)
                line = f"{competitor_data['fencer_id']},{competitor_data['age']},{competitor_data['fie_ranking']},{competitor_data['nationality']},{competitor_data['handness']},{competitor_data['weapon']}\n"
                competitorsFile.write(line)
                print("Competidor correcto")
            print(" --> Restantes " + str(len(competitors) - (len(wrong_competitors) + len(correct_competitors))) + " de " + str(len(competitors)))
            print("Aciertos --> " + str(len(correct_competitors)))
            print("Fallos --> " + str(len(wrong_competitors)))
        competitorsFile.close

        b = time.clock()
        print("Tiempo empleado --> " + str(b - a) + "segundos. Equivalente a --> " + str((b - a) / 60) + " minutos\n\n")
        print("Errores\n")
        print(wrong_competitors)

    def clean_competitors(self):
        df_competitors = pd.read_csv("../data/competidores.csv")
        aa = []
        competitorHead = "ID, Edad, FieRanking, Nacionalidad, Mano, Arma\n"
        competitorsFile = codecs.open("../data/competidores_ranking_limpio.csv", "w+", encoding='utf-8')
        competitorsFile.write(competitorHead)

        for competitor in df_competitors.values:
            weapon = competitor[-1][1:-1] # CAMBIAR ESTO CUANDO SE ESCRIBA BIEN EL FICHERO
            if weapon in ["Foil", "Sabre", "Epée", "None"]:
                line = f"{competitor[0]},{competitor[1]},{competitor[2]},{competitor[3]},{competitor[4]},{competitor[5]}\n"
                competitorsFile.write(line)
            else:
                competitor_weapon, competitor_ranking = weapon.split("(")
                line = f"{competitor[0]},{competitor[1]},{competitor_ranking[:-1]},{competitor[3]},{competitor[4]},{competitor_weapon}\n"

        competitorsFile.close


