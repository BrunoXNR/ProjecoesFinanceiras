# Cálculo Projeção de Patrimônio com Interface Gráfica

# Implementação de um janela de interface para realização dos cálculos e display dos resultados (versão 1.0 / m-script)

# Importação das bibliotecas utilizadas
import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors


# Configuração inicial da janela de interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Função para o cálculo da projeção (com aportes variáveis por período e regime de capitalização antecipado)
def valor_futuro_antecipado(capital_inicial, taxa_juros, aportes_por_periodo, prazo_meses):
    patrimonio_mensal = []
    valor_futuro_total = capital_inicial
    mes_atual = 0

    for aporte, duracao in aportes_por_periodo:
        for _ in range(duracao):
            valor_futuro_total = (valor_futuro_total + aporte) * (1 + taxa_juros)  # Parcelas antecipadas
            patrimonio_mensal.append(valor_futuro_total)
            mes_atual += 1

    while mes_atual < prazo_meses:
        valor_futuro_total = valor_futuro_total * (1 + taxa_juros)
        patrimonio_mensal.append(valor_futuro_total)
        mes_atual += 1

    return valor_futuro_total, patrimonio_mensal


# Função para o cálculo da projeção sem aportes
def valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo_meses):
    patrimonio_mensal_sem_aportes = []
    valor_futuro_sem_aporte = capital_inicial
    
    for mes in range(1, prazo_meses + 1):
        valor_futuro_sem_aporte = valor_futuro_sem_aporte * (1 + taxa_juros)
        patrimonio_mensal_sem_aportes.append(valor_futuro_sem_aporte)
    
    return valor_futuro_sem_aporte, patrimonio_mensal_sem_aportes


# Função para adicionar os inputs dos aportes por período e duração dos períodos
def adicionar_periodos():
    global periodo_entries, duracao_entries, num_periodos

    num_periodos = int(entry_num_periodos.get())
    periodo_entries = []
    duracao_entries = []

    frame_periodos.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    for i in range(num_periodos):
        label_aporte = ctk.CTkLabel(master=frame_periodos, text=f"Aporte Mensal Período {i+1} (R$):", font=("Arial", 13, "bold"))
        label_aporte.grid(row=i, column=0, padx=10, pady=5, sticky='ew')
        entry_aporte = ctk.CTkEntry(master=frame_periodos)
        entry_aporte.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        periodo_entries.append(entry_aporte)

        label_duracao = ctk.CTkLabel(master=frame_periodos, text=f"Duração Período {i+1} (Anos):", font=("Arial", 13, "bold"))
        label_duracao.grid(row=i, column=2, padx=10, pady=5, sticky='ew')
        entry_duracao = ctk.CTkEntry(master=frame_periodos)
        entry_duracao.grid(row=i, column=3, padx=10, pady=5, sticky='ew')
        duracao_entries.append(entry_duracao)


# Função para limpar os campos de entrada e os resultados
def limpar_campos():
    # Limpar os campos de entrada de texto
    entry_capital.delete(0, 'end')
    entry_prazo.delete(0, 'end')
    entry_taxa.delete(0, 'end')
    entry_num_periodos.delete(0, 'end')

    # Limpar os campos dos aportes adicionados
    for entry_aporte in periodo_entries:
        entry_aporte.delete(0, 'end')
    for entry_duracao in duracao_entries:
        entry_duracao.delete(0, 'end')

    # Remover o gráfico e os resultados da projeção (se houver)
    for widget in frame_resultados.winfo_children():
        widget.destroy()


# Função para calcular o valor total dos aportes na projeção
def calcular_total_aportes(aportes_por_periodo):
    total_aportes = 0
    for aporte, duracao in aportes_por_periodo:
        total_aportes += aporte * duracao
    return total_aportes


