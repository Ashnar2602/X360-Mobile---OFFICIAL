# X360 Mobile — Emulatore Xbox 360 per Android

<p align="center">
  <img src="https://x360mobile.com/logo.png" alt="Logo X360 Mobile" width="180"/>
</p>

<p align="center"><b>Emulazione sperimentale Xbox 360 ARM64 per Android con renderer Vulkan.</b></p>
<p align="center"><a href="https://www.x360mobile.com"><b>Sito ufficiale: www.x360mobile.com</b></a></p>

<p align="center">
  <a href="README.md">English</a> · <b>Italiano</b> ·
  <a href="README.de.md">Deutsch</a> · <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

> [!IMPORTANT]
> Questo è il repository pubblico di distribuzione. Contiene APK ufficiali
> firmati, note di rilascio, metadati per gli aggiornamenti e documentazione
> pubblica. Il sorgente attivo dell'emulatore è mantenuto separatamente e non è
> pubblicato qui.

## Il progetto

X360 Mobile è un port Android sperimentale il cui core ARM64 corrente combina
componenti e comportamenti delle linee di sviluppo Xenia EDGE e Xenia Canary,
insieme a interventi specifici per esecuzione, grafica, input, archiviazione e
interfaccia Android. Non è affiliato a Microsoft, Xbox o al progetto Xenia.

Compatibilità e prestazioni cambiano sensibilmente in base a gioco, dispositivo,
driver GPU e configurazione. Il semplice avvio di un titolo non implica che sia
completamente giocabile.

## Funzioni principali

- Core Android ARM64 e backend grafico Vulkan.
- Libreria e menu in gioco progettati per controller, utilizzabili anche touch.
- Controller fisici, controlli touch configurabili e vibrazione.
- Impostazioni per gioco, cVar personalizzate e profili consigliati.
- GamerTag, profili, salvataggi, contenuti installati, Title Update e DLC.
- Rilevamento ISO/XISO, XEX, cartelle estratte con `default.xex`, ZAR e
  strutture XBLA riconosciute.
- Metadati per Title ID, cache permanente delle cover e stato compatibilità.
- Avvio da frontend esterni e integrazione Android Document Provider.
- Aggiornamenti firmati con canali pubblici, prerelease e maintenance.

## Requisiti

| Componente | Requisito |
|---|---|
| Sistema operativo | Android 11 / API 30 o successivo |
| CPU / ABI | Dispositivo ARM a 64 bit (`arm64-v8a`) |
| Grafica | GPU Vulkan con driver Vulkan funzionante |
| Memoria | Almeno 8 GB di RAM consigliati per i titoli più pesanti |
| Prestazioni | È fortemente consigliato un SoC mobile recente di fascia alta |

I dispositivi Adreno sono quelli testati più estesamente. Mali e Xclipse sono
supportate dal backend Android, ma compatibilità di giochi e driver può variare.
I driver Vulkan personalizzati sono opzionali e validi soltanto per dispositivi
compatibili: possono migliorare un titolo e peggiorarne o bloccarne un altro.

## Installazione e aggiornamenti

1. Scarica l'ultima APK pubblica da [GitHub Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases).
2. Verifica che l'asset si chiami `x360-mobile-{versione}.apk` e provenga da
   questo repository.
3. Consenti l'installazione da questa origine quando richiesto da Android.
4. Completa il wizard e seleziona una cartella contenente giochi posseduti e
   acquisiti legalmente.

L'app controlla `update-manifest.json` in questo repository e scarica
direttamente le APK idonee. Prima dell'installazione verifica package, versione,
dimensione, SHA-256 e identità della firma. Le Public sono proposte per default;
Alpha, Preview e Release Candidate richiedono l'opzione prerelease. Hotfix,
Revision e Repack identificano i pacchetti di manutenzione.

Chi pubblica release deve seguire [VERSIONING.md](VERSIONING.md). Una release
GitHub non viene rilevata dall'app finché il workflow del manifest non termina
correttamente.

## Sorgenti di gioco supportate

La libreria rileva `.iso`/`.xiso`, `.xex`, `.zar`, giochi estratti con un
`default.xex` leggibile e strutture XBLA supportate. Il supporto del contenitore
non garantisce la compatibilità di ogni gioco. Sono consigliate ISO strippate,
se ottenute da un dump di proprietà dell'utente.

## Compatibilità e segnalazioni

Consulta il [sito di compatibilità](https://www.x360mobile.com) per risultati
aggiornati. Percentuali fisse presenti in vecchi annunci non sono attendibili:
i risultati cambiano con versione dell'app, driver e hardware.

Prima di aprire una [issue](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues),
cerca segnalazioni esistenti e indica versione app, gioco e Title ID,
dispositivo, SoC/GPU, Android, driver Vulkan, formato e passaggi di riproduzione.
Non caricare giochi, chiavi o contenuti console protetti da copyright.

## Note legali

- Xbox 360 e Xbox sono marchi di Microsoft Corporation.
- X360 Mobile non è affiliato, autorizzato, sponsorizzato o approvato da
  Microsoft, Xbox o dal progetto Xenia.
- L'app non fornisce giochi, software di sistema della console o contenuti
  protetti. L'utente deve usare esclusivamente dump ottenuti legalmente.
- L'emulazione è sperimentale; software e driver personalizzati sono utilizzati
  a proprio rischio.

<p align="center">© 2026 X360 Mobile Team · <a href="https://www.x360mobile.com">www.x360mobile.com</a></p>
