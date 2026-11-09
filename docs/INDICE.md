# Superstars — índice maestro de lo descubierto

**Entrada recomendada:** **b95**, `docs/notas/NOTAS_b95.md` (carrera por tick arcade W28/D27 igual en PAL/NTSC; fondo por DMA en cola sin frames perdidos junto a postes; choque contra cuerda 9E78/9F02; base b94). Inventario de movimientos: `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md`. Cadencias Elbow Duggan y Knee poste siguen BAJA «pulir al final».

Rutas relativas a la raíz del repositorio. Direcciones del 68000 arcade salvo indicación. **(np)** = no publicado: existe sólo en el backup privado del proyecto porque contiene datos del arcade (desensamblado, capturas, volcados, trazas RAM voluminosas) o es material interno; se cita para que se sepa que existe y cómo se obtuvo. Las notas por versión se conservan literales: sus rutas `/workspace/...` y `01_port_sgdk/…`, `02_arcade_decompilado/…`, `03_roms/…`, `04_herramientas/…`, `05_referencias/…` son del backup privado. Una nota antigua no es estado actual ni verificación nueva.

## Receta general de movimientos por luchador

**[PATRON_MOVIMIENTOS.md](PATRON_MOVIMIENTOS.md)** — selector→rutina→tablas por id/pareja→física/contacto→energía/reacción/final; catálogo de slots de los ocho luchadores, excepciones y correspondencia real con b92. Es estudio, no implementación; contenidos no confirmados marcados U. Cadencia visible Elbow Duggan suelo/poste y Knee Warrior poste: **BAJA, «pulir al final»**. Secciones §6–§10: orientación del rival tumbado (b93), pin (b94), investigación carrera/postes/cuerdas y b95.

- **Volteo del rival tumbado en Knee/Elbow (b92):** el arcade nunca cambia `+A` de la víctima; b92 usaba `vface` como bit7 en zonas/destino/caja/A2 mientras dibujaba al tumbado con `vface^1` → espejo al contacto. Causa y propuesta: `docs/PATRON_MOVIMIENTOS.md` §6; **corregido en b93** (`docs/notas/NOTAS_b93.md`).
- **Pin Warrior (cubrir) b93 vs arcade:** `11A72`/`BD10`/`BEF2`: X=Xv∓32 por bit7 del rival, Y=Yv+1, Z=203, orientación = rival^0x80. Propuesta en §7, **implementada en b94** (§8).

## Buscar antes de investigar de nuevo

- Notas por versión: `docs/notas/NOTAS_b49.md` … `NOTAS_b95.md`; resumen en `docs/CHANGELOG.md`.
- Rutinas anotadas del arcade (dirección, nombre, deducción): `docs/analisis/rutinas.md`.
- Ejemplo: `grep -rn -i '10a5e\|stomp\|AF66' docs/`.
- (np) Índices del backup: `DESCUBRIMIENTOS.csv` (tema, resumen, direcciones, ruta y línea), `DOCUMENTOS.csv`, `RUTINAS_DESENSAMBLADO.csv` (líneas de `arc_rec.dis`), `HERRAMIENTAS.csv`, `PROCEDENCIA.csv`, `INVENTARIO_TOTAL.csv`.

## Fuentes, mapa general y calidad

| Tema / dirección | Qué se sabe | Dónde mirar |
|---|---|---|
| Descompilado general | `arc_rec.dis` (np) es el alineado preferido; `arc.dis` (np) lineal tiene destinos desalineados. Se regeneran desde la ROM propia con `tools/analisis/rdis.py`. | `docs/analisis/INDICE.md`; `docs/analisis/auditoria.md` |
| Rutinas anotadas | Tabla de dirección, nombre y deducción, incluidas ramas y excepciones. | `docs/analisis/rutinas.md`; `tools/analisis/anot2.py` |
| RAM/hardware | Estructuras de actores, memoria compartida, registros de vídeo/sonido. | `docs/analisis/ram.md`; `docs/analisis/sistemas/luchadores.md` |
| Tablas ROM | Despachos, poses, cajas, energía, IA, mapas y geometría por dirección (sólo direcciones y descripción). | `docs/analisis/tablas.md` |
| Incertidumbres | Auditoría y discrepancias históricas; «leído 100 %» no garantiza corrección total. | `docs/analisis/sistemas/sin_confirmar.md`, `discrepancias_s66.md`, `cotejo_s66_wip19.md`; `docs/ESTUDIAR.md` |
| ROM de referencia | Set MAME `wwfsstar`; no se incluye. Cada uno usa su copia legal. | `README.md`; `tools/extractor/README.md` |

