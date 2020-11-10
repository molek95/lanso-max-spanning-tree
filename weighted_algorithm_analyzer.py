# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 19:43:17 2020

@author: adam
"""

#                'diam_span_collector': diam_span_collector,
#            'diam_edge_collector': diam_edge_collector,
#            '': diam_time,

import pandas as pd
import os

def algorithm_evaluation(file_name, result_url, k):
    path = './improved_algorithm_result/weighted/' + str(k) + '/' + file_name + '.csv'
    df = pd.read_csv(path)
    
    # random choice alg
    alg_time = 0
    for t in df['algorithm_time']:
        alg_time = alg_time + t
    alg_time = alg_time / len(df)
    
    # alg with det
    improved_alg_time = 0
    for t in df['improved_algorithm_time']:
        improved_alg_time = improved_alg_time + t
    improved_alg_time = improved_alg_time / len(df)
    
    # base alg (alg_1)
    base_alg_time = 0
    for t in df['algorithm_1_time']:
        base_alg_time = base_alg_time + t
    base_alg_time = base_alg_time / len(df)
    
    greedy_alg_time = 0
    alg_solution_dif = 0
    improved_alg_solution_dif = 0
    base_solution_dif = 0
    greedy_solution_dif = 0
   #diam_solution_dif = 0
    
    for t in df['greedy_time']:
        greedy_alg_time = greedy_alg_time + t
    greedy_alg_time = greedy_alg_time / len(df)
          
    #diam_time = 0
    #for t in df['diam_time']:
    #    diam_time = diam_time + t
    #diam_time = diam_time / len(df)
        
    if 'correct_span_collector' in df.columns:
        for index, row in df.iterrows():
            alg_solution_dif = alg_solution_dif + (row['correct_span_collector'] - row['algorithm_span_collector'])
        alg_solution_dif = alg_solution_dif / len(df)
        
        for index, row in df.iterrows():
            improved_alg_solution_dif = improved_alg_solution_dif + (row['correct_span_collector'] - row['improved_algorithm_span_collector'])
        improved_alg_solution_dif = improved_alg_solution_dif / len(df)
        
        for index, row in df.iterrows():
            base_solution_dif = base_solution_dif + (row['correct_span_collector'] - row['algorithm_1_span_collector'])
        base_solution_dif = base_solution_dif / len(df)
        
        for index,row in df.iterrows():
            greedy_solution_dif = greedy_solution_dif + (row['correct_span_collector'] - row['greedy_span_collector'])
        greedy_solution_dif = greedy_solution_dif / len(df)
        
       # for index,row in df.iterrows():
       #     diam_solution_dif = diam_solution_dif + (row['correct_span_collector'] - row['diam_span_collector'])
       # diam_solution_dif = diam_solution_dif / len(df)
        
    else:
        for index, row in df.iterrows():
            improved_alg_solution_dif = improved_alg_solution_dif + (row['improved_algorithm_span_collector'])
        improved_alg_solution_dif = improved_alg_solution_dif / len(df)
        
        for index, row in df.iterrows():
            alg_solution_dif = alg_solution_dif + (row['improved_algorithm_span_collector'] - row['algorithm_span_collector'])
        alg_solution_dif = alg_solution_dif / len(df)
        
        for index, row in df.iterrows():
            base_solution_dif = base_solution_dif + (row['improved_algorithm_span_collector'] - row['algorithm_1_span_collector'])
        base_solution_dif = base_solution_dif / len(df)
        
        for index,row in df.iterrows():
            greedy_solution_dif = greedy_solution_dif + (row['improved_algorithm_span_collector'] - row['greedy_span_collector'])
        greedy_solution_dif = greedy_solution_dif / len(df)
        
       # for index,row in df.iterrows():
       #     diam_solution_dif = diam_solution_dif + (row['improved_algorithm_span_collector'] - row['diam_span_collector'])
       # diam_solution_dif = diam_solution_dif / len(df)
    
    alg_time_list = list()
    base_alg_time_list = list()
    greedy_time_list = list()
    alg_solution_dif_list = list()
    base_solution_dif_list = list()
    greedy_solution_dif_list = list()    
    improved_alg_time_list = list()
    
    improved_alg_solution_dif_list = list()
    
    diam_time_list = list()
    diam_solution_dif_list = list()
    
    alg_time_list.append(str(alg_time))
    base_alg_time_list.append(str(base_alg_time))
    greedy_time_list.append(str(greedy_alg_time))
    alg_solution_dif_list.append(str(alg_solution_dif))
    base_solution_dif_list.append(str(base_solution_dif))
    greedy_solution_dif_list.append(str(greedy_solution_dif))
    improved_alg_time_list.append(str(improved_alg_time))
    
    improved_alg_solution_dif_list.append(str(improved_alg_solution_dif))
    
    #diam_time_list.append(str(diam_time))
    #diam_solution_dif_list.append(str(diam_solution_dif))
    
    if 'correct_span_collector' in df.columns:  
        result_data = {
            'random_select_alg_time': alg_time_list,
            'improved_alg_time': improved_alg_time_list,
            'alg_1_time': base_alg_time_list,
            'greedy_time': greedy_time_list,
            #'diam_time': diam_time_list,
            'ranom_select_alg_solution_dif': alg_solution_dif_list,
            'improved_alg_solution_dif': improved_alg_solution_dif_list,
            'alg_1_solution_dif': base_solution_dif_list,
            'greedy_solution_dif_list': greedy_solution_dif_list,
            #'diam_solution_dif_list': diam_solution_dif_list
        }
    else:
        result_data = {
            'random_select_alg_time': alg_time_list,
            'improved_alg_time': improved_alg_time_list,
            'alg_1_time': base_alg_time_list,
            'greedy_time': greedy_time_list,
            #'diam_time': diam_time_list,
            'avarage_spanning_tree_with_improved_alg': improved_alg_solution_dif,
            'random_select_alg_solution_dif': alg_solution_dif_list,
            'alg_1_solution_dif': base_solution_dif_list,
            'greedy_solution_dif_list': greedy_solution_dif_list,
            #'diam_solution_dif_list': diam_solution_dif_list
        }
    
    res_df = pd.DataFrame(result_data)
    
    if not os.path.exists('algorithm_evaluations'):
        os.makedirs('algorithm_evaluations')
    if not os.path.exists('algorithm_evaluations/weighted'):
        os.makedirs('algorithm_evaluations/weighted')
    if not os.path.exists('algorithm_evaluations/weighted/' + str(k)):
        os.makedirs('algorithm_evaluations/weighted/' + str(k))
    res_df.to_csv('./algorithm_evaluations/weighted/' + str(k) + '/' + str(result_url) + '.csv', index=False)