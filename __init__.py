# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShpFEPAM
                                 A QGIS plugin
        begin                : 2024-06-20
        copyright            : (C) 2024 by Romário Moraes Carvalho Neto
        email                : romariocarvalho@hotmail.com
 ***************************************************************************/

 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ShpFEPAM class from file ShpFEPAM.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .shp_fepam import ShpFEPAM
    return ShpFEPAM(iface)
