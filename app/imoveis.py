# -*- coding: utf-8 -*-
import requests
import datetime
import time
import os
import sys
import json
import random


class Imoveis(object):
    
    def __init__(self):
        self.inicio = time.time()
        self.args = sys.argv
        if 'localhost' in self.args:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
        self.inicio = time.time()
        self.URL_GET = self.URI + 'imoveis_integra/'
        self.URL_GET_MONGO = self.URI + 'imoveismongo/'
        self.URL_POST = self.URI + 'imoveis_integra/'
        self.URL_PUT = self.URI + 'imovel/'
        self.URL_RELEVANCIA = self.URI + 'imoveis_relevancia/'
        self.URL_RELEVANCIA_LOG = self.URI + 'imoveis_relevancia_log/'
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
        g['limit'] = 150
        itens = requests.get(self.URL_GET, params=g)
        if itens.status_code == 200:
            i = itens.json()
            for k,v in i.items():
                post = self.set_item(v)
                print(post['_id'])
                res = requests.post(self.URL_POST,json=json.dumps(post))
                print(res.status_code)
                if res.status_code == 200:
                    self.post_relevancia(post['ordem'])
                else:
                    print('não foi possivel salvar ' + str(post['id']))
                    print(res.status_code)
                del post
                del res
        self.fim = time.time()
        print(self.fim-self.inicio)
        return True
    
    imovel_ativo = {}
    
    def set_item(self,item):
        self.set_imovel(item)
        self.set_gerado(True)
        if 'images' in item:
            item['images'] = self.set_images(item['images'])
        item['tem_foto'] = self.get_gerado()
        item['data_atualizacao'] = datetime.datetime.fromtimestamp(item['data_atualizacao']).strftime("%Y-%m-%d %H:%M")
        for f in self.var_float:
            if f in item and item[f] is not None:
                if len(str(item[f])) > 0:
                    item[f] = float(self.retira_string(item[f],'float'))
            else:
                item[f] = 0
        for i in self.var_int:
            print(item[i], i)
            if i in item and item[i] is not None:
                if str(item[i]).lower() in ['sim','não','nao','']:
                    item[i] = 1
                else:
                    print(item[i])
                    item[i] = int(self.retira_string(item[i],'int'))
            else:
                item[i] = 0
        item['imovel_para'] = []
        for k,p in self.var_para.items():
            if k in item and item[k]:
                item['imovel_para'].append(p)
        if 'longitude' in item and 'latitude' in item:
            item['location'] = [item['longitude'],item['latitude']]
        item['ordem'] = self.get_ordem(item)
        return item
    
    def retira_string(self,valor,tipo):
        retorno = '';
        if ( isinstance(valor,float) and tipo is 'float' ) or ( isinstance(valor,int) and tipo is 'int' ):
            return valor
        v = str(valor).strip()
        print("'"+v+"'")
        print(len(v))
        for i in range(len(v)):
            print(i, valor[i])
            if i in ['-','.',':'] or isinstance(int(valor[i]),int):
                retorno = retorno + str(valor[i])
        print(retorno)
        return retorno
    
    def set_imovel(self,imovel):
        self.imovel_ativo = imovel
    
    def get_campo_imovel(self,campo):
        return self.imovel_ativo[campo]
    
    faixas = [
            {'min':90001, 'max':100000},
            {'min':80001, 'max':90000},
            {'min':70001, 'max':80000},
            {'min':60001, 'max':70000},
            {'min':50001, 'max':60000},
            {'min':40001, 'max':50000},
            {'min':30001, 'max':40000},
            {'min':20001, 'max':30000},
            {'min':10001, 'max':20000},
            {'min':0, 'max':10000},
            ]
    valores_ordem = {
            'descricao': {'pontos':5000,'comparacao':'string'},
            'preco': {'pontos':10000,'comparacao':'not_0'},
            'cidades_id': {'pontos':10000,'comparacao':'not_0'},
            'images': {'pontos':10000,'comparacao':'count'},
            'imoveis_tipos_id': {'pontos':5000,'comparacao':'not_0'}
                     }
    negativos = 0
    
    def get_negativos(self, faixa):
        if faixa:
            base = 40002 - self.get_negativos(False)
            for k,v in self.faixas.items():
                if base >= v['min'] and base <= v['max']:
                    return k
        else:
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
                        self.set_negativos(v['pontos'])
                elif v['comparacao'] == 'not_0':
                    if item[k] == 0:
                        self.set_negativos(v['pontos'])
                elif v['comparacao'] == 'count':
                    if len(item[k]) == 0:
                        self.set_negativos(v['pontos'])
            else:
                self.set_negativos(v['pontos'])
    data_relevancia = {}
    
    def set_data_relevancia(self,item):
        self.data_relevancia = {'id_empresa':item['id_empresa'],'tipo_negocio':item['tipo'],'id_tipo':item['imoveis_tipos_id'],'id_cidade':item['cidades_id']}
    
    def get_data_relevancia(self):
        return self.data_relevancia
    
    def get_ordem(self,item):
        self.set_data_relevancia(item)
        relevancia = self.get_relevancia(self.get_data_relevancia())
        return relevancia
    
    def post_relevancia(self,ordem):
        data = self.get_data_relevancia()
        rel = requests.post(self.URL_RELEVANCIA, params=data)
        if rel.status_code is 200:
            print('\n salvou relevancia ' + str(data['id_empresa']))
        else:
            print('\n não salvou relevancia ' + str(data['id_empresa']))
        data['id_imovel'] = self.get_campo_imovel('id')
        data['ordem'] = ordem
        data['data'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        log = requests.post(self.URL_RELEVANCIA_LOG, params=data)
        if log.status_code is 200:
            print('\n salvou relevancia log ' + str(data['id_empresa']))
        else:
            print('\n não salvou relevancia log ' + str(data['id_empresa']))
        data_up = {}
        data_up['integra_mongo_db'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        upd = requests.put(self.URL_PUT + str(data['id_imovel']), params=data_up)
        
    
    def get_relevancia(self, data):
        itens = requests.get(self.URL_RELEVANCIA, params=data)
        qtde = itens.json()
        if qtde < 9:
            return random.randrange(self.faixas[qtde]['min'],self.faixas[qtde]['max'])
        else:
            return random.randrange(0,10000)
        
    var_float = ['preco_venda','preco_locacao', 'preco_locacao_dia', 'preco','area','area_terreno','area_util','latitude','longitude']
    var_int = ['quartos','garagens','banheiros','tipo_venda','tipo_locacao','tipo_locacao_dia','destaque_tipo','destaque_bairro','_id']
    var_para = {'tipo_venda':'venda','tipo_locacao':'locacao','tipo_locacao_dia':'locacao_dia'}
    gerado_image = True
    url_image = 'https://images.portaisimobiliarios.com.br/portais/'
    arquivo_formato = '{}/{}/destaque_{}_{}.{}'
    
    def set_arquivo_destaque(self, image):
        arquivo = self.url_image + self.arquivo_formato
        return arquivo.format(image['id_empresa'],image['id_imovel'],image['id_imovel'],image['id'],image['extensao'])
    
    def get_image_nome(self,image, original):
        if 'http' in image['arquivo']:
            if original:
                return image['arquivo']
            else:
                if image['gerado_image'] == 1:
                    return self.set_arquivo_destaque(image)
                else:
                    self.set_gerado(False)
                    return image['arquivo']
        else:
            return 'https://www.pow.com.br/powsites/{}/imo/650F_{}'.format(image['id_empresa'],image['arquivo'])
    
    def set_images(self,images):
        retorno = {}
        if len(images) > 0:
            for v in images:
                retorno[v['id']] = v
                retorno[v['id']]['arquivo'] = self.get_image_nome(v,False)
                retorno[v['id']]['original'] = self.get_image_nome(v,True)
                retorno[v['id']]['titulo'] = v['titulo']
                if v['titulo'] and v['titulo'].strip():
                    retorno[v['id']]['titulo'] = self.get_campo_imovel('nome')
                retorno[v['id']]['id'] = v['id']
                retorno[v['id']]['gerado_image'] = v['gerado_image']
        return retorno
    
    def set_gerado(self,status):
        self.gerado = status
        
    def get_gerado(self):
        return self.gerado
    
if __name__ == '__main__':
    Imoveis()
