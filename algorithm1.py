#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:52:09 2019

@author: adamm
"""
import networkx as nx

def greedy_th(G,Q,e,k):
    q = len(Q)
    P = set()
    er_max = 0
    for (u,v) in Q:
        er_temp = nx.resistance_distance(G,u,v)
        if er_temp >= er_max:
            er_max = er_temp
    th = er_max
    while th >= (e/q)*er_max:
        for (u,v) in (Q-P):
            if (len(P)< k) and (nx.resistance_distance(G,u,v) >= th):
                G.add_edge(u,v)
                P.add((u,v))
        th=(1-e)*th
    return P