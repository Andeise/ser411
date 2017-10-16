#encoding: utf-8
import sys #biblioteca que fornece funcionalidades associadas as sistema operacional
import os
import numpy as np #Biblioteca NumPy. o import ficará cinza antes de ser utilizado.
try:
from rom osgeo import gdal, ogr, osr
except:
sys.exit("Erro: A biblioteca GDAL não foi encontrada!")
def Geo2Grid(location, dimensions, resolution, extent):
""" Sera convertido uma coordenada grografica para uma grade regular"""
x = location.GetX()
y = location.GetY()
col = int( ( x - extent['xmin'])/resolution['x'])
row = int( (dimensions['rows']) - (y - extent['ymin']) / resolution['y']) #A subtracao eh feita pq a grade x e y fica invertida...
return col, row