## Reloj, movimiento y animación

| Tema / dirección | Resumen | Ruta |
|---|---|---|
| 1508–1510 / 155A–157C | Lógica de actor cada 2 refrescos; MAME 57,444852941 Hz, tick 34,816 ms. La MD lo convierte a 50/60 Hz (`arcTick`, 28,72 Hz). | `docs/estudios/KNEEDROP_arcade.md` §2; `docs/analisis/sistemas/reloj.md`; `docs/notas/NOTAS_b90.md` |
| 3DCE–3E20 | Integración de velocidades y altura; posición 16.16, velocidades 8.8. | `docs/estudios/KNEEDROP_arcade.md` §3; `docs/estudios/DUGGAN_SUELO_arcade.md` §2 |
| 156FA / 159AC–15B3E | Solver de salto por tabla, límites/truncamiento/destino; no hay trayectoria fija universal. | `docs/estudios/KNEEDROP_arcade.md`; `TABLAS_DUGGAN.txt` (np) |
| 6CD8 / 7FE2 | Banco gráfico ≠ casilla de selector: W0, Hogan1, Macho2, Duggan3, Bossman4, Honky5, DiBiase6, André7. | `docs/analisis/INDICE.md`; `docs/analisis/sprites/BANCOS.md` |
| 1761E / 172FA / 1636C | Cajas/daño por pose e id, reacción por pose y filtro por acción. | `docs/estudios/ENERGIA_arcade.md`; `docs/analisis/tablas.md` |
| Pose→tiles / 46A0 | b88 corrigió el sentido del lanzamiento y el banco de paleta de bloques prestados. | `docs/notas/NOTAS_b88.md` |
| Carrera 93EE/945C/94CE, 0x95BC, 3DF0 | vel/4 px por tick (W 7 / D 6,75), poses 10–15 × 2 ticks; W 201,1 y D 193,9 px/s. Implementado en b95. | `docs/PATRON_MOVIMIENTOS.md` §9–§10; `docs/notas/NOTAS_b95.md` |

## Ataques — Duggan y Warrior

| Tema / dirección | Resumen | Ruta |
|---|---|---|
| Combo W FC84, FD70/FD7C | Poses 150..155, esperas y ventana de pulsación; no asumir duración de tabla como frames 60 Hz. | `docs/notas/NOTAS_b87.md`; `NOTAS_b86.md` como antecedente |
| Combo D FC4E→FC70→FDA0 / FE88 | El despacho humano de Duggan es distinto; b89 usa FD70/FD7C para ambos. Daño 1 por impacto. | `docs/estudios/ENERGIA_arcade.md` |
| Patada FF3A / 188AB / 188C7 | Daño 4 humano, excepción CPU 0, bonus contra carrera según recorrido. | `docs/estudios/ENERGIA_arcade.md` |
| Clothesline CD14 / 12E7A / 1302E | Entrada en carrera, poses 1D0–1DB y proximidad 16634; contacto/restas 4 o 2. | `docs/notas/NOTAS_b87.md`; `src/cl87.h`; `src/main.c` |
| Caída clothesline 9B9A | Acción 8/sub 17; dirección de viaje/flip y paleta revisados en b88. | `docs/notas/NOTAS_b88.md` |
| Knee W C706 / 10A5E | Input exacto K cabeza; zonas, variantes, solver, impacto y final. | `docs/estudios/KNEEDROP_arcade.md` |
| Knee W 112F0 / 112FA / 10F54 | Poses 61/62/7A: 8/18/10 refrescos; variante 76/77, no 7D. | Mismo estudio §§2–3; `src/knee90.h`; `docs/notas/NOTAS_b90.md` |
| Knee W A554 / 28EC | A2 de la víctima con arco 4/7/9/10/10/9/7/4/0; no es caída genérica. | Estudio Knee §4; `docs/notas/NOTAS_b90.md` |
| Knee W exterior AB1E→ACA4 / 21ED0 | b91 normaliza sólo Knee: contacto 528,75/309/128, no 540,125. | `docs/notas/NOTAS_b91.md` |
| Knee W poste F35A/F636/F6E6 | P o K→sub 2C; trayectoria cotejada, cadencia final irregular (**PENDIENTES, BAJA**). | `docs/notas/NOTAS_b91.md` |
| **Stomp Duggan CB75 / 1173A / 118BC** | **P cuerpo, 159×14/15A×10 refrescos visibles; impacto al entrar 15A; daño 1. No «codazo».** | **`docs/estudios/DUGGAN_SUELO_arcade.md` §1** |
| **Elbow Duggan CB72 / 10A5E / 11372** | **K cabeza, 61/62/1CB/1CC; variante 1CD/1CE; 8/18/10; offset −64, punto de impacto ±8,+4; daño 5.** | **Mismo estudio §2** |
| **Elbow Duggan poste F6EF / FC14** | **P/K→sub 2F; mismos holds, trayectoria 399/−462 en fixture; daño 10. Cadencia visible pendiente.** | **Mismo estudio §3** |
| Fallo 10C6A / 9FCC | −2 al atacante humano, acción 8/sub 5, 1CF→16→17→1A; no es penalización de cualquier caída. | Estudios Knee/Duggan y energía |
| Suelo D b92 | Motor Duggan independiente en lugar de las activaciones antiguas gs5/gs11; cadencia Elbow pendiente. | `src/duggan92.h`; `docs/notas/NOTAS_b92.md` |
| Movimientos restantes | Técnicas hechas/parciales/ausentes. | `docs/MOVIMIENTOS_DUGGAN_WARRIOR_b92.md` |

