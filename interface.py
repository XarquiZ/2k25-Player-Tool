import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QGroupBox, QSpacerItem,
                             QComboBox, QPushButton, QFrame, QScrollArea, QProgressBar, QMessageBox, QSizePolicy,QSlider, QListWidget, QSpinBox, QGridLayout, QDialog, QRadioButton, QListWidgetItem,)
from PyQt5.QtGui import QPixmap, QFont, QIntValidator
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from jogador import Jogador


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBA 2K25 - Menu Principal")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.jogador_atual = None  # Para rastrear o jogador carregado ou criado
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title = QLabel("NBA 2K25 - MyCareer")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Nome do jogador
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do Jogador")
        self.nome_input.setFont(QFont("Segoe UI", 16))
        self.nome_input.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.nome_input)

        # Altura (5'5" a 7'7")
        altura_layout = QHBoxLayout()
        altura_label = QLabel("Altura:")
        altura_label.setFont(QFont("Segoe UI", 16))
        altura_label.setStyleSheet("color: #FFFFFF;")
        self.altura_combo = QComboBox()
        alturas = ["Selecione a altura"] + [f"{feet}'{inches}\"" for feet in range(5, 8) for inches in range(12) if (feet == 5 and inches >= 5) or (feet == 7 and inches <= 7) or (feet == 6)]
        self.altura_combo.addItems(alturas)
        self.altura_combo.setCurrentIndex(0)  # Define o placeholder como padrão
        self.altura_combo.setFont(QFont("Segoe UI", 16))
        self.altura_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        altura_layout.addWidget(altura_label)
        altura_layout.addWidget(self.altura_combo)
        layout.addLayout(altura_layout)

        # Posição Primária
        posicao_layout = QHBoxLayout()
        posicao_label = QLabel("Posição:")
        posicao_label.setFont(QFont("Segoe UI", 16))
        posicao_label.setStyleSheet("color: #FFFFFF;")
        self.posicao_combo = QComboBox()
        posicoes = ["Selecione a posição"] + ["PG", "SG", "SF", "PF", "C"]
        self.posicao_combo.addItems(posicoes)
        self.posicao_combo.setCurrentIndex(0)  # Define o placeholder como padrão
        self.posicao_combo.setFont(QFont("Segoe UI", 16))
        self.posicao_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        posicao_layout.addWidget(posicao_label)
        posicao_layout.addWidget(self.posicao_combo)
        layout.addLayout(posicao_layout)

        # Time do jogador
        time_layout = QHBoxLayout()
        time_label = QLabel("Time:")
        time_label.setFont(QFont("Segoe UI", 16))
        time_label.setStyleSheet("color: #FFFFFF;")
        self.time_combo = QComboBox()
        times_nba = ["Selecione o time"] + [
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
            "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
            "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
            "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
            "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
            "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
            "Utah Jazz", "Washington Wizards"
        ]
        self.time_combo.addItems(times_nba)
        self.time_combo.setCurrentIndex(0)  # Define o placeholder como padrão
        self.time_combo.setFont(QFont("Segoe UI", 16))
        self.time_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        layout.addLayout(time_layout)

        # Ano de início (1970 a 2130) com QComboBox e barra deslizante
        ano_layout = QHBoxLayout()
        ano_label = QLabel("Ano de Início:")
        ano_label.setFont(QFont("Segoe UI", 16))
        ano_label.setStyleSheet("color: #FFFFFF;")
        self.ano_combo = QComboBox()
        anos = ["Selecione o ano"] + [str(ano) for ano in range(1970, 2131)]
        self.ano_combo.addItems(anos)
        self.ano_combo.setCurrentIndex(0)  # Define o placeholder como padrão
        self.ano_combo.setFont(QFont("Segoe UI", 16))
        self.ano_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        self.ano_combo.setMaxVisibleItems(10)  # Limita a 10 itens visíveis, adicionando barra deslizante
        ano_layout.addWidget(ano_label)
        ano_layout.addWidget(self.ano_combo)
        layout.addLayout(ano_layout)

        # Botão Criar Jogador
        criar_button = QPushButton("Criar Jogador")
        criar_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        criar_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        criar_button.clicked.connect(self.criar_jogador)
        layout.addWidget(criar_button)

        # Botão Carregar Jogador
        carregar_button = QPushButton("Carregar Jogador")
        carregar_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        carregar_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        carregar_button.clicked.connect(self.abrir_carregar_jogador)
        layout.addWidget(carregar_button)

        # Botão Excluir Jogador
        excluir_button = QPushButton("Excluir Jogador")
        excluir_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        excluir_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        excluir_button.clicked.connect(self.abrir_excluir_jogador)
        layout.addWidget(excluir_button)

        layout.addStretch()

    def criar_jogador(self):
        nome = self.nome_input.text().strip()
        if not nome:
            self.show_error("Por favor, insira um nome para o jogador!")
            return

        # Validação da altura
        altura_str = self.altura_combo.currentText()
        if altura_str == "Selecione a altura":
            self.show_error("Por favor, selecione uma altura válida!")
            return
        feet, inches = map(int, altura_str.replace('"', '').split("'"))
        altura_metros = (feet * 12 + inches) * 0.0254

        # Validação da posição
        posicao = self.posicao_combo.currentText()
        if posicao == "Selecione a posição":
            self.show_error("Por favor, selecione uma posição válida!")
            return

        # Validação do time
        time = self.time_combo.currentText()
        if time == "Selecione o time":
            self.show_error("Por favor, selecione um time válido!")
            return

        # Validação do ano
        ano_str = self.ano_combo.currentText()
        if ano_str == "Selecione o ano":
            self.show_error("Por favor, selecione um ano válido!")
            return
        ano = int(ano_str)

        jogador = Jogador(nome)
        jogador.altura = altura_metros
        jogador.posicao = posicao
        jogador.posicoes_compradas_primarias = [posicao]  # Posição inicial é comprada automaticamente
        jogador.posicoes_compradas_secundarias = []  # Inicializa vazio
        jogador.posicao_secundaria = None
        jogador.time = time
        jogador.ano_inicio = ano
        jogador.historico_posicoes = [(posicao, 0, ano)]
        print(f"MainWindow - Criando jogador: Posição: {jogador.posicao}, Posições compradas primárias: {jogador.posicoes_compradas_primarias}, Ano: {jogador.ano_inicio}")
        jogador.salvar()
        self.jogador_atual = jogador

        self.atributos_window = AtributosWindow(jogador, self)
        self.atributos_window.show()
        self.hide()

    def abrir_carregar_jogador(self):
        dialog = GerenciarJogadoresWindow(self, modo="carregar")
        if dialog.exec_():
            arquivo = dialog.get_selected_file()
            if arquivo:
                try:
                    jogador = Jogador("Temp")
                    jogador.carregar(arquivo)
                    self.jogador_atual = jogador
                    self.player_window = PlayerWindow(jogador, self)
                    self.player_window.show()
                    self.hide()
                except Exception as e:
                    self.show_error(f"Erro ao carregar jogador: {str(e)}")

    def abrir_excluir_jogador(self):
        dialog = GerenciarJogadoresWindow(self, modo="excluir")
        if dialog.exec_():
            arquivo = dialog.get_selected_file()
            if arquivo:
                resposta = QMessageBox.question(
                    self,
                    "Confirmar Exclusão",
                    f"Tem certeza que deseja excluir o jogador '{os.path.basename(arquivo)}'? Esta ação não pode ser desfeita.",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if resposta == QMessageBox.Yes:
                    try:
                        os.remove(arquivo)
                        self.show_success(f"Jogador '{os.path.basename(arquivo)}' excluído com sucesso!")
                        if self.jogador_atual and os.path.basename(arquivo) == f"{self.jogador_atual.nome}.json":
                            self.jogador_atual = None
                    except Exception as e:
                        self.show_error(f"Erro ao excluir jogador: {str(e)}")

    def atualizar_jogador(self):
        if self.jogador_atual:
            self.jogador_atual.carregar(f"dados/{self.jogador_atual.nome}.json")

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

class GerenciarJogadoresWindow(QDialog):
    def __init__(self, parent, modo="carregar"):
        super().__init__(parent)
        self.modo = modo  # "carregar" ou "excluir"
        self.setWindowTitle("Carregar Jogador" if modo == "carregar" else "Excluir Jogador")
        self.setFixedSize(500, 400)  # Aumentado para caber mais informações
        self.setStyleSheet("background-color: #1A1A1A;")
        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        title = QLabel("Carregar Jogador" if self.modo == "carregar" else "Excluir Jogador")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.jogadores_list = QListWidget()
        self.jogadores_list.setFont(QFont("Segoe UI", 12))  # Fonte menor para caber mais texto
        self.jogadores_list.setStyleSheet("""
            QListWidget { background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px; }
            QListWidget::item:selected { background: #FF6200; }
        """)
        self.carregar_lista_jogadores()
        layout.addWidget(self.jogadores_list)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        action_button = QPushButton("Carregar" if self.modo == "carregar" else "Excluir")
        action_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; min-width: 100px; }
            QPushButton:hover { background: #FF8340; }
        """)
        action_button.clicked.connect(self.action)
        button_layout.addWidget(action_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; min-width: 100px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def carregar_lista_jogadores(self):
        if os.path.exists("dados"):
            for arquivo in os.listdir("dados"):
                if arquivo.endswith(".json"):
                    caminho = os.path.join("dados", arquivo)
                    try:
                        with open(caminho, "r") as f:
                            data = json.load(f)
                            nome = data.get("nome", "Desconhecido")
                            posicao = data.get("posicao", "N/A")
                            time = data.get("time", "Sem Time")
                            altura_m = data.get("altura", 0)
                            altura_pes = altura_m / 0.0254
                            feet = int(altura_pes // 12)
                            inches = int(altura_pes % 12)
                            info = f"{nome} - {posicao} - {time} - {feet}'{inches}\""
                            item = QListWidgetItem(info)
                            item.setData(Qt.UserRole, caminho)  # Armazena o caminho do arquivo no item
                            self.jogadores_list.addItem(item)
                    except Exception as e:
                        item = QListWidgetItem(f"{arquivo} (Erro ao carregar: {str(e)})")
                        item.setData(Qt.UserRole, caminho)
                        self.jogadores_list.addItem(item)
        if self.jogadores_list.count() > 0:
            self.jogadores_list.setCurrentRow(0)

    def action(self):
        selected_item = self.jogadores_list.currentItem()
        if selected_item:
            self.selected_file = selected_item.data(Qt.UserRole)  # Recupera o caminho do arquivo
            self.accept()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um jogador!")

    def get_selected_file(self):
        return self.selected_file

# Para executar o aplicativo (se este for o arquivo principal)
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

class GerenciarJogadoresWindow(QDialog):
    def __init__(self, parent, modo="carregar"):
        super().__init__(parent)
        self.modo = modo  # "carregar" ou "excluir"
        self.setWindowTitle("Carregar Jogador" if modo == "carregar" else "Excluir Jogador")
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.selected_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        title = QLabel("Carregar Jogador" if self.modo == "carregar" else "Excluir Jogador")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.jogadores_list = QListWidget()
        self.jogadores_list.setFont(QFont("Segoe UI", 14))
        self.jogadores_list.setStyleSheet("""
            QListWidget { background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px; }
            QListWidget::item:selected { background: #FF6200; }
        """)
        self.carregar_lista_jogadores()
        layout.addWidget(self.jogadores_list)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        action_button = QPushButton("Carregar" if self.modo == "carregar" else "Excluir")
        action_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; min-width: 100px; }
            QPushButton:hover { background: #FF8340; }
        """)
        action_button.clicked.connect(self.action)
        button_layout.addWidget(action_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; min-width: 100px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def carregar_lista_jogadores(self):
        if os.path.exists("dados"):
            for arquivo in os.listdir("dados"):
                if arquivo.endswith(".json"):
                    item = QListWidgetItem(arquivo)
                    self.jogadores_list.addItem(item)
        if self.jogadores_list.count() > 0:
            self.jogadores_list.setCurrentRow(0)

    def action(self):
        selected_item = self.jogadores_list.currentItem()
        if selected_item:
            self.selected_file = os.path.join("dados", selected_item.text())
            self.accept()
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um jogador!")

    def get_selected_file(self):
        return self.selected_file

class EscolhaConfiguracaoWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Escolha o Tipo de Configuração")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("Escolha o Tipo de Configuração")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        desc_label = QLabel("Escolha como deseja configurar os pontos do seu jogador:")
        desc_label.setFont(QFont("Segoe UI", 14))
        desc_label.setStyleSheet("color: #FFFFFF;")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)

        presets_button = QPushButton("Escolher Presets de Pontos")
        presets_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        presets_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        presets_button.clicked.connect(self.abrir_dialogo_dificuldade)
        main_layout.addWidget(presets_button)

        custom_button = QPushButton("Configuração Personalizada")
        custom_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        custom_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        custom_button.clicked.connect(self.abrir_personalizado)
        main_layout.addWidget(custom_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        back_button.clicked.connect(self.back_to_main)
        main_layout.addWidget(back_button)

        main_layout.addStretch()

    def abrir_dialogo_dificuldade(self):
        dialog = EscolhaDificuldadeDialog(self.jogador, self, modo="presets")
        if dialog.exec_():
            escolha = dialog.get_choice()
            if escolha == "predefinida":
                # Aqui você pode abrir uma janela para dificuldade predefinida
                print("Dificuldade Predefinida selecionada")
            else:
                # Aqui você pode abrir uma janela para configuração personalizada
                print("Configuração Personalizada selecionada")

    def abrir_personalizado(self):
        # Aqui você pode abrir a janela de configuração personalizada diretamente
        print("Abrindo Configuração Personalizada")
        # Exemplo: self.custom_window = ConfiguracaoPersonalizadaWindow(self.jogador, self, modo="personalizado")
        # self.custom_window.show()
        # self.close()

    def back_to_main(self):
        self.parent.show()
        self.close()


class ConfiguracaoPersonalizadaWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Configuração Personalizada")
        self.setMinimumSize(900, 800)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Título principal
        title = QLabel("Configuração Personalizada")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #FF6200; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Área de rolagem para o conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # Seção de Custos de Atributos
        atributos_group = QGroupBox()
        atributos_group.setFont(QFont("Segoe UI", 18, QFont.Bold))
        atributos_group.setStyleSheet("QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding-top: 20px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        atributos_layout = QVBoxLayout(atributos_group)
        atributos_layout.setSpacing(10)

        atributos_title = QLabel("Custos de Atributos")
        atributos_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        atributos_title.setStyleSheet("color: #FF6200; margin-bottom: 10px;")
        atributos_title.setAlignment(Qt.AlignCenter)

        custos_label = QLabel("Defina o custo em pontos para aumentar atributos em cada faixa:")
        custos_label.setFont(QFont("Segoe UI", 14))
        custos_label.setStyleSheet("color: #FFFFFF; margin-bottom: 15px;")
        custos_label.setWordWrap(True)
        custos_label.setAlignment(Qt.AlignCenter)

        atributos_layout.addWidget(atributos_title)
        atributos_layout.addWidget(custos_label)

        self.custos_inputs = {}
        # Novos intervalos com valores padrão
        faixas = [
            ("0-69", 100),
            ("70-74", 150),
            ("75-79", 200),
            ("80-84", 250),
            ("85-89", 300),
            ("90-94", 400),
            ("95-99", 500)
        ]
        for faixa, valor_padrao in faixas:
            custo_layout = QHBoxLayout()
            custo_layout.setSpacing(10)
            label = QLabel(f"Faixa {faixa}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF; min-width: 120px;")
            input_field = QSpinBox()
            input_field.setRange(1, 1000000)
            # Carrega o valor atual do jogador, se existir, ou usa o padrão
            valor_inicial = self.jogador.custos_atributos.get(faixa, valor_padrao) if hasattr(self.jogador, 'custos_atributos') else valor_padrao
            input_field.setValue(valor_inicial)
            input_field.setFont(QFont("Segoe UI", 14))
            input_field.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            input_field.setFixedWidth(120)
            custo_layout.addWidget(label)
            custo_layout.addWidget(input_field)
            custo_layout.addStretch()
            atributos_layout.addLayout(custo_layout)
            self.custos_inputs[faixa] = input_field

        content_layout.addWidget(atributos_group)

        # Seção de Custos de Badges (mantida como estava)
        badges_group = QGroupBox()
        badges_group.setFont(QFont("Segoe UI", 18, QFont.Bold))
        badges_group.setStyleSheet("QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding-top: 20px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        badges_layout = QVBoxLayout(badges_group)
        badges_layout.setSpacing(10)

        badges_title = QLabel("Custos de Badges")
        badges_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        badges_title.setStyleSheet("color: #FF6200; margin-bottom: 10px;")
        badges_title.setAlignment(Qt.AlignCenter)

        badges_label = QLabel("Defina o custo em pontos para cada nível de badge:")
        badges_label.setFont(QFont("Segoe UI", 14))
        badges_label.setStyleSheet("color: #FFFFFF; margin-bottom: 15px;")
        badges_label.setWordWrap(True)
        badges_label.setAlignment(Qt.AlignCenter)

        badges_layout.addWidget(badges_title)
        badges_layout.addWidget(badges_label)

        self.custos_badges_inputs = {}
        niveis_badges = [("Bronze", 5), ("Prata", 10), ("Ouro", 15), ("Hall da Fama", 20)]
        for nivel, valor_padrao in niveis_badges:
            custo_layout = QHBoxLayout()
            custo_layout.setSpacing(10)
            label = QLabel(f"Nível {nivel}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF; min-width: 120px;")
            input_field = QSpinBox()
            input_field.setRange(1, 1000000)
            valor_inicial = self.jogador.custos_badges.get(nivel, valor_padrao) if hasattr(self.jogador, 'custos_badges') else valor_padrao
            input_field.setValue(valor_inicial)
            input_field.setFont(QFont("Segoe UI", 14))
            input_field.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            input_field.setFixedWidth(120)
            custo_layout.addWidget(label)
            custo_layout.addWidget(input_field)
            custo_layout.addStretch()
            badges_layout.addLayout(custo_layout)
            self.custos_badges_inputs[nivel] = input_field

        content_layout.addWidget(badges_group)

        # Seção de Metas de Estatísticas e Pontos (mantida como estava)
        stats_group = QGroupBox()
        stats_group.setFont(QFont("Segoe UI", 18, QFont.Bold))
        stats_group.setStyleSheet("QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding-top: 20px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(10)

        stats_title = QLabel("Metas de Estatísticas e Pontos Ganhos")
        stats_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        stats_title.setStyleSheet("color: #FF6200; margin-bottom: 10px;")
        stats_title.setAlignment(Qt.AlignCenter)

        stats_label = QLabel("No primeiro campo, defina quantas unidades no jogo (ex.: pontos, assistências) você precisa atingir.\nNo segundo campo, defina quantos pontos no aplicativo você ganhará (ou perderá, no caso de turnovers).")
        stats_label.setFont(QFont("Segoe UI", 14))
        stats_label.setStyleSheet("color: #FFFFFF; margin-bottom: 15px;")
        stats_label.setWordWrap(True)
        stats_label.setAlignment(Qt.AlignCenter)

        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(stats_label)

        self.stats_inputs = {}
        stats = ["Pontos", "Assistências", "Rebotes", "Steal", "Block", "Turnover"]
        for stat in stats:
            stat_layout = QHBoxLayout()
            stat_layout.setSpacing(10)
            if stat == "Turnover":
                meta_label = QLabel("Turnovers no jogo:")
                pontos_label = QLabel("Pontos perdidos:")
            else:
                meta_label = QLabel(f"{stat} no jogo:")
                pontos_label = QLabel("Pontos ganhos:")
            meta_label.setFont(QFont("Segoe UI", 14))
            meta_label.setStyleSheet("color: #FFFFFF; min-width: 150px;")
            pontos_label.setFont(QFont("Segoe UI", 14))
            pontos_label.setStyleSheet("color: #FFFFFF; min-width: 120px;")
            meta_input = QLineEdit("10" if stat != "Turnover" else "5")
            meta_input.setValidator(QIntValidator(1, 1000000))
            meta_input.setFont(QFont("Segoe UI", 14))
            meta_input.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            meta_input.setFixedWidth(120)
            pontos_input = QLineEdit("10" if stat != "Turnover" else "-5")
            if stat == "Turnover":
                pontos_input.setValidator(QIntValidator(-1000000, 0))
            else:
                pontos_input.setValidator(QIntValidator(1, 1000000))
            pontos_input.setFont(QFont("Segoe UI", 14))
            pontos_input.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            pontos_input.setFixedWidth(120)
            stat_layout.addWidget(meta_label)
            stat_layout.addWidget(meta_input)
            stat_layout.addWidget(pontos_label)
            stat_layout.addWidget(pontos_input)
            stat_layout.addStretch()
            stats_layout.addLayout(stat_layout)
            self.stats_inputs[stat] = (meta_input, pontos_input)

        content_layout.addWidget(stats_group)

        # Seção de Pontos dos Prêmios (mantida como estava)
        premios_group = QGroupBox()
        premios_group.setFont(QFont("Segoe UI", 18, QFont.Bold))
        premios_group.setStyleSheet("QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding-top: 20px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        premios_layout = QVBoxLayout(premios_group)
        premios_layout.setSpacing(10)

        premios_title = QLabel("Pontos dos Prêmios")
        premios_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        premios_title.setStyleSheet("color: #FF6200; margin-bottom: 10px;")
        premios_title.setAlignment(Qt.AlignCenter)

        premios_label = QLabel("Defina quantos pontos no aplicativo você ganhará ao conquistar cada prêmio:")
        premios_label.setFont(QFont("Segoe UI", 14))
        premios_label.setStyleSheet("color: #FFFFFF; margin-bottom: 15px;")
        premios_label.setWordWrap(True)
        premios_label.setAlignment(Qt.AlignCenter)

        premios_layout.addWidget(premios_title)
        premios_layout.addWidget(premios_label)

        self.premios = {
            "Jogador do Mês": 300,
            "All Star": 500,
            "Scoring Champion": 1000,
            "Rookie of the Year": 2500,
            "Most Improved Player": 2000,
            "Sixth Man of the Year": 2000,
            "Clutch Player of the Year": 1500,
            "Defensive Player of the Year": 5000,
            "Most Valuable Player": 20000,
            "Conference Finals MVP": 8000,
            "Finals MVP": 15000,
            "NBA Champion": 25000
        }
        self.premios_inputs = {}
        for premio, pontos_base in self.premios.items():
            premio_layout = QHBoxLayout()
            premio_layout.setSpacing(10)
            label = QLabel(f"{premio}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF; min-width: 300px;")
            input_field = QSpinBox()
            input_field.setRange(0, 1000000)
            valor_inicial = self.jogador.pontos_premios_personalizados.get(premio, pontos_base) if hasattr(self.jogador, 'pontos_premios_personalizados') and self.jogador.pontos_premios_personalizados else pontos_base
            input_field.setValue(valor_inicial)
            input_field.setFont(QFont("Segoe UI", 14))
            input_field.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            input_field.setFixedWidth(120)
            premio_layout.addWidget(label)
            premio_layout.addWidget(input_field)
            premio_layout.addStretch()
            premios_layout.addLayout(premio_layout)
            self.premios_inputs[premio] = input_field

        content_layout.addWidget(premios_group)

        # Área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: #2D2D2D; border: none;")
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        # Botões na parte inferior
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)

        apply_button = QPushButton("Aplicar Configurações")
        apply_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; min-width: 200px; }
            QPushButton:hover { background: #FF8340; }
        """)
        apply_button.clicked.connect(self.aplicar_configuracoes)
        buttons_layout.addWidget(apply_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; min-width: 200px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_main)
        buttons_layout.addWidget(back_button)

        main_layout.addLayout(buttons_layout)

    def aplicar_configuracoes(self):
        try:
            # Verificação dos campos
            faixas_esperadas = ["0-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95-99"]
            if not all(key in self.custos_inputs for key in faixas_esperadas):
                raise KeyError("Alguns campos de custos de atributos não foram inicializados corretamente.")
            if not all(key in self.custos_badges_inputs for key in ["Bronze", "Prata", "Ouro", "Hall da Fama"]):
                raise KeyError("Alguns campos de custos de badges não foram inicializados corretamente.")
            if not all(key in self.stats_inputs for key in ["Pontos", "Assistências", "Rebotes", "Steal", "Block", "Turnover"]):
                raise KeyError("Alguns campos de metas de estatísticas não foram inicializados corretamente.")
            if not all(key in self.premios_inputs for key in self.premios.keys()):
                raise KeyError("Alguns campos de pontos de prêmios não foram inicializados corretamente.")

            # Custos de Atributos
            custos = {faixa: self.custos_inputs[faixa].value() for faixa in faixas_esperadas}
            self.jogador.custos_atributos = custos

            # Custos de Badges
            custos_badges = {
                nivel: input_field.value() for nivel, input_field in self.custos_badges_inputs.items()
            }
            self.jogador.custos_badges = custos_badges

            # Metas de Estatísticas e Pontos
            estatisticas = {}
            for stat, (meta_input, pontos_input) in self.stats_inputs.items():
                meta = int(meta_input.text())
                pontos = int(pontos_input.text())
                if meta > 1000000:
                    raise ValueError(f"A meta para {stat} excede o limite de 1.000.000!")
                if stat == "Turnover":
                    if pontos > 0:
                        raise ValueError("Turnover deve ter um valor negativo!")
                    if pontos < -1000000:
                        raise ValueError("O valor de pontos perdidos para Turnover excede o limite de -1.000.000!")
                elif pontos > 1000000:
                    raise ValueError(f"Os pontos ganhos para {stat} excede o limite de 1.000.000!")
                estatisticas[stat] = pontos  # Ajustado para compatibilidade com a classe Jogador
            self.jogador.dificuldade = estatisticas

            # Pontos dos Prêmios
            if not hasattr(self.jogador, 'pontos_premios_personalizados'):
                self.jogador.pontos_premios_personalizados = {}
            for premio, input_field in self.premios_inputs.items():
                if input_field.value() > 1000000:
                    raise ValueError(f"Os pontos para {premio} excede o limite de 1.000.000!")
                self.jogador.pontos_premios_personalizados[premio] = input_field.value()

            self.jogador.salvar()

            self.show_success("Configurações aplicadas com sucesso!")
            self.parent.show()
            self.close()
        except ValueError as e:
            self.show_error(f"Erro: {str(e)}")
        except KeyError as e:
            self.show_error(f"Erro: Falha na inicialização dos campos - {str(e)}")

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_main(self):
        self.parent.show()
        self.close()

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, 
                             QComboBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EscolhaDificuldadeWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Escolha a Dificuldade")
        self.setMinimumSize(600, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        title = QLabel("Escolha a Dificuldade")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        desc_label = QLabel("Selecione a dificuldade com base na sua posição:\nOs pontos ganhos ou perdidos por estatística e os custos de atributos refletem o desafio de cada posição.")
        desc_label.setFont(QFont("Segoe UI", 14))
        desc_label.setStyleSheet("color: #FFFFFF;")
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)

        self.posicao_combo = QComboBox()
        posicoes = ["PG (Point Guard)", "SG (Shooting Guard)", "SF (Small Forward)", "PF (Power Forward)", "C (Center)"]
        self.posicao_combo.addItems(posicoes)
        posicao_atual = f"{self.jogador.posicao} ({self.get_nome_posicao(self.jogador.posicao)})"
        self.posicao_combo.setCurrentText(posicao_atual)
        self.posicao_combo.setFont(QFont("Segoe UI", 14))
        self.posicao_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        self.posicao_combo.currentIndexChanged.connect(self.atualizar_preview)
        main_layout.addWidget(self.posicao_combo)

        self.preview_widget = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_widget)
        self.preview_layout.setSpacing(5)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: #2D2D2D; border: none;")
        scroll_area.setWidget(self.preview_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        apply_button = QPushButton("Aplicar Configuração")
        apply_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        apply_button.clicked.connect(self.aplicar_configuracao)  # Conexão corrigida aqui
        main_layout.addWidget(apply_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_main)
        main_layout.addWidget(back_button)

        self.atualizar_preview()

    def get_nome_posicao(self, posicao):
        nomes = {"PG": "Point Guard", "SG": "Shooting Guard", "SF": "Small Forward", "PF": "Power Forward", "C": "Center"}
        return nomes.get(posicao, "Desconhecido")

    def atualizar_preview(self):
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                item.layout().deleteLater()
            elif item.widget():
                item.widget().deleteLater()

        presets = {
            "PG (Point Guard)": {
                "estatisticas": {"Pontos": 10, "Assistências": 5, "Rebotes": 20, "Steal": 10, "Block": 25, "Turnover": -25},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "SG (Shooting Guard)": {
                "estatisticas": {"Pontos": 10, "Assistências": 5, "Rebotes": 20, "Steal": 10, "Block": 25, "Turnover": -25},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "SF (Small Forward)": {
                "estatisticas": {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 10, "Block": 15, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "PF (Power Forward)": {
                "estatisticas": {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 10, "Block": 15, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "C (Center)": {
                "estatisticas": {"Pontos": 10, "Assistências": 15, "Rebotes": 5, "Steal": 15, "Block": 10, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            }
        }

        posicao_selecionada = self.posicao_combo.currentText()
        config = presets[posicao_selecionada]

        # Exibir estatísticas
        estatisticas_title = QLabel("Estatísticas por Partida:")
        estatisticas_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        estatisticas_title.setStyleSheet("color: #FF6200;")
        self.preview_layout.addWidget(estatisticas_title)

        for stat, pontos in config["estatisticas"].items():
            stat_layout = QHBoxLayout()
            label = QLabel(f"{stat}: {'-' if pontos < 0 else ''}{abs(pontos)} pontos")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            stat_layout.addWidget(label)
            stat_layout.addStretch()
            self.preview_layout.addLayout(stat_layout)

        # Exibir custos de atributos
        custos_title = QLabel("Custos de Atributos:")
        custos_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        custos_title.setStyleSheet("color: #FF6200;")
        self.preview_layout.addWidget(custos_title)

        for faixa, custo in config["custos_atributos"].items():
            custo_layout = QHBoxLayout()
            label = QLabel(f"{faixa}: {custo} pontos")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            custo_layout.addWidget(label)
            custo_layout.addStretch()
            self.preview_layout.addLayout(custo_layout)

    def aplicar_configuracao(self):  # Função corrigida
        presets = {
            "PG (Point Guard)": {
                "estatisticas": {"Pontos": 10, "Assistências": 5, "Rebotes": 20, "Steal": 10, "Block": 25, "Turnover": -25},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "SG (Shooting Guard)": {
                "estatisticas": {"Pontos": 10, "Assistências": 5, "Rebotes": 20, "Steal": 10, "Block": 25, "Turnover": -25},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "SF (Small Forward)": {
                "estatisticas": {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 10, "Block": 15, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "PF (Power Forward)": {
                "estatisticas": {"Pontos": 10, "Assistências": 10, "Rebotes": 10, "Steal": 10, "Block": 15, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            },
            "C (Center)": {
                "estatisticas": {"Pontos": 10, "Assistências": 15, "Rebotes": 5, "Steal": 15, "Block": 10, "Turnover": -20},
                "custos_atributos": {"0-69": 100, "70-74": 150, "75-79": 200, "80-84": 250, "85-89": 300, "90-94": 400, "95-99": 500}
            }
        }

        posicao_selecionada = self.posicao_combo.currentText()
        config = presets[posicao_selecionada]
        
        # Aplicar estatísticas e custos de atributos
        self.jogador.dificuldade = config["estatisticas"]
        self.jogador.custos_atributos = config["custos_atributos"]
        self.jogador.salvar()

        self.show_success(f"Configuração de dificuldade para {posicao_selecionada} aplicada com sucesso!")
        self.player_window = PlayerWindow(self.jogador, self.parent)
        self.player_window.show()
        self.close()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_main(self):
        self.parent.show()
        self.close()


class LoadPlayerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Carregar Jogador")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Selecione um Jogador")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        layout.addWidget(title)

        self.player_list = QListWidget()
        self.player_list.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 16px;")
        self.player_list.setFont(QFont("Segoe UI", 16))
        self.atualizar_lista_jogadores()
        layout.addWidget(self.player_list, stretch=1)

        load_button = QPushButton("Carregar")
        load_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        load_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        load_button.clicked.connect(self.load_selected_player)
        layout.addWidget(load_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

    def atualizar_lista_jogadores(self):
        self.player_list.clear()
        if os.path.exists("dados"):
            jogadores = [f.split(".json")[0] for f in os.listdir("dados") if f.endswith(".json")]
            self.player_list.addItems(jogadores if jogadores else ["Nenhum jogador salvo"])
        else:
            self.player_list.addItem("Nenhum jogador salvo")

    def load_selected_player(self):
        selected = self.player_list.currentItem()
        if selected and selected.text() != "Nenhum jogador salvo":
            jogador = Jogador(selected.text())
            jogador.carregar(f"dados/{selected.text()}.json")
            self.parent.player_window = PlayerWindow(jogador, self.parent)
            self.parent.player_window.show()
            self.close()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Selecione um jogador válido!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                background-color: #2D2D2D;
                QLabel { color: #FFFFFF; font-size: 14px; }
                QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
                QPushButton:hover { background: #FF8340; }
            """)
            msg_box.exec_()

    def back_to_main(self):
        self.parent.show()
        self.close()

class AddPlayerWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Adicionar Jogador")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Novo Jogador")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        layout.addWidget(title)

        self.nome_entry = QLineEdit()
        self.nome_entry.setPlaceholderText("Nome")
        self.nome_entry.setFont(QFont("Segoe UI", 16))
        self.nome_entry.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.nome_entry)

        self.altura_combo = QComboBox()
        alturas = [(feet, inches) for feet in range(5, 8) for inches in range(0, 12)
                   if (feet == 5 and inches >= 5) or (feet == 6) or (feet == 7 and inches <= 7)]
        altura_options = [f"{feet}'{inches}\"" for feet, inches in alturas]
        self.altura_combo.addItems(altura_options)
        self.altura_combo.setFont(QFont("Segoe UI", 16))
        self.altura_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.altura_combo)

        self.posicao_combo = QComboBox()
        self.posicao_combo.addItems(["PG", "SG", "SF", "PF", "C"])
        self.posicao_combo.setFont(QFont("Segoe UI", 16))
        self.posicao_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.posicao_combo)

        self.time_combo = QComboBox()
        teams = [
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
            "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors",
            "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
            "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
            "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
            "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"
        ]
        self.time_combo.addItems(teams)
        self.time_combo.setFont(QFont("Segoe UI", 16))
        self.time_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.time_combo)

        self.ano_inicio_spin = QSpinBox()
        self.ano_inicio_spin.setFont(QFont("Segoe UI", 16))
        self.ano_inicio_spin.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
        self.ano_inicio_spin.setMinimum(1970)
        self.ano_inicio_spin.setMaximum(2130)
        self.ano_inicio_spin.setValue(2025)
        layout.addWidget(QLabel("Ano de Início:", font=QFont("Segoe UI", 16)))
        layout.addWidget(self.ano_inicio_spin)

        save_button = QPushButton("Salvar e Configurar Atributos")
        save_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        save_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        save_button.clicked.connect(self.save_player)
        layout.addWidget(save_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        layout.addStretch()

    def save_player(self):
        nome = self.nome_entry.text().strip()
        altura_text = self.altura_combo.currentText()
        feet, inches = map(int, altura_text.replace('"', '').split("'"))
        altura_m = (feet * 12 + inches) * 0.0254
        posicao = self.posicao_combo.currentText()
        time = self.time_combo.currentText()
        ano_inicio = self.ano_inicio_spin.value()

        if nome:
            jogador = Jogador(nome)
            jogador.posicao = posicao
            jogador.posicoes_compradas_primarias = [posicao]  # Posição inicial é comprada automaticamente
            jogador.posicoes_compradas_secundarias = []
            jogador.time = time
            jogador.altura = altura_m
            jogador.ano_inicio = ano_inicio
            print(f"Antes de salvar - Posição: {jogador.posicao}, Posições compradas primárias: {jogador.posicoes_compradas_primarias}")
            jogador.salvar()
            print(f"Após salvar - Posição: {jogador.posicao}, Posições compradas primárias: {jogador.posicoes_compradas_primarias}")
            self.atributos_window = AtributosIniciaisWindow(jogador, self.parent)
            self.atributos_window.show()
            self.close()
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Digite um nome válido!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                background-color: #2D2D2D;
                QLabel { color: #FFFFFF; font-size: 14px; }
                QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
                QPushButton:hover { background: #FF8340; }
            """)
            msg_box.exec_()

    def back_to_main(self):
        self.parent.show()
        self.close()

class AtributosIniciaisWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle(f"Atributos Iniciais - {self.jogador.nome}")
        self.setMinimumSize(800, 600)  # Tamanho mínimo mantido
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Margens reduzidas para aproveitar mais espaço
        main_layout.setSpacing(5)  # Espaçamento mínimo no layout principal

        # Título
        title = QLabel("Defina os Atributos Iniciais (0-99)")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))  # Título um pouco menor para economizar espaço
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Conteúdo principal
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(4)  # Espaçamento reduzido entre itens

        self.atributos_entries = {}
        categorias = {
            "Finishing": ["Close Shot", "Driving Layup", "Driving Dunk", "Standing Dunk", "Post Control"],
            "Shooting": ["Mid-Range Shot", "Three-Point Shot", "Free Throw", "Post Fade"],
            "Playmaking": ["Pass Accuracy", "Ball Handle", "Speed With Ball"],
            "Defense/Rebounding": ["Interior Defense", "Perimeter Defense", "Steal", "Block", "Offensive Rebound", "Defensive Rebound"],
            "Physicals": ["Speed", "Acceleration", "Strength", "Vertical", "Stamina"]
        }

        for categoria, atributos in categorias.items():
            categoria_label = QLabel(categoria)
            categoria_label.setFont(QFont("Segoe UI", 14, QFont.Bold))  # Fonte um pouco menor
            categoria_label.setStyleSheet("color: #FF6200;")
            content_layout.addWidget(categoria_label)

            for attr in atributos:
                frame = QHBoxLayout()
                frame.setSpacing(5)  # Espaçamento reduzido no frame
                label = QLabel(attr)
                label.setFont(QFont("Segoe UI", 12))  # Fonte reduzida para caber mais
                label.setStyleSheet("color: #FFFFFF;")
                entry = QSpinBox()
                entry.setFont(QFont("Segoe UI", 12))  # Fonte reduzida
                entry.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 6px;")
                entry.setMinimum(0)
                entry.setMaximum(99)
                entry.setValue(50)
                entry.setFixedWidth(80)  # Largura reduzida para compactar
                frame.addWidget(label)
                frame.addWidget(entry)
                frame.addStretch()  # Apenas para alinhamento horizontal
                content_layout.addLayout(frame)

        # Adicionar o conteúdo ao layout principal com rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: #2D2D2D; border: none;")
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, stretch=1)  # Ocupa todo o espaço disponível

        # Botão Salvar
        save_button = QPushButton("Salvar e Configurar")
        save_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        save_button.setFont(QFont("Segoe UI", 14, QFont.Bold))  # Botão um pouco menor
        save_button.clicked.connect(self.save_atributos)
        main_layout.addWidget(save_button)

        # Botão Voltar
        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 14, QFont.Bold))  # Botão um pouco menor
        back_button.clicked.connect(self.back_to_main)
        main_layout.addWidget(back_button)

        # Sem stretch extra no final para evitar espaço vazio

    def save_atributos(self):
        atributos_iniciais = {attr: entry.value() for attr, entry in self.atributos_entries.items()}
        self.jogador.atributos = atributos_iniciais  # Atualiza os atributos do jogador
        self.jogador.salvar()
        self.config_window = ConfiguracaoJogadorWindow(self.jogador, self.parent)
        self.config_window.show()
        self.close()

    def back_to_main(self):
        self.parent.show()
        self.close()



class ConfiguracaoJogadorWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle(f"Configurar - {self.jogador.nome}")
        self.setMinimumSize(900, 700)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Configurações do Jogador")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        custo_layout = QVBoxLayout()
        custo_title = QLabel("Custos de Atributos (por ponto)")
        custo_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        custo_title.setStyleSheet("color: #FFFFFF;")
        custo_layout.addWidget(custo_title)

        self.custo_entries = {}
        faixas = {0: "0-75", 75: "75-85", 85: "85-95", 95: "95-99"}
        for faixa, descricao in faixas.items():
            frame = QHBoxLayout()
            label = QLabel(f"{descricao}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            entry = QLineEdit(str(self.jogador.custos_atributos[faixa]))
            entry.setFont(QFont("Segoe UI", 14))
            entry.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 8px;")
            entry.setFixedWidth(100)
            frame.addWidget(label)
            frame.addWidget(entry)
            frame.addStretch()
            custo_layout.addLayout(frame)
            self.custo_entries[faixa] = entry

        layout.addLayout(custo_layout)

        estatistica_layout = QVBoxLayout()
        estatistica_title = QLabel("Pontos por Estatística (a cada X)")
        estatistica_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        estatistica_title.setStyleSheet("color: #FFFFFF;")
        estatistica_layout.addWidget(estatistica_title)

        columns_layout = QHBoxLayout()

        left_column = QVBoxLayout()
        left_stats = ["Pontos", "Assistências", "Rebotes"]

        right_column = QVBoxLayout()
        right_stats = ["Steal", "Block", "Turnover"]

        self.ponto_entries = {}

        for stat in left_stats:
            frame = QHBoxLayout()
            label = QLabel(f"{stat}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            entry = QSpinBox()
            entry.setFont(QFont("Segoe UI", 14))
            entry.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 8px;")
            entry.setMinimum(1)
            entry.setMaximum(100)
            entry.setValue(self.jogador.pontos_estatisticas[stat])
            entry.setFixedSize(100, 40)
            frame.addWidget(label)
            frame.addWidget(entry)
            frame.addStretch()
            left_column.addLayout(frame)
            self.ponto_entries[stat] = entry

        for stat in right_stats:
            frame = QHBoxLayout()
            label = QLabel(f"{stat}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            entry = QSpinBox()
            entry.setFont(QFont("Segoe UI", 14))
            entry.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 8px;")
            entry.setMinimum(1)
            entry.setMaximum(100)
            entry.setValue(self.jogador.pontos_estatisticas[stat])
            entry.setFixedSize(100, 40)
            frame.addWidget(label)
            frame.addWidget(entry)
            frame.addStretch()
            right_column.addLayout(frame)
            self.ponto_entries[stat] = entry

        columns_layout.addLayout(left_column)
        columns_layout.addStretch()
        columns_layout.addLayout(right_column)

        estatistica_layout.addLayout(columns_layout)
        layout.addLayout(estatistica_layout)

        save_button = QPushButton("Salvar Configurações")
        save_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        save_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        save_button.clicked.connect(self.salvar_configuracoes)
        layout.addWidget(save_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

    def salvar_configuracoes(self):
        try:
            custos_atributos = {faixa: int(self.custo_entries[faixa].text()) for faixa in self.custo_entries}
            pontos_estatisticas = {stat: self.ponto_entries[stat].value() for stat in self.ponto_entries}
            pontos_premios = self.jogador.pontos_premios
            self.jogador.definir_configuracoes(custos_atributos, pontos_estatisticas, pontos_premios)
            self.jogador.salvar()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Sucesso")
            msg_box.setText("Configurações salvas com sucesso!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                background-color: #2D2D2D;
                QLabel { color: #FFFFFF; font-size: 14px; }
                QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
                QPushButton:hover { background: #FF8340; }
            """)
            msg_box.exec_()
            self.player_window = PlayerWindow(self.jogador, self.parent)
            self.player_window.show()
            self.close()
        except ValueError:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Erro")
            msg_box.setText("Insira valores numéricos válidos!")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setStyleSheet("""
                background-color: #2D2D2D;
                QLabel { color: #FFFFFF; font-size: 14px; }
                QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
                QPushButton:hover { background: #FF8340; }
            """)
            msg_box.exec_()

    def back_to_main(self):
        self.parent.show()
        self.close()

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class EscolhaDificuldadeDialog(QDialog):
    def __init__(self, jogador, parent=None, modo=None):
        super().__init__(parent)
        self.jogador = jogador  # Armazena o jogador
        self.modo = modo  # Armazena o modo (pode ser usado para lógica futura)
        self.setWindowTitle("Escolher Tipo de Dificuldade")
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Escolha o tipo de dificuldade:")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.predefinida_radio = QRadioButton("Dificuldade Predefinida")
        self.predefinida_radio.setFont(QFont("Segoe UI", 14))
        self.predefinida_radio.setStyleSheet("color: #FFFFFF;")
        self.predefinida_radio.setChecked(True)
        layout.addWidget(self.predefinida_radio)

        self.personalizada_radio = QRadioButton("Configuração Personalizada")
        self.personalizada_radio.setFont(QFont("Segoe UI", 14))
        self.personalizada_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.personalizada_radio)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def get_choice(self):
        """Retorna a escolha do usuário: 'predefinida' ou 'personalizada'."""
        if self.predefinida_radio.isChecked():
            return "predefinida"
        return "personalizada"

class PlayerWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent  # Isso é a MainWindow
        self.setWindowTitle(f"NBA 2K25 - {self.jogador.nome}")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        player_info_layout = QHBoxLayout()
        player_info_layout.setSpacing(10)

        self.title = QLabel(f"{self.jogador.nome}")
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title.setStyleSheet("color: #FF6200; background: #2D2D2D; padding: 8px; border-radius: 5px;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedWidth(180)
        player_info_layout.addWidget(self.title)

        self.time_label = QLabel(f"Time: {getattr(self.jogador, 'time', 'Não definido')}")
        self.time_label.setFont(QFont("Segoe UI", 14))
        self.time_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 8px; border-radius: 5px;")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFixedWidth(250)
        player_info_layout.addWidget(self.time_label)

        posicao = getattr(self.jogador, 'posicao', 'Não definida')
        posicao_secundaria = getattr(self.jogador, 'posicao_secundaria', None)
        posicao_texto = posicao if not posicao_secundaria else f"{posicao}/{posicao_secundaria}"
        self.posicao_label = QLabel(f"Pos.: {posicao_texto}")
        self.posicao_label.setFont(QFont("Segoe UI", 14))
        self.posicao_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 8px; border-radius: 5px;")
        self.posicao_label.setAlignment(Qt.AlignCenter)
        self.posicao_label.setFixedWidth(110)
        player_info_layout.addWidget(self.posicao_label)

        self.pontos_label = QLabel(f"Pontos: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 14))
        self.pontos_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 8px; border-radius: 5px;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        self.pontos_label.setFixedWidth(110)
        player_info_layout.addWidget(self.pontos_label)

        self.ano_label = QLabel(f"Ano: {getattr(self.jogador, 'ano_atual', 2025)}")
        self.ano_label.setFont(QFont("Segoe UI", 14))
        self.ano_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 8px; border-radius: 5px;")
        self.ano_label.setAlignment(Qt.AlignCenter)
        self.ano_label.setFixedWidth(110)
        player_info_layout.addWidget(self.ano_label)

        player_info_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(player_info_layout)

        menu_group = QGroupBox("Menu")
        menu_group.setFont(QFont("Segoe UI", 18, QFont.Bold))
        menu_group.setStyleSheet("""
            QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding: 15px; } 
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
        """)
        menu_layout = QGridLayout(menu_group)
        menu_layout.setHorizontalSpacing(20)
        menu_layout.setVerticalSpacing(15)

        button_style = """
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF6200, stop:1 #FF8340); color: #FFFFFF; border-radius: 8px; padding: 15px; font-size: 16px; min-width: 200px; min-height: 50px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF8340, stop:1 #FF6200); }
        """
        back_button_style = """
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #777777); color: #FFFFFF; border-radius: 8px; padding: 15px; font-size: 16px; min-width: 200px; min-height: 50px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #777777, stop:1 #555555); }
        """
        passar_ano_style = """
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2E7D32, stop:1 #4CAF50); color: #FFFFFF; border-radius: 8px; padding: 15px; font-size: 16px; min-width: 200px; min-height: 50px; border: 2px solid #FFFFFF; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4CAF50, stop:1 #2E7D32); }
        """

        perfil_button = QPushButton("Perfil/Nova Posição")
        perfil_button.setStyleSheet(button_style)
        perfil_button.clicked.connect(self.abrir_perfil)
        menu_layout.addWidget(perfil_button, 0, 0, Qt.AlignCenter)

        stats_button = QPushButton("Nova Partida")
        stats_button.setStyleSheet(button_style)
        stats_button.clicked.connect(self.abrir_estatisticas)
        menu_layout.addWidget(stats_button, 0, 1, Qt.AlignCenter)

        atributos_button = QPushButton("Comprar Atributos")
        atributos_button.setStyleSheet(button_style)
        atributos_button.clicked.connect(self.abrir_atributos)
        menu_layout.addWidget(atributos_button, 1, 0, Qt.AlignCenter)

        badges_button = QPushButton("Comprar/Melhorar Badges")
        badges_button.setStyleSheet(button_style)
        badges_button.clicked.connect(self.abrir_badges)
        menu_layout.addWidget(badges_button, 1, 1, Qt.AlignCenter)

        premios_button = QPushButton("Prêmios")
        premios_button.setStyleSheet(button_style)
        premios_button.clicked.connect(self.abrir_adicionar_premio)
        menu_layout.addWidget(premios_button, 2, 0, Qt.AlignCenter)

        historico_button = QPushButton("Histórico")
        historico_button.setStyleSheet(button_style)
        historico_button.clicked.connect(self.abrir_historico)
        menu_layout.addWidget(historico_button, 2, 1, Qt.AlignCenter)

        dificuldade_button = QPushButton("Mudar Dificuldade")
        dificuldade_button.setStyleSheet(button_style)
        dificuldade_button.clicked.connect(self.abrir_escolha_dificuldade)
        menu_layout.addWidget(dificuldade_button, 3, 0, Qt.AlignCenter)

        salvar_button = QPushButton("Salvar Progresso")
        salvar_button.setStyleSheet(button_style)
        salvar_button.clicked.connect(self.salvar_progresso)
        menu_layout.addWidget(salvar_button, 3, 1, Qt.AlignCenter)

        # Alterado de "Fechar e Salvar" para "Menu Principal"
        menu_principal_button = QPushButton("Menu Principal")
        menu_principal_button.setStyleSheet(back_button_style)
        menu_principal_button.clicked.connect(self.voltar_menu_principal)  # Nova função
        menu_layout.addWidget(menu_principal_button, 4, 0, 1, 2, Qt.AlignCenter)

        passar_ano_button = QPushButton("Passar o Ano")
        passar_ano_button.setStyleSheet(passar_ano_style)
        passar_ano_button.clicked.connect(self.passar_ano)
        menu_layout.addWidget(passar_ano_button, 5, 0, 1, 2, Qt.AlignCenter)

        main_layout.addWidget(menu_group)
        main_layout.addStretch()

    def atualizar_status(self):
        self.title.setText(f"{self.jogador.nome}")
        self.pontos_label.setText(f"Pontos: {self.jogador.pontos_disponiveis}")
        self.ano_label.setText(f"Ano: {getattr(self.jogador, 'ano_atual', 2025)}")
        self.time_label.setText(f"Time: {getattr(self.jogador, 'time', 'Não definido')}")
        posicao = getattr(self.jogador, 'posicao', 'Não definida')
        posicao_secundaria = getattr(self.jogador, 'posicao_secundaria', None)
        posicao_texto = posicao if not posicao_secundaria else f"{posicao}/{posicao_secundaria}"
        self.posicao_label.setText(f"Pos.: {posicao_texto}")

    def passar_ano(self):
        if not hasattr(self.jogador, 'ano_atual'):
            self.jogador.ano_atual = 2025
        self.jogador.ano_atual += 1
        self.ano_label.setText(f"Ano: {self.jogador.ano_atual}")
        self.jogador.salvar()
        self.show_success(f"Ano avançado para {self.jogador.ano_atual}!")

    def abrir_perfil(self):
        self.perfil_window = PerfilWindow(self.jogador, self)
        self.perfil_window.show()
        self.hide()

    def abrir_estatisticas(self):
        self.estatisticas_window = EstatisticasWindow(self.jogador, self)
        self.estatisticas_window.show()
        self.hide()

    def abrir_historico(self):
        self.historico_window = HistoricoWindow(self.jogador, self)
        self.historico_window.show()
        self.hide()

    def abrir_adicionar_premio(self):
        self.premio_window = AdicionarPremioWindow(self.jogador, self)
        self.premio_window.show()
        self.hide()

    def abrir_escolha_dificuldade(self):
        dialogo = EscolhaDificuldadeDialog(self)
        if dialogo.exec_():
            if dialogo.predefinida_radio.isChecked():
                self.config_window = EscolhaDificuldadeWindow(self.jogador, self)
                self.config_window.show()
            elif dialogo.personalizada_radio.isChecked():
                self.config_window = ConfiguracaoPersonalizadaWindow(self.jogador, self)
                self.config_window.show()
            self.hide()

    def abrir_atributos(self):
        self.atributos_window = AtributosDoJogadorWindow(self.jogador, self)
        self.atributos_window.show()
        self.hide()

    def abrir_badges(self):
        self.badges_window = BadgesWindow(self.jogador, self)
        self.badges_window.show()
        self.hide()

    def salvar_progresso(self):
        try:
            self.jogador.salvar()
            self.show_success("Progresso salvo com sucesso!")
        except Exception as e:
            self.show_error(f"Erro ao salvar progresso: {str(e)}")

    def voltar_menu_principal(self):  # Nova função substituindo fechar_e_salvar
        try:
            self.jogador.salvar()
            self.show_success("Progresso salvo com sucesso! Retornando ao Menu Principal.")
            self.parent.show()  # Mostra a MainWindow
            self.close()  # Fecha a PlayerWindow
        except Exception as e:
            self.show_error(f"Erro ao salvar progresso: {str(e)}")

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()


class BadgesWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        if not hasattr(self.jogador, 'pontos_disponiveis'):
            self.jogador.pontos_disponiveis = 100  # Valor padrão, ajustável
        if not hasattr(self.jogador, 'badges'):
            self.jogador.badges = {}
        self.parent = parent
        self.setWindowTitle(f"Badges de {self.jogador.nome}")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.pontos_gastos = 0
        self.badges_temp = self.jogador.badges.copy()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 10, 20, 20)  # Reduzi a margem superior de 30 para 10
        main_layout.setSpacing(10)  # Reduzi o espaçamento de 20 para 10

        # Título principal (reduzido)
        title = QLabel(f"Badges de {self.jogador.nome}")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))  # Reduzi de 24 para 18
        title.setStyleSheet("color: #FF6200; padding: 5px; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2D2D2D, stop:1 #1A1A1A); border-radius: 5px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Label de pontos (reduzido)
        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis} | Gastos: {self.pontos_gastos}")
        self.pontos_label.setFont(QFont("Segoe UI", 14))  # Reduzi de 18 para 14
        self.pontos_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 5px; border-radius: 5px;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.pontos_label)

        # Área de rolagem para as badges
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        # Definindo categorias para as badges
        self.badges = {
            "Inside Scoring": ["Aerial Wizard", "Float Game", "Hook Specialist", "Layup Mixmaster", "Paint Prodigy",
                              "Physical Finisher", "Post Fade Phenom", "Post Powerhouse", "Post-Up Poet", "Posterizer", "Rise Up"],
            "Outside Scoring": ["Deadeye", "Limitless Range", "Mini Marksman", "Set Shot Specialist", "Shifty Shooter"],
            "Playmaking": ["Ankle Assassin", "Bail Out", "Break Starter", "Dimer", "Handles For Days",
                          "Lightning Launch", "Strong Handle", "Unpluckable", "Versatile Visionary"],
            "Rebounding": ["Boxout Beast", "Rebound Chaser"],
            "Defense": ["Challenger", "Glove", "High-Flying Denier", "Immovable Enforcer", "Interceptor",
                       "Off-Ball Pest", "On-Ball Menace", "Paint Patroller", "Pick Dodger", "Post Lockdown"],
            "General Offense": ["Brick Wall", "Slippery Off-Ball"],
            "All Around": ["Pogo Stick"]
        }

        self.niveis = ["None", "Bronze", "Prata", "Ouro", "Hall da Fama"]
        self.descriptions = { ... }  # Mantive as descrições como no código original

        self.sliders = {}
        self.custo_labels = {}
        self.valor_labels = {}

        for categoria, badge_list in self.badges.items():
            group_box = QGroupBox(categoria)
            group_box.setFont(QFont("Segoe UI", 16, QFont.Bold))
            group_box.setStyleSheet("""
                QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding: 15px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            """)
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(10)

            for badge in badge_list:
                nivel = self.badges_temp.get(badge, "None")
                nivel_original = self.jogador.badges.get(badge, "None")
                if badge not in self.badges_temp:
                    self.badges_temp[badge] = nivel

                badge_layout = QHBoxLayout()
                badge_layout.setSpacing(10)

                nome_label = QLabel(f"{badge}")
                nome_label.setFont(QFont("Segoe UI", 14))
                nome_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 5px; border-radius: 3px;")
                nome_label.setFixedWidth(250)
                badge_layout.addWidget(nome_label)

                valor_label = QLabel(f"{nivel}")
                valor_label.setFont(QFont("Segoe UI", 14))
                valor_label.setStyleSheet(f"color: {self.get_cor_nivel(nivel)}; background: #2D2D2D; padding: 5px; border-radius: 3px;")
                valor_label.setFixedWidth(100)
                badge_layout.addWidget(valor_label)

                info_button = QPushButton("ℹ️")
                info_button.setFixedSize(30, 30)
                info_button.setStyleSheet("""
                    QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; font-size: 14px; padding: 0px; }
                    QPushButton:hover { background: #555555; }
                """)
                info_button.clicked.connect(lambda _, b=badge: self.mostrar_descricao(b))
                badge_layout.addWidget(info_button)

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(len(self.niveis) - 1)
                slider.setValue(self.niveis.index(nivel))
                slider.setFixedWidth(150)
                slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                slider.valueChanged.connect(lambda v, n=badge, vl=valor_label: self.atualizar_badge_temp(n, v, vl))
                badge_layout.addWidget(slider)

                dec_button = QPushButton("➖")
                dec_button.setFixedSize(30, 30)
                dec_button.setStyleSheet("""
                    QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #777777); color: #FFFFFF; border-radius: 5px; font-size: 14px; }
                    QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #777777, stop:1 #555555); }
                """)
                dec_button.clicked.connect(lambda _, s=slider, n=badge, vl=valor_label, v=nivel_original: self.diminuir_badge(s, n, vl, v))
                badge_layout.addWidget(dec_button)

                inc_button = QPushButton("➕")
                inc_button.setFixedSize(30, 30)
                inc_button.setStyleSheet("""
                    QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF6200, stop:1 #FF8340); color: #FFFFFF; border-radius: 5px; font-size: 14px; }
                    QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF8340, stop:1 #FF6200); }
                """)
                inc_button.clicked.connect(lambda _, s=slider, n=badge, vl=valor_label: self.incrementar_badge(s, n, vl))
                badge_layout.addWidget(inc_button)

                custo = self.calcular_custo(nivel)
                custo_label = QLabel(f"Custo: {custo}")
                custo_label.setFont(QFont("Segoe UI", 14))
                custo_label.setStyleSheet("color: #FFFFFF;")
                custo_label.setFixedWidth(100)
                badge_layout.addWidget(custo_label)

                self.sliders[badge] = slider
                self.custo_labels[badge] = custo_label
                self.valor_labels[badge] = valor_label
                group_layout.addLayout(badge_layout)

            scroll_layout.addWidget(group_box)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        # Layout dos botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        confirm_button = QPushButton("Confirmar")
        confirm_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF6200, stop:1 #FF8340); color: #FFFFFF; border-radius: 8px; padding: 12px; font-size: 16px; min-width: 150px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF8340, stop:1 #FF6200); }
        """)
        confirm_button.clicked.connect(self.confirmar_alteracoes)
        button_layout.addWidget(confirm_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #777777); color: #FFFFFF; border-radius: 8px; padding: 12px; font-size: 16px; min-width: 150px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #777777, stop:1 #555555); }
        """)
        back_button.clicked.connect(self.back_to_player)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

    def mostrar_descricao(self, badge):
        descricao = self.descriptions.get(badge, "Descrição não disponível.")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f"Descrição de {badge}")
        msg_box.setText(descricao)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def atualizar_badge_temp(self, nome, valor, valor_label):
        nivel_antigo = self.badges_temp[nome]
        nivel_novo = self.niveis[valor]

        if nivel_novo == nivel_antigo:
            return

        nivel_antigo_idx = self.niveis.index(nivel_antigo)
        nivel_novo_idx = self.niveis.index(nivel_novo)

        self.badges_temp[nome] = nivel_novo
        valor_label.setText(f"{nivel_novo}")
        valor_label.setStyleSheet(f"color: {self.get_cor_nivel(nivel_novo)}; background: #2D2D2D; padding: 5px; border-radius: 3px;")
        self.sliders[nome].setValue(valor)

        custo_novo = self.calcular_custo(nivel_novo)
        self.custo_labels[nome].setText(f"Custo: {custo_novo}")

        self.pontos_gastos = 0
        original_badges = self.jogador.badges.copy()
        for badge, novo_nivel in self.badges_temp.items():
            original_nivel = original_badges.get(badge, "None")
            if novo_nivel != original_nivel:
                original_idx = self.niveis.index(original_nivel)
                novo_idx = self.niveis.index(novo_nivel)
                if novo_idx > original_idx:
                    custo_incremental = sum(self.calcular_custo(self.niveis[i]) for i in range(original_idx + 1, novo_idx + 1))
                    self.pontos_gastos += custo_incremental

        self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis} | Gastos: {self.pontos_gastos}")

    def incrementar_badge(self, slider, nome, valor_label):
        valor_atual = slider.value()
        novo_valor = min(valor_atual + 1, len(self.niveis) - 1)
        if novo_valor > valor_atual:
            self.atualizar_badge_temp(nome, novo_valor, valor_label)
            slider.setValue(novo_valor)

    def diminuir_badge(self, slider, nome, valor_label, nivel_original):
        valor_atual = slider.value()
        nivel_original_idx = self.niveis.index(nivel_original)
        novo_valor = max(valor_atual - 1, nivel_original_idx)
        if novo_valor < valor_atual:
            self.atualizar_badge_temp(nome, novo_valor, valor_label)
            slider.setValue(novo_valor)

    def calcular_custo(self, nivel):
        if hasattr(self.jogador, 'custos_badges') and nivel in self.jogador.custos_badges:
            return self.jogador.custos_badges[nivel]
        return {"None": 0, "Bronze": 10, "Prata": 20, "Ouro": 30, "Hall da Fama": 40}.get(nivel, 0)

    def get_cor_nivel(self, nivel):
        if nivel == "None": return "#FFFFFF"
        elif nivel == "Bronze": return "#CD7F32"
        elif nivel == "Prata": return "#C0C0C0"
        elif nivel == "Ouro": return "#FFD700"
        else: return "#800080"

    def confirmar_alteracoes(self):
        custo_total = self.pontos_gastos
        if self.jogador.pontos_disponiveis < custo_total:
            self.show_error("Pontos insuficientes para confirmar as alterações!")
            self.pontos_gastos = 0
            self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis} | Gastos: {self.pontos_gastos}")
            return

        self.jogador.pontos_disponiveis -= custo_total
        self.jogador.badges = self.badges_temp.copy()
        self.jogador.salvar()
        self.show_success("Badges salvas com sucesso!")
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

    def back_to_player(self):
        self.pontos_gastos = 0
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

class InitialBadgesWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle(f"Escolher Badges Iniciais - {self.jogador.nome}")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.badges_temp = self.jogador.badges.copy() if hasattr(self.jogador, 'badges') else {}  # Usa badges existentes ou inicia vazio
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = QLabel(f"Escolher Badges Iniciais de {self.jogador.nome}")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Removido o label de pontos gastos
        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.pontos_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: #2D2D2D; border: none;")
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)
        grid_layout.setSpacing(10)

        # Lista de badges do NBA 2K25
        self.badges = {
            "Inside Scoring": [
                "Aerial Wizard", "Float Game", "Hook Specialist", "Layup Mixmaster", "Paint Prodigy",
                "Physical Finisher", "Post Fade Phenom", "Post Powerhouse", "Post-Up Poet", "Posterizer", "Rise Up"
            ],
            "Outside Scoring": [
                "Deadeye", "Limitless Range", "Mini Marksman", "Set Shot Specialist", "Shifty Shooter"
            ],
            "Playmaking": [
                "Ankle Assassin", "Bail Out", "Break Starter", "Dimer", "Handles For Days",
                "Lightning Launch", "Strong Handle", "Unpluckable", "Versatile Visionary"
            ],
            "Rebounding": [
                "Boxout Beast", "Rebound Chaser"
            ],
            "Defense": [
                "Challenger", "Glove", "High-Flying Denier", "Immovable Enforcer", "Interceptor",
                "Off-Ball Pest", "On-Ball Menace", "Paint Patroller", "Pick Dodger", "Post Lockdown"
            ],
            "General Offense": [
                "Brick Wall", "Slippery Off-Ball"
            ],
            "All Around": [
                "Pogo Stick"
            ]
        }

        # Dicionário com descrições traduzidas
        self.descriptions = {
            "Aerial Wizard": "Aumenta a capacidade de finalizar um alley-oop de um companheiro de equipe ou um rebote ofensivo.",
            "Float Game": "Melhora a habilidade de um jogador para fazer arremessos flutuantes.",
            "Hook Specialist": "Melhora a capacidade de um jogador para fazer arremessos de gancho no poste.",
            "Layup Mixmaster": "Melhora a habilidade de um jogador para finalizar bandejas acrobáticas ou sofisticadas com sucesso.",
            "Paint Prodigy": "Melhora a capacidade de um jogador para marcar enquanto trabalha na área pintada.",
            "Physical Finisher": "Melhora a habilidade de um jogador para resistir ao contato e converter bandejas.",
            "Post Fade Phenom": "Melhora a capacidade de um jogador para fazer arremessos de fadeaway e saltos no poste.",
            "Post Powerhouse": "Fortalece a habilidade de um jogador para empurrar os defensores para trás e derrubá-los com dropsteps.",
            "Post-Up Poet": "Aumenta as chances de enganar ou superar o defensor, assim como de marcar, ao realizar movimentos no poste.",
            "Posterizer": "Aumenta as chances de posterizar o defensor com uma enterrada em um contra-ataque.",
            "Rise Up": "Aumenta a probabilidade de enterrar ou posterizar o oponente quando está na área pintada.",
            "Challenger": "Melhora a eficácia de contestações bem cronometradas contra arremessadores de perímetro.",
            "Glove": "Aumenta a capacidade de roubar ou bloquear bandejas e tentativas de arremesso com sucesso.",
            "High-Flying Denier": "Aumenta a capacidade do defensor de antecipar uma tentativa de bloqueio.",
            "Immovable Enforcer": "Melhora a força de um defensor ao defender manejadores de bola que vêm diretamente contra ele.",
            "Interceptor": "Aumenta significativamente a frequência de passes interceptados ou desviados com sucesso.",
            "Off-Ball Pest": "Torna mais difícil para os oponentes se abrirem e manterem a marcação.",
            "On-Ball Menace": "Pressiona e marca de perto no perímetro.",
            "Paint Patroller": "Aumenta a capacidade de um jogador para bloquear ou contestar arremessos na área pintada.",
            "Pick Dodger": "Melhora a capacidade de um jogador para navegar por bloqueios e ao redor deles enquanto está na defesa.",
            "Post Lockdown": "Fortalece a capacidade de um jogador para defender o poste de forma eficaz, com maior chance de desarmar o oponente.",
            "Deadeye": "Arremessos de salto feitos com um defensor fechando recebem uma penalidade menor na contestação.",
            "Limitless Range": "Estende a distância a partir da qual um jogador pode arremessar três pontos de longa distância de forma eficaz.",
            "Mini Marksman": "Aumenta a probabilidade de acertar arremessos de salto sobre um defensor mais alto.",
            "Set Shot Specialist": "Aumenta as chances de acertar arremessos de salto estacionários.",
            "Shifty Shooter": "Melhora a capacidade de um jogador para acertar arremessos de salto com dribles difíceis.",
            "Ankle Assassin": "Aumenta a probabilidade de o defensor ter os tornozelos quebrados ou ser cruzado.",
            "Bail Out": "Facilita passes errados em bandejas, ajudando a passar de duplas marcações.",
            "Break Starter": "Após agarrar um rebote defensivo, passes longos para o outro lado da quadra são mais rápidos e precisos.",
            "Dimer": "Quando na meia-quadra, os passes têm 10% mais chance de acerto.",
            "Handles For Days": "Um jogador perde menos energia com movimentos consecutivos de drible, permitindo encadear combos mais rapidamente e por períodos mais longos.",
            "Lightning Launch": "Acelera o lançamento ao atacar a partir do perímetro.",
            "Strong Handle": "Reduz a probabilidade de ser desarmado ao driblar.",
            "Unpluckable": "Os defensores têm dificuldade em roubar a bola com tentativas de desarme.",
            "Versatile Visionary": "Melhora a capacidade de um jogador para passar rapidamente a bola para um companheiro aberto, incluindo alley-oops e passes rápidos no tempo certo.",
            "Boxout Beast": "Melhora a capacidade de um jogador para bloquear e lutar por uma boa posição de rebote.",
            "Rebound Chaser": "Melhora a capacidade de um jogador para perseguir rebotes a distâncias maiores que o normal.",
            "Brick Wall": "Aumenta a eficácia de bloqueios e drena a energia dos oponentes em contato físico.",
            "Slippery Off-Ball": "Quando tenta se abrir, o jogador navega eficazmente por tráfego intenso.",
            "Pogo Stick": "Permite que os jogadores se recuperem rapidamente e subam novamente para outro salto, tentativa de bloqueio ou rebote."
        }

        self.niveis = ["None", "Bronze", "Prata", "Ouro", "Hall da Fama"]
        self.sliders = {}
        row = 0
        for category, badge_list in self.badges.items():
            # Título da categoria
            category_label = QLabel(category)
            category_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
            category_label.setStyleSheet("color: #FF6200;")
            grid_layout.addWidget(category_label, row, 0, 1, 2)
            row += 1

            for i, badge in enumerate(badge_list):
                col = 0 if i % 2 == 0 else 2
                badge_row = row + (i // 2)
                badge_layout = QHBoxLayout()
                badge_layout.setSpacing(10)

                nivel = self.badges_temp.get(badge, "None")
                if badge not in self.badges_temp:
                    self.badges_temp[badge] = nivel

                # Label com o nome da badge
                badge_label = QLabel(f"{badge}: {nivel}")
                badge_label.setFont(QFont("Segoe UI", 14))
                badge_label.setFixedWidth(200)
                self.atualizar_cor_label(badge_label, nivel)
                badge_layout.addWidget(badge_label)

                # Botão de informação
                info_button = QPushButton("ℹ️")
                info_button.setFixedSize(30, 30)
                info_button.setStyleSheet("""
                    QPushButton { 
                        background: #2D2D2D; 
                        color: #FFFFFF; 
                        border-radius: 5px; 
                        font-size: 14px; 
                        padding: 0px; 
                    }
                    QPushButton:hover { 
                        background: #555555; 
                    }
                """)
                info_button.clicked.connect(lambda _, b=badge: self.mostrar_descricao(b))
                badge_layout.addWidget(info_button)

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(0)
                slider.setMaximum(len(self.niveis) - 1)
                slider.setValue(self.niveis.index(nivel))
                slider.valueChanged.connect(lambda v, n=badge, l=badge_label: self.atualizar_badge_temp(n, v, l))
                badge_layout.addWidget(slider)

                # Removido o label de custo, pois é gratuito
                self.sliders[badge] = slider
                grid_layout.addLayout(badge_layout, badge_row, col, 1, 2)

            row += (len(badge_list) + 1) // 2

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        confirm_button = QPushButton("Confirmar")
        confirm_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 12px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        confirm_button.clicked.connect(self.confirmar_badges)
        button_layout.addWidget(confirm_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 12px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_atributos)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

    def mostrar_descricao(self, badge):
        descricao = self.descriptions.get(badge, "Descrição não disponível.")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f"Descrição de {badge}")
        msg_box.setText(descricao)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #FFFFFF; 
            QLabel { color: #000000; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def atualizar_badge_temp(self, nome, valor, label):
        nivel_antigo = self.badges_temp[nome]
        nivel_novo = self.niveis[valor]

        if nivel_novo == nivel_antigo:
            return

        self.badges_temp[nome] = nivel_novo
        label.setText(f"{nome}: {nivel_novo}")
        self.atualizar_cor_label(label, nivel_novo)

    def calcular_custo(self, nivel):
        # Método mantido por compatibilidade, mas agora sempre retorna 0
        return 0

    def atualizar_cor_label(self, label, nivel):
        if nivel == "None":
            label.setStyleSheet("color: #FFFFFF;")
        elif nivel == "Bronze":
            label.setStyleSheet("color: #CD7F32;")
        elif nivel == "Prata":
            label.setStyleSheet("color: #C0C0C0;")
        elif nivel == "Ouro":
            label.setStyleSheet("color: #FFD700;")
        else:  # Hall da Fama
            label.setStyleSheet("color: #800080;")  # Roxo

    def confirmar_badges(self):
        # Removida a verificação de pontos insuficientes
        self.jogador.badges = self.badges_temp.copy()
        self.jogador.salvar()
        self.show_success("Badges iniciais salvas com sucesso!")

        # Abrir diálogo de escolha de dificuldade
        dialogo = EscolhaDificuldadeDialog(self.jogador, self)
        if dialogo.exec_():
            if dialogo.predefinida_radio.isChecked():
                self.config_window = EscolhaDificuldadeWindow(self.jogador, self.parent)
                self.config_window.show()
            elif dialogo.personalizada_radio.isChecked():
                self.config_window = ConfiguracaoPersonalizadaWindow(self.jogador, self.parent)
                self.config_window.show()
            self.close()

    def back_to_atributos(self):
        self.parent.show()
        self.close()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

# Diálogo de escolha de dificuldade
class EscolhaDificuldadeDialog(QDialog):
    def __init__(self, jogador, parent=None, modo=None):
        super().__init__(parent)
        self.jogador = jogador  # Armazena o jogador
        self.modo = modo  # Armazena o modo (pode ser usado para lógica futura)
        self.setWindowTitle("Escolher Tipo de Dificuldade")
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Escolha o tipo de dificuldade:")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.predefinida_radio = QRadioButton("Dificuldade Predefinida")
        self.predefinida_radio.setFont(QFont("Segoe UI", 14))
        self.predefinida_radio.setStyleSheet("color: #FFFFFF;")
        self.predefinida_radio.setChecked(True)
        layout.addWidget(self.predefinida_radio)

        self.personalizada_radio = QRadioButton("Configuração Personalizada")
        self.personalizada_radio.setFont(QFont("Segoe UI", 14))
        self.personalizada_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.personalizada_radio)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def get_choice(self):
        """Retorna a escolha do usuário: 'predefinida' ou 'personalizada'."""
        if self.predefinida_radio.isChecked():
            return "predefinida"
        return "personalizada"

