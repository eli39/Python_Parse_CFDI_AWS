#!/usr/bin/env python
from __future__ import print_function
from datetime import datetime
from xml.dom import minidom
import os
import sys
from sys import exit
import glob
import csv

def handler(event, context):
    
    start=datetime.now()
    atributos = dict()
    
    
    carpetaxml = 'cfdi/'
    extensionxml = os.path.join(carpetaxml, '*.xml')
    
    archivo = []
    
    if os.path.exists('csv/salida.txt'):
        os.remove('csv/salida.txt')
            
    for archivo in glob.glob(extensionxml):
        if archivo.endswith('.xml'):
            print (archivo)
            archivo = minidom.parse(archivo)   
            
        nodos = archivo.childNodes
        comprobante = nodos[0]
        
        comparacion = dict(comprobante.attributes.items())
        
        atributos['version'] = comparacion['version']
        atributos['tipoDeComprobante'] = comparacion['tipoDeComprobante']
        atributos['serie'] = comparacion['serie']
        atributos['folio'] = comparacion['folio']
        atributos['fecha']  = comparacion['fecha'][:10]
        atributos['hora']   = comparacion['fecha'][11:19]
        atributos['total'] = comparacion['total']
        atributos['folio'] = comparacion['folio']
        atributos['metodoDePago'] = comparacion['metodoDePago']
        atributos['Moneda'] = comparacion['Moneda']
        atributos['formaDePago'] = comparacion['formaDePago']
        atributos['LugarExpedicion'] = comparacion['LugarExpedicion']
        
        emisor = comprobante.getElementsByTagName('cfdi:Emisor')
        atributos['nombre'] = emisor[0].getAttribute('nombre')
        atributos['rfc'] = emisor[0].getAttribute('rfc')
        
        domiciliofiscal = comprobante.getElementsByTagName('cfdi:DomicilioFiscal')
        atributos['calle'] = domiciliofiscal[0].getAttribute('calle')
        atributos['noExterior'] = domiciliofiscal[0].getAttribute('noExterior')
        atributos['colonia'] = domiciliofiscal[0].getAttribute('colonia')
        atributos['localidad'] = domiciliofiscal[0].getAttribute('localidad')
        atributos['municipio'] = domiciliofiscal[0].getAttribute('municipio')
        atributos['estado'] = domiciliofiscal[0].getAttribute('estado')
        atributos['pais'] = domiciliofiscal[0].getAttribute('pais')
        atributos['codigoPostal'] = domiciliofiscal[0].getAttribute('codigoPostal')
        
        expedidoen = comprobante.getElementsByTagName('cfdi:ExpedidoEn')
        atributos['calleEx'] = expedidoen[0].getAttribute('calle')
        atributos['noExteriorEx'] = domiciliofiscal[0].getAttribute('noExterior')
        atributos['coloniaEx'] = domiciliofiscal[0].getAttribute('colonia')
        atributos['localidadEx'] = domiciliofiscal[0].getAttribute('localidad')
        atributos['municipioEx'] = domiciliofiscal[0].getAttribute('municipio')
        atributos['estadoEx'] = domiciliofiscal[0].getAttribute('estado')
        atributos['paisEx'] = domiciliofiscal[0].getAttribute('pais')
        atributos['codigoPostalEx'] = domiciliofiscal[0].getAttribute('codigoPostal')
        
        regimenfiscal = comprobante.getElementsByTagName('cfdi:RegimenFiscal')
        atributos['Regimen'] = regimenfiscal[0].getAttribute('Regimen')
        
        receptor = comprobante.getElementsByTagName('cfdi:Receptor')
        atributos['nombreRe'] = receptor[0].getAttribute('nombre')
        atributos['rfcRe'] = receptor[0].getAttribute('rfc')
        domicilio = comprobante.getElementsByTagName('cfdi:Domicilio')
        atributos['calleRe'] = domicilio[0].getAttribute('calle')
        atributos['noExteriorRe'] = domicilio[0].getAttribute('noExterior')
        atributos['coloniaRe'] = domicilio[0].getAttribute('colonia')
        atributos['localidadRe'] = domicilio[0].getAttribute('localidad')
        atributos['municipioRe'] = domicilio[0].getAttribute('municipio')
        atributos['estadoRe'] = domicilio[0].getAttribute('estado')
        atributos['paisRe'] = domicilio[0].getAttribute('pais')
        atributos['codigoPostalRe'] = domicilio[0].getAttribute('codigoPostal')
        
        conceptos = comprobante.getElementsByTagName('cfdi:Concepto')
        myArray1=[]
        myArray2=[]
        myArray3=[]
        myArray4=[]
        myArray5=[]
        for cont in range(len(conceptos)):
            myArray1.append(conceptos[cont].getAttribute('descripcion').encode("utf-8").replace(",",""))
            myArray2.append(conceptos[cont].getAttribute('valorUnitario').encode("utf-8"))
            myArray3.append(conceptos[cont].getAttribute('importe').encode("utf-8"))
            myArray4.append(conceptos[cont].getAttribute('cantidad').encode("utf-8"))
            myArray5.append(conceptos[cont].getAttribute('unidad').encode("utf-8"))
            atributos['descripcion'] = myArray1
            atributos['valorUnitario'] = myArray2
            atributos['importe'] = myArray3
            atributos['cantidad'] = myArray4
            atributos['unidad'] = myArray5         
        
        impuestos = comprobante.getElementsByTagName('cfdi:Impuestos')
        atributos['totalImpuestosTrasladados'] = impuestos[0].getAttribute('totalImpuestosTrasladados')
        
        traslados = comprobante.getElementsByTagName('cfdi:Traslado')
        atributos['impuesto'] = traslados[0].getAttribute('impuesto')
        atributos['tasa'] = traslados[0].getAttribute('tasa')
        atributos['importe'] = traslados[0].getAttribute('importe')
        
        
        
        
        archivocsv = 'csv/salida.txt'
        
        salidacsv = open(archivocsv, 'a')
        wr = csv.writer(salidacsv)
        
        wr.writerow(['----------------------------------------COMPROBANTE:'])
        wr.writerow([atributos['version']])
        wr.writerow([atributos['tipoDeComprobante']])
        wr.writerow([atributos['serie']])
        wr.writerow([atributos['folio']])
        wr.writerow([atributos['fecha']+" "+atributos['hora']])
        wr.writerow([atributos['total']])
        wr.writerow([atributos['metodoDePago']])
        wr.writerow([atributos['Moneda']])
        wr.writerow([atributos['formaDePago']])
        wr.writerow([atributos['LugarExpedicion']])
        
        wr.writerow([atributos['nombre']])
        wr.writerow([atributos['rfc']])
        wr.writerow([atributos['calle']]) 
        wr.writerow([atributos['noExterior']]) 
        wr.writerow([atributos['localidad']]) 
        wr.writerow([atributos['municipio']]) 
        wr.writerow([atributos['estado']]) 
        wr.writerow([atributos['pais']]) 
        wr.writerow([atributos['codigoPostal']])
        wr.writerow([atributos['calleEx']])
        wr.writerow([atributos['noExteriorEx']]) 
        wr.writerow([atributos['localidadEx']]) 
        wr.writerow([atributos['municipioEx']]) 
        wr.writerow([atributos['estadoEx']]) 
        wr.writerow([atributos['paisEx']]) 
        wr.writerow([atributos['codigoPostalEx']])
        wr.writerow([atributos['Regimen']]) 
        
        wr.writerow([atributos['nombreRe']])
        wr.writerow([atributos['rfcRe']])
        wr.writerow([atributos['calleRe']]) 
        wr.writerow([atributos['noExteriorRe']]) 
        wr.writerow([atributos['localidadRe']]) 
        wr.writerow([atributos['municipioRe']]) 
        wr.writerow([atributos['estadoRe']]) 
        wr.writerow([atributos['paisRe']]) 
        wr.writerow([atributos['codigoPostalRe']])
        
        wr.writerow([atributos['descripcion']])
        wr.writerow([atributos['valorUnitario']])
        wr.writerow([atributos['importe']])
        wr.writerow([atributos['cantidad']])
        wr.writerow([atributos['unidad']])    
        
        wr.writerow([atributos['totalImpuestosTrasladados']])
        wr.writerow([atributos['impuesto']])
        wr.writerow([atributos['tasa']])
        wr.writerow([atributos['importe']])
        
    wr.writerow(['--------------------------------------------RUNTIME:'])
    wr.writerow([datetime.now()-start])
    salidacsv.close()
              
    return{}
    
    
    
    
    
