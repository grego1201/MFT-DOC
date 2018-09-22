# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:12:19 2018

@author: greg
"""

import requests
from bs4 import BeautifulSoup
import codecs
import time

PREFIX_TABLEU = "/table?suitTable=SuiteTab_A&table="
PREFIX_128 = PREFIX_TABLEU + "128"
PREFIX_64 = PREFIX_TABLEU + "64"
PREFIX_8 = PREFIX_TABLEU + "8"

'''
def filtros:
        
    url = "http://fie.org/es/results-statistic/result"
    req = requests.get(url)
    
    values = {
        'calendar_models_CalendarsCompetition_FencCatId': [],
        'calendar_models_CalendarsCompetition_WeaponId': [],
        'calendar_models_CalendarsCompetition_GenderId': [],
        'calendar_models_CalendarsCompetition_CompTypeId': [],
        'calendar_models_CalendarsCompetition_CompCatId': [],
        'calendar_models_CalendarsCompetition_CPYear': [],
        'calendar_models_CalendarsCompetition_FedId': []        
            }
    
    if req.status_code == 200:
        print "codigo correcto"
    
        html = BeautifulSoup(req.text, "html.parser")
        formulario = html.find('form', {'id': 'calendar-form'})
        cont = 1
        for x in formulario.find_all('select'):
            sacarValores(x, x['id'])
        #print html
        print "valores sacados"
    
        print values['calendar_models_CalendarsCompetition_CPYear'][1:-1]
        
        #print html.find_all('div', {'class': 'select2-container' })
    else:
        print "pagina no encontrada"
'''
        
def obtenerPaginas():
    baseUrl = "http://fie.org/results-statistic/result?calendar_models_CalendarsCompetition%5BFencCatId%5D=&calendar_models_CalendarsCompetition%5BWeaponId%5D=&calendar_models_CalendarsCompetition%5BGenderId%5D=&calendar_models_CalendarsCompetition%5BCompTypeId%5D=&calendar_models_CalendarsCompetition%5BCompCatId%5D=&calendar_models_CalendarsCompetition%5BCPYear%5D=&calendar_models_CalendarsCompetition%5BFedId%5D=&calendar_models_CalendarsCompetition%5BDateBegin%5D=&calendar_models_CalendarsCompetition%5BDateEnd%5D=&calendar_models_CalendarsCompetition_page="
    

    # obtener páginas
    #totalPages = int(html.find('li', {'class': 'last'}).text)
    validPages = 54
    for x in range(1,validPages+1):
        pages.append(baseUrl + str(x))
    for page in pages:
        obtenerCompeticiones(page)
    print len(competitions)

        
def obtenerCompeticiones(page):
    req = requests.get(page)
    if req.status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")
        
        body = html.find_all('td', {'class': 'col1'})
        for x in body:
            competitions.append(x.find('a')['href'])
    else:
        print "Fallo con página --> " + page
    
def obtenerInformacionCompeticion(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            
            #obtener información competición
            infoTable = html.find('div', {'class': 'table-white'}).find_all('tr')[1].find_all('td')
            
            info = []
            for i in infoTable:
                info.append(i.text)
                
    
            competitionsFile.write(", ".join(info) + "\n")
            '''
            competitionInfo = {}
            for h in head:
                competitionInfo = dict(competitionInfo.items() + {h.text: info[head.index(h)].text}.items())

            #obtener resultados
            body = html.find('ul', {'id': 'yw0'})
            options = filter(lambda x: x != u'\n', body.contents)
            for option in options:
                print option.find('a')['href']
            '''
        else:
            print "Fallo en competición --> " + urlCompeticion
            
    except:
        return "Fallo en competición --> " + urlCompeticion


def obtenerRankingCompeticion(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            participantes = html.find('div', {'id': 'result-competition-grid'}).find('tbody').find_all('tr')
            ranking = []
            for participante in participantes:
                infoParticipante = participante.find_all('td')
                ranking.append({"Rank": infoParticipante[0].text,
                       "Points": infoParticipante[1].text,
                       "Name": infoParticipante[2].text,
                       "Nationality": infoParticipante[3].text,
                       "Birth Time": infoParticipante[4].text
                       })
        
            return ranking
        
        else:
            print "Fallo en competición --> " + urlCompeticion
            return []
        
    except:
        print "Fallo en competición --> " + urlCompeticion
        return  []

def obtenerPoulesCompeticion(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            poules = html.find('div', {'class': 'pools-table'}).find_all('table')            
            poulesResults = []
            for pool in poules:
                fencers = pool.find_all('tr', {'class': 'first'})
                resultsPool = []
                index = len(fencers)
                for fencer in fencers:
                    results = fencer.find_all('td')
                    assaults = []
                    for assault in range(0,index):
                        assaults.append({
                                "Oponent": assault,
                                "Result": results[2 + assault].text,
                                })
                
                    resultsPool.append({
                           "Poule position": int(results[2]['class'][0].strip('col')) - 2,
                           "Nationality": results[0].text,
                           "Name": results[1].text,
                           "Results": assaults,
                           "VM": results[2 + index].text,
                           "HS": results[3 + index].text,
                           "HR": results[4 + index].text,
                            "HSHR": results[5 + index].text
                            })
                    
                poulesResults.append(resultsPool)    
            print poulesResults[0]
            
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []
    
def obtenerTablon128Y64(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            tables = html.find('div', {'class': 'rank-table'}).find_all('table')
            
            tableu_128 = []
            tableu_64 = []
            for table in tables:
                table_128 = table.find('td', {'class': 'col_1'}).find_all('div', {'class': 'rank-table__teams'})
                table_64 = table.find('td', {'class': 'col_2'}).find_all('div', {'class': 'rank-table__teams'})
                        
                for part_1 in table_128:
                    assault = part_1.find_all('div', {'class': 'item'})
                    assault_result = []
                    for fencer in assault:
                        if fencer.find('div', {'class': 'col2'}).text == "":
                            break
                        assault_result.append({
                                "Fencer": fencer.find('div', {'class': 'col2'}).text,
                                "Fencer link": fencer.find('div', {'class': 'col2'}).find('a')['href'],
                                "Nationality": fencer.find('div', {'class': 'col3'}).text,
                                "Result": fencer.find('div', {'class': 'col4'}).text
                                })
                    tableu_128.append(assault_result)
                
                for part_2 in table_64:
                    assault = part_2.find_all('div', {'class': 'item'})
                    assault_result = []
                    
                    for fencer in assault:
                        if fencer.find('div', {'class': 'col2'}).text == "":
                            break
                        assault_result.append({
                                "Fencer": fencer.find('div', {'class': 'col2'}).text,
                                "Fencer link": fencer.find('div', {'class': 'col2'}).find('a')['href'],
                                "Nationality": fencer.find('div', {'class': 'col3'}).text,
                                "Result": fencer.find('div', {'class': 'col4'}).text
                                })
                    tableu_64.append(assault_result)
            
            return tableu_128, tableu_64
            
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:        
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []

pages = []    
competitions = []
fieUrl = "http://fie.org"

competitionHead = "Category, Gender, Weapon, Competition, Place, Date, Type, Event\n"
competitionsFile = codecs.open("../data/competiciones.csv", "w", encoding='utf-8')
competitionsFile.write(competitionHead)

a = time.clock()
'''
obtenerPaginas()
print "\n \n -------------------- "
print "Paginas obtenidas"
print " -------------------- \n \n"

obtenerCompeticiones(fieUrl)

print "\n \n -------------------- "
print "Competiciones creadas"
print " -------------------- \n \n"


for competition in competitions: 
    obtenerInformacionCompeticion(fieUrl + competition)
'''


obtenerTablon128Y64("http://fie.org/competitions/2018/47/results/table?suitTable=SuiteTab_A&table=128")


b = time.clock()

competitionsFile.close

print "Tiempo empleado --> " + str(b - a) + "segundos. Equivalente a --> " + str((b - a) / 60) + " minutos"









