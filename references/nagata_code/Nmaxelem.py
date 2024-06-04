# -*- coding: utf-8 -*-
"""
Created on Sun May  8 15:14:30 2022

@author: julia
"""

def Nmaxele(list1, N):
    final_list = []
  
    for i in range(0, N): 
        max1 = 0
          
        for j in range(len(list1)):     
            if list1[j] > max1:
                max1 = list1[j];
                  
        list1.remove(max1);
        final_list.append(max1)
          
    return (final_list)