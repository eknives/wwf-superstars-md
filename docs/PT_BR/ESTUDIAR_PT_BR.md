# Estudar — dúvidas, não uma lista de mudanças autorizadas

- **CPU/DMA/scroll e cadência do córner:** identificar que trabalho atravessa o VBlank e separar custo de CPU, transporte DMA, SAT e relógio lógico. A b91 só observou cruzamentos, não uma atribuição definitiva. PRIORIDADE BAIXA, polir no final. Não reciclar `experimental_post91.c.txt` como solução validada.
- **Som do público:** medir se o corte vem das amostras PCM4, de disparos repetidos, do Z80/mixagem ou do ritmo; comparar IDs/driver OKI/Z80 da análise com os recursos WAV convertidos. Sintoma relatado, causa pendente.
- **Macho verde / paletas emprestadas:** localizar o slot/banco efetivo e a correspondência na CRAM; não supor que seja um sprite quebrado nem modificar a paleta do ringue. Referência técnica b88, `46A0`.
- **Clotheslines restantes:** investigar costas/cordas/CPU/variante tardia e sua ligação FFFE; não aplicar bônus/duplicação ao percurso que os evita. Ver energia 162BC/1642A e colisão 16634.
- **Trilhas de chão do Duggan:** o novo estudo já identifica 159/15A e 61/62/1CB/1CC, variante 1CD/1CE e córner 2F. A b92 já substitui as ativações antigas gs5/gs11 e mede o MD por refresh; falta a cadência visível do Elbow e uma auditoria gráfica exaustiva. Os limites 23/24 e a falta de refiltro do stomp foram testados; outros córneres/lado de fora ficam sem certificar. Ver o estudo do Duggan.
- **Energia contra pin e levantar:** flags de B, contador restante, AF66/AF6A/AF72, CPU vs humano, resgate do parceiro e E0. O relatório de energia contém fórmulas; falta o confronto completo com o modelo do port antes de integrar.
- **Qualidade do código descompilado:** preferir `arc_rec.dis`; o `arc.dis` linear tem 94 destinos desalinhados segundo a análise. O «100% lido» histórico não implica que cada dedução esteja correta; consultar auditoria.md/sin_confirmar.md e estudos posteriores.
- **Testes fora dos fixtures:** frações/planos, quatro córneres, rival/humano/CPU, PAL/NTSC e Everdrive. A frequência física da placa não foi medida; os 57,444852941 Hz do MAME usam totais estimados.

## Acrescentado na b92
Perfilar a publicação/carga visível do Elbow do Duggan antes de propor uma correção global. SAT privado não conclusivo descartado. Dados pose92_refreshes.csv em 02_arcade_decompilado/notas_historicas/b92/shots92. Faltam lado de fora do Duggan, outros córneres, erro no córner, luta natural e Everdrive; não autoriza mudanças no Warrior/render.
