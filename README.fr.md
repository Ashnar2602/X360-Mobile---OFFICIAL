# X360 Mobile — Émulateur Xbox 360 pour Android

<p align="center"><img src="https://x360mobile.com/logo.png" alt="Logo X360 Mobile" width="180"/></p>
<p align="center"><b>Émulation expérimentale Xbox 360 ARM64 pour Android avec moteur de rendu Vulkan.</b></p>
<p align="center"><a href="https://www.x360mobile.com"><b>Site officiel : www.x360mobile.com</b></a></p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.it.md">Italiano</a> ·
  <a href="README.de.md">Deutsch</a> · <b>Français</b> ·
  <a href="README.es.md">Español</a>
</p>

> [!IMPORTANT]
> Ceci est le dépôt public de distribution. Il contient les APK officielles
> signées, les notes de version, les métadonnées de mise à jour et la
> documentation publique. Le code source actif de l'émulateur est maintenu
> séparément et n'est pas publié ici.

## À propos du projet

X360 Mobile est un port Android expérimental dont le cœur ARM64 actuel combine
des composants et comportements issus des lignes de développement Xenia EDGE
et Xenia Canary, ainsi que des travaux propres à Android sur l'exécution, le
rendu, les entrées, le stockage et l'interface. Il n'est affilié ni à
Microsoft, ni à Xbox, ni au projet Xenia.

La compatibilité et les performances varient fortement selon le jeu,
l'appareil, le pilote GPU et la configuration. Le démarrage d'un titre ne
signifie pas qu'il est entièrement jouable.

## Fonctionnalités principales

- Cœur Android ARM64 et backend graphique Vulkan.
- Bibliothèque et interface en jeu pensées pour la manette, avec contrôle tactile.
- Manettes physiques, commandes tactiles configurables et vibrations.
- Réglages par jeu, cVars personnalisées et profils recommandés.
- GamerTags, profils, sauvegardes, contenus installés, Title Updates et DLC.
- Détection ISO/XISO, XEX, dossiers extraits avec `default.xex`, ZAR et
  structures XBLA prises en charge.
- Métadonnées par Title ID, cache permanent des jaquettes et compatibilité.
- Lancement depuis des frontends externes et Android Document Provider.
- Mises à jour signées avec canaux publics, préversions et maintenance.

## Configuration requise

| Composant | Exigence |
|---|---|
| Système | Android 11 / API 30 ou version ultérieure |
| CPU / ABI | Appareil ARM 64 bits (`arm64-v8a`) |
| Graphismes | GPU Vulkan avec pilote Vulkan fonctionnel |
| Mémoire | 8 Go de RAM ou plus recommandés pour les jeux exigeants |
| Performances | Un SoC mobile haut de gamme récent est fortement recommandé |

Les appareils Adreno sont les plus largement testés. Mali et Xclipse sont pris
en charge par le backend Android, mais la compatibilité des jeux et pilotes peut
différer. Les pilotes Vulkan personnalisés sont facultatifs et réservés aux
appareils compatibles ; ils peuvent améliorer un jeu et en dégrader ou bloquer
un autre.

## Installation et mises à jour

1. Téléchargez la dernière APK publique depuis [GitHub Releases](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/releases).
2. Vérifiez que le fichier se nomme `x360-mobile-{version}.apk` et provient de
   ce dépôt.
3. Autorisez l'installation depuis cette source lorsque Android le demande.
4. Terminez l'assistant initial et choisissez un dossier contenant vos propres
   jeux acquis et extraits légalement.

L'application consulte `update-manifest.json` dans ce dépôt et télécharge
directement les APK admissibles. Avant installation, elle vérifie le package,
la version, la taille, le SHA-256 et l'identité de signature. Les versions
Public sont proposées par défaut ; Alpha, Preview et Release Candidate exigent
l'activation des préversions. Hotfix, Revision et Repack désignent les paquets
de maintenance.

Les responsables des publications doivent suivre [VERSIONING.md](VERSIONING.md).
Une version GitHub n'apparaît dans l'outil de mise à jour qu'après la réussite
du workflow du manifeste.

## Sources de jeux prises en charge

La bibliothèque détecte `.iso`/`.xiso`, `.xex`, `.zar`, les jeux extraits avec
un `default.xex` lisible et les structures XBLA prises en charge. La détection
d'un conteneur ne garantit pas la compatibilité de chaque jeu. Les ISO allégées
sont recommandées lorsqu'elles proviennent d'une copie légalement détenue.

## Compatibilité et signalements

Consultez le [site de compatibilité](https://www.x360mobile.com) pour les
résultats actuels. Les pourcentages fixes d'anciennes annonces ne sont pas
fiables : les résultats évoluent avec l'application, les pilotes et le matériel.

Avant d'ouvrir un [ticket](https://github.com/Ashnar2602/X360-Mobile---OFFICIAL/issues),
recherchez les rapports existants et indiquez la version de l'app, le jeu et son
Title ID, l'appareil, le SoC/GPU, Android, le pilote Vulkan, le format et les
étapes de reproduction. Ne publiez jamais de jeux, clés ou contenus protégés de
la console.

## Mentions légales

- Xbox 360 et Xbox sont des marques de Microsoft Corporation.
- X360 Mobile n'est ni affilié, ni autorisé, ni sponsorisé, ni approuvé par
  Microsoft, Xbox ou le projet Xenia.
- L'application ne fournit aucun jeu, logiciel système de console ou contenu
  protégé. Les utilisateurs doivent fournir leurs propres copies légales.
- L'émulation est expérimentale ; l'utilisation du logiciel et de pilotes
  personnalisés se fait à vos risques.

<p align="center">© 2026 X360 Mobile Team · <a href="https://www.x360mobile.com">www.x360mobile.com</a></p>
