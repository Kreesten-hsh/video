// timeline.js - Synchronisation automatique pour vocal1.m4a
window.WORDS = [
  {
    "word": "Arrête",
    "start": 0.0,
    "end": 0.24
  },
  {
    "word": "de",
    "start": 0.24,
    "end": 0.44
  },
  {
    "word": "payer",
    "start": 0.44,
    "end": 0.68
  },
  {
    "word": "des",
    "start": 0.68,
    "end": 0.92
  },
  {
    "word": "montés",
    "start": 0.92,
    "end": 1.18
  },
  {
    "word": "vidéo",
    "start": 1.18,
    "end": 1.6
  },
  {
    "word": "et",
    "start": 1.6,
    "end": 1.88
  },
  {
    "word": "des",
    "start": 1.88,
    "end": 2.14
  },
  {
    "word": "siens",
    "start": 2.14,
    "end": 2.86
  },
  {
    "word": "au",
    "start": 2.86,
    "end": 3.08
  },
  {
    "word": "debris,",
    "start": 3.08,
    "end": 3.44
  },
  {
    "word": "cette",
    "start": 3.8,
    "end": 3.98
  },
  {
    "word": "vidéo",
    "start": 3.98,
    "end": 4.3
  },
  {
    "word": "que",
    "start": 4.3,
    "end": 4.48
  },
  {
    "word": "tu",
    "start": 4.48,
    "end": 4.64
  },
  {
    "word": "regardes",
    "start": 4.64,
    "end": 5.02
  },
  {
    "word": "dans",
    "start": 5.02,
    "end": 5.1
  },
  {
    "word": "ce",
    "start": 5.1,
    "end": 5.24
  },
  {
    "word": "moment",
    "start": 5.24,
    "end": 5.52
  },
  {
    "word": "je",
    "start": 5.52,
    "end": 5.98
  },
  {
    "word": "n",
    "start": 5.98,
    "end": 6.18
  },
  {
    "word": "'ai",
    "start": 6.18,
    "end": 6.18
  },
  {
    "word": "pas",
    "start": 6.18,
    "end": 6.36
  },
  {
    "word": "monté",
    "start": 6.36,
    "end": 6.74
  },
  {
    "word": "sur",
    "start": 6.74,
    "end": 6.9
  },
  {
    "word": "premier",
    "start": 6.9,
    "end": 7.3
  },
  {
    "word": "pro",
    "start": 7.3,
    "end": 7.62
  },
  {
    "word": "et",
    "start": 7.62,
    "end": 8.04
  },
  {
    "word": "je",
    "start": 8.04,
    "end": 8.12
  },
  {
    "word": "n",
    "start": 8.12,
    "end": 8.26
  },
  {
    "word": "'ai",
    "start": 8.26,
    "end": 8.26
  },
  {
    "word": "pas",
    "start": 8.26,
    "end": 8.44
  },
  {
    "word": "étusé",
    "start": 8.44,
    "end": 8.86
  },
  {
    "word": "il",
    "start": 8.86,
    "end": 9.08
  },
  {
    "word": "n",
    "start": 9.08,
    "end": 9.14
  },
  {
    "word": "'y",
    "start": 9.14,
    "end": 9.2
  },
  {
    "word": "a",
    "start": 9.2,
    "end": 9.28
  },
  {
    "word": "vidéo",
    "start": 9.28,
    "end": 9.72
  },
  {
    "word": "qu",
    "start": 9.72,
    "end": 9.96
  },
  {
    "word": "'en",
    "start": 9.96,
    "end": 10.04
  },
  {
    "word": "vidéo",
    "start": 10.04,
    "end": 10.4
  },
  {
    "word": "ou",
    "start": 10.4,
    "end": 11.08
  },
  {
    "word": "cline,",
    "start": 11.08,
    "end": 11.46
  },
  {
    "word": "elle",
    "start": 11.84,
    "end": 11.92
  },
  {
    "word": "est",
    "start": 11.92,
    "end": 12.02
  },
  {
    "word": "générée",
    "start": 12.02,
    "end": 12.46
  },
  {
    "word": "à",
    "start": 12.46,
    "end": 12.62
  },
  {
    "word": "100",
    "start": 12.62,
    "end": 12.86
  },
  {
    "word": "%",
    "start": 12.86,
    "end": 13.12
  },
  {
    "word": "par",
    "start": 13.12,
    "end": 13.4
  },
  {
    "word": "du",
    "start": 13.4,
    "end": 13.54
  },
  {
    "word": "coup,",
    "start": 13.54,
    "end": 13.74
  },
  {
    "word": "en",
    "start": 14.18,
    "end": 14.24
  },
  {
    "word": "fait",
    "start": 14.24,
    "end": 14.46
  },
  {
    "word": "j",
    "start": 14.46,
    "end": 14.8
  },
  {
    "word": "'ai",
    "start": 14.8,
    "end": 14.86
  },
  {
    "word": "codé",
    "start": 14.86,
    "end": 15.18
  },
  {
    "word": "mon",
    "start": 15.18,
    "end": 15.34
  },
  {
    "word": "propre",
    "start": 15.34,
    "end": 15.56
  },
  {
    "word": "moteur",
    "start": 15.56,
    "end": 15.94
  },
  {
    "word": "en",
    "start": 15.94,
    "end": 16.12
  },
  {
    "word": "pittant",
    "start": 16.12,
    "end": 16.5
  },
  {
    "word": "et",
    "start": 16.5,
    "end": 16.74
  },
  {
    "word": "j",
    "start": 16.74,
    "end": 16.88
  },
  {
    "word": "'arrasquerai",
    "start": 16.88,
    "end": 17.34
  },
  {
    "word": "le",
    "start": 17.34,
    "end": 17.72
  },
  {
    "word": "principe",
    "start": 17.72,
    "end": 18.2
  },
  {
    "word": "et",
    "start": 18.2,
    "end": 18.5
  },
  {
    "word": "ultra",
    "start": 18.5,
    "end": 18.84
  },
  {
    "word": "simple,",
    "start": 18.84,
    "end": 19.22
  },
  {
    "word": "j",
    "start": 19.56,
    "end": 19.6
  },
  {
    "word": "'ai",
    "start": 19.6,
    "end": 19.6
  },
  {
    "word": "un",
    "start": 19.6,
    "end": 19.66
  },
  {
    "word": "résisme",
    "start": 19.66,
    "end": 20.04
  },
  {
    "word": "à",
    "start": 20.04,
    "end": 20.2
  },
  {
    "word": "voir",
    "start": 20.2,
    "end": 20.38
  },
  {
    "word": "sur",
    "start": 20.38,
    "end": 20.58
  },
  {
    "word": "mon",
    "start": 20.58,
    "end": 20.72
  },
  {
    "word": "téléphone,",
    "start": 20.72,
    "end": 21.16
  },
  {
    "word": "mon",
    "start": 21.7,
    "end": 21.78
  },
  {
    "word": "site",
    "start": 21.78,
    "end": 21.96
  },
  {
    "word": "coupe",
    "start": 21.96,
    "end": 22.32
  },
  {
    "word": "automatiquement",
    "start": 22.32,
    "end": 23.1
  },
  {
    "word": "tous",
    "start": 23.1,
    "end": 23.36
  },
  {
    "word": "les",
    "start": 23.36,
    "end": 23.52
  },
  {
    "word": "séliens",
    "start": 23.52,
    "end": 23.84
  },
  {
    "word": "est",
    "start": 23.84,
    "end": 24.12
  },
  {
    "word": "transcrit",
    "start": 24.12,
    "end": 24.6
  },
  {
    "word": "chaque",
    "start": 24.6,
    "end": 24.94
  },
  {
    "word": "mot",
    "start": 24.94,
    "end": 25.14
  },
  {
    "word": "à",
    "start": 25.14,
    "end": 25.3
  },
  {
    "word": "la",
    "start": 25.3,
    "end": 25.44
  },
  {
    "word": "ménie",
    "start": 25.44,
    "end": 25.66
  },
  {
    "word": "seconde,",
    "start": 25.66,
    "end": 26.32
  },
  {
    "word": "ensuite",
    "start": 26.48,
    "end": 26.7
  },
  {
    "word": "le",
    "start": 26.7,
    "end": 26.92
  },
  {
    "word": "coup",
    "start": 26.92,
    "end": 27.06
  },
  {
    "word": "d",
    "start": 27.06,
    "end": 27.3
  },
  {
    "word": "'hyéné",
    "start": 27.3,
    "end": 27.56
  },
  {
    "word": "toute",
    "start": 27.56,
    "end": 27.76
  },
  {
    "word": "la",
    "start": 27.76,
    "end": 28.02
  },
  {
    "word": "mes",
    "start": 28.02,
    "end": 28.22
  },
  {
    "word": "enseignes,",
    "start": 28.22,
    "end": 29.04
  },
  {
    "word": "il",
    "start": 29.04,
    "end": 29.2
  },
  {
    "word": "annume",
    "start": 29.2,
    "end": 29.62
  },
  {
    "word": "mon",
    "start": 29.62,
    "end": 29.82
  },
  {
    "word": "avatar",
    "start": 29.82,
    "end": 30.18
  },
  {
    "word": "en",
    "start": 30.18,
    "end": 30.48
  },
  {
    "word": "costume",
    "start": 30.48,
    "end": 30.78
  },
  {
    "word": "selon",
    "start": 30.78,
    "end": 31.26
  },
  {
    "word": "l",
    "start": 31.26,
    "end": 31.38
  },
  {
    "word": "'émotion,",
    "start": 31.38,
    "end": 31.76
  },
  {
    "word": "il",
    "start": 32.26,
    "end": 32.36
  },
  {
    "word": "ouvre",
    "start": 32.36,
    "end": 32.64
  },
  {
    "word": "les",
    "start": 32.64,
    "end": 32.76
  },
  {
    "word": "théminos,",
    "start": 32.76,
    "end": 33.26
  },
  {
    "word": "il",
    "start": 33.74,
    "end": 33.86
  },
  {
    "word": "affiche",
    "start": 33.86,
    "end": 34.26
  },
  {
    "word": "des",
    "start": 34.26,
    "end": 34.54
  },
  {
    "word": "listres",
    "start": 34.54,
    "end": 34.9
  },
  {
    "word": "structurés",
    "start": 34.9,
    "end": 35.64
  },
  {
    "word": "et",
    "start": 35.64,
    "end": 36.18
  },
  {
    "word": "il",
    "start": 36.18,
    "end": 36.3
  },
  {
    "word": "change",
    "start": 36.3,
    "end": 36.54
  },
  {
    "word": "le",
    "start": 36.54,
    "end": 36.74
  },
  {
    "word": "déco",
    "start": 36.74,
    "end": 37.02
  },
  {
    "word": "en",
    "start": 37.02,
    "end": 37.26
  },
  {
    "word": "rosenge",
    "start": 37.26,
    "end": 37.8
  },
  {
    "word": "ou",
    "start": 37.8,
    "end": 38.04
  },
  {
    "word": "en",
    "start": 38.04,
    "end": 38.3
  },
  {
    "word": "sé,",
    "start": 38.3,
    "end": 38.44
  },
  {
    "word": "et",
    "start": 38.84,
    "end": 38.96
  },
  {
    "word": "il",
    "start": 38.96,
    "end": 39.16
  },
  {
    "word": "compute",
    "start": 39.16,
    "end": 39.48
  },
  {
    "word": "tout",
    "start": 39.48,
    "end": 39.8
  },
  {
    "word": "avec",
    "start": 39.8,
    "end": 40.3
  },
  {
    "word": "ffmp",
    "start": 40.3,
    "end": 41.3
  },
  {
    "word": "en",
    "start": 41.3,
    "end": 41.96
  },
  {
    "word": "30",
    "start": 41.96,
    "end": 42.4
  },
  {
    "word": "images",
    "start": 42.4,
    "end": 42.66
  },
  {
    "word": "par",
    "start": 42.66,
    "end": 42.94
  },
  {
    "word": "seconde,",
    "start": 42.94,
    "end": 43.58
  },
  {
    "word": "pourquoi",
    "start": 43.74,
    "end": 44.0
  },
  {
    "word": "c",
    "start": 44.0,
    "end": 44.22
  },
  {
    "word": "'est",
    "start": 44.22,
    "end": 44.24
  },
  {
    "word": "une",
    "start": 44.24,
    "end": 44.38
  },
  {
    "word": "résolution",
    "start": 44.38,
    "end": 44.9
  },
  {
    "word": "pour",
    "start": 44.9,
    "end": 45.1
  },
  {
    "word": "les",
    "start": 45.1,
    "end": 45.28
  },
  {
    "word": "fondateurs",
    "start": 45.28,
    "end": 45.72
  },
  {
    "word": "saches",
    "start": 45.72,
    "end": 46.1
  },
  {
    "word": "et",
    "start": 46.1,
    "end": 46.38
  },
  {
    "word": "les",
    "start": 46.38,
    "end": 46.5
  },
  {
    "word": "entrepreneurs,",
    "start": 46.5,
    "end": 46.82
  },
  {
    "word": "parce",
    "start": 47.56,
    "end": 47.72
  },
  {
    "word": "que",
    "start": 47.72,
    "end": 47.86
  },
  {
    "word": "les",
    "start": 47.86,
    "end": 48.06
  },
  {
    "word": "idées,",
    "start": 48.06,
    "end": 48.52
  },
  {
    "word": "parce",
    "start": 48.84,
    "end": 49.28
  },
  {
    "word": "qu",
    "start": 49.28,
    "end": 49.52
  },
  {
    "word": "'il",
    "start": 49.52,
    "end": 49.68
  },
  {
    "word": "y",
    "start": 49.68,
    "end": 49.82
  },
  {
    "word": "a",
    "start": 49.82,
    "end": 50.16
  },
  {
    "word": "vidéo",
    "start": 50.16,
    "end": 50.52
  },
  {
    "word": "classique",
    "start": 50.52,
    "end": 51.0
  },
  {
    "word": "ou",
    "start": 51.0,
    "end": 51.24
  },
  {
    "word": "une",
    "start": 51.24,
    "end": 51.5
  },
  {
    "word": "fortune,",
    "start": 51.5,
    "end": 51.82
  },
  {
    "word": "font",
    "start": 52.4,
    "end": 52.48
  },
  {
    "word": "des",
    "start": 52.48,
    "end": 52.74
  },
  {
    "word": "erreurs",
    "start": 52.74,
    "end": 53.2
  },
  {
    "word": "visuels",
    "start": 53.2,
    "end": 53.74
  },
  {
    "word": "et",
    "start": 53.74,
    "end": 54.0
  },
  {
    "word": "prennent",
    "start": 54.0,
    "end": 54.38
  },
  {
    "word": "des",
    "start": 54.38,
    "end": 54.8
  },
  {
    "word": "heures",
    "start": 54.8,
    "end": 55.08
  },
  {
    "word": "à",
    "start": 55.08,
    "end": 55.26
  },
  {
    "word": "corriger,",
    "start": 55.26,
    "end": 55.78
  },
  {
    "word": "avec",
    "start": 56.18,
    "end": 56.38
  },
  {
    "word": "du",
    "start": 56.38,
    "end": 56.58
  },
  {
    "word": "code",
    "start": 56.58,
    "end": 56.8
  },
  {
    "word": "1",
    "start": 56.8,
    "end": 57.16
  },
  {
    "word": "vidéo",
    "start": 57.16,
    "end": 57.52
  },
  {
    "word": "complète",
    "start": 57.52,
    "end": 58.34
  },
  {
    "word": "me",
    "start": 58.34,
    "end": 59.0
  },
  {
    "word": "prendre",
    "start": 59.0,
    "end": 59.24
  },
  {
    "word": "2",
    "start": 59.24,
    "end": 59.86
  },
  {
    "word": "minutes",
    "start": 59.86,
    "end": 60.18
  },
  {
    "word": "à",
    "start": 60.18,
    "end": 60.46
  },
  {
    "word": "générer",
    "start": 60.46,
    "end": 60.86
  },
  {
    "word": "et",
    "start": 60.86,
    "end": 61.1
  },
  {
    "word": "coûte",
    "start": 61.1,
    "end": 61.32
  },
  {
    "word": "0",
    "start": 61.32,
    "end": 61.58
  },
  {
    "word": "euros,",
    "start": 61.58,
    "end": 62.02
  },
  {
    "word": "que",
    "start": 62.36,
    "end": 62.5
  },
  {
    "word": "ce",
    "start": 62.5,
    "end": 62.6
  },
  {
    "word": "soit",
    "start": 62.6,
    "end": 62.82
  },
  {
    "word": "où",
    "start": 62.82,
    "end": 63.0
  },
  {
    "word": "expliquait",
    "start": 63.0,
    "end": 63.5
  },
  {
    "word": "ton",
    "start": 63.5,
    "end": 63.7
  },
  {
    "word": "logiciel,",
    "start": 63.7,
    "end": 64.28
  },
  {
    "word": "présenté",
    "start": 64.7,
    "end": 65.06
  },
  {
    "word": "ton",
    "start": 65.06,
    "end": 65.24
  },
  {
    "word": "off",
    "start": 65.24,
    "end": 65.46
  },
  {
    "word": "ou",
    "start": 65.46,
    "end": 65.66
  },
  {
    "word": "publier",
    "start": 65.66,
    "end": 66.08
  },
  {
    "word": "tous",
    "start": 66.08,
    "end": 66.34
  },
  {
    "word": "les",
    "start": 66.34,
    "end": 66.56
  },
  {
    "word": "jouçons",
    "start": 66.56,
    "end": 66.86
  },
  {
    "word": "jamais",
    "start": 66.86,
    "end": 67.26
  },
  {
    "word": "à",
    "start": 67.26,
    "end": 67.42
  },
  {
    "word": "le",
    "start": 67.42,
    "end": 67.52
  },
  {
    "word": "mettre",
    "start": 67.52,
    "end": 67.68
  },
  {
    "word": "à",
    "start": 67.68,
    "end": 67.86
  },
  {
    "word": "camera,",
    "start": 67.86,
    "end": 68.18
  },
  {
    "word": "tout",
    "start": 68.7,
    "end": 68.8
  },
  {
    "word": "est",
    "start": 68.8,
    "end": 68.98
  },
  {
    "word": "automatisé,",
    "start": 68.98,
    "end": 69.78
  },
  {
    "word": "si",
    "start": 70.22,
    "end": 70.32
  },
  {
    "word": "tu",
    "start": 70.32,
    "end": 70.5
  },
  {
    "word": "veux",
    "start": 70.5,
    "end": 70.62
  },
  {
    "word": "que",
    "start": 70.62,
    "end": 70.78
  },
  {
    "word": "j",
    "start": 70.78,
    "end": 70.98
  },
  {
    "word": "'ai",
    "start": 70.98,
    "end": 70.98
  },
  {
    "word": "déplacé",
    "start": 70.98,
    "end": 71.36
  },
  {
    "word": "ce",
    "start": 71.36,
    "end": 71.5
  },
  {
    "word": "système",
    "start": 71.5,
    "end": 71.74
  },
  {
    "word": "à",
    "start": 71.74,
    "end": 71.96
  },
  {
    "word": "retenue",
    "start": 71.96,
    "end": 72.26
  },
  {
    "word": "pour",
    "start": 72.26,
    "end": 72.4
  },
  {
    "word": "parata,",
    "start": 72.4,
    "end": 72.94
  },
  {
    "word": "et",
    "start": 73.46,
    "end": 73.48
  },
  {
    "word": "ta",
    "start": 73.48,
    "end": 73.66
  },
  {
    "word": "site",
    "start": 73.66,
    "end": 73.94
  },
  {
    "word": "graphique",
    "start": 73.94,
    "end": 74.38
  },
  {
    "word": "envoie",
    "start": 74.38,
    "end": 74.82
  },
  {
    "word": "un",
    "start": 74.82,
    "end": 75.0
  },
  {
    "word": "accord",
    "start": 75.0,
    "end": 75.28
  },
  {
    "word": "dans",
    "start": 75.28,
    "end": 75.6
  },
  {
    "word": "le",
    "start": 75.6,
    "end": 75.66
  },
  {
    "word": "message",
    "start": 75.66,
    "end": 75.86
  },
  {
    "word": "privé.",
    "start": 75.86,
    "end": 76.32
  }
];

