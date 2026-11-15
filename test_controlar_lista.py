import os
import random
import tempfile
import unittest

from build_blocklist import CANARIES, HASH_BYTES, MASK, fnv
import controlar_lista as cl


def escribir(directorio, nombre, hashes):
    ruta = os.path.join(directorio, nombre)
    with open(ruta, 'wb') as f:
        for h in hashes:
            f.write(h.to_bytes(HASH_BYTES, 'little'))
    return ruta


def buena(n, semilla=1):
    r = random.Random(semilla)
    canarios = {fnv(c.encode()) for c in CANARIES}
    s = set()
    while len(s) < n:
        v = r.randrange(MASK)
        if v not in canarios:
            s.add(v)
    return sorted(s)


class Controles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.mkdtemp()
        cls.lista = buena(200_000)

    def test_buena_pasa(self):
        self.assertEqual(cl.controlar(escribir(self.dir, 'b.bin', self.lista)), [])

    def test_con_google_no_pasa(self):
        h = sorted(self.lista[:-1] + [fnv(b'google.com')])
        self.assertTrue(any('google.com' in p for p in cl.controlar(escribir(self.dir, 'g.bin', h))))

    def test_desordenada_no_pasa(self):
        h = list(self.lista); h[10], h[11] = h[11], h[10]
        self.assertTrue(any('desordenada' in p for p in cl.controlar(escribir(self.dir, 'd.bin', h))))

    def test_repetida_no_pasa(self):
        h = list(self.lista); h[11] = h[10]
        self.assertTrue(any('repetida' in p for p in cl.controlar(escribir(self.dir, 'r.bin', h))))

    def test_salto_no_pasa(self):
        anterior = escribir(self.dir, 'a.bin', buena(160_000, 2))
        nueva = escribir(self.dir, 'n.bin', self.lista)     # 200 mil contra 160 mil: 25 %, pasa
        self.assertEqual(cl.controlar(nueva, anterior), [])
        nueva = escribir(self.dir, 'n2.bin', buena(240_000, 3))   # 50 % más: no pasa
        self.assertTrue(any('de golpe' in p for p in cl.controlar(nueva, anterior)))

    def test_muy_grande_no_pasa(self):
        h = buena(cl.MAXIMO + 1, 4)
        self.assertTrue(any('muy grande' in p for p in cl.controlar(escribir(self.dir, 'm.bin', h))))

    def test_muy_chica_no_pasa(self):
        h = buena(1000, 5)
        self.assertTrue(any('muy chica' in p for p in cl.controlar(escribir(self.dir, 'c.bin', h))))

    def test_rota_no_pasa(self):
        ruta = os.path.join(self.dir, 'x.bin')
        open(ruta, 'wb').write(b'123')
        self.assertTrue(any('roto' in p for p in cl.controlar(ruta)))

    def test_sin_anterior_no_compara(self):
        nueva = escribir(self.dir, 's.bin', self.lista)
        self.assertEqual(cl.controlar(nueva, os.path.join(self.dir, 'no-existe.bin')), [])


if __name__ == '__main__':
    unittest.main()
