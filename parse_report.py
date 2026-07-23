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
            print("\n==========================================")
            print("         📊 RESUMEN DE DEPENDABOT          ")
            print("==========================================\n")
            
            target = data.get("target", "Desconocido")
            status = data.get("status", "N/A")
            updates = data.get("updates", [])

            print(f"🎯 Proyecto Objetivo : {target}")
            print(f"⚡ Estado de Ejecución: {status.upper()}")
            print(f"📦 Actualizaciones   : {len(updates)}\n")

            if updates:
                print("--- Detalle de Paquetes ---")
                for item in updates:
                    pkg = item.get("package", "Desconocido")
                    old_v = item.get("old_version", "?")
                    new_v = item.get("new_version", "?")
                    type_up = item.get("type", "routine").upper()
                    
                    print(f" • [{type_up}] {pkg}: {old_v} ➡️ {new_v}")
            print("\n==========================================\n")

        except Exception as e:
            print(f"❌ Error al leer el YAML: {e}")

if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else "result.yaml"
    parse_dependabot_result(report_file)
