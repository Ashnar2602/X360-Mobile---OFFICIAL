# X360 Mobile — Emulador de Xbox 360 para Android

<p align="center"><img src="https://x360mobile.com/logo.png" alt="Logo de X360 Mobile" width="180"/></p>
<p align="center"><b>Emulación experimental de Xbox 360 ARM64 para Android con renderizador Vulkan.</b></p>
<p align="center"><a href="https://www.x360mobile.com"><b>Sitio oficial: www.x360mobile.com</b></a></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.it.md">Italiano</a> ·
  <a href="README.de.md">Deutsch</a> · <a href="README.fr.md">Français</a> ·
  <b>Español</b>
</p>

> [!IMPORTANT]
> Este es el repositorio público de distribución. Contiene versiones APK
> oficiales firmadas, notas de versión, metadatos de actualización y
> documentación pública. El código fuente activo del emulador se mantiene por
> separado y no se publica aquí.

## Acerca del proyecto

X360 Mobile es un port experimental para Android cuyo núcleo ARM64 actual
combina componentes y comportamientos de las líneas de desarrollo Xenia EDGE y
Xenia Canary, además de trabajo específico para ejecución, gráficos, entrada,
almacenamiento e interfaz en Android. No está afiliado con Microsoft, Xbox ni
el proyecto Xenia.

La compatibilidad y el rendimiento varían mucho según el juego, dispositivo,
controlador GPU y configuración. Que un título arranque no significa que sea
completamente jugable.

## Funciones principales

- Núcleo Android ARM64 y backend gráfico Vulkan.
- Biblioteca e interfaz en juego pensadas para mando, con soporte táctil.
- Mandos físicos, controles táctiles configurables y vibración.
- Ajustes por juego, cVars personalizadas y perfiles recomendados.
- GamerTags, perfiles, partidas guardadas, contenido instalado, Title Updates y DLC.
- Detección de ISO/XISO, XEX, carpetas extraídas con `default.xex`, ZAR y
  estructuras XBLA compatibles.
- Metadatos por Title ID, caché permanente de carátulas y compatibilidad.
- Lanzamiento desde frontends externos y Android Document Provider.
- Actualizaciones firmadas con canales públicos, preliminares y de mantenimiento.

## Requisitos

| Componente | Requisito |
|---|---|
| Sistema operativo | Android 11 / API 30 o posterior |
| CPU / ABI | Dispositivo ARM de 64 bits (`arm64-v8a`) |
| Gráficos | GPU Vulkan con un controlador Vulkan funcional |
| Memoria | Se recomiendan 8 GB de RAM o más para títulos exigentes |
| Rendimiento | Se recomienda encarecidamente un SoC móvil reciente de gama alta |

Los dispositivos Adreno son los más probados. Mali y Xclipse están soportados
por el backend Android, pero la compatibilidad de juegos y controladores puede
variar. Los controladores Vulkan personalizados son opcionales y solo sirven en
dispositivos compatibles; pueden mejorar un juego y perjudicar o bloquear otro.

## Instalación y actualizaciones

1. Descarga la última APK pública desde [GitHub Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases).
2. Comprueba que el archivo se llame `x360-mobile-{versión}.apk` y proceda de
   este repositorio.
3. Permite la instalación desde este origen cuando Android lo solicite.
4. Completa el asistente inicial y elige una carpeta con juegos propios
   volcados legalmente.

La app consulta `update-manifest.json` en este repositorio y descarga
directamente las APK válidas. Antes de instalar verifica paquete, versión,
tamaño, SHA-256 e identidad de firma. Las versiones Public se ofrecen por
defecto; Alpha, Preview y Release Candidate requieren activar las preliminares.
Hotfix, Revision y Repack identifican paquetes de mantenimiento.

Los responsables de publicación deben seguir [VERSIONING.md](VERSIONING.md).
Una versión de GitHub no aparece en el actualizador hasta que termina
correctamente el workflow del manifiesto.

## Fuentes de juego compatibles

La biblioteca detecta `.iso`/`.xiso`, `.xex`, `.zar`, juegos extraídos con un
`default.xex` legible y estructuras XBLA compatibles. Reconocer el contenedor no
garantiza la compatibilidad de todos los juegos. Se recomiendan ISO reducidas
cuando procedan de un volcado legalmente propiedad del usuario.

## Compatibilidad e informes

Consulta el [sitio de compatibilidad](https://www.x360mobile.com) para ver
resultados actuales. Los porcentajes fijos de anuncios antiguos no son fiables:
los resultados cambian con la versión, los controladores y el hardware.

Antes de abrir una [incidencia](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues),
busca informes existentes e incluye versión de la app, juego y Title ID,
dispositivo, SoC/GPU, Android, controlador Vulkan, formato y pasos para
reproducir. No subas juegos, claves ni contenido protegido de la consola.

## Aviso legal

- Xbox 360 y Xbox son marcas de Microsoft Corporation.
- X360 Mobile no está afiliado, autorizado, patrocinado ni respaldado por
  Microsoft, Xbox o el proyecto Xenia.
- La app no incluye juegos, software de sistema de consola ni contenido
  protegido. Los usuarios deben aportar sus propios volcados legales.
- La emulación es experimental; el uso del software y de controladores
  personalizados es responsabilidad del usuario.

<p align="center">© 2026 X360 Mobile Team · <a href="https://www.x360mobile.com">www.x360mobile.com</a></p>
