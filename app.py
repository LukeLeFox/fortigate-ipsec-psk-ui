#!/usr/bin/env python3

from dataclasses import dataclass

import requests
from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

REQUEST_TIMEOUT = 15


@dataclass
class Phase1Item:
    name: str
    interface: str | None = None
    remote_gw: str | None = None
    psksecret: str | None = None


def normalize_host(host: str) -> str:
    host = host.strip()
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "https://" + host
    return host.rstrip("/")


def get_runtime_config() -> dict:
    return {
        "host": session.get("host", ""),
        "token": session.get("token", ""),
        "vdom": session.get("vdom", ""),
        "verify_ssl": session.get("verify_ssl", False),
    }


def has_config() -> bool:
    cfg = get_runtime_config()
    return bool(cfg["host"] and cfg["token"])


def build_headers() -> dict[str, str]:
    cfg = get_runtime_config()
    return {
        "Authorization": f"Bearer {cfg['token']}",
        "Accept": "application/json",
    }


def build_params(extra: dict | None = None) -> dict:
    cfg = get_runtime_config()
    params = {}
    if cfg["vdom"]:
        params["vdom"] = cfg["vdom"]
    if extra:
        params.update(extra)
    return params


def api_get(path: str, extra_params: dict | None = None) -> dict:
    cfg = get_runtime_config()
    url = f"{cfg['host']}{path}"

    if not cfg["verify_ssl"]:
        requests.packages.urllib3.disable_warnings()

    response = requests.get(
        url,
        headers=build_headers(),
        params=build_params(extra_params),
        verify=cfg["verify_ssl"],
        timeout=REQUEST_TIMEOUT,
    )

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text[:500]}")

    try:
        return response.json()
    except ValueError as exc:
        raise Exception("La risposta del FortiGate non è JSON valido") from exc


def normalize_results(data: dict) -> list[dict]:
    results = data.get("results", [])

    if isinstance(results, dict):
        return [results]

    if isinstance(results, list):
        return [item for item in results if isinstance(item, dict)]

    return []


def get_phase1_list() -> list[Phase1Item]:
    data = api_get("/api/v2/cmdb/vpn.ipsec/phase1-interface")
    results = normalize_results(data)

    items = []
    for item in results:
        name = str(item.get("name", "")).strip()
        if not name:
            continue

        items.append(
            Phase1Item(
                name=name,
                interface=item.get("interface"),
                remote_gw=item.get("remote-gw"),
                psksecret=item.get("psksecret"),
            )
        )

    return sorted(items, key=lambda x: x.name.lower())


def get_phase1_list_with_plaintext() -> list[Phase1Item]:
    data = api_get(
        "/api/v2/cmdb/vpn.ipsec/phase1-interface",
        {"plain-text-password": 1},
    )
    results = normalize_results(data)

    items = []
    for item in results:
        name = str(item.get("name", "")).strip()
        if not name:
            continue

        items.append(
            Phase1Item(
                name=name,
                interface=item.get("interface"),
                remote_gw=item.get("remote-gw"),
                psksecret=item.get("psksecret"),
            )
        )

    return sorted(items, key=lambda x: x.name.lower())


def get_psk_from_all_tunnels(selected_name: str) -> str | None:
    items = get_phase1_list_with_plaintext()
    for item in items:
        if item.name == selected_name:
            return item.psksecret
    return None


