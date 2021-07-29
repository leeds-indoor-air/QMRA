import math as m
'''
From Duguid 1946 (via Excel model)
'''
diameter_small = [1.5, 3, 6, 12, 20] #micron
diameter_large = [28, 36, 45, 62.5, 87.5, 112.5, 137.5, 175, 225, 375, 750, 1500] #micron

cough_small = [50, 290, 970, 1600, 870]
cough_large = [420, 240, 110, 140, 85, 48, 38, 35, 29, 34, 12, 2]

talk_small = [1, 13, 52, 78, 40]
talk_large = [24, 12, 6, 7, 5, 4, 3, 2, 1, 3, 1, 0]

sneeze_small = [1000 * x for x in [26, 160, 350, 280, 97, 37, 17, 9, 10, 4.5]]
sneeze_large = [1000 * x for x in [2.5, 1.8, 2.0, 1.4, 2.1, 1.0, 0.140]]

volume_small = [ m.pi * m.pow(d * 1e-6, 3) / 6 for d in diameter_small ] #m^3
volume_large = [ m.pi * m.pow(d * 1e-6, 3) / 6 for d in diameter_large ] #m^3

total_cough_small = [ n * v * 1e9 for n, v in zip(cough_small, volume_small) ] #ul
total_talk_small = [ n * v * 1e9 for n, v in zip(talk_small, volume_small) ] #ul
total_sneeze_small = [ n * v * 1e9 for n, v in zip(sneeze_small, volume_small) ] #ul

total_cough_large = [ n * v * 1e9 for n, v in zip(cough_large, volume_large) ] #ul
total_talk_large = [ n * v * 1e9 for n, v in zip(talk_large, volume_large) ] #ul
total_sneeze_large = [ n * v * 1e9 for n, v in zip(sneeze_large, volume_large) ] #ul
