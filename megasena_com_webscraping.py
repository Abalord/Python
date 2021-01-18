# Importando as bibliotecas
from random import sample
import pandas as pd
import cfscrape
from bs4 import BeautifulSoup
from lxml import etree

def main():
    
    class MegaSena:

        def __init__(self, dezenas, totalJogos):

            if dezenas >= 6 and dezenas <= 10:
                self.__dezenas = dezenas
            else:
                print("Erro: insira a dezena entre 6, 7, 8, 9 ou 10")

            self.__totalJogos = totalJogos
            self.__resultado = None
            self.__Jogos = None

        @property
        def dezenas(self):
            return self.__dezenas

        @dezenas.setter
        def dezenas(self, value):
            if value >= 6 and value <= 10:
                self.__dezenas = value
            else:
                print("Erro: insira a dezena entre 6, 7, 8, 9 ou 10")

        @property
        def resultado(self):
            return self.__resultado

        @resultado.setter
        def resultado(self, value):
            self.__resultado = value

        @property
        def totalJogos(self):
            return self.__totalJogos

        @totalJogos.setter
        def totalJogos(self, value):
            self.__totalJogos = value

        @property
        def Jogos(self):
            return self.__Jogos

        @Jogos.setter
        def Jogos(self, value):
            self.__Jogos = value

        def __Sample(self):
            dez = self.__dezenas
            sorteados = sorted(sample(range(1, 61), dez), key=int)
            return sorteados

        def sorteio(self):
            return self.__Sample()

        def fazerJogos(self):
            total_jogos = self.__totalJogos
            jogo = []
            for i in range(0,total_jogos):
                jogo.append(self.sorteio())
            self.__Jogos = jogo

        def conferirNumeros(self):
            pagina = "https://www.google.com/search?q=caixa+mega+sena"
            scraper = cfscrape.create_scraper()
            url = pagina
            result = scraper.get(url)
            soup = BeautifulSoup(result.content, 'html.parser')
            t = soup.find(class_='MDTDab').text
            numeros_sorteados = [int(t[0:2]),int(t[2:4]),int(t[4:6]),int(t[6:8]),int(t[8:10]),int(t[10:12])]
            
            nossosNumeros = self.__Jogos
            df = pd.DataFrame()
            resultado = numeros_sorteados
            jogo_n = []
            numeros = []
            resultado_sorteo = []
            qnt_acertos = []
            numeros_sorteados = []

            for i in range(0,len(nossosNumeros)):
                jogo_n.append(i+1)
                numeros.append(str(nossosNumeros[i]).strip('[]'))
                resultado_sorteo.append(str(resultado).strip('[]'))
                qnt_acertos.append(len(set(nossosNumeros[i]).intersection(resultado)))
                numeros_sorteados.append(0 if str(list(set(nossosNumeros[i]).intersection(resultado))).strip('[]') == '' else \
                                         str(list(set(nossosNumeros[i]).intersection(resultado))).strip('[]'))

            df['Jogo Nº'] = jogo_n
            df['Meus números'] = numeros
            df['Dezenas Sorteadas'] = resultado_sorteo
            df['Quantidade de acertos'] = qnt_acertos
            df['Meus números sorteados'] = numeros_sorteados
            return df

    dezenas = int(input("Insira a quantidade de dezenas: ")) # Inserindo a quantidade de dezenas
    
    while dezenas < 6 or dezenas > 10:
        print("\n")
        print("Insira um número entra 6 a 10")
        dezenas = int(input("Insira a quantidade de dezenas: "))
    else:
        pass
    
    totalJogos = int(input("Insira a quantidade total de jogos: ")) # Inserindo o total de jogos
    print("\n")
    
    MegaSena = MegaSena(dezenas, totalJogos) # Criando o nosso objeto
    
    operacao = int(input("Seleciona a opção:\n\
            1 -> Fazer Jogos \n\
            2 -> Ver números do último concurso da Mega Sena \n\
            3 -> Conferir resultados \n\
            4 -> Sair \n"))

    # Opções para navegar no programa    
    while operacao != 4:

        if operacao == 1:
            MegaSena.fazerJogos()
            print("Seus números")
            print(MegaSena.Jogos)
            print("\n")
            operacao = int(input("Seleciona a opção:\n\
            1 -> Fazer Jogos \n\
            2 -> Ver números do último concurso da Mega Sena \n\
            3 -> Conferir resultados \n\
            4 -> Sair \n"))

        elif operacao == 2:
            
            pagina = "https://www.google.com/search?q=caixa+mega+sena"
            scraper = cfscrape.create_scraper()
            url = pagina
            result = scraper.get(url)
            soup = BeautifulSoup(result.content, 'html.parser')
            t = soup.find(class_='MDTDab').text
            numeros_sorteados = [int(t[0:2]),int(t[2:4]),int(t[4:6]),int(t[6:8]),int(t[8:10]),int(t[10:12])]
            
            print("Números Mega Sena do último concurso")
            print(numeros_sorteados)
            print("\n")
            operacao = int(input("Seleciona a opção:\n\
            1 -> Fazer Jogos \n\
            2 -> Ver números do último concurso da Mega Sena \n\
            3 -> Conferir resultados \n\
            4 -> Sair \n"))
        
        elif operacao == 3:
            print("Resultado")
            print(MegaSena.conferirNumeros())
            operacao = 4            
            
    print("Obrigado!")


if __name__ == "__main__":
    main()