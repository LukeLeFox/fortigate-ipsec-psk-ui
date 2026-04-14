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
- No offline processing of configuration files
- No attempt to bypass FortiGate access controls
- Stateless interaction with the firewall API
- Designed for temporary administrative use

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

The application provides the following features:

- Manual configuration of FortiGate connection parameters (host, token, VDOM, SSL verification)
- Retrieval of IPsec Phase 1 tunnel list
- Selection of a specific tunnel
- Retrieval of the associated PSK using the FortiGate API parameter `plain-text-password=1`
- Display of the PSK in the web interface

---

## Funzionalità

L'applicazione fornisce le seguenti funzionalità:

- Configurazione manuale dei parametri di connessione (host, token, VDOM, verifica SSL)
- Recupero della lista delle VPN IPsec Phase 1
- Selezione di un tunnel specifico
- Recupero della PSK tramite parametro API `plain-text-password=1`
- Visualizzazione della chiave in interfaccia web

---

## Requirements

- Python 3.10 or newer
- Flask
- requests
- FortiGate device reachable via HTTPS
- API token with sufficient privileges (typically `super_admin`)
- Correct VDOM context if multi-VDOM is in use

---

## Requisiti

- Python 3.10 o superiore
- Flask
- requests
- Dispositivo FortiGate raggiungibile via HTTPS
- API token con privilegi adeguati (tipicamente `super_admin`)
- Contesto VDOM corretto in ambienti multi-VDOM

---

## Installation

```bash
git clone <repository-url>
cd fortigate-ipsec-psk-ui
pip install -r requirements.txt
python app.py
