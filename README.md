# 🤖 Bot Reportes

Proyecto orquestador diseñado para procesar, transformar y notificar los resultados generados por el runner de Dependabot.

## 🏗️ Arquitectura
- **Motor (Core):** `dependabot/cli` (Ejecuta el análisis de dependencias).
- **Puente (Wrapper):** `bot-reportes` (Lee los resultados y envía las notificaciones).
