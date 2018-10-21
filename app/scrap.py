# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:12:19 2018

@author: greg
"""

import requests
from bs4 import BeautifulSoup
import codecs
import time
        
def obtenerPaginas():
    baseUrl = "http://fie.org/results-statistic/result?calendar_models_CalendarsCompetition%5BFencCatId%5D=&calendar_models_CalendarsCompetition%5BWeaponId%5D=&calendar_models_CalendarsCompetition%5BGenderId%5D=&calendar_models_CalendarsCompetition%5BCompTypeId%5D=&calendar_models_CalendarsCompetition%5BCompCatId%5D=&calendar_models_CalendarsCompetition%5BCPYear%5D=&calendar_models_CalendarsCompetition%5BFedId%5D=&calendar_models_CalendarsCompetition%5BDateBegin%5D=&calendar_models_CalendarsCompetition%5BDateEnd%5D=&calendar_models_CalendarsCompetition_page="
    validPages = 59
    for x in range(1,validPages+1):
        pages.append(baseUrl + str(x))
    for page in pages:
        obtenerCompeticiones(page)

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
            infoTable = html.find('div', {'class': 'table-white'}).find_all('tr')[1].find_all('td')
            info = []
            for i in infoTable:
                info.append(i.text)
                
            competitionsFile.write(", ".join(info) + "\n")
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
                if  participante.find('td', {'class': 'col2'}) is None:
                    ranking.append({"Rank": infoParticipante[0].text,
                           "Points": "",
                           "Name": infoParticipante[1].text,
                           "Nationality": infoParticipante[2].text,
                           "Birth Time": infoParticipante[3].text
                           })
                else: 
                    ranking.append({"Rank": infoParticipante[0].text,
                           "Points": infoParticipante[1].text,
                           "Name": infoParticipante[2].text,
                           "Nationality": infoParticipante[3].text,
                           "Birth Time": infoParticipante[4].text
                           })
        
            return ranking
        
        else:
            print "obtenerRankingCompeticion Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except:
        print "obtenerRankingCompeticion Excepción: Fallo en competición --> " + urlCompeticion
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
            return poulesResults
            
        else:
            print "obtenerPoulesCompeticion Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:
        print e
        print "\n"
        print "obtenerPoulesCompeticion Excepción: Fallo en competición --> " + urlCompeticion
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

def obtenerTablon64(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
        
            tables = html.find('div', {'class': 'rank-table'}).find_all('table')
            tableu_32 = []
            tableu_16 = []
            tableu_8 = []
                                                
            for table in tables:             
                table_32 = table.find('td', {'class': 'col_2'}).find_all('div', {'class': 'rank-table__teams'})
                table_16 = table.find('td', {'class': 'col_3'}).find_all('div', {'class': 'rank-table__teams'})
                table_8 = table.find('td', {'class': 'col_4'}).find_all('div', {'class': 'rank-table__teams'})
                
                for part in table_32:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_32.append(assault_result)
                    
                for part in table_16:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_16.append(assault_result)
                    
                for part in table_8:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_8.append(assault_result)
                    
            return tableu_32, tableu_16, tableu_8
                
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:        
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []

def obtenerTablon32(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            tables = html.find('div', {'class': 'rank-table'}).find_all('table')
            tableu_32 = []
            tableu_16 = []
            tableu_8 = []
            for table in tables:
                table_32 = table.find('td', {'class': 'col_1'}).find_all('div', {'class': 'rank-table__teams'})
                table_16 = table.find('td', {'class': 'col_2'}).find_all('div', {'class': 'rank-table__teams'})
                table_8 = table.find('td', {'class': 'col_3'}).find_all('div', {'class': 'rank-table__teams'})
                
                for part in table_32:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_32.append(assault_result)
                    
                for part in table_16:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_16.append(assault_result)
                    
                for part in table_8:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_8.append(assault_result)
                    
            return tableu_32, tableu_16, tableu_8
                
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:        
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []

def obtenerTablon16(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
        
            tables = html.find('div', {'class': 'rank-table'}).find_all('table')
            tableu_16 = []
            tableu_8 = []
            
            for table in tables:
                table_16 = table.find('td', {'class': 'col_1'}).find_all('div', {'class': 'rank-table__teams'})
                table_8 = table.find('td', {'class': 'col_2'}).find_all('div', {'class': 'rank-table__teams'})
            
                for part in table_16:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_16.append(assault_result)
                    
                for part in table_8:
                    assault = part.find_all('div', {'class': 'item'})
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
                    tableu_8.append(assault_result)
                    
            return tableu_16, tableu_8
                
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
            return []
        
    except Exception as e:        
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []
                 
def obtenerTablon8(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            tables = html.find('div', {'class': 'rank-table'})
            
            table4 = tables.find('td', {'class': 'col_2'}).find_all('div', {'class': 'rank-table__teams'})
            table2 = tables.find('td', {'class': 'col_3'}).find_all('div', {'class': 'rank-table__teams'})
            
            tableu_4 = obtenerDatosTablon(table4)
            tableu_2 = obtenerDatosTablon(table2)
                    
            return tableu_4, tableu_2
        
        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
        return []
        
    except Exception as e:        
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []
    
def obtenerDatosTablon(tablon):
    board = []
    
    for part in tablon:
        assault = part.find_all('div', {'class': 'item'})
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
        board.append(assault_result)
    return board

def escribirResultados(competitionID, tablon):
    line = ""
    
    for asalto in tablon:
        fencer1 = asalto[0]
        if len(asalto) == 1:
            fencer2 = {'Fencer link': u'', 'Result': u''}
        else:
            fencer2 = asalto[1]
        line += competitionID + ", " + str(len(tablon) * 2) + ", " + fencer1['Fencer link'] + ', ' + fencer2['Fencer link'] + \
        ', ' + fencer1['Result'] + ', ' + fencer2['Result'] + "\n"

    return line

def detectarTipoCompeticionYTablones(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            tables = html.find('div', {'class': 'table-white'}).find_all('td')
            pestanias = html.find('ul', {'id': 'yw0'}).find_all('li')
            nombrePestanias = []
            for pestania in pestanias:
                item = pestania.find('a')
                nombrePestanias.append((item.text, item['href']))
            
            if tables[6].text == "T":
                return "Equipos", nombrePestanias
            else:
                return "Individual", nombrePestanias

        else:
            print "Conexión: Fallo en competición --> " + urlCompeticion
        return []
        
    except Exception as e:
        print e
        print "\n"
        print "Excepción: Fallo en competición --> " + urlCompeticion
        return  []
    
def check64Tableu(urlCompeticion):
    try:
        req = requests.get(urlCompeticion)
        if req.status_code == 200:
            html = BeautifulSoup(req.text, "html.parser")
            tables = html.find_all('a', {'class': 'btn-transparent'})
            
            if tables[-3].text == "tablo 64":
                return "64"
            elif tables[-3].text == "tablo 32":
                return "32"
            else:
                return "16"

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
competitionsFile = codecs.open("../data/competiciones.csv", "w+", encoding='utf-8')
competitionsFile.write(competitionHead)

eliminiatoriaHead = "CompetitionID, Tableu, Competitor1, Competitor2, ResultCompetitor1, ResultCompetitor2\n"
eliminatoriaFile = codecs.open("../data/eliminatoria.csv", "w+", encoding='utf-8')
eliminatoriaFile.write(eliminiatoriaHead)


a = time.clock()

obtenerPaginas()
print "\n \n -------------------- "
print "Paginas obtenidas"
print " -------------------- \n \n"

obtenerCompeticiones(fieUrl)
print "\n \n -------------------- "
print "Competiciones creadas"
print " -------------------- \n \n"

errors = []
equipos = []

for competition in competitions:
    base_url = fieUrl + competition
    print base_url
    
    try:
        tipo, pestanias = detectarTipoCompeticionYTablones(base_url)
        if tipo == "Individual":
            obtenerRankingCompeticion(base_url + "/rank")
            obtenerPoulesCompeticion(base_url + "/pools")
            tablon128 = tablon64 = tablon32 = tablon16 = tablon8 = tablon4 = tablon2 = ""
            
            for pestania in pestanias:
                link = fieUrl + str(pestania[1])
                if pestania[0] == "tablo 64":
                    tablon32, tablon16, tablon8 = obtenerTablon64(link)
                elif pestania[0] == "tablo 32":
                    tablon32, tablon16, tablon8 = obtenerTablon32(link)
                elif pestania[0] == "tablo 16":
                    tablon16, tablon8 = obtenerTablon16(link)
                elif pestania[0] == "quarterfinal":
                    tablon4, tablon2 = obtenerTablon8(link)
                    
            tablones = [tablon128, tablon64, tablon32, tablon16, tablon8, tablon4, tablon2]
            
            for tablon in tablones:
                if tablon is "":
                    next
                year, competitionID = base_url.split("competitions/")[1].split("/")[0:2]
                line = escribirResultados(year + "-" + competitionID, tablon)
                eliminatoriaFile.write(line)
            print "Competición lista --> " + str(base_url) + "\n errores --> " + str(len(errors))
        else:
            print "Competición pasada por equipos --> "+ str(base_url)
            equipos.append(base_url)
        print "\nRestantes --> " + str(len(competitions) - competitions.index(competition)) + "/" + str(len(competitions)) + "\n"
    
    except Exception as e:
        print "Error con la siguiente url -->" + str(base_url)
        print "\nRestantes --> " + str(len(competitions) - competitions.index(competition)) + "/" + str(len(competitions)) + "\n"

        errors.append(base_url)
    
print "\n \n -------------------- "
print "Información obtenida"
print " -------------------- \n \n"

b = time.clock()

competitionsFile.close
eliminatoriaFile.close

print "Tiempo empleado --> " + str(b - a) + "segundos. Equivalente a --> " + str((b - a) / 60) + " minutos\n\n"
print "Errores\n"
print errors









