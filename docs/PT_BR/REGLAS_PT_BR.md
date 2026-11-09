# Regras do projeto

Regras da encomenda/conversa; não equivalem a afirmar que todo o port já as cumpre.

1. Igualdade notável e, ao fechar uma técnica, idêntica ao arcade em entrada, ritmo real, colisão, física, reação, poses e paleta. MAME + código/tabela com endereço como fonte; não inventar números nem confundir ticks com frames de 60 Hz. Não dar como verificado o que falta.
2. Confirmar o escopo antes de implementar. Só o que foi pedido; os estudos não autorizam ROM/código. Cada versão numa pasta nova, base anterior intacta, ROM nova e MD5; não reutilizar o nome de uma versão para outra ROM.
3. Prioridade de desenvolvimento: Duggan. Hogan é considerado referência perfeita a preservar; não mexer na implementação dele nem nos recursos originais/1P sem permissão expressa.
4. Preservar as paletas corretas dos parceiros, HUD e árbitro, incluindo blocos de sprites emprestados. **Não mexer nos córneres superiores nem no logo WWF do fundo do ringue**, editados pelo Emilio.
5. Sem IA nova: o rival não ataca sozinho. O START mantém a função de seguir já existente; não transformá-la em IA nem confundir rival não controlado com a CPU do arcade.
6. Controles atuais: A=P, B=K; **C equivale exatamente a A+B**; **Y troca o lutador controlado**, requer controle de 6 botões. Ao terminar a contagem de 3/20 a luta recomeça, não a seleção. A seleção ainda leva a Duggan/Warrior independentemente do que for escolhido.
7. Energia interna independente de vdmg/vlast: humano 48, subtração saturada em 0, sem regeneração durante a luta, zero não é KO; reinício a cada luta. Ambos os lutadores humanos. **Todo lutador novo deve integrar a energia e os danos do arcade**, sem acrescentar uma barra fictícia nem valores de FAQ como se fossem RAM. HUD de energia não autorizado na b90/b91.
8. Conservar gráficos/poses existentes como prefixo salvo permissão; auditar mudanças e compilar localmente com o ambiente fixado. Validações curtas, capturas e CSV de RAM; fixtures não equivalem a uma luta completa nem a um teste no Everdrive.
9. Não copiar a ROM do arcade neste backup. São permitidos análises e recursos convertidos. Consultar seu MD5 de referência; obter a ROM legalmente e à parte, se for preciso para MAME/conversores.
10. Não repetir pesquisa já disponível: primeiro INDICE.md e DESCUBRIMIENTOS.csv. Uma nota antiga não demonstra o estado atual; prevalecem as notas mais recentes e seus limites explícitos. Experimentos descartados não são código entregue.
