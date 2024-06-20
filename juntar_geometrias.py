## ATENÇAO nao usar cedilhas e acentos. Cuidar margens muito 'picotadas'. Dissolver é melhor
#todo: verificar se colunas não possuem mesmo nome e se tiverem, precisam estar com o mesmo tipo de dado

from os import listdir, mkdir
from os.path import isfile, join
from qgis.core import QgsWkbTypes, QgsVectorLayer, QgsProject, QgsField, edit
from qgis.PyQt.QtCore import QVariant
from qgis import processing

def juntar(mypath):
    #mypath = "F:\\USUARIO\\Desktop\\lixo\\SIRGAS2000_GEO"
    saida = f"{mypath}\\Geometrias"

    try:  #caso jah exista
        mkdir(saida)
    except:
        pass

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyshapes = [f for f in onlyfiles if f[-4:] == '.shp'] 
    #print(onlyshapes)
    lista_pontos = []
    lista_linhas = []
    lista_poligonos = []

    def separador(layer, listaPts, listaLinhas, listaPoligonos):
        for feat in layer.getFeatures():
            
            geometria = feat.geometry()
            geomSingleType = QgsWkbTypes.isSingleType(geometria.wkbType())
            if geometria.type() == QgsWkbTypes.PointGeometry:
                listaPts.append(layer)
                break
                # the geometry type can be of single or multi type
                # if geomSingleType:
                #     x = geometria.asPoint()
                #     print("Point: ", x)
                # else:
                #     x = geometria.asMultiPoint()
                #     print("MultiPoint: ", x)
            elif geometria.type() == QgsWkbTypes.LineGeometry:
                listaLinhas.append(layer)
                break
                # if geomSingleType:
                #     x = geometria.asPolyline()
                #     print("Line: ", x, "length: ", geometria.length())
                # else:
                #     x = geometria.asMultiPolyline()
                #     print("MultiLine: ", x, "length: ", geometria.length())
            elif geometria.type() == QgsWkbTypes.PolygonGeometry:
                listaPoligonos.append(layer)
                break
                # if geomSingleType:
                #     x = geometria.asPolygon()
                #     print("Polygon: ", x, "Area: ", geometria.area())
                # else:
                #     x = geometria.asMultiPolygon()
                #     print("MultiPolygon: ", x, "Area: ", geometria.area())
            else:
                print("Unknown or invalid geometry")
                layer.setName('ERRO')
                QgsProject.instance().addMapLayer(layer)
                # try:
                #     arrumar_geometria = processing.run("native:fixgeometries", {'INPUT':layer,
                #                                                                'OUTPUT':'TEMPORARY_OUTPUT'})
                # except:
                #     break
                break

    #adicionar nome layer para FEPAM em cada feature
    for shp in onlyshapes:
        
        Layer = QgsVectorLayer(f'{mypath}\\{shp}', f'{shp[:-4]}', "ogr")
        atributo_novo = 'nomeLayer'

        with edit(Layer):
            listaFieldName = [ field.name() for field in Layer.fields()] #lista para armazenar os fields (cabecalho)
            if atributo_novo not in listaFieldName:
                Layer.dataProvider().addAttributes([QgsField(atributo_novo, QVariant.String)])#.Int)]) #.Double)])
                Layer.updateFields()

            listaFieldName = [ field.name() for field in Layer.fields()] #lista atualizada para armazenar os fields (cabecalho)

            for feature in Layer.getFeatures():
                attrs = { listaFieldName.index(atributo_novo) : f'{shp[:-4]}'}
                Layer.dataProvider().changeAttributeValues({ feature.id() : attrs })

    # separa cada geometria
    for shp in onlyshapes:
        
        Layer = QgsVectorLayer(f'{mypath}\\{shp}', f'{shp[:-4]}', "ogr")
        separador(Layer, lista_pontos, lista_linhas, lista_poligonos)

    #merge files:
    if lista_pontos != []:
        merge_pontos = processing.run("native:mergevectorlayers", {'LAYERS': lista_pontos,'CRS':None,'OUTPUT':f"{saida}\\pontos.shp"})
        Layer_pts = QgsVectorLayer(merge_pontos['OUTPUT'], 'pontos', "ogr")
        QgsProject.instance().addMapLayer(Layer_pts)

    if lista_linhas != []:
        merge_linhas = processing.run("native:mergevectorlayers", {'LAYERS': lista_linhas,'CRS':None,'OUTPUT':f"{saida}\\linhas.shp"})
        Layer_linhas = QgsVectorLayer(merge_linhas['OUTPUT'], 'linhas', "ogr")
        QgsProject.instance().addMapLayer(Layer_linhas)

    if lista_poligonos != []:
        merge_poligonos = processing.run("native:mergevectorlayers", {'LAYERS': lista_poligonos,'CRS':None,'OUTPUT':f"{saida}\\poligonos.shp"})
        Layer_poligonos = QgsVectorLayer(merge_poligonos['OUTPUT'], 'poligonos', "ogr")
        QgsProject.instance().addMapLayer(Layer_poligonos)