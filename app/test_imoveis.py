# -*- coding: utf-8 -*-
### python -m unittest
import unittest
import random
import sys
import datetime
from imoveis import Imoveis
import time

class TestImoveis(unittest.TestCase):
    def setUp(self):
        self.imoveis = Imoveis()
        
    imovel = {
            "_id": 1679018, 
            "area": 55.51, 
            "area_terreno": 0.0, 
            "area_util": 46.61, 
            "bairro": "Rio Verde", 
            "bairro_cidade": 4, 
            "bairro_combo": 3862, 
            "bairros_link": "rio_verde", 
            "banheiros": "1", 
            "celular_corretor": None, 
            "cep": "83405-330", 
            "cidade": "Colombo", 
            "cidade_link": "colombo_pr", 
            "cidade_nome": "Colombo", 
            "cidades_id": 4, 
            "cidades_link": "colombo_pr", 
            "cobertura": "0", 
            "comercial": 0, 
            "condominio": "0", 
            "condominio_valor": "", 
            "creci": "J06127", 
            "data_atualizacao": 1545165671, 
            "ddd": 41, 
            "descricao": "Refer\u00eancia w0727\r\n\r\nMAIS UM LAN\u00c7AMENTO DE APARTAMENTOS NOVOS NO BAIRRO RIO VERDE EM COLOMBO \u2013 PR.\r\nPr\u00e9dio com 15 unidades de apartamentos novos\u2026\r\nContendo 09 unidades dispon\u00edveis,\r\nApartamentos com piso cer\u00e2micos na (sala, sacada, cozinha, lavanderia, banheiros e nos dois dormit\u00f3rios),\r\nAzulejos at\u00e9 o teto no (Banheiro, cozinha e lavanderia), Medidor de G\u00e1s Individual, Sal\u00e3o de Festas, e vagas de estacionamentos.\r\nPr\u00e9dio Em Excelente localiza\u00e7\u00e3o no bairro \u201cRio Verde\u201d, Colombo \u2013 PR,\r\npr\u00f3ximo de Escolas, Creches, linha de \u00f4nibus, Supermercados, comercio em geral.\r\n\r\nAPARTAMENTOS;\r\n\r\nSala\r\nSacada\r\nCozinha\r\n\u00c1rea de Servi\u00e7o conjugada\r\nBanheiro\r\n2 Dormit\u00f3rios\r\n1 vaga de estacionamento\r\nAPTO n\u00ba 101\r\n\u00c1rea Privativa de 46,61m\u00b2\r\n\r\n\u00c1rea Total de 55,51m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 149.000,00\r\n\r\nAPTO n\u00ba 201\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 159.000,00\r\n\r\nAPTO n\u00ba 202\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 159.000,00\r\n\r\nAPTO n\u00ba 203\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 157.000,00\r\n\r\nAPTO n\u00ba 204\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 157.000,00\r\n\r\nAPTO n\u00ba 303\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 157.000,00\r\n\r\nAPTO n\u00ba 401\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 159.000,00\r\n\r\nAPTO n\u00ba 402\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 159.000,00\r\n\r\nAPTO n\u00ba 403\r\n\u00c1rea Privativa de 49,31m\u00b2\r\n\r\n\u00c1rea Total de 58,20m\u00b2\r\n\r\nVaga de Estacionamento\r\n\r\nValor R$ 157.000,00\r\n\r\nIM\u00d3VEL NOVO, EM \u00d3TIMA LOCALIZA\u00c7\u00c3O,\r\nIm\u00f3vel permite financiamento.\r\nAproveite use seu FGTS.\r\nAgende j\u00e1 uma visita com um de nossos corretores\r\nMais informa\u00e7\u00f5es, ligue: (41) 3037-7500/3663-3666/99950-6500\r\n\r\nOs pre\u00e7os e condi\u00e7\u00f5es de pagamento s\u00e3o orientativos e poder\u00e3o sofrer altera\u00e7\u00f5es eventualmente,\r\nn\u00e3o refletindo \u00e0s condi\u00e7\u00f5es de pagamentos vigentes.\r\nA unidade apresentada poder\u00e1 tamb\u00e9m n\u00e3o estar mais dispon\u00edvel para venda.\r\nConsulte o corretor para obter informa\u00e7\u00f5es atualizadas.\r\nVenha Conferir, e Fa\u00e7a um Bom Neg\u00f3cio.\r\n\r\nW Batistel Im\u00f3veis Seguran\u00e7a e tranquilidade do In\u00edcio ao Fim!!!", 
            "destaque_bairro": 1, 
            "destaque_tipo": 1, 
            "email_corretor": "", 
            "empresa_email": "contato@wbatistel.com.br", 
            "empresa_telefone_sms": "4199950650", 
            "estado": "Paran\u00e1", 
            "garagens": "1", 
            "id": 1679018, 
            "id_cidade": 4, 
            "id_empresa": 83166, 
            "id_tipo": 1, 
            "images": [
              {
                "arquivo": "F_1679018_21222130.jpg", 
                "data": "2018-07-19T17:17:04Z", 
                "extensao": None, 
                "gerado_image": 0, 
                "id": 21222130, 
                "id_empresa": 83166, 
                "id_imovel": 1679018, 
                "ordem": 0, 
                "titulo": ""
              }, 
              {
                "arquivo": "F_1679018_21222131.jpg", 
                "data": "2018-07-19T17:17:53Z", 
                "extensao": None, 
                "gerado_image": 0, 
                "id": 21222131, 
                "id_empresa": 83166, 
                "id_imovel": 1679018, 
                "ordem": 1, 
                "titulo": ""
              }, 
              {
                "arquivo": "F_1679018_21222132.jpg", 
                "data": "2018-07-19T17:18:00Z", 
                "extensao": None, 
                "gerado_image": 0, 
                "id": 21222132, 
                "id_empresa": 83166, 
                "id_imovel": 1679018, 
                "ordem": 2, 
                "titulo": ""
              }, 
              {
                "arquivo": "F_1679018_21222133.jpg", 
                "data": "2018-07-19T17:17:04Z", 
                "extensao": None, 
                "gerado_image": 0, 
                "id": 21222133, 
                "id_empresa": 83166, 
                "id_imovel": 1679018, 
                "ordem": 23, 
                "titulo": ""
              }, 
              {
                "arquivo": "F_1679018_21222134.jpg", 
                "data": "2018-07-19T17:17:04Z", 
                "extensao": None, 
                "gerado_image": 0, 
                "id": 21222134, 
                "id_empresa": 83166, 
                "id_imovel": 1679018, 
                "ordem": 24, 
                "titulo": ""
              }, 
            ], 
            "imobiliaria_bairro": "Rio Verde", 
            "imobiliaria_cidade": "Colombo", 
            "imobiliaria_logradouro": "Avenida Londres", 
            "imobiliaria_nome": "WBatistel Corretor de Im\u00f3veis", 
            "imobiliaria_nome_seo": "WBatistel-Imoveis", 
            "imobiliaria_numero": "498", 
            "imobiliaria_telefone": "3037-7500", 
            "imobiliaria_whatsapp": "41999506500", 
            "imoveis_tipos_english": "Apartment", 
            "imoveis_tipos_id": 1, 
            "imoveis_tipos_link": "apartamento", 
            "imoveis_tipos_titulo": "Apartamento", 
            "imovel_id_cidade": 4, 
            "imovel_para": "venda", 
            "latitude": "-25.3735774", 
            "lazer": 0, 
            "locacao": 0, 
            "locacao_dia": 0, 
            "locacao_email": "", 
            "logo": "7319563975_logopeq.jpg", 
            "logradouro": "Travessa Chile", 
            "logradouro_": "Travessa Chile", 
            "longitude": "-49.198110199999974", 
            "mapa": "-25.3735774, -49.198110199999974", 
            "mobiliado": "0", 
            "mostramapa": 1, 
            "mudou": 1, 
            "nome": "Excelentes Apartamentos Novos no bairro Rio Verde em Colombo", 
            "nome_corretor": None, 
            "nome_empresa": "WBatistel Corretor de Im\u00f3veis", 
            "novo": "1", 
            "numero": "112", 
            "ordem": 3820444, 
            "pagina_limite_ofertas": 20, 
            "preco": 157000.0, 
            "preco_locacao": 0.0, 
            "preco_locacao_dia": 0.0, 
            "preco_venda": 157000.0, 
            "quartos": "2", 
            "referencia": "w0727", 
            "residencial": 1, 
            "situacao_link": "novo", 
            "situacao_titulo": "Novo", 
            "sms_corretor": None, 
            "sms_limite": 0, 
            "sms_quem": 0, 
            "status": "0-0-0-0", 
            "suites": "0", 
            "terreno": "0", 
            "tipo": "venda", 
            "tipo_locacao": 0, 
            "tipo_locacao_dia": 0, 
            "tipo_negocio": "venda", 
            "tipo_venda": 1, 
            "uf": "PR", 
            "uso": "Residencial", 
            "valores": "157000.00-0.00-0.00", 
            "venda": 1, 
            "video": "", 
            "views": 0, 
            "vila": ""
          }
        
            
            
    imovel_item = {}
    def test_set_pontos(self):
        imovel_item = self.imoveis.set_item(self.imovel)
        retorno = self.imoveis.set_pontos(imovel_item)
        self.assertTrue(self.imoveis.get_negativos() == 0)
    
    def test_set_pontos_s_image(self):
        imovel_item = self.imoveis.set_item(self.imovel)
        imovel_item['images'] = []
        retorno = self.imoveis.set_pontos(imovel_item)
        self.assertTrue(self.imoveis.get_negativos() == 5000)
        
    def test_set_pontos_s_image_preco(self):
        imovel_item = self.imoveis.set_item(self.imovel)
        imovel_item['preco'] = 0
        retorno = self.imoveis.set_pontos(imovel_item)
        self.assertTrue(self.imoveis.get_negativos() == 1000)
        
    def test_set_pontos_s_image_c_preco(self):
        imovel_item = self.imoveis.set_item(self.imovel)
        imovel_item['preco'] = 500
        retorno = self.imoveis.set_pontos(imovel_item)
        self.assertTrue(self.imoveis.get_negativos() == 0)
        
        
        
    
if __name__ == '__main__':
    unittest.main()# -*- coding: utf-8 -*-


