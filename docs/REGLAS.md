# Reglas del proyecto

Reglas del encargo/conversación; no equivalen a afirmar que todo el port ya las cumpla.

1. Igualdad notable y, al cerrar una técnica, idéntica al arcade en input, ritmo real, colisión, física, reacción, poses y paleta. MAME + código/tabla con dirección como fuente; no inventar números ni confundir ticks con frames60Hz. No dar por verificado lo que falta.
2. Confirmar alcance antes de implementar. Sólo lo pedido; los estudios no autorizan ROM/código. Cada versión en carpeta nueva, base anterior intacta, ROM nueva y MD5; no reutilizar el nombre de una versión para otra ROM.
3. Prioridad de desarrollo: Duggan. Hogan se considera referencia perfecta a preservar; no tocar su implementación ni los recursos originales/1P sin permiso expreso.
4. Preservar paletas correctas de compañeros, HUD y árbitro, incluyendo bloques prestados de sprites. **No tocar esquineros superiores ni logo WWF del fondo del ring**, editados por Emilio.
5. Sin IA nueva: rival no ataca solo. START conserva la función de seguimiento existente; no convertirlo en IA ni confundir rival no controlado con CPU arcade.
6. Controles actuales: A=P, B=K; **C equivale exactamente a A+B**; **Y cambia luchador controlado**, requiere mando6botones. Al terminar cuenta3/20 se reinicia combate, no selección. Selección aún conduce a Duggan/Warrior independientemente de lo elegido.
7. Energía interna independiente de vdmg/vlast: humano48, resta saturada a0, sin regeneración durante combate, cero no KO; reinicio por combate. Ambos luchadores humanos. **Todo luchador nuevo debe integrar energía y daños arcade**, no añadir una barra ficticia ni valores de FAQ como si fueran RAM. HUD de energía no autorizado en b90/b91.
8. Conservar gráficos/poses existentes como prefijo salvo permiso; auditar cambios y compilar localmente con el entorno fijado. Validaciones cortas, capturas y CSV de RAM; fixtures no equivalen a partida completa ni prueba Everdrive.
9. No copiar ROM arcade en este respaldo. Se permiten análisis y recursos convertidos. Consultar su referencia MD5; obtener legalmente la ROM por separado si hace falta para MAME/conversores.
10. No repetir investigación ya disponible: primero INDICE.md y DESCUBRIMIENTOS.csv. Una nota antigua no demuestra estado actual; prevalecen notas más recientes y sus límites explícitos. Experimentos descartados no son código entregado.
