# -*- coding: utf-8 -*-
import requests
import datetime
import time
import os
import sys
import json

class Imoveis(object):
    
    def __init__(self):
        self.args = sys.argv
        if 'localhost' in self.args:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
        self.inicio = time.time()
        self.URL_GET = self.URI + 'imoveis_integra/'
        self.argumentos = {}
        for a in self.args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = self.args.index(a)
                self.argumentos[cortado[1]] = self.args[posicao_e+1]
        self.set_acao()
        
        
    def set_acao(self):
        if 'a' in self.argumentos:
            func = getattr(Imoveis, '{}'.format(self.argumentos['a']))
            func(self)
        
    
    def integra_mongo(self):
        print('integra_mongo')
        return True
        #itens = requests.get(self.URL_GET,params=g)
        
    def filtro_padrao(self,data):
        
        
    
if __name__ == '__main__':
    Imoveis()