class EscolhaDificuldadeDialog(QDialog):
    def __init__(self, jogador, parent=None, modo=None):
        super().__init__(parent)
        self.jogador = jogador  # Armazena o jogador
        self.modo = modo  # Armazena o modo (pode ser usado para lógica futura)
        self.setWindowTitle("Escolher Tipo de Dificuldade")
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Escolha o tipo de dificuldade:")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.predefinida_radio = QRadioButton("Dificuldade Predefinida")
        self.predefinida_radio.setFont(QFont("Segoe UI", 14))
        self.predefinida_radio.setStyleSheet("color: #FFFFFF;")
        self.predefinida_radio.setChecked(True)
        layout.addWidget(self.predefinida_radio)

        self.personalizada_radio = QRadioButton("Configuração Personalizada")
        self.personalizada_radio.setFont(QFont("Segoe UI", 14))
        self.personalizada_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.personalizada_radio)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def get_choice(self):
        """Retorna a escolha do usuário: 'predefinida' ou 'personalizada'."""
        if self.predefinida_radio.isChecked():
            return "predefinida"
        return "personalizada"

class AtributosDoJogadorWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        if not hasattr(self.jogador, 'pontos_disponiveis'):
            self.jogador.pontos_disponiveis = 10000
        if not hasattr(self.jogador, 'atributos'):
            self.jogador.atributos = {}
        self.parent = parent
        self.setWindowTitle(f"Atributos de {self.jogador.nome}")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.pontos_gastos = 0
        self.atributos_temp = self.jogador.atributos.copy()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(10)

        title = QLabel(f"Atributos de {self.jogador.nome}")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #FF6200; padding: 5px; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2D2D2D, stop:1 #1A1A1A); border-radius: 5px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis} | Gastos: {self.pontos_gastos}")
        self.pontos_label.setFont(QFont("Segoe UI", 14))
        self.pontos_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 5px; border-radius: 5px;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.pontos_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)

        self.atributos_categorias = {
            "Finishing": ["Driving Layup", "Post Fade", "Post Hook", "Post Control", "Draw Foul", "Standing Dunk", "Driving Dunk"],
            "Shooting": ["Close Shot", "Mid-Range Shot", "Three-Point Shot", "Free Throw", "Shot IQ"],
            "Playmaking": ["Ball Handle", "Pass IQ", "Pass Accuracy", "Pass Vision", "Hands", "Pass Perception"],
            "Rebounding": ["Offensive Rebound", "Defensive Rebound"],
            "Defense": ["Interior Defense", "Perimeter Defense", "Block", "Steal", "Defensive Consistency", "Help Defense IQ"],
            "Physicals": ["Speed", "Speed With Ball", "Vertical", "Strength", "Stamina", "Hustle", "Agility"],
            "General": ["Offensive Consistency", "Intangibles"]
        }

        self.sliders = {}
        self.valor_labels = {}
        self.custo_labels = {}

        for categoria, atributo_list in self.atributos_categorias.items():
            group_box = QGroupBox(categoria)
            group_box.setFont(QFont("Segoe UI", 16, QFont.Bold))
            group_box.setStyleSheet("""
                QGroupBox { color: #FF6200; background-color: #2D2D2D; border: 2px solid #FF6200; border-radius: 8px; padding: 15px; }
                QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }
            """)
            group_layout = QVBoxLayout(group_box)
            group_layout.setSpacing(10)

            for atributo in atributo_list:
                valor = self.atributos_temp.get(atributo, 25)
                valor_original = self.jogador.atributos.get(atributo, 25)

                atributo_layout = QHBoxLayout()
                atributo_layout.setSpacing(10)

                nome_label = QLabel(f"{atributo}")
                nome_label.setFont(QFont("Segoe UI", 14))
                nome_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 5px; border-radius: 3px;")
                nome_label.setFixedWidth(250)
                atributo_layout.addWidget(nome_label)

                valor_label = QLabel(f"{valor}")
                valor_label.setFont(QFont("Segoe UI", 14))
                valor_label.setStyleSheet("color: #FFFFFF; background: #2D2D2D; padding: 5px; border-radius: 3px;")
                valor_label.setFixedWidth(50)
                atributo_layout.addWidget(valor_label)

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(25)
                slider.setMaximum(99)
                slider.setValue(valor)
                slider.setFixedWidth(150)
                slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                slider.valueChanged.connect(lambda v, n=atributo, vl=valor_label: self.atualizar_atributo_temp(n, v, vl))
                atributo_layout.addWidget(slider)

                dec_button = QPushButton("➖")
                dec_button.setFixedSize(30, 30)
                dec_button.setStyleSheet("""
                    QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #777777); color: #FFFFFF; border-radius: 5px; font-size: 14px; }
                    QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #777777, stop:1 #555555); }
                """)
                dec_button.clicked.connect(lambda _, s=slider, n=atributo, vl=valor_label, v=valor_original: self.diminuir_atributo(s, n, vl, v))
                atributo_layout.addWidget(dec_button)

                inc_button = QPushButton("➕")
                inc_button.setFixedSize(30, 30)
                inc_button.setStyleSheet("""
                    QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF6200, stop:1 #FF8340); color: #FFFFFF; border-radius: 5px; font-size: 14px; }
                    QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF8340, stop:1 #FF6200); }
                """)
                inc_button.clicked.connect(lambda _, s=slider, n=atributo, vl=valor_label: self.incrementar_atributo(s, n, vl))
                atributo_layout.addWidget(inc_button)

                custo = self.calcular_custo(valor, valor_original)
                custo_label = QLabel(f"Custo: {custo}")
                custo_label.setFont(QFont("Segoe UI", 14))
                custo_label.setStyleSheet("color: #FFFFFF;")
                custo_label.setFixedWidth(100)
                atributo_layout.addWidget(custo_label)

                self.sliders[atributo] = slider
                self.valor_labels[atributo] = valor_label
                self.custo_labels[atributo] = custo_label
                group_layout.addLayout(atributo_layout)

            scroll_layout.addWidget(group_box)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        confirm_button = QPushButton("Confirmar")
        confirm_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF6200, stop:1 #FF8340); color: #FFFFFF; border-radius: 8px; padding: 12px; font-size: 16px; min-width: 150px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FF8340, stop:1 #FF6200); }
        """)
        confirm_button.clicked.connect(self.confirmar_alteracoes)
        button_layout.addWidget(confirm_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #777777); color: #FFFFFF; border-radius: 8px; padding: 12px; font-size: 16px; min-width: 150px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #777777, stop:1 #555555); }
        """)
        back_button.clicked.connect(self.back_to_player)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

    def atualizar_atributo_temp(self, nome, valor, valor_label):
        valor_antigo = self.atributos_temp.get(nome, 25)
        if valor == valor_antigo:
            return

        self.atributos_temp[nome] = valor
        valor_label.setText(f"{valor}")
        self.sliders[nome].setValue(valor)

        valor_original = self.jogador.atributos.get(nome, 25)
        custo_novo = self.calcular_custo(valor, valor_original)
        self.custo_labels[nome].setText(f"Custo: {custo_novo}")

        self.pontos_gastos = self.calcular_pontos_gastos_total()
        self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis} | Gastos: {self.pontos_gastos}")

    def incrementar_atributo(self, slider, nome, valor_label):
        valor_atual = slider.value()
        novo_valor = min(valor_atual + 1, 99)
        if novo_valor > valor_atual:
            self.atualizar_atributo_temp(nome, novo_valor, valor_label)
            slider.setValue(novo_valor)

    def diminuir_atributo(self, slider, nome, valor_label, valor_original):
        valor_atual = slider.value()
        novo_valor = max(valor_atual - 1, valor_original)
        if novo_valor < valor_atual:
            self.atualizar_atributo_temp(nome, novo_valor, valor_label)
            slider.setValue(novo_valor)

    def calcular_custo(self, valor_atual, valor_original):
        """Calcula o custo total somando o custo de cada ponto entre valor_original e valor_atual."""
        if valor_atual <= valor_original:
            return 0

        faixas = [
            (0, 69, self.jogador.custos_atributos.get("0-69", 100)),
            (70, 74, self.jogador.custos_atributos.get("70-74", 150)),
            (75, 79, self.jogador.custos_atributos.get("75-79", 200)),
            (80, 84, self.jogador.custos_atributos.get("80-84", 250)),
            (85, 89, self.jogador.custos_atributos.get("85-89", 300)),
            (90, 94, self.jogador.custos_atributos.get("90-94", 400)),
            (95, 99, self.jogador.custos_atributos.get("95-99", 500))
        ]

        custo_total = 0
        for ponto in range(valor_original + 1, valor_atual + 1):
            for inicio, fim, custo in faixas:
                if inicio <= ponto <= fim:
                    custo_total += custo
                    break

        return custo_total

    def calcular_pontos_gastos_total(self):
        total = 0
        original_atributos = self.jogador.atributos.copy()
        for attr, novo_valor in self.atributos_temp.items():
            original_valor = original_atributos.get(attr, 25)
            total += self.calcular_custo(novo_valor, original_valor)
        return total

    def confirmar_alteracoes(self):
        custo_total = self.calcular_pontos_gastos_total()
        if self.jogador.pontos_disponiveis < custo_total:
            self.show_error("Pontos insuficientes para confirmar as alterações!")
            return

        self.jogador.pontos_disponiveis -= custo_total
        self.jogador.atributos = self.atributos_temp.copy()
        self.jogador.salvar()
        self.show_success("Atributos salvos com sucesso!")
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

    def back_to_player(self):
        self.pontos_gastos = 0
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; 
            QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

