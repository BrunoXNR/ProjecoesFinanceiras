# Projeção de Valor Futuro - Parcelas Postecipadas


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Input das variáveis do cálculo
capital_inicial = int(input("Digite o valor inicial: "))
taxa_juros = float(input("Digite a taxa de juros ao mês: "))
prazo = int(input("Digite o prazo total em meses: "))
aporte = int(input("Digite o valor dos aportes mensais: "))

taxa_juros = taxa_juros / 100


# Cálculo do Valor Futuro com Aportes
def valor_futuro_com_aporte(capital_inicial, taxa_juros, prazo, aporte):
    patrimonio_mensal = []
    valor_futuro_total = capital_inicial

    for mes in range(1, prazo + 1):
        valor_futuro_total = valor_futuro_total * (1 + taxa_juros) + aporte
        patrimonio_mensal.append(valor_futuro_total)
    
    return valor_futuro_total, patrimonio_mensal


# Cálculo do Valor Futuro sem Aportes
def valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo):
    patrimonio_mensal_sem_aportes = []

    for mes in range(1, prazo + 1):
        valor_futuro_sem_aporte = capital_inicial * (1 + taxa_juros) ** mes
        patrimonio_mensal_sem_aportes.append(valor_futuro_sem_aporte)
    
    return valor_futuro_sem_aporte, patrimonio_mensal_sem_aportes


# Chamada das Funções
valor_futuro_final, patrimonio_mensal = valor_futuro_com_aporte(capital_inicial, taxa_juros, prazo, aporte)
print(f"Valor Futuro com Aporte: R$ {valor_futuro_final:.2f}")


valor_futuro_sem_aporte_final, patrimonio_mensal_sem_aporte_final = valor_futuro_sem_aporte(capital_inicial, taxa_juros, prazo)
print(f"Valor Futuro sem Aporte: R$ {valor_futuro_sem_aporte_final:.2f}")



# Criando o DataFrame para plotagem
df = pd.DataFrame({
    'Mês': np.arange(1, prazo + 1),
    'Patrimônio com Aporte': patrimonio_mensal,
    'Patrimônio sem Aporte': patrimonio_mensal_sem_aporte_final
})


# Plotagem do Gráfico
sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.lineplot(x='Mês', y='Patrimônio com Aporte', data=df, marker='o', color='b', label='Com Aporte')
sns.lineplot(x='Mês', y='Patrimônio sem Aporte', data=df, marker='o', color='r', label='Sem Aporte')

plt.title('Patrimônio Projetado (Parcelas Postecipadas)', fontsize=16)
plt.xlabel('Tempo (Meses)', fontsize=14)
plt.ylabel('Patrimônio (R$)', fontsize=14)
plt.legend(title='Tipo de Investimento', fontsize=12)
plt.tight_layout()


# Mostrar o gráfico
plt.show()
