
---

# 🔒 `docs/SECURITY.md`

```markdown
# Security Policy

## Scope

This project is designed as a minimal administrative interface for interacting with FortiGate REST APIs.

It is not intended for exposure to untrusted environments or public networks.

---

## Ambito

Questo progetto è progettato come interfaccia amministrativa minimale per interagire con le API REST di FortiGate.

Non è destinato all'esposizione su reti pubbliche o ambienti non fidati.

---

## Sensitive Data Handling

The application processes the following sensitive data:

- FortiGate API tokens
- IPsec pre-shared keys in plain text

No data is intentionally stored, persisted, or logged.

---

## Gestione dati sensibili

L'applicazione gestisce i seguenti dati sensibili:

- API token FortiGate
- Pre-shared key IPsec in chiaro

Nessun dato viene salvato, persistito o loggato intenzionalmente.

---

## Deployment Recommendations

- Run the application only on localhost (127.0.0.1)
- Do not expose the service externally
- Use HTTPS when possible
- Restrict FortiGate API access using trusted hosts
- Use dedicated API administrators
- Avoid long-lived API tokens

---

## Raccomandazioni di deploy

- Eseguire l'applicazione solo su localhost (127.0.0.1)
- Non esporre il servizio all'esterno
- Utilizzare HTTPS quando possibile
- Limitare l'accesso API tramite trusted hosts
- Utilizzare utenti API dedicati
- Evitare token API a lunga durata

---

## Threat Model

The primary risks associated with this application include:

- Unauthorized access to the web interface
- Exposure of API tokens
- Exposure of plain-text PSKs
- Misconfiguration leading to external exposure

---

## Modello di minaccia

I principali rischi associati a questa applicazione includono:

- Accesso non autorizzato all'interfaccia web
- Esposizione dei token API
- Esposizione delle PSK in chiaro
- Configurazioni errate che espongono il servizio

---

## Non-Goals

This project explicitly does not aim to:

- Bypass authentication mechanisms
- Decrypt FortiGate encrypted configuration fields
- Exploit vulnerabilities in FortiOS
- Provide offensive security capabilities

---

## Obiettivi non inclusi

Questo progetto non ha l'obiettivo di:

- Bypassare meccanismi di autenticazione
- Decrittare configurazioni FortiGate cifrate
- Sfruttare vulnerabilità
- Fornire strumenti offensivi

---

## Responsible Usage

Users are responsible for ensuring:

- They have proper authorization
- They comply with organizational policies
- They respect applicable laws and regulations

---

## Uso responsabile

Gli utenti sono responsabili di:

- Avere le autorizzazioni necessarie
- Rispettare le policy aziendali
- Rispettare normative e regolamenti applicabili