class EscolhaDificuldadeDialog(QDialog):
    def __init__(self, jogador, parent=None, modo=None):
        super().__init__(parent)
        self.jogador = jogador  # Armazena o jogador
        self.modo = modo  # Armazena o modo (pode ser usado para lógica futura)
        self.setWindowTitle("Escolher Tipo de Dificuldade")
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Escolha o tipo de dificuldade:")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.predefinida_radio = QRadioButton("Dificuldade Predefinida")
        self.predefinida_radio.setFont(QFont("Segoe UI", 14))
        self.predefinida_radio.setStyleSheet("color: #FFFFFF;")
        self.predefinida_radio.setChecked(True)
        layout.addWidget(self.predefinida_radio)

        self.personalizada_radio = QRadioButton("Configuração Personalizada")
        self.personalizada_radio.setFont(QFont("Segoe UI", 14))
        self.personalizada_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.personalizada_radio)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def get_choice(self):
        """Retorna a escolha do usuário: 'predefinida' ou 'personalizada'."""
        if self.predefinida_radio.isChecked():
            return "predefinida"
        return "personalizada"

class PerfilWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Perfil do Jogador")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #1A1A1A;")
        print(f"PerfilWindow - Inicializando para {self.jogador.nome}")
        print(f"Posição inicial: {self.jogador.posicao}, Posições compradas primárias: {self.jogador.posicoes_compradas_primarias}")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Perfil do Jogador")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pontos_label)

        altura_m = self.jogador.altura
        altura_pes_total = altura_m / 0.0254
        feet = int(altura_pes_total // 12)
        inches = int(altura_pes_total % 12)
        self.info_label = QLabel(
            f"Nome: {self.jogador.nome}\n"
            f"Altura: {feet}'{inches}\"\n"
            f"Time: {self.jogador.time}\n"
            f"Ano de Início: {self.jogador.ano_inicio}\n"
            f"Posição Primária: {self.jogador.posicao}\n"
            f"Posição Secundária: {self.jogador.posicao_secundaria if self.jogador.posicao_secundaria else 'Nenhuma'}"
        )
        self.info_label.setFont(QFont("Segoe UI", 16))
        self.info_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.info_label)

        posicao_primaria_layout = QHBoxLayout()
        posicao_primaria_label = QLabel("Posição Primária (1000 pontos):")
        posicao_primaria_label.setFont(QFont("Segoe UI", 14))
        posicao_primaria_label.setStyleSheet("color: #FFFFFF;")
        self.posicao_primaria_combo = QComboBox()
        posicoes = ["PG", "SG", "SF", "PF", "C"]
        self.posicao_primaria_combo.addItems([f"{pos} ✓" if pos in self.jogador.posicoes_compradas_primarias else pos for pos in posicoes])
        # Garantir que a posição atual seja pré-selecionada
        posicao_atual_com_marcador = f"{self.jogador.posicao} ✓" if self.jogador.posicao in self.jogador.posicoes_compradas_primarias else self.jogador.posicao
        if posicao_atual_com_marcador in [self.posicao_primaria_combo.itemText(i) for i in range(self.posicao_primaria_combo.count())]:
            self.posicao_primaria_combo.setCurrentText(posicao_atual_com_marcador)
        else:
            self.posicao_primaria_combo.setCurrentText(self.jogador.posicao)  # Fallback para a posição sem marcador
        self.posicao_primaria_combo.setFont(QFont("Segoe UI", 14))
        self.posicao_primaria_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        posicao_primaria_buy_button = QPushButton("Comprar")
        posicao_primaria_buy_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        posicao_primaria_buy_button.clicked.connect(self.comprar_posicao_primaria)
        posicao_primaria_layout.addWidget(posicao_primaria_label)
        posicao_primaria_layout.addWidget(self.posicao_primaria_combo)
        posicao_primaria_layout.addWidget(posicao_primaria_buy_button)
        layout.addLayout(posicao_primaria_layout)

        posicao_secundaria_layout = QHBoxLayout()
        posicao_secundaria_label = QLabel("Posição Secundária (500 pontos):")
        posicao_secundaria_label.setFont(QFont("Segoe UI", 14))
        posicao_secundaria_label.setStyleSheet("color: #FFFFFF;")
        self.posicao_secundaria_combo = QComboBox()
        self.posicao_secundaria_combo.addItems([f"{pos} ✓" if pos in self.jogador.posicoes_compradas_secundarias else pos for pos in posicoes] + ["Nenhuma"])
        if self.jogador.posicao_secundaria:
            self.posicao_secundaria_combo.setCurrentText(self.jogador.posicao_secundaria)
        else:
            self.posicao_secundaria_combo.setCurrentText("Nenhuma")
        self.posicao_secundaria_combo.setFont(QFont("Segoe UI", 14))
        self.posicao_secundaria_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        posicao_secundaria_buy_button = QPushButton("Comprar")
        posicao_secundaria_buy_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        posicao_secundaria_buy_button.clicked.connect(self.comprar_posicao_secundaria)
        posicao_secundaria_layout.addWidget(posicao_secundaria_label)
        posicao_secundaria_layout.addWidget(self.posicao_secundaria_combo)
        posicao_secundaria_layout.addWidget(posicao_secundaria_buy_button)
        layout.addLayout(posicao_secundaria_layout)

        time_layout = QHBoxLayout()
        time_label = QLabel("Time (Gratuito):")
        time_label.setFont(QFont("Segoe UI", 14))
        time_label.setStyleSheet("color: #FFFFFF;")
        self.time_combo = QComboBox()
        times_nba = [
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
            "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
            "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
            "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
            "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
            "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
            "Utah Jazz", "Washington Wizards"
        ]
        self.time_combo.addItems(times_nba)
        self.time_combo.setCurrentText(self.jogador.time)
        self.time_combo.setFont(QFont("Segoe UI", 14))
        self.time_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_combo)
        layout.addLayout(time_layout)

        confirm_button = QPushButton("Confirmar Alterações")
        confirm_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        confirm_button.clicked.connect(self.confirmar_alteracoes)
        layout.addWidget(confirm_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_player)
        layout.addWidget(back_button)

        layout.addStretch()

    def comprar_posicao_primaria(self):
        nova_posicao = self.posicao_primaria_combo.currentText().replace(" ✓", "")
        if nova_posicao not in self.jogador.posicoes_compradas_primarias:
            if self.jogador.pontos_disponiveis < 1000:
                self.show_error("Você precisa de 1000 pontos para comprar uma nova posição primária!")
                return
            self.jogador.pontos_disponiveis -= 1000
            self.jogador.posicoes_compradas_primarias.append(nova_posicao)
            self.show_success(f"Posição primária '{nova_posicao}' comprada com sucesso!")
        self.jogador.posicao = nova_posicao
        self.jogador.salvar()
        self.atualizar_interface()

    def comprar_posicao_secundaria(self):
        nova_posicao = self.posicao_secundaria_combo.currentText().replace(" ✓", "")
        if nova_posicao == "Nenhuma":
            self.jogador.posicao_secundaria = None
            self.jogador.salvar()
            self.atualizar_interface()
            self.show_success("Posição secundária removida!")
            return
        if nova_posicao not in self.jogador.posicoes_compradas_secundarias:
            if self.jogador.pontos_disponiveis < 500:
                self.show_error("Você precisa de 500 pontos para comprar uma nova posição secundária!")
                return
            self.jogador.pontos_disponiveis -= 500
            self.jogador.posicoes_compradas_secundarias.append(nova_posicao)
            self.show_success(f"Posição secundária '{nova_posicao}' comprada com sucesso!")
        self.jogador.posicao_secundaria = nova_posicao
        self.jogador.salvar()
        self.atualizar_interface()

    def confirmar_alteracoes(self):
        nova_posicao_primaria = self.posicao_primaria_combo.currentText().replace(" ✓", "")
        nova_posicao_secundaria = self.posicao_secundaria_combo.currentText().replace(" ✓", "")
        novo_time = self.time_combo.currentText()

        if nova_posicao_primaria in self.jogador.posicoes_compradas_primarias:
            self.jogador.posicao = nova_posicao_primaria
        else:
            self.show_error("Você precisa comprar a nova posição primária antes de selecioná-la!")
            return

        if nova_posicao_secundaria == "Nenhuma":
            self.jogador.posicao_secundaria = None
        elif nova_posicao_secundaria in self.jogador.posicoes_compradas_secundarias:
            self.jogador.posicao_secundaria = nova_posicao_secundaria
        else:
            self.show_error("Você precisa comprar a posição secundária antes de selecioná-la!")
            return

        self.jogador.time = novo_time

        self.jogador.salvar()
        self.atualizar_interface()
        self.parent.atualizar_status()
        self.show_success("Alterações salvas com sucesso!")

    def atualizar_interface(self):
        altura_m = self.jogador.altura
        altura_pes_total = altura_m / 0.0254
        feet = int(altura_pes_total // 12)
        inches = int(altura_pes_total % 12)
        self.info_label.setText(
            f"Nome: {self.jogador.nome}\n"
            f"Altura: {feet}'{inches}\"\n"
            f"Time: {self.jogador.time}\n"
            f"Ano de Início: {self.jogador.ano_inicio}\n"
            f"Posição Primária: {self.jogador.posicao}\n"
            f"Posição Secundária: {self.jogador.posicao_secundaria if self.jogador.posicao_secundaria else 'Nenhuma'}"
        )
        self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.atualizar_posicoes_combo()

    def atualizar_posicoes_combo(self):
        posicoes = ["PG", "SG", "SF", "PF", "C"]
        self.posicao_primaria_combo.clear()
        self.posicao_primaria_combo.addItems([f"{pos} ✓" if pos in self.jogador.posicoes_compradas_primarias else pos for pos in posicoes])
        # Garantir que a posição atual seja pré-selecionada
        posicao_atual_com_marcador = f"{self.jogador.posicao} ✓" if self.jogador.posicao in self.jogador.posicoes_compradas_primarias else self.jogador.posicao
        if posicao_atual_com_marcador in [self.posicao_primaria_combo.itemText(i) for i in range(self.posicao_primaria_combo.count())]:
            self.posicao_primaria_combo.setCurrentText(posicao_atual_com_marcador)
        else:
            self.posicao_primaria_combo.setCurrentText(self.jogador.posicao)  # Fallback para a posição sem marcador
        self.posicao_secundaria_combo.clear()
        self.posicao_secundaria_combo.addItems([f"{pos} ✓" if pos in self.jogador.posicoes_compradas_secundarias else pos for pos in posicoes] + ["Nenhuma"])
        if self.jogador.posicao_secundaria:
            self.posicao_secundaria_combo.setCurrentText(self.jogador.posicao_secundaria)
        else:
            self.posicao_secundaria_combo.setCurrentText("Nenhuma")

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_player(self):
        self.jogador.salvar()
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class EstatisticasWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Adicionar Estatísticas do Jogo")
        self.setMinimumSize(800, 400)  # Ajustei a altura mínima, já que não exibo estatísticas
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        title = QLabel("Adicionar Estatísticas do Jogo")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Label de Pontos Disponíveis
        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF; padding: 10px; background: #2D2D2D; border-radius: 5px;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        self.pontos_label.setFixedHeight(50)
        main_layout.addWidget(self.pontos_label)

        # Grid para campos de entrada
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)
        self.stats_inputs = {}

        stats_list = ["Pontos", "Assistências", "Rebotes", "Steal", "Block", "Turnover"]
        for idx, stat in enumerate(stats_list):
            row = idx // 2
            col = (idx % 2) * 2

            label = QLabel(f"{stat}:")
            label.setFont(QFont("Segoe UI", 16))
            label.setStyleSheet("color: #FFFFFF;")
            label.setAlignment(Qt.AlignRight)
            label.setFixedWidth(150)

            input_field = QLineEdit("0")
            input_field.setFont(QFont("Segoe UI", 16))
            input_field.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 10px;")
            input_field.setFixedWidth(200)
            input_field.setFixedHeight(40)

            self.stats_inputs[stat] = input_field
            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(input_field, row, col + 1)

        # Checkbox "Player of the Game"
        self.player_of_game_check = QCheckBox("Player of the Game")
        self.player_of_game_check.setFont(QFont("Segoe UI", 16))
        self.player_of_game_check.setStyleSheet("color: #FFFFFF;")
        self.player_of_game_check.setFixedHeight(40)
        grid_layout.addWidget(self.player_of_game_check, len(stats_list) // 2, 0, 1, 4, Qt.AlignCenter)

        # Ajustar o grid para ocupar a largura total
        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        grid_widget.setStyleSheet("background: #2D2D2D; border-radius: 5px; padding: 10px;")
        main_layout.addWidget(grid_widget)

        # Botões
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        add_button = QPushButton("Adicionar Estatísticas")
        add_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        add_button.setFixedHeight(50)
        add_button.clicked.connect(self.adicionar_estatisticas)
        button_layout.addWidget(add_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFixedHeight(50)
        back_button.clicked.connect(self.back_to_player)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

        # Espaçamento final
        main_layout.addStretch()

    def adicionar_estatisticas(self):
        try:
            pontos = int(self.stats_inputs["Pontos"].text())
            assistencias = int(self.stats_inputs["Assistências"].text())
            rebotes = int(self.stats_inputs["Rebotes"].text())
            steals = int(self.stats_inputs["Steal"].text())
            blocks = int(self.stats_inputs["Block"].text())
            turnovers = int(self.stats_inputs["Turnover"].text())
        except ValueError:
            self.show_error("Insira valores numéricos válidos!")
            return

        estatisticas_jogo = {
            "Pontos": pontos, "Assistências": assistencias, "Rebotes": rebotes,
            "Steal": steals, "Block": blocks, "Turnover": turnovers
        }
        pontos_ganhos = self.calcular_pontos_ganhos(estatisticas_jogo)

        # Adicionar 10 pontos se "Player of the Game" estiver marcado
        if self.player_of_game_check.isChecked():
            pontos_ganhos += 10

        self.jogador.adicionar_estatisticas(pontos, assistencias, rebotes, steals, blocks, turnovers)
        self.jogador.pontos_disponiveis += pontos_ganhos
        self.jogador.salvar()

        self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.parent.atualizar_status()

        self.show_success(
            f"Estatísticas adicionadas!\n"
            f"Pontos: {pontos}, Assistências: {assistencias}, Rebotes: {rebotes}, "
            f"Steals: {steals}, Blocks: {blocks}, Turnovers: {turnovers}\n"
            f"Pontos ganhos: {pontos_ganhos}"
        )

    def calcular_pontos_ganhos(self, estatisticas_jogo):
        pontos_ganhos = 0
        if not hasattr(self.jogador, 'dificuldade') or not self.jogador.dificuldade:
            self.show_error("Nenhuma configuração de dificuldade definida!")
            return pontos_ganhos

        # Verificar o formato de self.jogador.dificuldade
        dificuldade = self.jogador.dificuldade
        if isinstance(list(dificuldade.values())[0], dict):  # Configuração Personalizada
            for stat, valor in estatisticas_jogo.items():
                if stat in dificuldade:
                    meta = dificuldade[stat]["meta"]
                    pontos_por_meta = dificuldade[stat]["pontos"]
                    vezes_atingida = valor // meta  # Quantas vezes a meta foi alcançada
                    pontos_ganhos += vezes_atingida * pontos_por_meta
        else:  # Dificuldade Predefinida
            for stat, valor in estatisticas_jogo.items():
                if stat in dificuldade:
                    pontos_ganhos += valor * dificuldade[stat]

        return pontos_ganhos

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_player(self):
        self.parent.show()
        self.close()

class AtributosWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Definir Atributos Iniciais")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = QLabel("Definir Atributos Iniciais")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        self.pontos_label = QLabel("Pontos Usados: 0")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.pontos_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: #2D2D2D; border: none;")
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)
        grid_layout.setSpacing(10)

        self.atributos = [
            "Driving Layup", "Post Fade", "Post Hook", "Post Control", "Draw Foul",
            "Close Shot", "Mid-Range Shot", "Three-Point Shot", "Free Throw",
            "Ball Handle", "Pass IQ", "Pass Accuracy", "Offensive Rebound",
            "Standing Dunk", "Driving Dunk", "Shot IQ", "Pass Vision",
            "Hands", "Defensive Rebound", "Interior Defense", "Perimeter Defense",
            "Block", "Steal", "Speed", "Speed With Ball", "Vertical",
            "Strength", "Stamina", "Hustle", "Agility", "Pass Perception",
            "Defensive Consistency", "Help Defense IQ", "Offensive Consistency", "Intangibles"
        ]
        self.inputs = {}
        for i, attr in enumerate(self.atributos):
            row = i // 2
            col = 0 if i % 2 == 0 else 2
            attr_layout = QHBoxLayout()
            attr_layout.setSpacing(10)
            label = QLabel(f"{attr}:")
            label.setFont(QFont("Segoe UI", 14))
            label.setStyleSheet("color: #FFFFFF;")
            label.setFixedWidth(200)
            spin_box = QSpinBox()
            spin_box.setRange(0, 99)
            spin_box.setValue(25)
            spin_box.setFont(QFont("Segoe UI", 14))
            spin_box.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            spin_box.setFixedWidth(100)
            spin_box.valueChanged.connect(lambda value, sb=spin_box: self.atualizar_pontos_e_cor(sb))
            attr_layout.addWidget(label)
            attr_layout.addWidget(spin_box)
            self.inputs[attr] = spin_box
            grid_layout.addLayout(attr_layout, row, col, 1, 2)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        confirm_button = QPushButton("Confirmar")
        confirm_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 12px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        confirm_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        confirm_button.clicked.connect(self.confirmar_atributos)
        button_layout.addWidget(confirm_button)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 12px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        back_button.clicked.connect(self.back_to_main)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

        self.atualizar_pontos_e_cor()

    def atualizar_pontos_e_cor(self, spin_box=None):
        total_usado = sum(spin_box.value() for spin_box in self.inputs.values())
        pontos_usados = total_usado - len(self.atributos) * 25
        self.pontos_label.setText(f"Pontos Usados: {pontos_usados}")

        for spin_box in self.inputs.values():
            valor = spin_box.value()
            if 0 <= valor <= 74:
                spin_box.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            elif 75 <= valor <= 84:
                spin_box.setStyleSheet("background: #2E7D32; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            elif 85 <= valor <= 94:
                spin_box.setStyleSheet("background: #1976D2; color: #FFFFFF; border-radius: 5px; padding: 5px;")
            elif 95 <= valor <= 99:
                spin_box.setStyleSheet("background: #7B1FA2; color: #FFFFFF; border-radius: 5px; padding: 5px;")

    def confirmar_atributos(self):
        for attr, spin_box in self.inputs.items():
            self.jogador.atributos[attr] = spin_box.value()
        self.jogador.salvar()

        # Abrir a tela de configuração de badges iniciais
        self.initial_badges_window = InitialBadgesWindow(self.jogador, self)
        self.initial_badges_window.show()
        self.hide()

    def back_to_main(self):
        self.parent.show()
        self.close()


class EscolhaDificuldadeDialog(QDialog):
    def __init__(self, jogador, parent=None, modo=None):
        super().__init__(parent)
        self.jogador = jogador  # Armazena o jogador
        self.modo = modo  # Armazena o modo (pode ser usado para lógica futura)
        self.setWindowTitle("Escolher Tipo de Dificuldade")
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Escolha o tipo de dificuldade:")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.predefinida_radio = QRadioButton("Dificuldade Predefinida")
        self.predefinida_radio.setFont(QFont("Segoe UI", 14))
        self.predefinida_radio.setStyleSheet("color: #FFFFFF;")
        self.predefinida_radio.setChecked(True)
        layout.addWidget(self.predefinida_radio)

        self.personalizada_radio = QRadioButton("Configuração Personalizada")
        self.personalizada_radio.setFont(QFont("Segoe UI", 14))
        self.personalizada_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.personalizada_radio)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #555555; }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

    def get_choice(self):
        """Retorna a escolha do usuário: 'predefinida' ou 'personalizada'."""
        if self.predefinida_radio.isChecked():
            return "predefinida"
        return "personalizada"

class PremiosWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Selecionar Prêmio Recebido")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Selecionar Prêmio Recebido")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pontos_label)

        # Seleção de Prêmio
        premio_layout = QHBoxLayout()
        premio_label = QLabel("Prêmio:")
        premio_label.setFont(QFont("Segoe UI", 14))
        premio_label.setStyleSheet("color: #FFFFFF;")
        self.premio_combo = QComboBox()
        self.premios = {
            "Jogador do Mês": "Premiação para o melhor jogador do mês",
            "All Star": "Seleção para o jogo das estrelas",
            "Scoring Champion": "Maior pontuador da temporada regular",
            "Rookie of the Year": "Melhor novato da temporada",
            "Most Improved Player": "Jogador que mais evoluiu",
            "Sixth Man of the Year": "Melhor jogador reserva",
            "Clutch Player of the Year": "Melhor jogador em momentos decisivos",
            "Defensive Player of the Year": "Melhor jogador defensivo da temporada",
            "Most Valuable Player": "Jogador mais valioso da temporada regular",
            "Conference Finals MVP": "Melhor jogador das finais de conferência",
            "Finals MVP": "Melhor jogador das finais da NBA",
            "NBA Champion": "Campeão da NBA"
        }
        self.premio_combo.addItems(self.premios.keys())
        self.premio_combo.setFont(QFont("Segoe UI", 14))
        self.premio_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        self.premio_combo.currentTextChanged.connect(self.atualizar_descricao)
        premio_layout.addWidget(premio_label)
        premio_layout.addWidget(self.premio_combo)
        layout.addLayout(premio_layout)

        # Descrição do Prêmio
        self.descricao_label = QLabel(self.premios[self.premio_combo.currentText()])
        self.descricao_label.setFont(QFont("Segoe UI", 12))
        self.descricao_label.setStyleSheet("color: #FFFFFF;")
        self.descricao_label.setWordWrap(True)
        layout.addWidget(self.descricao_label)

        # Pontos do Prêmio
        self.pontos_premio_label = QLabel(f"Pontos: {self.calcular_pontos_premio(self.premio_combo.currentText())}")
        self.pontos_premio_label.setFont(QFont("Segoe UI", 14))
        self.pontos_premio_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.pontos_premio_label)

        # Botão Confirmar
        confirm_button = QPushButton("Confirmar Prêmio")
        confirm_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        confirm_button.clicked.connect(self.confirmar_premio)
        layout.addWidget(confirm_button)

        # Botão Voltar
        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_player)
        layout.addWidget(back_button)

        layout.addStretch()

    def atualizar_descricao(self, premio):
        self.descricao_label.setText(self.premios[premio])
        self.pontos_premio_label.setText(f"Pontos: {self.calcular_pontos_premio(premio)}")

    def calcular_pontos_premio(self, premio):
        # Pontos base atualizados conforme a lista fornecida
        pontos_base = {
            "Jogador do Mês": 300,
            "All Star": 500,
            "Scoring Champion": 1000,
            "Rookie of the Year": 2500,
            "Most Improved Player": 2000,
            "Sixth Man of the Year": 2000,
            "Clutch Player of the Year": 1500,
            "Defensive Player of the Year": 5000,
            "Most Valuable Player": 20000,
            "Conference Finals MVP": 8000,
            "Finals MVP": 15000,
            "NBA Champion": 25000
        }

        # Verificar se há personalização
        if hasattr(self.jogador, 'pontos_premios_personalizados') and self.jogador.pontos_premios_personalizados:
            pontos = self.jogador.pontos_premios_personalizados.get(premio, pontos_base[premio])
        else:
            pontos = pontos_base[premio]

        # Removido o multiplicador por dificuldade
        return pontos

    def confirmar_premio(self):
        premio = self.premio_combo.currentText()
        pontos_ganhos = self.calcular_pontos_premio(premio)
        self.jogador.pontos_disponiveis += pontos_ganhos
        self.jogador.salvar()
        self.pontos_label.setText(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.parent.atualizar_status()
        self.show_success(f"Prêmio '{premio}' recebido com sucesso!\nPontos ganhos: {pontos_ganhos}")
        self.close()
        self.parent.show()

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_player(self):
        self.parent.show()
        self.close()

class AdicionarPremioWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Adicionar Prêmio ao Histórico")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        title = QLabel("Adicionar Prêmio ao Histórico")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Descrição
        desc_label = QLabel("Selecione um prêmio para adicionar ao seu histórico deste ano e receber a bonificação em pontos:")
        desc_label.setFont(QFont("Segoe UI", 14))
        desc_label.setStyleSheet("color: #FFFFFF;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)

        # Lista de prêmios com valores configurados, atualizada conforme a lista fornecida
        self.premios_padrao = {
            "Jogador do Mês": 300,
            "All Star": 500,
            "Scoring Champion": 1000,
            "Rookie of the Year": 2500,
            "Most Improved Player": 2000,
            "Sixth Man of the Year": 2000,
            "Clutch Player of the Year": 1500,
            "Defensive Player of the Year": 5000,
            "Most Valuable Player": 20000,
            "Conference Finals MVP": 8000,
            "Finals MVP": 15000,
            "NBA Champion": 25000
        }
        self.premios = self.jogador.pontos_premios_personalizados if hasattr(self.jogador, 'pontos_premios_personalizados') and self.jogador.pontos_premios_personalizados else self.premios_padrao

        # ComboBox para escolher o prêmio
        self.premio_combo = QComboBox()
        self.premio_combo.addItems([f"{premio} ({pontos} pontos)" for premio, pontos in self.premios.items()])
        self.premio_combo.setFont(QFont("Segoe UI", 14))
        self.premio_combo.setStyleSheet("background: #3A3A3A; color: #FFFFFF; border-radius: 5px; padding: 5px;")
        main_layout.addWidget(self.premio_combo)

        # Botão Adicionar
        add_button = QPushButton("Adicionar Prêmio")
        add_button.setStyleSheet("""
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #FF8340; }
        """)
        add_button.clicked.connect(self.adicionar_premio)
        main_layout.addWidget(add_button)

        # Botão Voltar
        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_player)
        main_layout.addWidget(back_button)

        main_layout.addStretch()

    def adicionar_premio(self):
        try:
            # Obter o índice selecionado no ComboBox
            index = self.premio_combo.currentIndex()
            if index < 0:
                raise ValueError("Nenhum prêmio selecionado!")

            # Obter o nome do prêmio diretamente das chaves de self.premios
            premio_nome = list(self.premios.keys())[index]
            pontos = self.premios[premio_nome]

            # Inicializar histórico se não existir
            if not hasattr(self.jogador, 'historico_premios') or self.jogador.historico_premios is None:
                self.jogador.historico_premios = {}

            # Definir o ano atual
            ano_atual = getattr(self.jogador, 'ano_atual', "2025")
            if ano_atual not in self.jogador.historico_premios:
                self.jogador.historico_premios[ano_atual] = []

            # Adicionar o prêmio ao histórico
            self.jogador.historico_premios[ano_atual].append(premio_nome)

            # Inicializar pontos_disponiveis se não existir
            if not hasattr(self.jogador, 'pontos_disponiveis') or self.jogador.pontos_disponiveis is None:
                self.jogador.pontos_disponiveis = 0

            # Adicionar os pontos como bonificação a pontos_disponiveis
            self.jogador.pontos_disponiveis += pontos

            # Salvar as alterações no jogador
            self.jogador.salvar()

            # Exibir mensagem de sucesso e voltar ao PlayerWindow
            self.show_success(f"Prêmio '{premio_nome}' adicionado ao histórico de {ano_atual}!\nVocê ganhou {pontos} pontos.")
            self.back_to_player()

        except ValueError as e:
            self.show_error(f"Erro de valor: {str(e)}")
        except Exception as e:
            self.show_error(f"Erro inesperado ao adicionar prêmio: {str(e)}")

    def show_success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Erro")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            background-color: #2D2D2D; QLabel { color: #FFFFFF; font-size: 14px; }
            QPushButton { background: #FF6200; color: #FFFFFF; border-radius: 5px; padding: 10px; font-size: 14px; }
            QPushButton:hover { background: #FF8340; }
        """)
        msg_box.exec_()

    def back_to_player(self):
        # Voltar ao PlayerWindow e atualizar o status
        self.parent.atualizar_status()
        self.parent.show()
        self.close()

class HistoricoWindow(QMainWindow):
    def __init__(self, jogador, parent):
        super().__init__()
        self.jogador = jogador
        self.parent = parent
        self.setWindowTitle("Histórico do Jogador")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #1A1A1A;")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("Histórico do Jogador")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #FF6200;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Exibir pontos disponíveis
        self.pontos_label = QLabel(f"Pontos Disponíveis: {self.jogador.pontos_disponiveis}")
        self.pontos_label.setFont(QFont("Segoe UI", 16))
        self.pontos_label.setStyleSheet("color: #FFFFFF;")
        self.pontos_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pontos_label)

        historico_text = "\n".join([f"Posição: {pos}, Temporada: {temp}, Ano: {ano}" 
                                  for pos, temp, ano in self.jogador.historico_posicoes])
        historico_label = QLabel(historico_text if historico_text else "Sem histórico ainda.")
        historico_label.setFont(QFont("Segoe UI", 16))
        historico_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(historico_label)

        back_button = QPushButton("Voltar")
        back_button.setStyleSheet("""
            QPushButton { background: #2D2D2D; color: #FFFFFF; border-radius: 5px; padding: 15px; font-size: 16px; }
            QPushButton:hover { background: #555555; }
        """)
        back_button.clicked.connect(self.back_to_player)
        layout.addWidget(back_button)

        layout.addStretch()

    def back_to_player(self):
        self.parent.show()
        self.close()


        

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Definir o estilo global para QMessageBox
    app.setStyleSheet("""
        QMessageBox {
            background-color: #2D2D2D;
            color: #FFFFFF;
            font-size: 14px;
        }
        QMessageBox QLabel {
            color: #FFFFFF;
            font-size: 14px;
        }
        QMessageBox QPushButton {
            background: #FF6200;
            color: #FFFFFF;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        QMessageBox QPushButton:hover {
            background: #FF8340;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


    