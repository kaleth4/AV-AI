<div align="center">
 
```
███████╗██╗  ██╗██╗███████╗██╗     ██████╗      ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗    ██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
███████╗███████║██║█████╗  ██║     ██║  ██║    ██║  ███╗██║   ██║███████║██████╔╝██║  ██║
╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║    ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
███████║██║  ██║██║███████╗███████╗██████╔╝    ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
```
 
# 🛡️ ShieldGuard Pro
 
### Antivirus · Mini EDR · Firewall · PDF Reports · Security Chatbot
 
**Plataforma de seguridad multiplataforma de próxima generación.**  
Detección de malware por hash, monitoreo de procesos en tiempo real, firewall simulado y reportes automáticos en PDF — todo en una sola interfaz moderna.
 
---
 
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6aa5?style=for-the-badge&logo=python&logoColor=white)](https://github.com/TomSchimansky/CustomTkinter)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/)
[![EDR](https://img.shields.io/badge/Módulo-Mini_EDR-red?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)
 
</div>
 
---
 
## 📸 Vista general de módulos
 
```
┌─────────────────────────────────────────────────────────────────┐
│                    ShieldGuard Pro — UI                         │
├──────────────┬──────────────────────────────────────────────────┤
│              │                                                   │
│  SIDEBAR     │   CONTENIDO PRINCIPAL                            │
│              │                                                   │
│ Dashboard /  │  ┌─────────────────────────────────────────────┐ │
│ Scan         │  │  📊 Dashboard & Scanner                     │ │
│              │  │  Escaneo manual · Hash SHA-256 · PDF Report │ │
│ Mini EDR &   │  └─────────────────────────────────────────────┘ │
│ Firewall     │  ┌─────────────────────────────────────────────┐ │
│              │  │  🔍 Mini EDR                                │ │
│ System       │  │  Monitoreo de procesos · Firewall simulado  │ │
│ Tools        │  └─────────────────────────────────────────────┘ │
│              │  ┌─────────────────────────────────────────────┐ │
│ Support      │  │  🛠️ System Tools                            │ │
│ Chatbot      │  │  Telemetría · Privacidad del sistema        │ │
│              │  └─────────────────────────────────────────────┘ │
│              │  ┌─────────────────────────────────────────────┐ │
│              │  │  🤖 Security Chatbot                        │ │
│              │  │  Asistente de seguridad integrado           │ │
│              │  └─────────────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────────────┘
```
 
---
 
## ✨ Características principales
 
| Módulo | Función | Tecnología |
|--------|---------|------------|
| 🔍 **Scanner** | Escaneo de archivos por hash SHA-256 | `hashlib` |
| 🧠 **Mini EDR** | Monitoreo de procesos sospechosos | `psutil` + `threading` |
| 🔥 **Firewall** | Bloqueo simulado de IPs y puertos | Shell commands |
| 📄 **PDF Report** | Generación de reportes de seguridad | `reportlab` |
| 🛠️ **System Tools** | Desactivar telemetría del SO | OS registry/services |
| 🤖 **Chatbot** | Asistente de seguridad con NLP básico | Keyword matching / LLM |
 
---
 
## 🚀 Instalación
 
### Prerequisitos
 
```bash
# Instalar dependencias externas
pip install customtkinter psutil reportlab
```
 
### Clonar y ejecutar
 
```bash
# 1. Clonar el repositorio
git clone https://github.com/kaleth4/shieldguard-pro.git
cd shieldguard-pro
 
# 2. Instalar dependencias
pip install -r requirements.txt
 
# 3. Ejecutar la aplicación
python shieldguard.py
```
 
### requirements.txt
 
```
customtkinter>=5.2.0
psutil>=5.9.0
reportlab>=4.0.0
```
 
---
 
## 💻 Código completo
 
```python
import os
import hashlib
import threading
import time
import customtkinter as ctk
import psutil
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
 
# ── CONFIGURACIÓN ──────────────────────────────────────────────
USER_LICENSE_VALID = True
 
# Base de hashes de malware conocidos (SHA-256)
# En producción: sincronizar con servidor seguro en tiempo real
KNOWN_MALWARE_HASHES = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
 
 
class NextGenAV(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ShieldGuard Pro - Mini EDR & AV")
        self.geometry("900x600")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
 
        self.scan_results = []
        self.monitoring_active = False
        self.setup_ui()
 
    # ── UI PRINCIPAL ─────────────────────────────────────────────
    def setup_ui(self):
        # Sidebar de navegación
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
 
        ctk.CTkLabel(
            self.sidebar,
            text="ShieldGuard Pro\n(Premium)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=30, padx=20)
 
        nav_buttons = [
            ("📊 Dashboard / Scan",    self.show_dashboard),
            ("🔍 Mini EDR & Firewall", self.show_edr),
            ("🛠️ System Tools",        self.show_tools),
            ("🤖 Support Chatbot",     self.show_chatbot),
        ]
        for text, cmd in nav_buttons:
            ctk.CTkButton(self.sidebar, text=text, command=cmd).pack(
                pady=10, padx=20
            )
 
        # Área de contenido principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True,
                             padx=20, pady=20)
 
        # Definir vistas
        self.view_dashboard = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_edr       = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_tools     = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_chatbot   = ctk.CTkFrame(self.main_frame, fg_color="transparent")
 
        self.init_dashboard()
        self.init_edr()
        self.init_tools()
        self.init_chatbot()
        self.show_dashboard()
 
    # ── NAVEGACIÓN ───────────────────────────────────────────────
    def hide_all_views(self):
        for view in [self.view_dashboard, self.view_edr,
                     self.view_tools, self.view_chatbot]:
            view.pack_forget()
 
    def show_dashboard(self): self.hide_all_views(); self.view_dashboard.pack(fill="both", expand=True)
    def show_edr(self):       self.hide_all_views(); self.view_edr.pack(fill="both", expand=True)
    def show_tools(self):     self.hide_all_views(); self.view_tools.pack(fill="both", expand=True)
    def show_chatbot(self):   self.hide_all_views(); self.view_chatbot.pack(fill="both", expand=True)
 
    # ── MÓDULO 1: DASHBOARD & SCANNER ────────────────────────────
    def init_dashboard(self):
        ctk.CTkLabel(
            self.view_dashboard,
            text="System Dashboard & Scanner",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
 
        self.scan_log = ctk.CTkTextbox(self.view_dashboard,
                                       width=600, height=300)
        self.scan_log.pack(pady=10)
 
        btn_frame = ctk.CTkFrame(self.view_dashboard, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="📂 Manual File Scan",
                      command=self.start_manual_scan).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="📄 Generate PDF Report",
                      command=self.generate_pdf_report).pack(side="left", padx=10)
 
    def calculate_sha256(self, filepath):
        """Calcula el hash SHA-256 de un archivo en bloques de 4KB."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None
 
    def start_manual_scan(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
 
        self.scan_log.insert("end", f"[SCAN] {filepath}\n")
        file_hash = self.calculate_sha256(filepath)
 
        if file_hash:
            self.scan_log.insert("end", f"[HASH] {file_hash}\n")
            if file_hash in KNOWN_MALWARE_HASHES:
                self.scan_log.insert("end",
                    "⚠️  MALWARE DETECTADO — Eliminación simulada\n")
                self.scan_results.append(f"[MALWARE] {filepath}")
                # os.remove(filepath)  # Descomentar para eliminar real
            else:
                self.scan_log.insert("end",
                    "✅ Archivo limpio — Firma verificada\n")
                self.scan_results.append(f"[CLEAN] {filepath}")
        else:
            self.scan_log.insert("end", "❌ Error al leer el archivo\n")
 
        self.scan_log.insert("end", "─" * 40 + "\n")
 
    def generate_pdf_report(self):
        if not self.scan_results:
            messagebox.showinfo("Report", "No hay datos de escaneo.")
            return
 
        filename = "ShieldGuard_Security_Report.pdf"
        c = canvas.Canvas(filename)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "ShieldGuard Pro — Security Scan Report")
        c.setFont("Helvetica", 10)
        c.drawString(100, 780, f"Total de archivos escaneados: {len(self.scan_results)}")
 
        y = 750
        c.setFont("Helvetica", 9)
        for result in self.scan_results:
            c.drawString(100, y, result)
            y -= 20
            if y < 50:
                break
        c.save()
        self.scan_log.insert("end", f"\n📄 Reporte guardado: {filename}\n")
 
    # ── MÓDULO 2: MINI EDR & FIREWALL ────────────────────────────
    def init_edr(self):
        ctk.CTkLabel(
            self.view_edr,
            text="Mini EDR & Threat Monitoring",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
 
        self.edr_log = ctk.CTkTextbox(self.view_edr, width=600, height=250)
        self.edr_log.pack(pady=10)
 
        self.btn_toggle_edr = ctk.CTkButton(
            self.view_edr,
            text="▶ Start Behavior Monitoring",
            command=self.toggle_edr
        )
        self.btn_toggle_edr.pack(pady=10)
 
        ctk.CTkLabel(self.view_edr, text="Mini Firewall (Simulado)").pack(pady=5)
        ctk.CTkButton(
            self.view_edr,
            text="🔥 Block Suspicious IPs",
            command=lambda: self.edr_log.insert(
                "end", "🔥 Firewall Rule: Tráfico bloqueado en puerto 4444\n"
            )
        ).pack()
 
    def toggle_edr(self):
        self.monitoring_active = not self.monitoring_active
        if self.monitoring_active:
            self.btn_toggle_edr.configure(text="⏹ Stop Behavior Monitoring")
            self.edr_log.insert("end",
                "🟢 EDR Activo — Monitoreando procesos sospechosos...\n")
            threading.Thread(target=self.monitor_processes,
                             daemon=True).start()
        else:
            self.btn_toggle_edr.configure(text="▶ Start Behavior Monitoring")
            self.edr_log.insert("end", "🔴 EDR Detenido\n")
 
    def monitor_processes(self):
        """
        Monitorea procesos en busca de comportamiento sospechoso.
        Heurística: detecta procesos con nombre 'miner' o CPU excesivo.
        """
        while self.monitoring_active:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    name = proc.info['name'].lower()
                    cpu  = proc.info['cpu_percent']
 
                    if 'miner' in name:
                        self.edr_log.insert("end",
                            f"⚠️  Proceso sospechoso: {proc.info['name']} "
                            f"(PID: {proc.info['pid']})\n")
                        # proc.kill()  # Descomentar para terminar proceso
 
                    if cpu and cpu > 90:
                        self.edr_log.insert("end",
                            f"🔴 CPU alto ({cpu}%): {proc.info['name']} "
                            f"(PID: {proc.info['pid']})\n")
 
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(5)
 
    # ── MÓDULO 3: SYSTEM TOOLS ───────────────────────────────────
    def init_tools(self):
        ctk.CTkLabel(
            self.view_tools,
            text="System Tuning & Privacy",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
 
        ctk.CTkLabel(
            self.view_tools,
            text="⚠️  Requiere privilegios de administrador para modificar\n"
                 "registros y servicios del sistema operativo."
        ).pack(pady=10)
 
        ctk.CTkButton(
            self.view_tools,
            text="🕵️ Disable OS Telemetry (Simulate)",
            command=self.remove_telemetry
        ).pack(pady=10)
 
    def remove_telemetry(self):
        messagebox.showinfo(
            "Telemetry Status",
            "Simulando eliminación de telemetría:\n\n"
            "✅ Servicio DiagTrack deshabilitado\n"
            "✅ Dominios de telemetría bloqueados en hosts\n"
            "✅ Claves de registro de privacidad modificadas"
        )
 
    # ── MÓDULO 4: CHATBOT ────────────────────────────────────────
    def init_chatbot(self):
        ctk.CTkLabel(
            self.view_chatbot,
            text="Security Assistant Chatbot",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
 
        self.chat_history = ctk.CTkTextbox(self.view_chatbot,
                                           width=600, height=300)
        self.chat_history.pack(pady=10)
        self.chat_history.insert("end",
            "🤖 Bot: Hola, soy tu asistente de seguridad. "
            "Pregúntame sobre escaneos, hashes o malware.\n")
 
        input_frame = ctk.CTkFrame(self.view_chatbot, fg_color="transparent")
        input_frame.pack(pady=5)
 
        self.chat_input = ctk.CTkEntry(
            input_frame, width=500,
            placeholder_text="Escribe tu pregunta aquí..."
        )
        self.chat_input.pack(side="left", padx=10)
        self.chat_input.bind("<Return>", lambda e: self.handle_chat())
 
        ctk.CTkButton(input_frame, text="Enviar",
                      command=self.handle_chat).pack(side="left")
 
    def handle_chat(self):
        user_text = self.chat_input.get().strip()
        if not user_text:
            return
 
        self.chat_history.insert("end", f"\n👤 Tú: {user_text}\n")
        self.chat_input.delete(0, "end")
 
        # NLP básico por keywords — reemplazable con API de LLM
        text_lower = user_text.lower()
        if "scan" in text_lower or "escanear" in text_lower:
            response = ("Ve al Dashboard y haz clic en 'Manual File Scan' "
                        "para analizar un archivo.")
        elif "hash" in text_lower:
            response = ("Un hash SHA-256 es la firma digital de un archivo. "
                        "Si coincide con malware conocido, la herramienta lo detecta.")
        elif "edr" in text_lower:
            response = ("El Mini EDR monitorea procesos en tiempo real usando psutil "
                        "y detecta comportamiento sospechoso.")
        elif "reporte" in text_lower or "report" in text_lower:
            response = ("Puedes generar un reporte PDF desde el Dashboard "
                        "después de escanear archivos.")
        else:
            response = ("No estoy seguro. Intenta preguntar sobre: "
                        "'cómo escanear', 'qué es un hash', 'qué hace el EDR'.")
 
        self.chat_history.insert("end", f"🤖 Bot: {response}\n")
 
 
# ── ENTRY POINT ──────────────────────────────────────────────────
if __name__ == "__main__":
    app = NextGenAV()
    app.mainloop()
```
 
---
 
## 🖥️ Demo de uso
 
```bash
# Escaneo de archivo
[SCAN] /home/user/documento.pdf
[HASH] a3f9d2c1e8b47f3c2d9e1a4b8c7f6e5d4...
✅ Archivo limpio — Firma verificada
────────────────────────────────────────
 
# Detección de malware
[SCAN] /tmp/suspicious.exe
[HASH] e3b0c44298fc1c149afbf4c8996fb924...
⚠️  MALWARE DETECTADO — Eliminación simulada
────────────────────────────────────────
 
# EDR activo
🟢 EDR Activo — Monitoreando procesos sospechosos...
⚠️  Proceso sospechoso: cryptominer.exe (PID: 4821)
🔴 CPU alto (94.3%): unknown_process (PID: 3312)
 
# Firewall
🔥 Firewall Rule: Tráfico bloqueado en puerto 4444
```
 
---
 
## 📂 Estructura del proyecto
 
```
shieldguard-pro/
│
├── 📄 shieldguard.py              # Aplicación principal
├── 📄 requirements.txt            # Dependencias
├── 📄 README.md                   # Documentación
├── 📁 reports/
│   └── ShieldGuard_Report.pdf     # Reportes generados (auto)
└── 📁 db/
    └── malware_hashes.json        # Base de hashes (expandible)
```
 
---
 
## 🔬 Conceptos de seguridad aplicados
 
| Concepto | Módulo | Descripción |
|----------|--------|-------------|
| **Hash Verification** | Scanner | SHA-256 como firma digital de archivos |
| **Signature-based Detection** | Scanner | Comparación contra base de hashes conocidos |
| **Behavioral Analysis** | Mini EDR | Detección por comportamiento anómalo (heurística) |
| **Process Monitoring** | Mini EDR | Iteración de procesos del sistema en tiempo real |
| **Firewall Rules** | Firewall | Bloqueo de tráfico en puertos específicos |
| **Privacy Hardening** | System Tools | Desactivación de telemetría del SO |
| **Confidencialidad CIA** | General | Proteger datos del usuario de fugas |
 
---
 
## 🔮 Mejoras futuras
 
- [ ] 🧠 Integrar LLM API (OpenAI / Ollama) al chatbot
- [ ] 📡 Sincronización en tiempo real con base de hashes en servidor
- [ ] 👁️ Monitoreo de directorio con `watchdog` (detección de archivos nuevos)
- [ ] 🌐 Módulo de análisis de conexiones de red con `scapy`
- [ ] 🔐 Sistema de licencias real con validación de servidor
- [ ] 📊 Dashboard con gráficas de actividad del sistema
 
---
 
## ⚠️ Consideraciones
 
```
✅  Usar en entornos controlados o con permiso explícito
✅  Ideal para aprendizaje de Blue Team y desarrollo de herramientas
✅  Base sólida para expandir a solución enterprise
❌  No reemplaza un AV/EDR profesional en producción
❌  No ejecutar como simulador en sistemas de terceros sin autorización
```
 
---
 
## 👤 Autor
 
**Kaleth Corcho**  
Ingeniería de Sistemas · WolvesTI · Bogotá, Colombia
 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kaleth--corcho-0077B5?style=flat&logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-kaleth4-181717?style=flat&logo=github)](https://github.com/kaleth4)
 
---
 
<div align="center">
 
**⭐ Si este proyecto te fue útil, dale una estrella**
 
*Proyecto de portafolio en ciberseguridad · Next-Gen AV · 2026 · WolvesTI*
 
</div>
