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
        self.URL_POST = self.URI + 'imoveis_integra/'
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
        else:
            self.integra_mongo()
        
    def integra_mongo(self):
        g = {}
        g['limit'] = 10
        itens = requests.get(self.URL_GET, params=g)
        if itens.status_code == 200:
            i = itens.json()
            for k,v in i.items():
                post = json.dumps(self.set_item(v))
                print(post)
                exit()
                res = requests.post(self.URL_POST,json=post)
                del post
                del res
        print('integra_mongo')
        return True
    
    imovel_ativo = {}
    
    def set_imovel(self,imovel):
        self.imovel_ativo = item
    
    def get_campo_imovel(self,campo):
        return self.imovel_ativo[campo]
    
    def set_item(self,item):
        self.set_imovel(item)
        if 'images' in item:
            item['images'] = self.set_image(item['images'])
        
        return item
    
    url_image = 'https://images.portaisimobiliarios.com.br/portais/'
    arquivo_formato = '{{id_empresa}}/{{id_imovel}}/destaque_{{id_imovel}}_{{id_image}}.{{extensao}}'
    
    def set_arquivo_destaque(image):
        arquivo = url_image + arquivo_formato
        arquivo.format(image['id_empresa'],image['id_imovel'],image['id_imovel'],image['id'],image['extensao'])
        return arquivo
    
    def get_image_nome(self,image, original):
        if 'http' in image['arquivo']:
            if original:
                return image['arquivo']
            else:
                if image['gerado_image'] == 1:
                    return self.set_arquivo_destaque(image)
                else:
                    return image['arquivo']
        else:
            return 'https://www.pow.com.br/powsites/{}/imo/650F_{}'.format(image['id_empresa'],image['arquivo'])
    
    def set_images(self,images):
        retorno = {}
        for k,v in images.items():
            retorno[k] = {}
            retorno[k]['arquivo'] = self.get_image_nome(v,False)
            retorno[k]['original'] = self.get_image_nome(v,True)
            retorno[k]['titulo'] = image['titulo']
            if image['titulo'] and image['titulo'].strip():
                retorno[k]['titulo'] = self.get_campo_imovel('nome')
            retorno[k]['id'] = image['id']
            retorno[k]['gerado_image'] = image['gerado_image'];
        return retorno
    
    
if __name__ == '__main__':
    Imoveis()
