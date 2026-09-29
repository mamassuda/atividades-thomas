import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Pokemon_full.csv')

#? print(df.head())

print(df.columns)

#! #! #! Teste 1 - Attack por tipo #! #! #! 

df_mean_attack = df.groupby('type')['attack'].mean().sort_values(ascending=False)
#? print(df_mean_attack)

plt.figure(figsize=(12, 6))     #* Gráfico de barras 
ax = df_mean_attack.plot(kind='bar', color="#820FDB", edgecolor='black')

# config do gráfico
plt.title('Média do Ataque por Tipo de Pokémon', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Pokémon', fontsize=12)
plt.ylabel('Média do Ataque', fontsize=12)

# ha='right' garante que o texto fique alinhado perfeitamente embaixo da barra
plt.xticks(rotation=45, ha='right')

# Adicionando o valor exato em cima de cada barra (requer Matplotlib 3.4+)
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

#* removendo bordas e adicionando linhas de grade
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# tight_layout evita que os textos cortem nas bordas da imagem
plt.tight_layout() 
plt.show(block=False)

#! #! #! Teste 2 - Defense por tipo #! #! #! 


df_mean_defense = df.groupby('type')['defense'].mean().sort_values(ascending=False)

linha_mean_attack = df_mean_attack.mean()
linha_mean_defense = df_mean_defense.mean()

#? print(df_mean_defense)

plt.figure(figsize=(12, 6))     #* Gráfico de barras_2
ax = df_mean_defense.plot(kind='bar', color="#FD5029", edgecolor='black')

# config do gráfico
plt.title('Média da Defesa por Tipo de Pokémon', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Pokémon', fontsize=12)
plt.ylabel('Média da Defesa', fontsize=12)  

plt.xticks(rotation=45, ha='right')

for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', padding=3, fontsize=10)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show(block=False)

#! #! #! Gráfico final 3 - Relação entre as médias de Ataque e Defesa #! #! #!

df_mean_stats = df.groupby('type')[['attack', 'defense']].mean()

import matplotlib.pyplot as plt

# 1. Preparando a figura
plt.figure(figsize=(12, 8))

# Criando o gráfico de dispersão com os pontos pretos originais
plt.scatter(df_mean_stats['attack'], df_mean_stats['defense'], color='black', s=80)

# Calculando o "meio" do gráfico (a média das médias)
linha_vertical = df_mean_stats['attack'].mean()
linha_horizontal = df_mean_stats['defense'].mean()

# Pegando os limites atuais do gráfico para podermos pintar os fundos até a borda
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()

# ==========================================
# Destacando os Quadrantes com Cores
# ==========================================
# Quadrante Superior Direito (Fortes) - Fundo Verde Suave
plt.fill_between([linha_vertical, x_max], linha_horizontal, y_max, color='#d4edda', alpha=0.5)

# Quadrante Inferior Esquerdo (Fracos) - Fundo Vermelho Suave
plt.fill_between([x_min, linha_vertical], y_min, linha_horizontal, color='#f8d7da', alpha=0.5)

# Opcional: Pintando os outros dois com cores neutras (Azul e Amarelo clarinhos)
plt.fill_between([x_min, linha_vertical], linha_horizontal, y_max, color='#cce5ff', alpha=0.3)
plt.fill_between([linha_vertical, x_max], y_min, linha_horizontal, color='#fff3cd', alpha=0.3)

# ==========================================
# melhorando legibilidade
# ==========================================
for tipo, linha in df_mean_stats.iterrows():
    # Eles garantem que o nome fique um pouco ao lado e abaixo da bolinha, sem encostar nela.
    # Diminuímos também o fontsize para 9 para poluir menos a tela.
    plt.text(linha['attack'] + 0.8, linha['defense'] - 0.2, tipo, fontsize=9, alpha=0.9)


# Desenhando as linhas tracejadas no final para ficarem por cima do fundo colorido
plt.axvline(x=linha_vertical, color='red', linestyle='--', alpha=0.6)
plt.axhline(y=linha_horizontal, color='blue', linestyle='--', alpha=0.6)

# Títulos dos quadrantes principais nos cantos extremos
plt.text(x_max - 1, y_max - 2, 'Fortes (Ataque e Defesa)', 
         color='green', fontsize=12, fontweight='bold', ha='right')

plt.text(x_min + 1, y_min + 1, 'Fracos (Ataque e Defesa)', 
         color='red', fontsize=12, fontweight='bold', ha='left')

# Acabamentos finais
plt.title('Relação entre as médias de Ataque e Defesa por Tipo de Pokémon', fontsize=14, fontweight='bold')
plt.xlabel('Média do Ataque', fontsize=12)
plt.ylabel('Média da Defesa', fontsize=12)

# Fixando os limites para o gráfico não expandir infinitamente
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.show()

plt.show()
