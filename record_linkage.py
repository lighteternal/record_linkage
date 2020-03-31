#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:48:40 2020

@author: Dimitris Papadopoulos
"""
# Scope: Entity resolution (record linkage) on product descriptions (cameras) from different e-shops (e.g. wallmart, ebay)
# PoC using similarity measures on just 2 e-shop descriptions
# Two-step procedure: First check the available info (columns) and extract similar headers, then perform record linkage on those

import recordlinkage
import os, json
import pandas as pd
import numpy as np
import glob
pd.set_option('display.max_columns', None)
#https://github.com/J535D165/recordlinkage/issues/126

df1 = pd.DataFrame()
path_to_json1 = 'data/www.shopmania.in/' 
json_pattern1 = os.path.join(path_to_json1,'*.json')
file_list1 = glob.glob(json_pattern1)

for file in file_list1:
    data1 = pd.read_json(file, typ='series')
    df1 = df1.append(data1, ignore_index = True)

df2 = pd.DataFrame()
path_to_json2 = 'data/www.wexphotographic.com/' 
json_pattern2 = os.path.join(path_to_json2,'*.json')
file_list2 = glob.glob(json_pattern2)

for file in file_list2:
    data2 = pd.read_json(file, typ='series')
    df2 = df2.append(data2, ignore_index = True)
    
#Extracting column names (needed for index similarity)    
df1_index = list(df1.columns)  
df2_index = list(df2.columns)  

#Check index similarity first to automatically identify columns with similar titles
indexer = recordlinkage.FullIndex()
index_of_dfs = pd.DataFrame(list(zip(df1_index, df2_index)))
index_of_dfs.columns = ['A', 'B']
candidate_links_1 = indexer.index(index_of_dfs, index_of_dfs)
comp = recordlinkage.Compare()
comp.string('A', 'B', method='jarowinkler')
index_similarity = comp.compute(candidate_links_1, index_of_dfs, index_of_dfs)
#Extract only indices (index_similarity pairs) that are similar enough e.g.>0.85
pairs = index_similarity[(index_similarity.iloc[:,0]> 0.9)]
pairs_index = pairs.index

#Compare the dataframes (actual record linkage), but only condidering similar enough columns
indexer = recordlinkage.FullIndex()
candidate_links = indexer.index(df1, df2)
comp = recordlinkage.Compare()
pairs_index_titles = []
for i in range(len(pairs_index)):
    #pairs_index_titles contain the (similar enough)columns that were used for distance computation
    pairs_index_titles.append(df1.columns[pairs_index[i][0]] + "--" + df2.columns[pairs_index[i][1]])
    #comp.string('<page title>', '<page title>', method='jarowinkler')
    comp.string(df1.columns[pairs_index[i][0]],df2.columns[pairs_index[i][1]], method='jarowinkler')
#results contain the df1-df2 product pairs
results = comp.compute(candidate_links, df1, df2)
