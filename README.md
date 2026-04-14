# FortiGate IPsec PSK UI

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Flask](https://img.shields.io/badge/framework-Flask-lightgrey)
![Status](https://img.shields.io/badge/status-active-success)

## Overview

This project provides a lightweight web-based interface for interacting with a FortiGate firewall using its REST API.

The application enables authorized administrators to retrieve IPsec Phase 1 pre-shared keys (PSKs) in plain text, when permitted by the device configuration and administrator privileges.

This tool does not implement any form of decryption or reverse engineering. It acts solely as a frontend for an officially documented FortiGate API behavior.

---

## Descrizione

Questo progetto fornisce un'interfaccia web minimale per interagire con un firewall FortiGate tramite API REST.

L'applicazione consente ad amministratori autorizzati di recuperare le pre-shared key (PSK) delle VPN IPsec Phase 1 in chiaro, quando consentito dalla configurazione del dispositivo e dai privilegi dell'utente.

Questo strumento non implementa alcuna forma di decrittazione o reverse engineering. Si limita a fungere da frontend per un comportamento ufficialmente documentato da Fortinet.

---

## Scope and Design Principles

- No credential persistence
- No data storage
- No offline configuration processing
- No attempt to bypass FortiGate access controls
- Stateless API interaction
- Designed for temporary administrative usage

---

## Principi di progettazione

- Nessuna persistenza delle credenziali
- Nessun salvataggio di dati
- Nessuna elaborazione offline di configurazioni
- Nessun tentativo di bypass dei controlli FortiGate
- Interazione stateless con le API
- Pensato per uso amministrativo temporaneo

---

## Functionality

- Manual configuration of FortiGate connection parameters
- Retrieval of IPsec Phase 1 tunnels
- Selection of a specific tunnel
- Retrieval of the associated PSK using the API parameter `plain-text-password=1`
- Display of the PSK in the web interface

---

## Funzionalità

- Configurazione manuale dei parametri di connessione
- Recupero della lista dei tunnel IPsec Phase 1
- Selezione di un tunnel specifico
- Recupero della PSK tramite parametro API `plain-text-password=1`
- Visualizzazione della chiave nell'interfaccia web

---

## Requirements

- Python 3.10 or newer
- Flask
- requests
- FortiGate reachable via HTTPS
- API token with sufficient privileges (typically `super_admin`)
- Correct VDOM context in multi-VDOM environments

---

## Requisiti

- Python 3.10 o superiore
- Flask
- requests
- FortiGate raggiungibile via HTTPS
- API token con privilegi adeguati (tipicamente `super_admin`)
- Contesto VDOM corretto

---

## Installation

```bash
git clone <repository-url>
cd fortigate-ipsec-psk-ui
pip install -r requirements.txt
python app.py
```

Access:

```
http://127.0.0.1:5001
```

---

## Installazione

```bash
git clone <repository-url>
cd fortigate-ipsec-psk-ui
pip install -r requirements.txt
python app.py
```

Aprire:

```
http://127.0.0.1:5001
```

---

## Security

This project is designed for controlled environments and trusted operators.

It must not be deployed as a publicly accessible service.

The application does not implement authentication, access control, or encryption layers beyond what is provided by the FortiGate API and the execution environment.

---

## Sicurezza

Questo progetto è progettato per ambienti controllati e operatori fidati.

Non deve essere esposto come servizio pubblico.

L'applicazione non implementa meccanismi di autenticazione o controllo accessi aggiuntivi rispetto a quelli forniti dal FortiGate.

---

## Security Considerations

This application processes highly sensitive information:

- FortiGate API tokens
- IPsec pre-shared keys in plain text

Operational recommendations:

- Run only on localhost (127.0.0.1)
- Do not expose the interface externally
- Use dedicated API administrators
- Restrict API access using trusted hosts
- Avoid disabling SSL verification unless strictly necessary
- Do not log or persist sensitive data
- Rotate API tokens when appropriate

---

## Considerazioni di sicurezza

Questa applicazione gestisce informazioni altamente sensibili:

- API token FortiGate
- Pre-shared key IPsec in chiaro

Raccomandazioni operative:

- Eseguire solo su localhost (127.0.0.1)
- Non esporre l'interfaccia all'esterno
- Utilizzare utenti API dedicati
- Limitare l'accesso tramite trusted hosts
- Evitare di disabilitare SSL se non necessario
- Non salvare o loggare dati sensibili
- Ruotare i token API quando opportuno

---

## Limitations

- Plain-text PSK retrieval depends on FortiGate firmware behavior
- The API may still return encrypted values (e.g. `ENC ...`)
- Requires sufficient administrative privileges
- Incorrect VDOM selection may prevent access to the desired configuration
- Not intended for large-scale automation

---

## Limitazioni

- La disponibilità della PSK in chiaro dipende dal firmware FortiGate
- L'API può restituire valori cifrati (`ENC ...`)
- Richiede privilegi amministrativi adeguati
- Un VDOM errato può impedire l'accesso
- Non pensato per automazioni massive

---

## Official References

Fortinet Community:

Technical Tip: Use the FortiGate API to recover an IPsec pre-shared key in plain text format  
[[https://community.fortinet.com/t5/FortiGate/Technical-Tip-Use-the-FortiGate-API-to-recover-an-IPsec-pre/ta-p/331876](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Use-the-FortiGate-API-to-recover-an-IPsec-pre/ta-p/331876)
](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Use-the-FortiGate-API-to-recover-an-IPsec-pre/ta-p/331876)

---

## Disclaimer

This project is intended exclusively for authorized administrative use.

The author does not support or encourage:

- unauthorized access to systems
- attempts to bypass vendor security controls
- reverse engineering of encrypted configuration data

Use of this tool is entirely at the user's responsibility.

---

## License

MIT

