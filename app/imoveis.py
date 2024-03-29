#############################################
# ############## POW INTERNET ############# #
# Controle de imóveis portais imobiliarios  #
# Acessa RESTAPIImoveis                     #
# Data 31.10.2019                           #
# Uso,                                      #
# tags: localhost                           #
# -verbose
# 
#
#
###########################################

# -*- coding: utf-8 -*-

import requests
import datetime
import time
import os
import sys
import json
import random
from requests.auth import HTTPBasicAuth

class Imoveis(object):
    
    def __init__(self):
        self.inicio = time.time()
        self.args = sys.argv
        endereco = '/var/www/json/keys.json'
        if 'localhost' in self.args:
            self.localhost = True
            self.URI = 'http://localhost:5000/'
        elif 'programacao' in self.args:
            self.localhost = True
            self.URI = 'http://172.20.0.2/'
            endereco = '../keys.json'
        else:
            self.localhost = False
            self.URI = 'http://imoveis.powempresas.com/'
        with open(endereco) as json_file:
            data = json.load(json_file)
        self.user = data['basic']['user']
        self.passwd = data['basic']['passwd']
        self.auth = HTTPBasicAuth(self.user,self.passwd)
        self.inicio = time.time()
        self.URL_GET = self.URI + 'imoveis_integra/'
        self.URL_GET_MONGO = self.URI + 'imoveismongo/'
        self.URL_POST = self.URI + 'imoveis_integra/'
        self.URL_PUT = self.URI + 'imovel/'
        self.URL_RELEVANCIA_DROP = self.URI + 'imovel_relevancia_drop/'
        self.URL_RELEVANCIA = self.URI + 'imoveis_relevancia/'
        self.URL_RELEVANCIA_LOG = self.URI + 'imoveis_relevancia_log/'
        self.ARQUIVO_LOG = '/var/log/sistema/integra_mongo.log'
        self.FORMATO_LOG = '{data} - status_code {status_code} - empresa {id_empresa} - id {id} - ordem {ordem} - funcao: {acao} - tempo: {tempo} '
        self.FORMATO_LOG_DADOS = '{data} - status_code {status_code} - qtde: {qtde} - funcao: {acao}_totais - tempo: {tempo} '
        self.FORMATO_LOG_RELEVANCIA = '{data} - status_code {status_code} - empresa {id_empresa} - id {id} - ordem {ordem} - funcao: {acao} - tempo: {tempo}'
        self.FORMATO_LOG_BUSCA = '{data} - status_code {status_code} - qtde: {qtde} - funcao: {acao} - tempo: {tempo}'
        self.argumentos = {}
        for a in self.args:
            if '-' in a:
                cortado = a.split('-')
                posicao_e = self.args.index(a)
                self.argumentos[cortado[1]] = self.args[posicao_e+1]
        self.set_acao()
        
    # arquivo = log, dados, relevancia
    def set_log(self, data, arquivo):
        if 'dados' in arquivo:
            linha = self.FORMATO_LOG_DADOS.format(**data)
        elif 'relevancia' in arquivo:
            linha = self.FORMATO_LOG_RELEVANCIA.format(**data)
        elif 'busca' in arquivo:
            linha = self.FORMATO_LOG_BUSCA.format(**data)
        else:
            linha = self.FORMATO_LOG.format(**data)
        with open(self.ARQUIVO_LOG,'a') as arq:
            arq.write(linha)
            arq.write('\r\n')

    def set_acao(self):
        if 'python -m unittest' not in self.args:
            if 'a' in self.argumentos:
                func = getattr(Imoveis, '{}'.format(self.argumentos['a']))
                func(self)
            else:
                self.integra_mongo()
        
    def drop_relevancia(self):
        return True
        
    def integra_mongo(self):
        g = {}
        g['limit'] = 200
        if 'qtde' in self.argumentos:
            g['limit'] = self.argumentos['qtde']
        if 'id_empresa' in self.argumentos:
            g['id_empresa'] = self.argumentos['id_empresa']
        data_log_dados = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'acao':'integra_mongo','qtde':0}
        
        inicio_query = time.time()
        try:
            itens = requests.get(self.URL_GET, params=g, auth=self.auth)
            status_code = itens.status_code
        except requests.exceptions.HTTPError as errh:
            status_code = 403
            if 'verbose' in self.argumentos:
                print("Http Error:",errh)
            pass
        except requests.exceptions.ConnectionError as errc:
            status_code = 401
            if 'verbose' in self.argumentos:
                print("Error Connecting:",errc)
            pass
        except requests.exceptions.Timeout as errt:
            status_code = 408
            if 'verbose' in self.argumentos:
                print("Timeout Error:",errt)
            pass
        except requests.exceptions.RequestException as err:
            status_code = 400
            if 'verbose' in self.argumentos:
                print("OOps: Something Else",err)
            pass
        except:
            status_code = 500
            print("OOps: Something Else")
            pass
        fim_query = time.time()
        tempo_query = fim_query - inicio_query
        data_query = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'acao':'query_mysql','qtde':g['limit'], 'status_code':status_code, 'tempo':tempo_query}
        self.set_log(data_query, 'busca')
        data_log_dados['status_code'] = status_code
        if status_code == 200:
            i = itens.json()
            data_log_dados['qtde'] = len(i)
            if len(i) > 0:
                self.processa_itens(i)
        self.fim = time.time()
        data_log_dados['tempo'] = self.fim-self.inicio
        self.set_log(data_log_dados, 'dados')

    
    imovel_ativo = {}
    
    def processa_itens(self,itens):
        for k,v in itens.items():
            data_log = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'acao':'item_mongo','ordem':0,'id':v['id'],'id_empresa':v['id_empresa']}
            tempo_i = time.time()
            post = self.set_item(v)
            data_log['ordem'] = post['ordem']
            try:
                inicio_post = time.time()
                res = requests.post(self.URL_POST,json=json.dumps(post), auth=self.auth)
                status_code = res.status_code
                fim_post = time.time()
                tempo_post = fim_post-inicio_post
                data_log_ = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status_code':status_code, 'acao':'post_item','ordem':0,'id':v['id'],'id_empresa':v['id_empresa'], 'tempo': tempo_post}
                if 'completo' in self.argumentos:
                    self.set_log(data_log_,'log')
            except:
                status_code = 500
            data_log['status_code'] = status_code
            if status_code == 200:
                inicio_post_re = time.time()
                self.post_relevancia(post['ordem'])
                fim_post_re = time.time()
                tempo_post_re = fim_post_re-inicio_post_re
                data_log_re = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status_code':0, 'acao':'post_relevancia','ordem':0,'id':v['id'],'id_empresa':v['id_empresa'], 'tempo': tempo_post_re}
                if 'completo' in self.argumentos:
                    self.set_log(data_log_re,'log')
            del post
            del res
            tempo_f = time.time()
            data_log['tempo'] = tempo_f - tempo_i
            del tempo_i, tempo_f
            self.set_log(data_log, 'log')
            
    
    def set_item(self,item):
        inicio_set_item = time.time()
        self.set_imovel(item)
        self.set_gerado(True)
        if 'images' in item:
            item['images'] = self.set_images(item['images'])
        item['tem_foto'] = self.get_gerado()
        item['data_atualizacao'] = datetime.datetime.fromtimestamp(item['data_atualizacao']).strftime("%Y-%m-%d %H:%M")
        for f in self.var_float:
            if f in item and item[f] is not None:
                if len(str(item[f])) > 0:
                    item[f] = float(item[f])
            else:
                item[f] = 0
        for f in self.var_latitude:
            if f in item and item[f]:
                try:
                    item[f] = float(self.retira_string(item[f],'float'))
                except:
                    item[f] = None
            else:
                item[f] = None
        for i in self.var_int:
            if i in item and item[i] is not None:
                if str(item[i]).strip().lower() in ['sim','não','nao','','N','S']:
                    item[i] = 1
                else:
                    item[i] = int(self.retira_string(item[i],'int'))
            else:
                item[i] = 0
        item['imovel_para'] = []
        for k,p in self.var_para.items():
            if k in item and item[k]:
                item['imovel_para'].append(p)
        if 'longitude' in item and 'latitude' in item:
            item['location'] = [item['longitude'],item['latitude']]
        item['id_empresa'] = str(item['id_empresa'])
        item['id'] = str(item['id'])
        item['ordem'] = self.get_ordem(item)
        item['integra'] = 'python'
        fim_set_item = time.time()
        tempo_set_item = fim_set_item-inicio_set_item
        data_log = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status_code':200, 'acao':'set_item','ordem':item['ordem'],'id':item['id'],'id_empresa':item['id_empresa'], 'tempo': tempo_set_item}
        if 'completo' in self.argumentos:
            self.set_log(data_log,'log')
        
        return item
    
    def retira_string(self,valor,tipo):
        if ( isinstance(valor,float) and tipo == 'float' ) or ( isinstance(valor,int) and tipo == 'int' ):
            return valor
        v = str(valor).strip()
        alfa = 'abcdefghijklmnopqrstuvyxz ABCDEFGHIJKLMNOPQRSTUVYXZçã/,'
        for a in alfa:
            if a in v:
                v = v.replace(a,'')
        if len(v) == 0:
            v = 0
        return v
    
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
                    if not isinstance(item[k],str) or item[k] == '':
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
        inicio_time_relevancia = time.time()
        try:
            rel = requests.post(self.URL_RELEVANCIA, params=data, auth=self.auth)
            status_code = rel.status_code
        except:
            status_code = 500
        data_log_r = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'acao':'relevancia','ordem':ordem,'id':self.get_campo_imovel('id'),'id_empresa':self.get_campo_imovel('id_empresa')}
        data_log_r['status_code'] = status_code
        fim_time_relevancia = time.time()
        data_log_r['tempo'] = fim_time_relevancia-inicio_time_relevancia
        if 'completo' in self.argumentos:
            self.set_log(data_log_r, 'relevancia')
        if status_code == 200:
            data['id_imovel'] = self.get_campo_imovel('id')
            data['ordem'] = ordem
            data['data'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            try:
                inicio_post = time.time()
                log = requests.post(self.URL_RELEVANCIA_LOG, params=data, auth=self.auth)
                fim_post = time.time()
                tempo_post = fim_post-inicio_post
                data_log_ = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status_code':status_code, 'acao':'post_relevancia_log','ordem':data['ordem'],'id':data['id_imovel'],'id_empresa':data['id_empresa'], 'tempo': tempo_post}
                if 'completo' in self.argumentos:
                    self.set_log(data_log_,'log')
            except:
                pass
            data_up = {}
            data_up['integra_mongo_db'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            try:
                inicio_put = time.time()
                upd = requests.put(self.URL_PUT + str(data['id_imovel']), params=data_up, auth=self.auth)
                status_code_up = rel.status_code
                fim_put = time.time()
                tempo_put = fim_put-inicio_put
                data_log_put = {'data':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'status_code':status_code_up, 'acao':'put_','ordem':data['ordem'],'id':data['id_imovel'],'id_empresa':data['id_empresa'], 'tempo': tempo_put}
                if 'completo' in self.argumentos:
                    self.set_log(data_log_put,'log')
            except:
                status_code_up = 500
            data_log_r['status_code'] = status_code_up
            data_log_r['acao'] = 'updateMySQL'
            if 'completo' in self.argumentos:
                self.set_log(data_log_r, 'relevancia')
            

    def get_relevancia(self, data):
        itens = requests.get(self.URL_RELEVANCIA, params=data, auth=self.auth)
        qtde = itens.json()
        if qtde < 9:
            return random.randrange(self.faixas[qtde]['min'],self.faixas[qtde]['max'])
        else:
            return random.randrange(0,10000)
        
    var_latitude = ['latitude','longitude']
    var_float = ['preco_venda','preco_locacao', 'preco_locacao_dia', 'preco','area','area_terreno','area_util']
    var_int = ['quartos','garagens','banheiros','tipo_venda','tipo_locacao','tipo_locacao_dia','destaque_tipo','destaque_bairro','_id']
    var_para = {'tipo_venda':'venda','tipo_locacao':'locacao','tipo_locacao_dia':'locacao_dia'}
    gerado_image = True
    url_image = 'https://images.portaisimobiliarios.com.br/portais/'
    arquivo_formato = '{}/{}/destaque_{}_{}.{}'
    
    def set_arquivo_destaque(self, image):
        arquivo = self.url_image + self.arquivo_formato
        return arquivo.format(image['id_empresa'],image['id_imovel'],image['id_imovel'],image['id'],image['extensao'])
    
    def get_image_nome(self,image, original,qtde, total):
        if 'http' in image['arquivo']:
            if original:
                return image['arquivo']
            else:
                if image['gerado_image'] == 1:
                    return self.set_arquivo_destaque(image)
                elif image['gerado_image'] == 0:
                    self.set_gerado(False)
                    return image['arquivo']
                else:
                    return image['arquivo']
        else:
            return 'https://www.pow.com.br/powsites/{}/imo/{}/650F_{}'.format(image['id_empresa'],image['id_imovel'],image['arquivo'])
    
    def set_images(self,images):
        retorno = []
        gerado = 0
        total_images = len(images)
        if total_images > 0:
            for v in images:
                gerado = gerado + 1
                y = v
                imovel = {}
                imovel = y
                imovel['original'] = self.get_image_nome(y,True,gerado, total_images)
                imovel['arquivo'] = self.get_image_nome(y,False,gerado, total_images)
                imovel['titulo'] = y['titulo']
                if y['titulo'] and y['titulo'].strip():
                    imovel['titulo'] = self.get_campo_imovel('nome')
                imovel['id'] = y['id']
                imovel['gerado_image'] = y['gerado_image']
                retorno.append(imovel)
                del imovel
        return retorno
    
    def set_gerado(self,status):
        self.gerado = status
        
    def get_gerado(self):
        return self.gerado
    
if __name__ == '__main__':
    Imoveis()
