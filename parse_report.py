import os
import sys
import yaml

def parse_dependabot_result(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️ No se encontró el archivo de reporte: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            print("=== 📊 RESUMEN DE DEPENDABOT ===")
            print(f"Estructura cargada correctamente: {type(data)}")
            # Aquí procesaremos las métricas y vulnerabilidades encontradas
        except Exception as e:
            print(f"❌ Error al leer el YAML: {e}")

if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else "result.yaml"
    parse_dependabot_result(report_file)
