#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:11:46 2020

@author: adam
"""


import graph
filename = 'barabasi_albert0.json'
g = graph.read_json_file('./barabasi_albert_graph/' + filename)
graph.draw(g)