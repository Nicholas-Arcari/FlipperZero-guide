## Aspetti Legali

### Italia

- **Art. 615-ter c.p. (Accesso abusivo):** eseguire comandi su un PC altrui senza autorizzazione è reato
- **Art. 615-quater c.p. (Detenzione di codici di accesso):** possedere password rubate tramite exfiltration è reato
- **Art. 617-quater c.p. (Intercettazione):** catturare credenziali WiFi altrui è intercettazione
- **Art. 640-ter c.p. (Frode informatica):** alterare il funzionamento di un sistema per trarne vantaggio

### Best Practice per il Pentest

- **Autorizzazione scritta** che menziona esplicitamente "test di attacchi USB HID / BadUSB"
- **Scope preciso:** quali PC, quali utenti, quali orari, quali tecniche sono permesse
- **Catena di custodia:** documenta ogni payload eseguito con timestamp e target
- **Pulizia:** al termine, rimuovi TUTTI gli artefatti (file scaricati, chiavi di registro, utenti creati)
- **Non exfiltrare dati reali:** in un PoC, dimostra la capacità senza estrarre dati sensibili reali

---

