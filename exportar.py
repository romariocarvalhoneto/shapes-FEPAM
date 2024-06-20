## transformar todos os shapes que estao na pasta para outro Sist coord
## serah criada nova pasta dentro da pasta de trabalho

from os import listdir, mkdir
from os.path import isfile, join
from qgis.core import QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem, QgsVectorFileWriter
from qgis import processing


def exportar(mypath):
    #mypath = "F:\\USUARIO\\Desktop\\lixo"
    datum = 'EPSG:4674'
    saida = f"{mypath}\\SIRGAS2000_GEO"

    try:
        mkdir(saida)
    except FileExistsError:
        pass  # Pasta já existe

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyshapes = [f for f in onlyfiles if f[-4:].lower() in ['.shp', '.kml', '.kmz', '.dxf']]

    for shp in onlyshapes:
        try:
            caminho_arquivo = join(mypath, shp)
            layer_name = shp[:-4]
            if shp[-4:].lower() == '.dxf':
                # Carregar o DXF com um parâmetro específico para DXF
                caminho_arquivo += '|layername=entities'
                Layer = QgsVectorLayer(caminho_arquivo, layer_name, "ogr")

                # Verificar se o DXF foi carregado corretamente
                if Layer.isValid():
                    print(caminho_arquivo)
                    extractZ = processing.run("native:extractzvalues", {'INPUT':'F:\\USUARIO\\Desktop\\lixo\\margem.dxf',
                                                                        'SUMMARIES':[0],
                                                                        'COLUMN_PREFIX':'z_',
                                                                        'OUTPUT':'TEMPORARY_OUTPUT'})

                    temp_layer = extractZ['OUTPUT']

                    params = {
                        'INPUT': temp_layer,
                        'TARGET_CRS': QgsCoordinateReferenceSystem(datum),
                        'OUTPUT': f"{saida}\\{layer_name}.shp"
                    }
                    reprojetado = processing.run("native:reprojectlayer", params)
                    Layer_Novo = QgsVectorLayer(reprojetado['OUTPUT'], layer_name, "ogr")
                    QgsProject.instance().addMapLayer(Layer_Novo)
                else:
                    print(f"Erro ao carregar DXF: {caminho_arquivo}")

            else:
                # Tratamento para arquivos não DXF
                Layer = QgsVectorLayer(caminho_arquivo, layer_name, "ogr")
                if Layer.isValid():
                    params = {
                        'INPUT': Layer,
                        'TARGET_CRS': QgsCoordinateReferenceSystem(datum),
                        'OUTPUT': f"{saida}\\{layer_name}.shp"
                    }
                    reprojetado = processing.run("native:reprojectlayer", params)
                    Layer_Novo = QgsVectorLayer(reprojetado['OUTPUT'], layer_name, "ogr")
                    QgsProject.instance().addMapLayer(Layer_Novo)
                else:
                    print(f"Layer inválido: {shp}")

        except Exception as e:
            print(f"Erro ao processar {shp}: {e}")

# if TIPO == 'kml':
#     for shp in onlyshapes:
#         Layer = QgsVectorLayer(f'{mypath}\\{shp}', f'{shp[:-4]}', "ogr")
#         reprojetado = processing.run("native:reprojectlayer", {'INPUT':Layer,
#                                                 'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
#                                                 'OPERATION':'+proj=pipeline +step +inv +proj=utm +zone=22 +south +ellps=GRS80 +step +proj=unitconvert +xy_in=rad +xy_out=deg',
#                                                 'OUTPUT':f"{saida}\\{shp[:-4]}.kml"})
#         # Layer_Novo = QgsVectorLayer(reprojetado['OUTPUT'], f'{shp[:-4]}', "ogr")
        # QgsProject.instance().addMapLayer(Layer_Novo)]