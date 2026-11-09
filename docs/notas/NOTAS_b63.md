# b63 (desde b62) — md5 c4e24dd1024eced745681c0bd9c0ef7d
Solo cambia rfStep (src/main.c):
- refAvoid limitado a 2 px/frame por eje hacia su destino (ya no salta).
- Cualquier movimiento real tras rfClamp+refAvoid anima: avanza rfPh, pose andar (frente/espalda según oy>rfy), flip por ox<rfx. Quieto = congela.
Prueba: empuje f1008-1020 ahora 2 px/f y pose 619→620 (antes congelada).
Queda: salto de 28 px en f62 (rfClamp inicial, antes del combate).
Shots: shots/b63_empuje_contact.png, shots/b63_000*.png (Duggan entra en el árbitro).
