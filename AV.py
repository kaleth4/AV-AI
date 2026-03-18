import os
import hashlib
import threading
import time
import customtkinter as ctk
import psutil
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas

# --- Configuration & Dummy Databases ---
# In a real app, this would be fetched from a secure server (One-time payment validation)
USER_LICENSE_VALID = True 
# Dummy hash for testing (this is the SHA-256 hash of an empty text file)
KNOWN_MALWARE_HASHES = {"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}

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

    def setup_ui(self):
        # --- Sidebar Navigation ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(self.sidebar, text="ShieldGuard Pro\n(Premium)", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.pack(pady=30, padx=20)

        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard / Scan", command=self.show_dashboard)
        self.btn_dashboard.pack(pady=10, padx=20)

        self.btn_edr = ctk.CTkButton(self.sidebar, text="Mini EDR & Firewall", command=self.show_edr)
        self.btn_edr.pack(pady=10, padx=20)

        self.btn_tools = ctk.CTkButton(self.sidebar, text="System Tools", command=self.show_tools)
        self.btn_tools.pack(pady=10, padx=20)

        self.btn_chatbot = ctk.CTkButton(self.sidebar, text="Support Chatbot", command=self.show_chatbot)
        self.btn_chatbot.pack(pady=10, padx=20)

        # --- Main Content Area ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Define views
        self.view_dashboard = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_edr = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_tools = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_chatbot = ctk.CTkFrame(self.main_frame, fg_color="transparent")

        self.init_dashboard()
        self.init_edr()
        self.init_tools()
        self.init_chatbot()

        self.show_dashboard()

    # --- UI View Switchers ---
    def hide_all_views(self):
        for view in [self.view_dashboard, self.view_edr, self.view_tools, self.view_chatbot]:
            view.pack_forget()

    def show_dashboard(self):
        self.hide_all_views()
        self.view_dashboard.pack(fill="both", expand=True)

    def show_edr(self):
        self.hide_all_views()
        self.view_edr.pack(fill="both", expand=True)

    def show_tools(self):
        self.hide_all_views()
        self.view_tools.pack(fill="both", expand=True)

    def show_chatbot(self):
        self.hide_all_views()
        self.view_chatbot.pack(fill="both", expand=True)

    # --- 1. Dashboard & Scanner Module ---
    def init_dashboard(self):
        ctk.CTkLabel(self.view_dashboard, text="System Dashboard & Scanner", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        self.scan_log = ctk.CTkTextbox(self.view_dashboard, width=600, height=300)
        self.scan_log.pack(pady=10)

        btn_frame = ctk.CTkFrame(self.view_dashboard, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Manual File Scan", command=self.start_manual_scan).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Generate PDF Report", command=self.generate_pdf_report).pack(side="left", padx=10)

    def calculate_sha256(self, filepath):
        """Calculates the SHA-256 hash of a file for signature verification."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return None

    def start_manual_scan(self):
        filepath = filedialog.askopenfilename()
        if not filepath: return
        
        self.scan_log.insert("end", f"Scanning: {filepath}\n")
        file_hash = self.calculate_sha256(filepath)
        
        if file_hash:
            self.scan_log.insert("end", f"Hash: {file_hash}\n")
            if file_hash in KNOWN_MALWARE_HASHES:
                self.scan_log.insert("end", "⚠️ MALWARE DETECTED! (Automated removal simulated)\n", "warning")
                self.scan_results.append(f"Malware Found: {filepath}")
                # os.remove(filepath) # UNCOMMENT TO ACTUALLY DELETE FILES (Be careful!)
            else:
                self.scan_log.insert("end", "✅ File is clean. Signature verified.\n")
                self.scan_results.append(f"Clean: {filepath}")
        else:
            self.scan_log.insert("end", "❌ Error reading file.\n")
        self.scan_log.insert("end", "-"*40 + "\n")

    def generate_pdf_report(self):
        if not self.scan_results:
            messagebox.showinfo("Report", "No scan data to report.")
            return
        
        filename = "Security_Report.pdf"
        c = canvas.Canvas(filename)
        c.drawString(100, 800, "ShieldGuard Pro - Security Scan Report")
        y = 750
        for result in self.scan_results:
            c.drawString(100, y, result)
            y -= 20
            if y < 50: # Page break logic omitted for brevity
                break
        c.save()
        self.scan_log.insert("end", f"\n📄 PDF Report saved as {filename}\n")

    # --- 2. Mini EDR & Firewall Module ---
    def init_edr(self):
        ctk.CTkLabel(self.view_edr, text="Mini EDR & Threat Monitoring", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        self.edr_log = ctk.CTkTextbox(self.view_edr, width=600, height=250)
        self.edr_log.pack(pady=10)

        self.btn_toggle_edr = ctk.CTkButton(self.view_edr, text="Start Behavior Monitoring", command=self.toggle_edr)
        self.btn_toggle_edr.pack(pady=10)

        ctk.CTkLabel(self.view_edr, text="Mini Firewall (Simulated)").pack(pady=5)
        ctk.CTkButton(self.view_edr, text="Block Suspicious IPs (Simulate)", command=lambda: self.edr_log.insert("end", "Firewall Rule Added: Blocked traffic on port 4444.\n")).pack()

    def toggle_edr(self):
        self.monitoring_active = not self.monitoring_active
        if self.monitoring_active:
            self.btn_toggle_edr.configure(text="Stop Behavior Monitoring")
            self.edr_log.insert("end", "EDR Active: Monitoring processes for suspicious behavior...\n")
            threading.Thread(target=self.monitor_processes, daemon=True).start()
        else:
            self.btn_toggle_edr.configure(text="Start Behavior Monitoring")
            self.edr_log.insert("end", "EDR Stopped.\n")

    def monitor_processes(self):
        """Monitors for suspicious behavior (e.g., high CPU usage by unknown apps)"""
        while self.monitoring_active:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    # Dummy heuristic: flag processes named 'miner' or using excessive CPU unexpectedly
                    if 'miner' in proc.info['name'].lower():
                        self.edr_log.insert("end", f"⚠️ Suspicious Process Detected: {proc.info['name']} (PID: {proc.info['pid']})\n")
                        # proc.kill() # UNCOMMENT TO AUTOMATE KILLING (Be careful!)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(5) # Poll every 5 seconds

    # --- 3. System Tools (Telemetry) ---
    def init_tools(self):
        ctk.CTkLabel(self.view_tools, text="System Tuning & Privacy", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.view_tools, text="These tools require administrative privileges to modify OS registries/services.").pack(pady=10)
        
        ctk.CTkButton(self.view_tools, text="Disable OS Telemetry (Simulate)", command=self.remove_telemetry).pack(pady=10)

    def remove_telemetry(self):
        messagebox.showinfo("Telemetry Status", "Simulating telemetry removal:\n- Disabled DiagTrack service\n- Blocked telemetry domains in hosts file\n- Modified privacy registry keys.")

    # --- 4. Custom Chatbot Module ---
    def init_chatbot(self):
        ctk.CTkLabel(self.view_chatbot, text="Security Assistant Chatbot", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        self.chat_history = ctk.CTkTextbox(self.view_chatbot, width=600, height=300)
        self.chat_history.pack(pady=10)
        self.chat_history.insert("end", "Bot: Hello! I'm your security assistant. Ask me about scans, hashes, or malware.\n")

        self.chat_input = ctk.CTkEntry(self.view_chatbot, width=500, placeholder_text="Type your question here...")
        self.chat_input.pack(side="left", padx=20)
        
        ctk.CTkButton(self.view_chatbot, text="Send", command=self.handle_chat).pack(side="left")

    def handle_chat(self):
        user_text = self.chat_input.get()
        if not user_text: return
        
        self.chat_history.insert("end", f"\nYou: {user_text}\n")
        self.chat_input.delete(0, "end")

        # Simple NLP logic (can be replaced with an LLM API)
        response = "Bot: I'm not sure. Try asking about 'how to scan' or 'what is a hash'."
        if "scan" in user_text.lower():
            response = "Bot: You can scan files by going to the Dashboard and clicking 'Manual File Scan'."
        elif "hash" in user_text.lower():
            response = "Bot: A hash is a digital signature of a file. We use SHA-256 to verify if a file is safe or known malware."

        self.chat_history.insert("end", response + "\n")

if __name__ == "__main__":
    app = NextGenAV()
    app.mainloop()