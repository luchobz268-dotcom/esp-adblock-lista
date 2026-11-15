# Lista para la plaquita AdBlock

Una lista de direcciones de publicidad y rastreo, armada sola cada lunes, para un bloqueador de publicidad
hecho con una placa ESP32-C3.

## De dónde sale

De la lista **Hagezi Pro** ([hagezi/dns-blocklists](https://github.com/hagezi/dns-blocklists)). Acá sólo se
pasa a la forma que entiende la placa: el trabajo de juntar las direcciones es de Hagezi.

## Qué se revisa antes de publicarla

Si alguna de estas cosas falla, esa semana no se publica nada y la placa sigue con la lista que ya tenía:

- que tenga una cantidad razonable de direcciones, y que entre en la memoria de la placa;
- que no cambie de tamaño de golpe contra la semana anterior;
- que no bloquee páginas que tienen que andar, como Google, YouTube, WhatsApp o Mercado Libre;
- que esté entera y en orden.

## Dónde se baja

- `https://raw.githubusercontent.com/luchobz268-dotcom/esp-adblock-lista/lista/blocklist.bin`
- Copia en otro servidor: `https://cdn.jsdelivr.net/gh/luchobz268-dotcom/esp-adblock-lista@lista/blocklist.bin`

En la misma carpeta está `lista.txt`, con la fecha y la cantidad de direcciones.

## Licencia

El programa que arma la lista es MIT (ver `LICENSE`). La lista Hagezi tiene su propia licencia (GPL 3.0).
