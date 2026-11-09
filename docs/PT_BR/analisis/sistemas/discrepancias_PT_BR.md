# Discrepâncias port (s66 wip19, 67efe37a…) vs arcade — sem corrigir
1. Não está o efeito de grade do público (1C1854). (C)
2. Não há driver de som; os pedidos a 0x25E6 não têm equivalente. (C)
3. Falta a tabela de atordoamento da CPU para o Duggan. (C)
4. lieTab está medido a olho; não é a tabela 0xAF66. (C)
5. A transição 0x15→0x01 e o ataque de volta são aproximados (WHIP_RET). (C)
6. O acaso do público não usa a fórmula do RNG 0x450A (registradores + semente 1C003A). Pendente de verificar no código do port. (P)
7. Seleção de rival por nível (0x21C4, com rng): falta conferir se o port segue a mesma ordem. (P)

## Revisão (leitura completa 0x17C6–0x8AB0)
- Pendente: contrastar com o código da s66. Esta passada não chegou a fazê-lo, então as 7 discrepâncias continuam NÃO CONFIRMADAS contra o port.
- Dados novos do arcade (já confirmados) para comparar:
  - A barra de energia mostra ceil(energia/4), com um máximo de 12 segmentos.
  - A energia se conserva entre combates; só é reiniciada no combate 0, a partir da tabela 0x7FEC.
  - O RNG 0x450A não soma d1 nem a3.
  - Com um humano com energia 0 toca a música 8.
  - Em versus (modo 2) não há game over: o vencedor continua no modo de 1 jogador.
