# Attacchi WiFi e Contromisure - WiFi Marauder

Panoramica dei vettori di attacco WiFi eseguibili con ESP32 Marauder via Flipper Zero, con relative contromisure.

---

## Deauthentication Attack

### Principio
Invio di frame di deautenticazione 802.11 spoofati per disconnettere client da un AP. Sfrutta il fatto che i management frame 802.11 non sono autenticati nel protocollo originale.

### Impatto
- DoS: disconnessione di tutti i client dall'AP target
- Enabler per altri attacchi: forza il client a riconnettersi → cattura handshake
- Disruption: rende inutilizzabile una rete WiFi

### Contromisure
- **802.11w (PMF - Protected Management Frames):** autentica i management frame con MIC. Impedisce lo spoofing. Obbligatorio in WPA3, opzionale in WPA2
- **Client isolation:** limita i danni di un deauth sui singoli client
- **WIDS (Wireless Intrusion Detection System):** rileva deauth massivi e genera allarme
- **WPA3:** include PMF obbligatorio → deauth non funziona

---

## Evil Portal

### Principio
Creazione di un captive portal falso (evil twin + phishing) per catturare credenziali. L'ESP32 crea un AP con SSID identico al target, il client si connette e viene rediretto a una pagina di login fasulla.

### Impatto
- Credential harvesting: username/password WiFi, credenziali aziendali
- Session hijacking: intercettazione del traffico post-login
- Malware delivery: pagina che serve payload

### Contromisure
- **HSTS (HTTP Strict Transport Security):** impedisce il downgrade a HTTP
- **Certificate pinning:** il browser rifiuta certificati non validi
- **VPN obbligatoria:** il traffico è criptato end-to-end
- **User awareness:** non inserire credenziali in captive portal sospetti
- **802.1X/EAP-TLS:** autenticazione basata su certificati, non password

---

## PMKID Capture

### Principio
Cattura del PMKID dalla prima parte del 4-Way Handshake (EAPOL M1). Non richiede un client connesso - basta un frame dal AP. Il PMKID è derivato dalla PMK e può essere attaccato offline con hashcat.

### Impatto
- Recupero della password WPA2 se debole (offline brute force)
- Non richiede client attivi - funziona su AP senza client
- Più efficiente dell'handshake capture tradizionale

### Contromisure
- **Password WPA2 forte** (>12 caratteri, mista, non dizionario)
- **WPA3-SAE:** usa Dragonfly key exchange, resistente a offline brute force
- **Password rotation:** cambiare la password periodicamente
- **Disabilitare PMKID caching** sull'AP (opzione specifica del vendor)

---

## Handshake Capture (4-Way WPA2)

### Principio
Cattura dei 4 frame EAPOL scambiati durante l'autenticazione WPA2. Richiede che un client si connetta (o venga forzato con deauth). L'handshake catturato viene crackato offline.

### Impatto
- Identico al PMKID: recupero password WPA2 offline
- Richiede un client attivo o deauth per forzare la riconnessione

### Contromisure
- Stesse del PMKID + **monitoraggio deauth** (WIDS)

---

## Beacon Spam / Probe Flood

### Principio
- **Beacon Spam:** generazione di centinaia di SSID falsi che riempiono la lista WiFi dei client
- **Probe Flood:** invio massiccio di Probe Request per sovraccaricare gli AP

### Impatto
- Confusione: l'utente non trova la rete reale tra centinaia di SSID falsi
- DoS: rallentamento degli AP che devono processare le richieste
- Distrazione: usato come copertura per altri attacchi

### Contromisure
- **WIDS:** rileva beacon anomali e probe flood
- **Client configurazione:** connessione automatica solo a reti note
- **Ignorare SSID sconosciuti:** policy aziendale

---

## Wardriving

### Principio
Scansione sistematica delle reti WiFi in un'area geografica, raccogliendo SSID, BSSID, tipo di sicurezza, potenza del segnale e coordinate GPS.

### Impatto
- Mappatura completa dell'infrastruttura WiFi di un target
- Identificazione di reti con sicurezza debole (WEP, WPA-TKIP, open)
- Input per attacchi mirati

### Contromisure
- **Nascondere SSID:** inefficace (il SSID è comunque nei Probe Response)
- **WPA2/WPA3:** sicurezza forte rende il wardriving solo ricognitivo
- **Segmentazione:** reti guest separate dalle reti corporate
- **WIDS perimetrale:** rilevamento di scansioni dall'esterno

---

## Matrice Attacchi - Quick Reference

| Attacco | Complessità | Marauder Tool | Impatto | Contromisura Chiave |
|---------|-------------|---------------|---------|-------------------|
| Deauth | Bassa | deauth | DoS + enabler | 802.11w/PMF |
| Evil Portal | Media | evilportal | Credential theft | HSTS + awareness |
| PMKID | Bassa | sniffpmkid | Password recovery | WPA3/password forte |
| Handshake | Media | sniffraw | Password recovery | WPA3/password forte |
| Beacon Spam | Bassa | beaconspam | Confusione | WIDS |
| Probe Flood | Bassa | probeflood | DoS AP | WIDS |
| Wardriving | Bassa | wardrive | Reconnaissance | WPA2/WPA3 forte |