# Função para o cálculo da projeção com aportes e rendimento dos juros
def calcular_projecao():
    capital_inicial = int(entry_capital.get())
    prazo_anos = int(entry_prazo.get())
    taxa_juros = float(entry_taxa.get()) / 100

    # Verificar se o usuário escolheu taxa anual e converter para taxa mensal
    if combo_taxa.get() == "Anual":
        taxa_juros = (1 + taxa_juros) ** (1 / 12) - 1  # Conversão de juros anuais para mensais

    aportes_por_periodo = []
    total_aportes = 0

    for i in range(num_periodos):
        aporte = int(periodo_entries[i].get())
        duracao_anos = int(duracao_entries[i].get())
        duracao_meses = duracao_anos * 12
        aportes_por_periodo.append((aporte, duracao_meses))
        total_aportes += aporte * duracao_meses

    prazo_meses = prazo_anos * 12

    # Cálculo do valor futuro com e sem aportes
    valor_futuro_final, patrimonio_mensal = valor_futuro_antecipado(capital_inicial, taxa_juros, aportes_por_periodo, prazo_meses)
    valor_futuro_sem_aporte_final, patrimonio_mensal_sem_aporte = valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo_meses)

    rendimento_juros = valor_futuro_final - capital_inicial - total_aportes
    renda_passiva = valor_futuro_final * taxa_juros
    renda_passiva_formatada = f"R$ {renda_passiva:,.2f}"

    # Formatação dos valores para exibição
    valor_futuro_formatado = f"R$ {valor_futuro_final:,.2f}"
    valor_futuro_sem_aporte_formatado = f"R$ {valor_futuro_sem_aporte_final:,.2f}"
    rendimento_juros_formatado = f"R$ {rendimento_juros:,.2f}"

    # Cria uma moldura maior para encapsular os resultados à direita
    resultados_frame = ctk.CTkFrame(master=frame_resultados)
    resultados_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')  # Resultados à direita

    # Frame e label para o valor final com aporte
    frame_valor_com_aporte = ctk.CTkFrame(master=resultados_frame)
    frame_valor_com_aporte.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

    label_valor_com_aporte = ctk.CTkLabel(master=frame_valor_com_aporte, 
                                text=f"Valor Final com Aporte: {valor_futuro_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_valor_com_aporte.pack(pady=10)

    # Frame e label para o valor final sem aporte
    frame_valor_sem_aporte = ctk.CTkFrame(master=resultados_frame)
    frame_valor_sem_aporte.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

    label_valor_sem_aporte = ctk.CTkLabel(master=frame_valor_sem_aporte, 
                                text=f"Valor Final sem Aporte: {valor_futuro_sem_aporte_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_valor_sem_aporte.pack(pady=10)

    # Frame e label para o rendimento dos juros
    frame_rendimento_juros = ctk.CTkFrame(master=resultados_frame)
    frame_rendimento_juros.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

    label_rendimento_juros = ctk.CTkLabel(master=frame_rendimento_juros, 
                                text=f"Rendimento dos Juros: {rendimento_juros_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_rendimento_juros.pack(pady=10)

    # Cria o frame e label para exibir a renda passiva vitalícia (sem moldura)
    frame_renda_passiva = ctk.CTkFrame(master=resultados_frame)
    frame_renda_passiva.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

    label_renda_passiva = ctk.CTkLabel(master=frame_renda_passiva, 
                                text=f"Renda Vitalícia: {renda_passiva_formatada}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_renda_passiva.pack(pady=10)
 

    # Cria o dataframe para plotagem do gráfico
    df = pd.DataFrame({
        'Mês': np.arange(1, prazo_meses + 1),
        'Valor': patrimonio_mensal,
        'Valor sem Aporte': patrimonio_mensal_sem_aporte
    })

    # Plotagem do gráfico
    fig, ax = plt.subplots(figsize=(8, 4))

    # Altera as cores da área de plotagem e ao redor da área de plotagem
    fig.patch.set_facecolor('#2C2F33')  # Fundo ao redor do gráfico
    ax.set_facecolor('#2C2F33')  # Fundo da área de plotagem

    # Alterar as cores das linhas
    line_com_aporte = sns.lineplot(x='Mês', y='Valor', data=df, ax=ax, label='Com Aporte', color='#1E90FF')  # Azul suave
    line_sem_aporte = sns.lineplot(x='Mês', y='Valor sem Aporte', data=df, ax=ax, label='Sem Aporte', color='#32CD32')  # Verde claro

    # Ajustar grid e bordas
    ax.grid(True, which='major', axis='x', color='gray', linestyle='--', linewidth=0.3)  # Linhas de grade em branco
    ax.spines['top'].set_color('#2C2F33')
    ax.spines['right'].set_color('#2C2F33')
    ax.spines['left'].set_color('#FFFFFF')  # Bordas laterais em branco
    ax.spines['bottom'].set_color('#FFFFFF')

    # Ajustar cor dos títulos dos eixos para branco
    ax.xaxis.label.set_color('#FFFFFF')  # Título do eixo X em branco
    ax.yaxis.label.set_color('#FFFFFF')  # Título do eixo Y em branco

    # Ajustar cor dos valores dos eixos para branco
    ax.tick_params(axis='x', colors='#FFFFFF')  # Valores do eixo X em branco
    ax.tick_params(axis='y', colors='#FFFFFF')  # Valores do eixo Y em branco

    # Ajustar título do gráfico (opcional)
    ax.title.set_color('#FFFFFF')  # Título do gráfico em branco

    # Configuração das grades a cada 12 meses
    ax.xaxis.set_major_locator(plt.MultipleLocator(12))  # Configura para mostrar os valores do eixo X em intervalos de 12 meses
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))   

    # Atualizar os limites do gráfico para ajustar adequadamente
    ax.set_xlim([1, prazo_meses])


    # Display dos valores finais da projeção
    valor_futuro_formatado = f"R$ {valor_futuro_final:,.2f}"
    valor_futuro_sem_aporte_formatado = f"R$ {valor_futuro_sem_aporte_final:,.2f}"

    # Configura o layout do frame_resultados para ter duas colunas: uma para o gráfico e outra para os resultados
    frame_resultados.grid_columnconfigure(0, weight=3)  # Coluna 0 para o gráfico (mais espaço)
    frame_resultados.grid_columnconfigure(1, weight=1)  # Coluna 1 para os resultados (menos espaço)

    # Gráfico à esquerda
    canvas = FigureCanvasTkAgg(fig, master=frame_resultados)
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')  # Expande para ocupar toda a altura

    # Cria uma moldura maior para encapsular os resultados à direita
    resultados_frame = ctk.CTkFrame(master=frame_resultados)
    resultados_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')  # Resultados à direita

    # Configura as colunas dentro do resultados_frame para alinhar os frames de resultado
    resultados_frame.grid_columnconfigure(0, weight=1)

    # Frame e label para o valor final com aporte (sem moldura)
    frame_valor_com_aporte = ctk.CTkFrame(master=resultados_frame)
    frame_valor_com_aporte.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

    label_valor_com_aporte = ctk.CTkLabel(master=frame_valor_com_aporte, 
                                text=f"Valor Final com Aporte: {valor_futuro_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_valor_com_aporte.pack(pady=10)

    # Frame e label para o valor final sem aporte (sem moldura)
    frame_valor_sem_aporte = ctk.CTkFrame(master=resultados_frame)
    frame_valor_sem_aporte.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

    label_valor_sem_aporte = ctk.CTkLabel(master=frame_valor_sem_aporte, 
                                text=f"Valor Final sem Aporte: {valor_futuro_sem_aporte_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_valor_sem_aporte.pack(pady=10)

    # Adicionar frame e label para o valor do rendimento (juros) com aportes
    frame_rendimento_com_aporte = ctk.CTkFrame(master=resultados_frame)
    frame_rendimento_com_aporte.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

    label_rendimento_com_aporte = ctk.CTkLabel(master=frame_rendimento_com_aporte, 
                                text=f"Total Recebido de Rendimento: {rendimento_juros_formatado}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_rendimento_com_aporte.pack(pady=10)

    # Cria o frame e label para exibir a renda passiva vitalícia (sem moldura)
    frame_renda_passiva = ctk.CTkFrame(master=resultados_frame)
    frame_renda_passiva.grid(row=4, column=0, padx=10, pady=5, sticky='ew')

    label_renda_passiva = ctk.CTkLabel(master=frame_renda_passiva, 
                                text=f"Renda Vitalícia: {renda_passiva_formatada}",
                                justify="center",
                                font=("Arial", 16, "bold"))
    label_renda_passiva.pack(pady=10)


    # Adicionar interatividade ao gráfico usando mplcursors
    cursor = None  # Inicialmente sem cursor

    # Função para ativar o cursor ao entrar no gráfico
    def on_enter(event):
        nonlocal cursor
        if cursor is None:  # Cria o cursor somente se ele não existir
            cursor = mplcursors.cursor(ax, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            sel.annotation.set_text(f'Mês: {int(sel.target[0])}\nValor: R$ {sel.target[1]:,.2f}')
            sel.annotation.get_bbox_patch().set(facecolor="#1E90FF", alpha=0.8)

    # Função para esconder o cursor quando o mouse sair da área do gráfico
    def on_leave(event):
        nonlocal cursor
        if cursor is not None:
            cursor.remove()  # Remove o cursor quando sair da área do gráfico
            cursor = None

    # Conectar eventos de entrada e saída do mouse na área do gráfico
    canvas.mpl_connect('figure_enter_event', on_enter)
    canvas.mpl_connect('figure_leave_event', on_leave)


# Corrigindo o erro do arquivo do ícone que vai embutido no projeto
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o arquivo, seja em execução como script ou como executável """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Cria a janela de interface 
app = ctk.CTk()
app.title("Projeção Financeira")
app.geometry("1000x1600")
app.iconbitmap(resource_path("logofh.ico"))


# Cria o campo principal para inputs e resultados
frame_main = ctk.CTkFrame(master=app)
frame_main.pack(pady=20, padx=20, fill="both", expand=True)

# Cria os campos para os inputs dos aportes
frame_inputs = ctk.CTkFrame(master=frame_main)
frame_inputs.pack(pady=10, padx=10, fill="x", expand=True)

# Cria os campos para inputs dos períodos
frame_periodos = ctk.CTkFrame(master=frame_main)
frame_periodos.pack(pady=10, padx=10, fill="x", expand=True)

# Cria os campos para exibir os resultados
frame_resultados = ctk.CTkFrame(master=frame_main)
frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

# Organizando o layout dos inputs em um grid e centralizando
frame_inputs.grid_columnconfigure((0, 1, 2, 4, 5), weight=1)

# Campo de input do capital inicial
label_capital = ctk.CTkLabel(master=frame_inputs, text="Capital Inicial (R$):", font=("Arial", 13, "bold"))
label_capital.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
entry_capital = ctk.CTkEntry(master=frame_inputs)
entry_capital.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

# Campo de input do prazo
label_prazo = ctk.CTkLabel(master=frame_inputs, text="Prazo (Anos):", font=("Arial", 13, "bold")) 
label_prazo.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
entry_prazo = ctk.CTkEntry(master=frame_inputs)
entry_prazo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

# Campo de input da taxa de juros (a.m)
label_taxa = ctk.CTkLabel(master=frame_inputs, text="Taxa de Juros (%):", font=("Arial", 13, "bold"))
label_taxa.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
entry_taxa = ctk.CTkEntry(master=frame_inputs)
entry_taxa.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

# Seleção entre taxa de juros mensal ou anual
label_tipo_taxa = ctk.CTkLabel(master=frame_inputs, text="Tipo de Taxa de Juros:", font=("Arial", 13, "bold"))
label_tipo_taxa.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
combo_taxa = ctk.CTkComboBox(master=frame_inputs, values=["Mensal", "Anual"])
combo_taxa.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
combo_taxa.set("Mensal")  # Valor padrão

# Campo de input do número de períodos de aporte
label_num_periodos = ctk.CTkLabel(master=frame_inputs, text="Número de Períodos de Aporte:", font=("Arial", 13, "bold"))
label_num_periodos.grid(row=4, column=0, padx=5, pady=5, sticky='ew')
entry_num_periodos = ctk.CTkEntry(master=frame_inputs)
entry_num_periodos.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

# Botão para adicionar os períodos de aporte
button_adicionar_periodos = ctk.CTkButton(master=frame_inputs, text="Adicionar Períodos", command=adicionar_periodos)
button_adicionar_periodos.grid(row=5, column=0, padx=5, pady=10)

# Botão para calcular a projeção
button_calcular = ctk.CTkButton(master=frame_inputs, text="Calcular Projeção", command=calcular_projecao)
button_calcular.grid(row=5, column=1, padx=5, pady=10)

# Botão para limpar os campos
button_limpar = ctk.CTkButton(master=frame_inputs, text="Limpar", command=limpar_campos)
button_limpar.grid(row=5, column=2, padx=5, pady=10)

# Executa o script
app.mainloop()
