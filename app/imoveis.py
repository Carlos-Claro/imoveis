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
        self.URL_RELEVANCIA = self.URI + 'imoveis_relevancia'
        self.URL_RELEVANCIA_LOG = self.URI + 'imoveis_relevancia_log'
        self.argumentos = {}
        for a in self.args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = self.args.index(a)
                self.argumentos[cortado[1]] = self.args[posicao_e+1]
        self.set_acao()
        
        
    def set_acao(self):
        if 'python -m unittest' not in self.args:
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
        return True
    
    imovel_ativo = {}
    
    def set_imovel(self,imovel):
        self.imovel_ativo = imovel
    
    def get_campo_imovel(self,campo):
        return self.imovel_ativo[campo]
    
    pontos = {
            'max':50000
            ,'faixa1':40000
            ,'faixa2':30000
            ,'faixa3':20000}
    valores_ordem = {
            'descricao': {'pontos':1000,'comparacao':'string'},
            'preco': {'pontos':1000,'comparacao':'not_0'},
            'cidades_id': {'pontos':5000,'comparacao':'not_0'},
            'images': {'pontos':5000,'comparacao':'count'},
            'imoveis_tipos_id': {'pontos':1000,'comparacao':'not_0'}
                     }
    negativos = 0
    
    def get_negativos(self):
        return self.negativos
    
    def set_negativos(self,pontos):
        if pontos == 0:
            self.negativos = 0
        else:
            self.negativos = self.negativos + pontos
    
    def set_pontos(self,item):
        self.set_negativos(0)
        for k,v in self.valores_ordem.items():
            if k in item:
                if v['comparacao'] == 'string':
                    if not isinstance(item[k],str) or item[k] is '':
                        self.negativos = self.set_negativos(v['pontos'])
                elif v['comparacao'] == 'not_0':
                    if item[k] == 0:
                        self.negativos = self.set_negativos(v['pontos'])
                elif v['comparacao'] == 'count':
                    if len(item[k]) == 0:
                        self.negativos = self.set_negativos(v['pontos'])
            else:
                print(k)
                self.negativos = self.set_negativos(v['pontos'])
    
    
    def get_ordem(self,item):
        return item
        
        
    var_float = ['preco_venda','preco_locacao', 'preco_locacao_dia', 'preco','area','area_terreno','area_util','latitude','longitude']
    var_int = ['quartos','garagens','banheiros','tipo_venda','tipo_locacao','tipo_locacao_dia','destaque_tipo','destaque_bairro','_id']
    var_para = {'tipo_venda':'venda','tipo_locacao':'locacao','tipo_locacao_dia':'locacao_dia'}
    gerado_image = True
    
    def set_item(self,item):
        self.set_imovel(item)
        self.gerado = True
        if 'images' in item:
            item['images'] = self.set_images(item['images'])
        item['tem_foto'] = self.gerado_image
        item['data_atualizacao'] = datetime.datetime.fromtimestamp(item['data_atualizacao']).strftime("%Y-%m-%d %H:%M")
        item['data_update'] = datetime.datetime.now()
        for f in self.var_float:
            if f in item:
                item[f] = float(item[f])
        for i in self.var_int:
            if i in item:
                item[i] = int(item[i])
        item['imovel_para'] = []
        for k,p in self.var_para.items():
            if k in item and item[k]:
                item['imovel_para'].append(p)
        if 'longitude' in item and 'latitude' in item:
            item['location'] = [item['longitude'],item['latitude']]
        #item['ordem'] = self.get_ordem(item)
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
                    self.gerado_image = False
                    return image['arquivo']
        else:
            return 'https://www.pow.com.br/powsites/{}/imo/650F_{}'.format(image['id_empresa'],image['arquivo'])
    
    def set_images(self,images):
        retorno = {}
        for v in images:
            print(v)
            retorno[v['id']] = {}
            retorno[v['id']]['arquivo'] = self.get_image_nome(v,False)
            retorno[v['id']]['original'] = self.get_image_nome(v,True)
            retorno[v['id']]['titulo'] = v['titulo']
            if v['titulo'] and v['titulo'].strip():
                retorno[v['id']]['titulo'] = self.get_campo_imovel('nome')
            retorno[v['id']]['id'] = v['id']
            retorno[v['id']]['gerado_image'] = v['gerado_image'];
        return retorno
    
    
if __name__ == '__main__':
    Imoveis()
