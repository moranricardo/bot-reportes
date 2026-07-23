import os
import sys
import yaml
import requests

def create_github_issue(repo, token, title, body):
    """Crea un Issue en el repositorio especificado usando la API de GitHub."""
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "title": title,
        "body": body,
        "labels": ["dependabot", "reporte"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        issue_url = response.json().get("html_url")
        print(f"✅ Issue creado exitosamente: {issue_url}")
    else:
        print(f"❌ Error al crear el Issue ({response.status_code}): {response.text}")

def parse_dependabot_result(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️ No se encontró el archivo de reporte: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            target = data.get("target", "Desconocido")
            status = data.get("status", "N/A")
            updates = data.get("updates", [])

            # Formatear el contenido del reporte
            title = f"📊 Reporte de Dependabot: {target} [{status.upper()}]"
            
            body_lines = [
                f"### 🎯 Proyecto Objetivo: `{target}`",
                f"**Estado de Ejecución:** `{status.upper()}`",
                f"**Total de Actualizaciones:** {len(updates)}",
                "",
                "### 📦 Detalle de Paquetes:"
            ]

            if updates:
                for item in updates:
                    pkg = item.get("package", "Desconocido")
                    old_v = item.get("old_version", "?")
                    new_v = item.get("new_version", "?")
                    type_up = item.get("type", "routine").upper()
                    body_lines.append(f"- **[{type_up}]** `{pkg}`: `{old_v}` ➡️ `{new_v}`")
            else:
                body_lines.append("_No hay actualizaciones pendientes._")

            body_content = "\n".join(body_lines)
            
            # Imprimir en consola
            print("\n" + body_content + "\n")

            # Intentar publicar el Issue si existe el token en el entorno
            token = os.environ.get("GITHUB_TOKEN")
            repo = os.environ.get("GITHUB_REPOSITORY", "moranricardo/bot-reportes")

            if token:
                create_github_issue(repo, token, title, body_content)
            else:
                print("ℹ️ Variable GITHUB_TOKEN no encontrada. (Procesado solo en consola local)")

        except Exception as e:
            print(f"❌ Error al leer o procesar el YAML: {e}")

if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else "result.yaml"
    parse_dependabot_result(report_file)
