import json
import os

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.altura = 1.98
        self.time = "Los Angeles Lakers"
        self.ano_inicio = 2025
        self.posicao = "PG"  # Valor padrão, será sobrescrito
        self.posicao_secundaria = None
        self.historico_posicoes = []
        self.atributos = {}
        self.estatisticas = {"Pontos": 0, "Assistências": 0, "Rebotes": 0, "Steal": 0, "Block": 0, "Turnover": 0}
        self.pontos_disponiveis = 0
        self.pontos_premios = 1000
        # Atualização dos custos dos atributos com os novos intervalos e valores
        self.custos_atributos = {
            "0-69": 100,
            "70-74": 150,
            "75-79": 200,
            "80-84": 250,
            "85-89": 300,
            "90-94": 400,
            "95-99": 500
        }
        self.dificuldade = {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 15, "Block": 15, "Turnover": -5}
        self.pontos_premios_personalizados = {}
        self.posicoes_compradas_primarias = []  # Inicializa como lista vazia
        self.posicoes_compradas_secundarias = []

    # O restante do código (métodos adicionar_estatisticas, salvar e carregar) permanece igual
    def adicionar_estatisticas(self, pontos, assistencias, rebotes, steals, blocks, turnovers):
        self.estatisticas["Pontos"] += pontos
        self.estatisticas["Assistências"] += assistencias
        self.estatisticas["Rebotes"] += rebotes
        self.estatisticas["Steal"] += steals
        self.estatisticas["Block"] += blocks
        self.estatisticas["Turnover"] += turnovers

    def salvar(self):
        data = {
            "nome": self.nome,
            "altura": self.altura,
            "time": self.time,
            "ano_inicio": self.ano_inicio,
            "posicao": self.posicao,
            "posicao_secundaria": self.posicao_secundaria,
            "historico_posicoes": self.historico_posicoes,
            "atributos": self.atributos,
            "estatisticas": self.estatisticas,
            "pontos_disponiveis": self.pontos_disponiveis,
            "pontos_premios": self.pontos_premios,
            "custos_atributos": self.custos_atributos,
            "dificuldade": self.dificuldade,
            "pontos_premios_personalizados": self.pontos_premios_personalizados,
            "posicoes_compradas_primarias": self.posicoes_compradas_primarias,
            "posicoes_compradas_secundarias": self.posicoes_compradas_secundarias
        }
        if not os.path.exists("dados"):
            os.makedirs("dados")
        with open(f"dados/{self.nome}.json", "w") as f:
            json.dump(data, f, indent=4)

    def carregar(self, arquivo):
        with open(arquivo, "r") as f:
            data = json.load(f)
            print(f"Carregando jogador {self.nome} - posicoes_compradas_primarias: {data.get('posicoes_compradas_primarias', [])}")  # Depuração
            self.nome = data["nome"]
            self.altura = data["altura"]
            self.time = data.get("time", "Los Angeles Lakers")
            self.ano_inicio = data.get("ano_inicio", 2025)
            self.posicao = data["posicao"]
            self.posicao_secundaria = data.get("posicao_secundaria", None)
            self.historico_posicoes = data["historico_posicoes"]
            self.atributos = data["atributos"]
            self.estatisticas = data["estatisticas"]
            self.pontos_disponiveis = data["pontos_disponiveis"]
            self.pontos_premios = data.get("pontos_premios", 1000)
            self.custos_atributos = data.get("custos_atributos", {
                "0-69": 100,
                "70-74": 150,
                "75-79": 200,
                "80-84": 250,
                "85-89": 300,
                "90-94": 400,
                "95-99": 500
            })
            self.dificuldade = data.get("dificuldade", {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 15, "Block": 15, "Turnover": -5})
            self.pontos_premios_personalizados = data.get("pontos_premios_personalizados", {})
            self.posicoes_compradas_primarias = data.get("posicoes_compradas_primarias", [])
            self.posicoes_compradas_secundarias = data.get("posicoes_compradas_secundarias", [])