window.SCENES = [
  {
    "start": 0.0,
    "end": 1.2,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/stop.png",
      "label": "ARRÊTE DE PAYER",
      "bg": "red"
    }
  },
  {
    "start": 1.2,
    "end": 2.4,
    "type": "big",
    "data": {
      "text": "MONTEURS CHERS",
      "sub": "350€ À 1500€",
      "bg": "red"
    }
  },
  {
    "start": 2.4,
    "end": 4.64,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/money.png",
      "label": "IA HORS DE PRIX",
      "bg": "grid"
    }
  },
  {
    "start": 4.64,
    "end": 6.9,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/pointing.png",
      "label": "REGARDE BIEN",
      "bg": "diamonds"
    }
  },
  {
    "start": 6.9,
    "end": 12.62,
    "type": "cards",
    "data": {
      "cards": [
        {
          "icon": "❌",
          "title": "PREMIERE"
        },
        {
          "icon": "❌",
          "title": "IA VEO/KLING"
        }
      ],
      "bg": "grid"
    }
  },
  {
    "start": 12.62,
    "end": 14.86,
    "type": "big",
    "data": {
      "text": "100% CODE",
      "sub": "ZÉRO MONTAGE",
      "bg": "red"
    }
  },
  {
    "start": 14.86,
    "end": 16.12,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/laptop.png",
      "label": "DEV SENIOR",
      "bg": "grid"
    }
  },
  {
    "start": 16.12,
    "end": 18.84,
    "type": "window",
    "data": {
      "title": "video_engine.py",
      "text": "$ python render.py\n> Stack: Python + Playwright\n> Zero React / Zero Remotion\n> Memory Pipe -> FFmpeg",
      "bg": "circles"
    }
  },
  {
    "start": 18.84,
    "end": 20.72,
    "type": "list",
    "data": {
      "items": [
        "1. AUDIO VOCAL PHONE",
        "2. SILENCE REMOVAL",
        "3. WHISPER MOT À MOT"
      ],
      "bg": "diamonds"
    }
  },
  {
    "start": 20.72,
    "end": 21.96,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/mic.png",
      "label": "DICTAPHONE TÉL",
      "bg": "grid"
    }
  },
  {
    "start": 21.96,
    "end": 24.12,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/scissors.png",
      "label": "CUT SILENCES",
      "bg": "grid"
    }
  },
  {
    "start": 24.12,
    "end": 26.48,
    "type": "cards",
    "data": {
      "cards": [
        {
          "icon": "⚡",
          "title": "FASTER-WHISPER"
        },
        {
          "icon": "⏱️",
          "title": "TIMESTAMPS"
        }
      ],
      "bg": "circles"
    }
  },
  {
    "start": 26.48,
    "end": 29.82,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/idea.png",
      "label": "AUTOMATISATION",
      "bg": "grid"
    }
  },
  {
    "start": 29.82,
    "end": 32.76,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/shock.png",
      "label": "STICKERS DYNAMIQUES",
      "bg": "diamonds"
    }
  },
  {
    "start": 32.76,
    "end": 34.9,
    "type": "window",
    "data": {
      "title": "terminal@dev",
      "text": "$ ffmpeg -i pipe:0\n> libx264 yuv420p\n> 30 FPS FLUIDE",
      "bg": "grid"
    }
  },
  {
    "start": 34.9,
    "end": 37.26,
    "type": "list",
    "data": {
      "items": [
        "• AVATARS STICKERS",
        "• MACHINE À ÉCRIRE",
        "• SOUS-TITRES DYNAMIQUES"
      ],
      "bg": "grid"
    }
  },
  {
    "start": 37.26,
    "end": 40.3,
    "type": "cards",
    "data": {
      "cards": [
        {
          "icon": "🔷",
          "title": "DIAMONDS"
        },
        {
          "icon": "⚪",
          "title": "CIRCLES"
        },
        {
          "icon": "🟥",
          "title": "RED IMPACT"
        },
        {
          "icon": "📐",
          "title": "GRID"
        }
      ],
      "bg": "diamonds"
    }
  },
  {
    "start": 40.3,
    "end": 44.38,
    "type": "big",
    "data": {
      "text": "FFMPEG 30 FPS",
      "sub": "PIPE RAM DIRECT",
      "bg": "red"
    }
  },
  {
    "start": 44.38,
    "end": 46.5,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/prof.png",
      "label": "RÉVOLUTION SAAS",
      "bg": "grid"
    }
  },
  {
    "start": 46.5,
    "end": 51.5,
    "type": "cards",
    "data": {
      "cards": [
        {
          "icon": "🚀",
          "title": "FONDATEURS SAAS"
        },
        {
          "icon": "💼",
          "title": "ENTREPRENEURS"
        }
      ],
      "bg": "circles"
    }
  },
  {
    "start": 51.5,
    "end": 53.2,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/skeptic.png",
      "label": "TROP CHER ?",
      "bg": "diamonds"
    }
  },
  {
    "start": 53.2,
    "end": 55.26,
    "type": "big",
    "data": {
      "text": "STOP ERREURS",
      "sub": "HALLUCINATIONS IA",
      "bg": "red"
    }
  },
  {
    "start": 55.26,
    "end": 59.86,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/stop.png",
      "label": "PERTE DE TEMPS",
      "bg": "grid"
    }
  },
  {
    "start": 59.86,
    "end": 61.58,
    "type": "big",
    "data": {
      "text": "2 MINUTES",
      "sub": "GÉNÉRATION ÉCLAIR",
      "bg": "red"
    }
  },
  {
    "start": 61.58,
    "end": 62.78,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/happy.png",
      "label": "0€ DE COÛT",
      "bg": "grid"
    }
  },
  {
    "start": 62.78,
    "end": 63.98,
    "type": "window",
    "data": {
      "title": "saas-app.com",
      "text": "DEMO LOGICIEL\n> Taux de conversion : +45%\n> Engagement x3",
      "bg": "circles"
    }
  },
  {
    "start": 63.98,
    "end": 65.18,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/laptop.png",
      "label": "ZÉRO CAMÉRA",
      "bg": "diamonds"
    }
  },
  {
    "start": 65.18,
    "end": 71.5,
    "type": "rpg",
    "data": {
      "zone": "PRODUCTION B2B",
      "quest": "100K VUES",
      "illustration": "🏆",
      "speaker": "KREESTEN",
      "mini_avatar": "assets/avatars/mini.png",
      "text": "Tout est 100% automatisé par du code.",
      "bg": "grid"
    }
  },
  {
    "start": 71.5,
    "end": 73.94,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/pointing.png",
      "label": "POUR TON BIZ",
      "bg": "grid"
    }
  },
  {
    "start": 73.94,
    "end": 75.14,
    "type": "cards",
    "data": {
      "cards": [
        {
          "icon": "🎨",
          "title": "TON AVATAR"
        },
        {
          "icon": "📐",
          "title": "TA CHARTE"
        }
      ],
      "bg": "circles"
    }
  },
  {
    "start": 75.14,
    "end": 76.34,
    "type": "big",
    "data": {
      "text": "ENVOIE 'CODE'",
      "sub": "EN MESSAGE PRIVÉ",
      "bg": "red"
    }
  },
  {
    "start": 76.34,
    "end": 76.72,
    "type": "face",
    "data": {
      "avatar": "assets/avatars/pointing.png",
      "label": "DM MAINTENANT",
      "bg": "grid"
    }
  }
];