## Energía, suelo, pin y árbitro

| Dirección / tema | Resumen | Ruta |
|---|---|---|
| 7EE6→7F76 / 7FEC | Humanos 48; CPU 8190/progresión/DIP distinta; HUD ceil(E/4) hasta 12. | `docs/estudios/ENERGIA_arcade.md` § Energía inicial |
| +3C/+3E / 16488–1649A | Energía/daño separados; resta saturada a 0; sin regeneración pasiva; 0 no es KO. | Mismo estudio § Reglas comunes; `src/main.c` |
| 1698A / 1642A / 16418 | CPU puño/patada 0, bonus contra acción 1/15/16 y duplicación F9.0. | Estudio energía; no confundir CPU con rival sin control |
| 162BC–162DA | La excepción clothesline FFFE omite bonus y duplicación. | Estudio energía; `docs/notas/NOTAS_b90.md` |
| 117E0 / 10DC0 / 10DCC | Stomp 1, drop 5 suelo / 10 poste. No usar la escala 2/3 del FAQ como RAM. | Estudios energía, Knee y Duggan |
| AF66 / AF6A / AA00 | Esperas en suelo 112/82/54/22 ticks, entradas 24/10/6/3, levantada 8..40 ticks por índice/flags. | Estudio energía; estudio Knee §4; `docs/analisis/sistemas/pin_cuenta.md` |
| AD12 / ADEA / AE7E / AF72 | Levantarse/kickout leen energía; E0 restringe el escape pero no da victoria inmediata. Integración en el port pendiente. | Estudio energía |
| Forcejeo / 14CFC / 2209C | Llaves/whip/rebote ordinario sin daño propio; choque exterior especial 5 con condiciones. | Estudio energía; `docs/analisis/sistemas/cuerdas.md` |
| Árbitro / cuentas | Cuenta 3/20 y animaciones; b89 reinicia el combate sin volver a la selección. | `docs/analisis/sistemas/arbitro.md`, `pin_cuenta.md`; `docs/notas/NOTAS_b89.md` |
| Pin W/D BD10/11A72/BEF2, B012/B0A0 | Cubre en Xv∓32 (W) / Xv∓36 (D); zafarse junto a la cuerda = arcade desde b95. | `docs/PATRON_MOVIMIENTOS.md` §7–§10; `docs/notas/NOTAS_b94.md`, `NOTAS_b95.md` |

## Selección, gráficos, escenario y sonido

