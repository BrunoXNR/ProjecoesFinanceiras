# Projeção de Valor Futuro - Parcelas Postecipadas - Aportes Variáveis por Período


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Input das variáveis do cálculo
capital_inicial = int(input("Digite o valor inicial: "))
prazo_anos = int(input("Digite o prazo total da projeção em anos: "))
num_periodos = int(input("Digite o número de períodos de aportes diferentes: "))


# Input dos aportes por período 
aportes_por_periodo = []
for i in range(num_periodos):
    aporte = int(input(f"Digite o valor do aporte mensal para o período {i+1}: "))
    duracao_anos = int(input(f"Digite a duração do período {i+1} em anos: "))
    duracao_meses = duracao_anos * 12  # Convertendo anos para meses
    aportes_por_periodo.append((aporte, duracao_meses))


taxa_juros = float(input("Digite a taxa de juros ao mês: "))

prazo_meses = prazo_anos * 12  # Convertendo prazo total de anos para meses
taxa_juros = taxa_juros / 100


# Cálculo do Valor Futuro com Aportes 
def valor_futuro_antecipado(capital_inicial, taxa_juros, aportes_por_periodo):
    patrimonio_mensal = []
    valor_futuro_total = capital_inicial
    mes_atual = 0

    for aporte, duracao in aportes_por_periodo:
        for _ in range(duracao):
            valor_futuro_total = valor_futuro_total * (1 + taxa_juros) + aporte  # Parcelas postecipadas
            patrimonio_mensal.append(valor_futuro_total)
            mes_atual += 1


    # Caso os períodos de aporte sejam menores que o prazo total
    while mes_atual < prazo_meses:
        valor_futuro_total = valor_futuro_total * (1 + taxa_juros)
        patrimonio_mensal.append(valor_futuro_total)
        mes_atual += 1

    return valor_futuro_total, patrimonio_mensal


# Cálculo do Valor Futuro sem Aportes
def valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo_meses):
    patrimonio_mensal_sem_aportes = []
    valor_futuro_sem_aporte = capital_inicial
    
    for mes in range(1, prazo_meses + 1):
        valor_futuro_sem_aporte = valor_futuro_sem_aporte * (1 + taxa_juros)
        patrimonio_mensal_sem_aportes.append(valor_futuro_sem_aporte)
    
    return valor_futuro_sem_aporte, patrimonio_mensal_sem_aportes


# Chamada das Funções
valor_futuro_final, patrimonio_mensal = valor_futuro_antecipado(capital_inicial, taxa_juros, aportes_por_periodo)
print(f"Valor Futuro com Aporte Antecipado: R$ {valor_futuro_final:.2f}")

valor_futuro_sem_aporte_final, patrimonio_mensal_sem_aporte_final = valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo_meses)
print(f'Valor Futuro sem Aporte: R$ {valor_futuro_sem_aporte_final:.2f}')



# Criando o DataFrame para plotagem
df = pd.DataFrame({
    'Mês': np.arange(1, prazo_meses + 1),
    'Patrimônio com Aporte': patrimonio_mensal,
    'Patrimônio sem Aporte': patrimonio_mensal_sem_aporte_final
})


# Plotagem do Gráfico
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.lineplot(x='Mês', y='Patrimônio com Aporte', data=df, marker='o', color='b', label='Com Aporte')
sns.lineplot(x='Mês', y='Patrimônio sem Aporte', data=df, marker='o', color='r', label='Sem Aporte')

plt.title('Projeção de Crescimento do Patrimônio (Parcelas Postecipadas)', fontsize=16)
plt.xlabel('Tempo (Meses)', fontsize=14)
plt.ylabel('Patrimônio (R$)', fontsize=14)
plt.legend(title='Tipo de Investimento', fontsize=12)
plt.tight_layout()

# Mostrar o gráfico
plt.show()
