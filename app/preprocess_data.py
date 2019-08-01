import codecs
import time
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

class CompetitorDataPreprocess:
    def __init__(self):
        self.competitors_file_path = "../data/competidores.csv"
        self.competitors_file_headers = ['ID', 'Edad', 'FieRanking', 'Nacionalidad', 'Mano', 'Arma']

    def replaces_nones_fie_ranking(self):
        df = pd.read_csv("../data/competidores_ranking_limpio.csv", header=1, names=self.competitors_file_headers)
        df['FieRanking'].replace('None', 9999999, inplace=True)
        df['FieRanking'].replace(' None', 9999999, inplace=True)
        df['Mano'].replace('right', 'Right', inplace=True)
        df.to_csv('../data/competidores_ranking_limpio.csv', index=False)

    def remove_nones_weapon(self):
        df = pd.read_csv("../data/competidores_ranking_limpio.csv", header=1, names=self.competitors_file_headers)
        df = df[df.Arma != " None "]
        df.to_csv('../data/competidores_ranking_limpio.csv')

    def remove_no_epee(self):
        df = pd.read_csv("../data/competidores_ranking_limpio.csv", header=1, names=self.competitors_file_headers)
        df = df[df.Arma != " Epée "]
        df.to_csv('../data/competidores_ranking_limpio.csv')

class MatchPreprocess:
    def __init__(self):
        self.origin_file_path = "../data/competition_with_competitors_data.csv"
        self.winner_path = "../data/2_competition_with_winner.csv"
        self.wout_results_path = "../data/3_competition_wout_results_columns.csv"
        self.wout_id_path = "../data/4_competition_wout_id_columns.csv"
        self.wout_fids_path = "../data/5_competition_wout_fids_columns.csv"
        self.frankings_path = "../data/6_competition_frankings_columns.csv"
        self.origin_file_head = ["ID", "TABLEU", "C1_ID", "C1_AGE", "C1_RANKING", "C1_NATIONALITY", "C1_HANDNESS", "C1_WEAPON", "C2_ID", "C2_AGE", "C2_RANKING", "C2_NATIONALITY", "C2_HANDNESS", "C2_WEAPON", "RESULT_C1", "RESULT_C2"]
        self.winner_file_head = self.origin_file_head[:]
        self.wout_results_head = self.winner_file_head[:]
        self.wout_results_head.append("WINNER")
        self.wout_id_head = self.wout_results_head[:]
        self.wout_id_head.remove("RESULT_C1")
        self.wout_id_head.remove("RESULT_C2")
        self.wout_fids_head = self.wout_id_head[:]
        self.wout_fids_head.remove("ID")
        self.frankings_head = self.wout_fids_head[:]
        self.frankings_head.remove("C1_ID")
        self.frankings_head.remove("C2_ID")

    def preprocess_file(self):
        self.replaces_nones_fie_ranking()
        self.remove_none_results_rows()
        self.normalize_handness()
        self.normalize_weapon()
        self.add_victory_field()
        self.drop_results_columns()
        self.drop_id_column()
        self.drop_fencers_id_column()
        self.make_fencers_ranking_to_int()

    def normalize_handness(self):
        df = pd.read_csv(self.origin_file_path, header=1, names=self.origin_file_head)
        for i in range(1, 3):
            df["C" + str(i) + "_HANDNESS"].replace(' Right', 0.0, inplace=True)
            df["C" + str(i) + "_HANDNESS"].replace(' Left', 1.0, inplace=True)
        df.to_csv(self.origin_file_path)

    def normalize_weapon(self):
        df = pd.read_csv(self.origin_file_path, header=1, names=self.origin_file_head)
        for i in range(1, 3):
            df["C" + str(i) + "_WEAPON"].replace(' Sabre ', 0.0, inplace=True)
            df["C" + str(i) + "_WEAPON"].replace(' Foil ', 1.0, inplace=True)
            df["C" + str(i) + "_WEAPON"].replace(' Epée ', 2.0, inplace=True)
        df.to_csv(self.origin_file_path)



    def replaces_nones_fie_ranking(self):
        df = pd.read_csv(self.origin_file_path, header=1, names=self.origin_file_head)
        for i in range(1, 3):
            df["C" + str(i) + "_RANKING"].replace('None', 9999999, inplace=True)
            df["C" + str(i) + "_RANKING"].replace(' None', 9999999, inplace=True)
            df["C" + str(i) + "_HANDNESS"].replace(' right ', ' Right', inplace=True)
            df["C" + str(i) + "_HANDNESS"].replace(' right', ' Right', inplace=True)
        df.to_csv(self.origin_file_path)

    def remove_none_results_rows(self):
        df = pd.read_csv(self.origin_file_path, header=1, names=self.origin_file_head)
        df = df.drop(df[df['RESULT_C1'] == ' '].index)
        df.to_csv(self.origin_file_path)

    def drop_results_columns(self):
        df = pd.read_csv(self.winner_path, header=1, names=self.wout_results_head)
        df = df.drop(['RESULT_C1', 'RESULT_C2'], axis = 1)
        df.to_csv(self.wout_results_path)

    def drop_id_column(self):
        df = pd.read_csv(self.wout_results_path, header=1, names=self.wout_id_head)
        df = df.drop(['ID'], axis = 1)
        df.to_csv(self.wout_id_path, index = False)

    def drop_fencers_id_column(self):
        df = pd.read_csv(self.wout_id_path, header=1, names=self.wout_fids_head)
        df = df.drop(['C1_ID', 'C2_ID'], axis = 1)
        df.to_csv(self.wout_fids_path, index = False)

    def make_fencers_ranking_to_int(self):
        df = pd.read_csv(self.wout_fids_path, header=1, names=self.frankings_head)
        fencer1_ranking = []
        fencer2_ranking = []
        for result in df["C1_RANKING"]:
            fencer1_ranking.append(int(result))

        for result in df["C2_RANKING"]:
            fencer2_ranking.append(int(result))

        df["C1_RANKING"] = fencer1_ranking
        df["C2_RANKING"] = fencer2_ranking
        df.to_csv(self.frankings_path, index = False)

    def add_victory_field(self):
        df = pd.read_csv(self.origin_file_path, header=1, names=self.origin_file_head)
        fencer1_results = []
        fencer2_results = []
        match_winner = []
        for result in df["RESULT_C1"]:
            fencer1_results.append(result)

        for result in df["RESULT_C2"]:
            fencer2_results.append(result)

        for i in range(df.shape[0]):
            f1_points = int(fencer1_results[i].split("/")[1])
            f2_points = int(fencer2_results[i].split("/")[1])
            match_winner.append(float(0) if f1_points > f2_points else float(1))

        df['WINNER'] = match_winner
        df.to_csv(self.winner_path)
