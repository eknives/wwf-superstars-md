# b63 (a partir da b62) — md5 c4e24dd1024eced745681c0bd9c0ef7d
Só muda o rfStep (src/main.c):
- refAvoid limitado a 2 px/frame por eixo rumo ao seu destino (já não salta).
- Qualquer movimento real após rfClamp+refAvoid anima: avança rfPh, pose de andar (frente/costas conforme oy>rfy), flip por ox<rfx. Parado = congela.
Teste: empurrão f1008-1020 agora 2 px/f e pose 619→620 (antes congelada).
Resta: salto de 28 px em f62 (rfClamp inicial, antes da luta).
Shots: shots/b63_empuje_contact.png, shots/b63_000*.png (o Duggan entra no árbitro).
