# b64 (a partir da b63) — md5 9b3cffff1bd585fc241f684f09ab77a4
Só o rfStep:
- O passo de seguir (hx/hy) já não avança rfPh nem põe pose antes do clamp: a animação é decidida no final com o movimento LÍQUIDO após rfClamp+refAvoid+rfClamp.
- No limite lateral (RF_MARGIN 16, não toca as cordas), empurrões de ±1 px sem seguir em Y não contam como andar: congela o último frame.
- Líquido 0 = congela (como no arcade).
Teste no MAME: árbitro forçado na borda direita (x 887) com o Duggan colado na corda: pose fixa 618 o tempo todo.
Atenção: com a b63 nesse mesmo teste também não ciclava; não consegui reproduzir o ciclo no lugar. Ao descer pela diagonal da borda ele anda sim (movimento real).
Shots: shots/b64_borde_*.png, b64_borde_contact.png.
