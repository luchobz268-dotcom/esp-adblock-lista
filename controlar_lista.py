#!/usr/bin/env python3
"""Controles de una lista armada antes de publicarla.

Uso: controlar_lista.py nueva.bin [anterior.bin]
Sale con 0 si la lista se puede publicar. Si no, explica por qué y sale con 1, y no se publica nada:
la placa sigue con la lista que ya tiene.

Los mismos controles que hace la placa, más estrictos, para que una lista mala falle acá (donde se ve)
y no en la placa en silencio.
"""
import sys

from build_blocklist import CANARIES, HASH_BYTES, fnv, norm

MINIMO = 150_000      # menos que esto: alguna fuente se achicó o se cortó
MAXIMO = 250_000      # más que esto no entran dos copias en la placa (medido el 2026-11-15)
SALTO = 0.30          # cambio máximo contra la semana anterior (la placa rechaza desde el 50 %)


def leer(ruta):
    with open(ruta, 'rb') as f:
        data = f.read()
    if not data or len(data) % HASH_BYTES:
        raise ValueError(f'archivo roto: {len(data)} bytes, no es múltiplo de {HASH_BYTES}')
    return [int.from_bytes(data[i:i + HASH_BYTES], 'little') for i in range(0, len(data), HASH_BYTES)]


def controlar(nueva, anterior=None):
    """Devuelve la lista de problemas (vacía = se puede publicar)."""
    problemas = []
    try:
        h = leer(nueva)
    except ValueError as e:
        return [str(e)]
    n = len(h)
    if n < MINIMO:
        problemas.append(f'muy chica: {n:,} direcciones (mínimo {MINIMO:,})')
    if n > MAXIMO:
        problemas.append(f'muy grande: {n:,} direcciones (máximo {MAXIMO:,}, si no no entran dos en la placa)')
    for i in range(1, n):
        if h[i] == h[i - 1]:
            problemas.append(f'repetida en la posición {i}'); break
        if h[i] < h[i - 1]:
            problemas.append(f'desordenada en la posición {i}'); break
    todas = set(h)
    for c in CANARIES:
        if fnv(norm(c).encode()) in todas:
            problemas.append(f'bloquea {c}, que tiene que andar')
    if anterior:
        try:
            m = len(leer(anterior))
        except (OSError, ValueError):
            m = 0                         # primera vez, o la anterior no se pudo leer: no se compara
        if m and abs(n - m) > m * SALTO:
            problemas.append(f'cambió demasiado de golpe: {m:,} -> {n:,} direcciones (tope {int(SALTO * 100)} %)')
    return problemas


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    nueva = sys.argv[1]
    anterior = sys.argv[2] if len(sys.argv) > 2 else None
    problemas = controlar(nueva, anterior)
    if problemas:
        print('NO SE PUBLICA:')
        for p in problemas:
            print(' -', p)
        sys.exit(1)
    print(f'bien: {len(leer(nueva)):,} direcciones, se puede publicar')


if __name__ == '__main__':
    main()
