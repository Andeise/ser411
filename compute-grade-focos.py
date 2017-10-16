#encoding: utf-8
#Iniciar sempre com o codigo anterior
#Criar colunas e linhas e extensão espacial:
#Objetivo: Criar grade numerica com valores acumulados de focos de queimada Aula 05.10.
#importar pacotes:

import sys #biblioteca que fornece funcionalidades associadas as sistema operacional
import os
import numpy as np #Biblioteca NumPy. o import ficará cinza antes de ser utilizado.
try:
    from osgeo import gdal, ogr, osr
except:
    sys.exit("Erro: A biblioteca GDAL não foi encontrada!")
from utils1 import*

gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()

vector_file = "/home/gribeiro/Dados/Queimadas/focos/focos-2016.shp"
vector_file_base_name = os.path.basename(vector_file)
layer_name = os.path.splitext(vector_file_base_name)[0]

spatial_extent = { 'xmin': -89.975, 'ymin': -59.975,
                   'xmax': -29.975, 'ymax': 10.025 }
spatial_resolution = { 'x': 0.05, 'y': 0.05 }
grid_dimensions = { 'cols': 1200, 'rows': 1400 }

file_format = "GTiff"
output_file_name = "/home/gribeiro/Dados/Queimadas/focos/grade-2016.tiff"

#Para recuperar a camada de informação com os focos, que estarao na layer:

layer_focos = shp_focos.GetLayer(layer_name)
if layer_focos is None:
    sys.exit("Erro, não foi possivel acessar a camada {0} no arquivo {1}!").format(layer_name, vector_file)

#Criando uma matriz numerica, pois ja foi criado o shp e add as infos. Utilizaremos a bib do NumPy. Ou seja, será uma gerado uma matriz bidimensioanl com 0
#e a cada vez que contabilizar um foco, será mudado de 0 para 1.

matriz = np.zeros((grid_dimensions['rows'], grid_dimensions['cols']), np.int16)

#Interando por cada um dos focos calculando sua localização na grade:

for foco in layer_focos: #A variavel foco seera associada a um objeto da camda e sera possivel pegar a geometria dele.
    location = foco.GetGeometryRef()
    col,row = Geo2Grid(location,grid_dimensions,spatial_resolution,spatial_extent)

#Será contabilizado mais 1

    matriz[row, col] +=1

#Criar o raster para ser salvo no disco utilizando Gdal:

driver = gdal.GetDriverByName(file_format)
if driver is None:
    sys.exit("Erro, nao foi possovel identificar o driver '{0}'.".format(file_format))
raster = driver.Create(output_file_name, grid_dimensions['cols'],grid_dimensions['rows'],1, gdal.GDT_UInt16)
if raster is None:
    sys.exit("Erro: não foi possivel criar o arquivo'{0}'.".format(output_file_name))

#Define os paramentros de transformacao de coorde.

raster.SetGeoTransform((spatial_extent['xmin'], spatial_resolution['x'], 0, spatial_extent['ymax'],0, -spatial_resolution['y']))

#Usar as infor do sistema de coordenadas espacial do layer para de focos na definicao da gade de saida

srs_focos = layer_focos.GetSpatialRef()
raster.SetProjection(srs_focos.ExportToWkt())

#Para acessar o objeto associado a primeira banda do raster e escreve o array NumPy na banda Gdal:

band = raster.GetRasterBand(1)
band.WriteArray(matriz, 0, 0)
band.FlushCache()