| Tema / direcciones | Resumen | Ruta |
|---|---|---|
| SELECT 704E / 7240 / 729C | 2×3 Savage/Hogan/Warrior / Honky/Duggan/Bossman, WWF central, elegir compañero; 1P/VS/COOP. | `docs/estudios/SELECCION_arcade.md` |
| 749E/74F2/7552 / 7098/72A4 | Navegación sin wrap, botón 1 confirma, temporizador interno 384 refrescos; autoplay/flash aparte. | Estudio selección; `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| 2034A / 20404 / 210A8 / 2FAE | Escena/mapa/retratos/cursores y paletas convertidos de datos arcade. | Estudio selección; `src/gen/select89_data.h` y `res/` (generados, np) |
| Flicker b91 | 896 tiles de overlay retrasaban HINT; ahora sólo se publican celdas sucias en VBlank. | `docs/notas/NOTAS_b91.md` |
| C=A+B / Y | Normalización previa a flancos; Y cambia el luchador controlado (mando de 6 botones). | `docs/notas/NOTAS_b89.md`; `src/select89.h` |
| Ring 21E5A/21ED0 / 221B2 | Límites interiores/exteriores y plano; no confundir coordenadas de mundo con pantalla. | `docs/analisis/sistemas/cuerdas.md`; `docs/notas/NOTAS_b91.md` |
| Cuerdas / paletas / HUD | Casos y discrepancias históricas; preservar esquineros/logo editados por Emilio (no publicados). | `docs/analisis/sistemas/cuerdas.md`; `src/gen/ropes.h`, `src/gen/hud.h` (np); `docs/REGLAS.md` |
| Streaming del fondo | b95: columnas/filas por cola DMA con presupuesto; sin frames perdidos junto a postes. | `docs/notas/NOTAS_b95.md`; `docs/ARQUITECTURA.md` |
| Público 23170 | Tablas de animación/cámara y recursos de crowd; audio entrecortado comunicado, sin causa certificada. | `docs/analisis/sistemas/publico.md` |
| Sonido 25E6 / OKI / Z80 | Driver, IDs y campana; WAV decodificados (np). | `docs/analisis/sistemas/sonido.md` |
| IA 18F16 y siguientes | Sólo referencia arcade, **no autorización para IA del port**. | `docs/analisis/sistemas/ia.md`; `docs/analisis/rutinas.md`; `docs/REGLAS.md` |

## Código actual, entregas y herramientas

- Compilar: `docs/COMPILAR.md`. Con los recursos reales, la ROM b95 da MD5 **7be789d70d892c1efb86af8630b296a6**.
- Arquitectura de `main.c`: `docs/ARQUITECTURA.md`.
- Pruebas MAME vigentes (b95): `tools/mame/`. Herramientas de análisis: `tools/analisis/`. Extractor de recursos: **PENDIENTE**, `tools/extractor/README.md`.
- ROMs b48–b95, copias de código anteriores, capturas y trazas: (np), en el backup privado; MD5 de cada ROM en `docs/CHANGELOG.md`.

## Últimas versiones

| Versión | Resumen | Ruta |
|---|---|---|
| b92 | Stomp/Elbow/Elbow poste de Duggan; cadencia del Elbow sin cerrar. | `docs/notas/NOTAS_b92.md`; `src/duggan92.h`, `src/duggan92_poses.h` |
| b93 | `oriVictima=vface^1` en zonas, destino, poste, caja, exterior; A2 sin espejo. | `docs/notas/NOTAS_b93.md`; `docs/PATRON_MOVIMIENTOS.md` §6 |
| b94 | Tumbado sin ±32; cubre Xv∓32/∓36; Warrior mira al revés del tumbado; pin Duggan por zona cuerpo. | `docs/notas/NOTAS_b94.md`; §7–§8 |
| Investigación 9-11-2026 | Carrera, ralentización junto a postes y cuerdas (sin cambios en el port). | `docs/PATRON_MOVIMIENTOS.md` §9 |
| b95 | Carrera W28/D27 por arcTick, pose cada 2 ticks; fondo por DMA en cola; choque contra cuerda 16 px por delante → sub 2 → rebote hacia dentro y tumbado; soilNudge con vface^1. | `docs/notas/NOTAS_b95.md`; §10 |
