# RÈGLE FONDAMENTALE : BANNISSEMENT ABSOLU ET DÉFINITIF DU HUD SUPÉRIEUR

Le bandeau HUD supérieur (`#agent-hud`, `AGENT404 // SYS.ONLINE`, `hud-timer`, `hud-progress-bar`, etc.) est **strictement et définitivement banni** de l'ensemble du projet :

1. **Aucun élément HUD dans le DOM HTML** : `index.html` ne doit JAMAIS contenir `#agent-hud` ou tout conteneur similaire tout en haut de l'écran.
2. **Aucun style HUD dans CSS** : `style.css` ne doit JAMAIS réintroduire `#agent-hud`, `.hud-brand`, `.hud-timer`, `.hud-dot` ou `#hud-progress-bar`.
3. **Aucune logique HUD dans JavaScript** : `video.js` ne doit JAMAIS manipuler `hud-progress-fill` ou `hud-timer`.
4. **Placement de la zone de sous-titres** : La zone supérieure est réservée exclusivement au conteneur de sous-titres (`#subtitles-zone`).
5. **Garantie par test** : Le test unitaire automatisé `test_hud_banned_from_project` dans `tests/test_governance.py` veille à ce qu'aucune régression ne puisse être commitée.
