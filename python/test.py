#!/usr/bin/python
# -*- encoding: utf-8 -*-

import string
#from huffman import huffman
from huffman2 import Encoder
from huffman2 import Decoder

def flatten(lst):
    return sum( ([x] if not isinstance(x, list) else flatten(x) for x in lst), [] )

def letraANumero(letra, abecedario):
    return ord(letra)-ord(abecedario[0])

def numeroALetra(numero, abecedario):
    return chr(numero + ord(abecedario[0]))

def transformarADistancias(lista):
    nuevaLista = []
    for indice,item in enumerate(lista):
        if indice == 0:
            nuevaLista.append(lista[indice])
        else:
            nuevaLista.append(lista[indice] - lista[indice-1])

    return nuevaLista

def volverDeDistancias(lista):
    nuevaLista = []
    for indice,item in enumerate(lista):
        if indice == 0:
            nuevaLista.append(lista[indice])
        else:
            nuevaLista.append(lista[indice] + nuevaLista[indice-1])

    return nuevaLista


def comprimir(aComprimir):
    diccionario = {}
    nuevoDiccionario = {}
    abecedario = string.uppercase
    # Inicialización del abecedario (a)
    for letra in abecedario:
        diccionario[letra] = {
            'count' : 0,
            'pos'   : []
        }

    # 1) Recorro todo el archivo y armo el diccionario: letra: (cantidadDeApariciones, posiciones)
    for indice,letra in enumerate(aComprimir):
        if letra in diccionario:
            diccionario[letra]['count']+=1
            diccionario[letra]['pos'].append(indice)
        # el else sólo funciona si no está inicializado el archivo (en (a)), es una posible optimización que quizás empeora
        else:
            diccionario[letra] = {
                'count' : 1,
                'pos'   : [indice,]
            }

    for indice in diccionario:
        item = diccionario[indice]
        nuevoDiccionario[letraANumero(indice, abecedario)] = {
            'count' : item['count'],
            'pos' : transformarADistancias(item['pos']),
        }

    letras = []
    countpos = []
    for indice in nuevoDiccionario:
        item = nuevoDiccionario[indice]
        letras.append(indice)
        aux = item['pos']
        aux.insert(0,item['count'])
        countpos.append(aux)

    # huffman
    #print '$'.join( str(i) for i in flatten(countpos))
    enc = Encoder('$'.join( str(i) for i in flatten(countpos)))
    enc.write('comprimido.lalala')
    # /huffman

    return flatten(countpos)

def descomprimir(comprimido):
    abecedario = string.uppercase
    diccionario = {}
    for letra in abecedario:
        diccionario[letra] = {
            'count' : 0,
            'pos'   : []
        }

    countPos = []

    i = 0
    while i<len(comprimido):
        count = comprimido[i]
        pos = []
        i+=1
        j=i
        while j<i+int(count):
            pos.append(comprimido[j])
            j+=1

        pos = volverDeDistancias(pos)
        countPos.append({
            'count' : count,
            'pos'   : pos,
        })
        i = j

    casiFinal = {}
    for indice,item in enumerate(countPos):
        letra = numeroALetra(indice,abecedario)
        for pos in item['pos']:
            casiFinal[pos] = letra

    descomprimido = ''.join(casiFinal.values())

    return descomprimido

def main():
    aComprimir = 'ABCEASDFASDFASEKJAEOAFJPSJAFSDFASFAELFKASLDKFAOEKOFKOKAFSDLFKALSDKFLASKD'
    aComprimir = 'acomprimir.abc'
    aComprimir = open(aComprimir).read()
    aComprimir = aComprimir.replace('\n','')
    comprimido = comprimir(aComprimir)
    descomprimido = descomprimir(comprimido)

    #print "Entró %s\nSalió %s" % (aComprimir, descomprimido)
    # huffman
    dec = Decoder('comprimido.lalala')
    comprimido = dec._decode()
    comprimido = [int(i) for i in comprimido.split('$')]
    descomprimido = descomprimir(comprimido)

    if descomprimido == aComprimir:
        print 'yay'
    else:
        print descomprimido

    #print "Entró %s\nSalió %s" % (aComprimir, descomprimido)
    # /huffman

if __name__ == '__main__':
    main()

