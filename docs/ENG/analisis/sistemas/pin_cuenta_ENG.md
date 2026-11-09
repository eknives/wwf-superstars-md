# Pin and count

## Start
- Covering = action 0x17 (0xBD10). It is set by 0x1190C, 0x11A72 and 0x12972.
- At the same time they mark the opponent with +0x18 bit5, and that moves the referee to state 2.
- When the count ends, the covered wrestler goes to action 0x19 (roll, 0x12B00).

## Time on the floor: action 0xB (0xAB1E)
- +0x38 = table 0xAF66[band] = 112 / 82 / 54 / 22 ticks. Each tick is 2 frames, so it lasts 224 / 164 / 108 / 44 frames.
- Band (0x1CE9C) = energy / (maximum/4), capped at 3:
  - Human: maximum 48 (0x7FEC).
  - CPU: maximum from table 0x8190[level*8 + slot].
- CPU: the time is halved if 0x1CD80 gives CS (+0xF6 >= 0x1CD48[id], high meter) or if +0xF9 bit0.
- +0x20 if coming from outside the ring.
- Button mashing (0xAD12, threshold 0xAF6A = 24 / 10 / 6 / 3) → action 0x19.

## Exit from the pin: own kick-out, action 0x1E
- **Human (0xADEA):** the threshold is AF72[energy]/2; presses during the count free him.
- **CPU (0xAE7E):** level d1 from 0xAF26:

  | Energy | d1 |
  |---|---|
  | ≥ 0x36 | 0 |
  | ≥ 0x30 | 1 |
  | ≥ 0x24 | 2 |
  | ≥ 0x19 | 3 |
  | ≥ 0xE | 4 |
  | > 0 | 5 |
  | 0 | 6: never gets out |

  He gets out when count*2 + parity ≥ d1 (plus conditions on the referee's frames).
- **Immediate kick-out (0x11BC6):** roll against table 0x11C30[difficulty*3 + 0x1CEF4].

## Partner save (0x129A4)
- There is no save if the covered wrestler has energy 0, or if the partner cannot (3/16 probability).
- The CPU comes in with state 0xF (0x1B486).
