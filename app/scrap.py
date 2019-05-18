# -*- coding: utf-8 -*-
"""
Created on Mon May 14 17:12:19 2018

@author: greg
"""

import requests
from bs4 import BeautifulSoup
import codecs
import time
import pandas as pd
import numpy as np
from competition import Competition
from competitor import Competitor
from dataManager import DataManager

competition_manager = Competition()
competitor_manager = Competitor()
data_manager = DataManager()
