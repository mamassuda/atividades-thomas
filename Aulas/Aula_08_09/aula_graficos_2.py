


#! #! #! ################################# #! #! #!
#! #! Aqui vamos testar a biblioteca Plotnine #! #! 
#! #! #! ################################# #! #! #! 


#! A biblioteca Plotnine é uma biblioteca de visualização de dados em Python que
#! é inspirada na gramática de gráficos do ggplot2 do R. 
#! Ela permite criar gráficos complexos de forma declarativa, 
#! utilizando uma sintaxe baseada em camadas

#* BIBLIOTECAS UTILIZADAS #*

import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

df = pd.read_csv('Aula_08_09/Pokemon_full.csv')

# Colchetes duplos [['attack', 'defense']] para passar uma lista de colunas
df_attack = df.groupby('type')[['attack', 'defense']].mean().reset_index()

#print(df_attack)

grafico1 = (
    ggplot(df_attack, aes(x="defense", y="attack", color="type", label="type"))
    + geom_point(size=3)
    + theme_minimal()
    + geom_text(nudge_y=1.5, size=8, show_legend=False)
    + labs( 
        title= "Média de Ataque vs Defesa por Tipo de Pokémon",
        subtitle="Análise comparativa das estatísticas",
        x="Média de Defesa (Defense)",
        y= "Média de Ataque (Attack)",
        color= "Tipo de Pokémon",
        caption="Fonte: Pokemon_full.csv"

    )
    + theme_minimal()
    + theme(
        figure_size=(10,6),
        plot_title=element_text(size=14, fontweight="bold", margin={'b':6})
    )

    )


grafico1.save("grafico_pokemon.png", dpi=300)
print("Gráfico salvo")