TEMPLATE = """
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <title>FortiGate PSK Recovery</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 1100px;
      margin: 40px auto;
      padding: 0 20px;
      background: #f7f7f7;
    }
    h1 {
      font-size: 48px;
      margin-bottom: 24px;
    }
    .box {
      margin-top: 20px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 20px;
    }
    .label {
      font-weight: bold;
      font-size: 20px;
      margin-bottom: 12px;
    }
    .row {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .col {
      display: flex;
      flex-direction: column;
      gap: 8px;
      flex: 1;
    }
    input[type="text"], input[type="password"], select {
      width: 100%;
      padding: 14px;
      font-size: 18px;
      border-radius: 8px;
      border: 1px solid #bbb;
      background: #fff;
      box-sizing: border-box;
    }
    button {
      padding: 14px 20px;
      font-size: 18px;
      border-radius: 8px;
      border: 1px solid #aaa;
      cursor: pointer;
      background: #efefef;
    }
    .actions {
      display: flex;
      gap: 12px;
      margin-top: 16px;
    }
    .psk {
      font-family: Consolas, monospace;
      font-size: 20px;
      background: #f3f3f3;
      padding: 14px;
      border-radius: 8px;
      word-break: break-all;
    }
    .error {
      margin-top: 18px;
      color: red;
      font-size: 18px;
    }
    .warn {
      margin-top: 16px;
      color: #9a6700;
      font-size: 17px;
    }
    .meta {
      color: #555;
      font-size: 14px;
      margin-top: 14px;
    }
    .checkbox-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 10px;
      font-size: 16px;
    }
  </style>
</head>
<body>
  <h1>FortiGate PSK Recovery</h1>

  <div class="box">
    <div class="label">Connessione</div>

    <form method="post" action="/connect">
      <div class="col">
        <label for="host">FortiGate URL o IP</label>
        <input type="text" id="host" name="host" placeholder="es: 192.168.1.1 oppure https://192.168.1.1" value="{{ cfg.host }}" required>

        <label for="token">API Token</label>
        <input type="password" id="token" name="token" placeholder="Inserisci API token" value="{{ cfg.token }}" required>

        <label for="vdom">VDOM</label>
        <input type="text" id="vdom" name="vdom" placeholder="lascia vuoto per default/root" value="{{ cfg.vdom }}">

        <label class="checkbox-row">
          <input type="checkbox" name="verify_ssl" {% if cfg.verify_ssl %}checked{% endif %}>
          Verifica SSL
        </label>
      </div>

      <div class="actions">
        <button type="submit">Connetti</button>
        {% if connected %}
          <button type="submit" formaction="/disconnect" formmethod="post">Reset</button>
        {% endif %}
      </div>
    </form>

    {% if cfg.host %}
      <div class="meta">
        Host: {{ cfg.host }}{% if cfg.vdom %} | VDOM: {{ cfg.vdom }}{% endif %} | SSL verify: {{ "on" if cfg.verify_ssl else "off" }}
      </div>
    {% endif %}
  </div>

  {% if connected %}
    <div class="box">
      <div class="label">Seleziona tunnel</div>

      <form method="post" action="/recover">
        <div class="row">
          <select name="phase1" required>
            <option value="">-- Seleziona VPN --</option>
            {% for i in items %}
              <option value="{{ i.name }}" {% if selected_name == i.name %}selected{% endif %}>
                {{ i.name }}{% if i.interface %} ({{ i.interface }}{% if i.remote_gw %} - {{ i.remote_gw }}{% endif %}){% endif %}
              </option>
            {% endfor %}
          </select>
          <button type="submit">Recupera</button>
        </div>
      </form>
    </div>
  {% endif %}

  {% if selected_name %}
    <div class="box">
      <div class="label">Tunnel selezionato</div>
      <div>{{ selected_name }}</div>
    </div>
  {% endif %}

  {% if psk %}
    <div class="box">
      <div class="label">PSK</div>
      <div class="psk">{{ psk }}</div>
      {% if encrypted_notice %}
        <div class="warn">
          Attenzione: il FortiGate ha restituito ancora un valore cifrato/mascherato ("ENC ...").
        </div>
      {% endif %}
    </div>
  {% endif %}

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}
</body>
</html>
"""


def render_page(
    *,
    items=None,
    psk=None,
    error=None,
    selected_name=None,
    encrypted_notice=False,
):
    if items is None:
        items = []

    return render_template_string(
        TEMPLATE,
        cfg=get_runtime_config(),
        connected=has_config(),
        items=items,
        psk=psk,
        error=error,
        selected_name=selected_name,
        encrypted_notice=encrypted_notice,
    )


@app.route("/", methods=["GET"])
def index():
    if not has_config():
        return render_page()

    try:
        items = get_phase1_list()
        return render_page(items=items)
    except Exception as exc:
        return render_page(error=str(exc)), 500


@app.route("/connect", methods=["POST"])
def connect():
    host = normalize_host(request.form.get("host", ""))
    token = request.form.get("token", "").strip()
    vdom = request.form.get("vdom", "").strip()
    verify_ssl = bool(request.form.get("verify_ssl"))

    session["host"] = host
    session["token"] = token
    session["vdom"] = vdom
    session["verify_ssl"] = verify_ssl

    try:
        items = get_phase1_list()
        return render_page(items=items)
    except Exception as exc:
        return render_page(error=str(exc)), 500


@app.route("/disconnect", methods=["POST"])
def disconnect():
    session.clear()
    return render_page()


@app.route("/recover", methods=["POST"])
def recover():
    if not has_config():
        return render_page(error="Configura prima la connessione al FortiGate."), 400

    selected_name = request.form.get("phase1", "").strip()

    try:
        items = get_phase1_list()

        if not selected_name:
            return render_page(
                items=items,
                error="Nessun tunnel selezionato.",
            )

        psk = get_psk_from_all_tunnels(selected_name)

        if not psk:
            return render_page(
                items=items,
                selected_name=selected_name,
                error=f"Nessuna PSK trovata per '{selected_name}'.",
            )

        encrypted_notice = psk.strip().upper().startswith("ENC ")

        return render_page(
            items=items,
            psk=psk,
            selected_name=selected_name,
            encrypted_notice=encrypted_notice,
        )

    except Exception as exc:
        try:
            items = get_phase1_list()
        except Exception:
            items = []

        return render_page(
            items=items,
            error=str(exc),
            selected_name=selected_name if selected_name else None,
        ), 500


if __name__ == "__main__":
    print("Avvio server su http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=False)
