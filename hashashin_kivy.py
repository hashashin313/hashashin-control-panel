from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
import psutil
import platform
import os
import subprocess
import requests
import json
from datetime import datetime

class HashashinKivyApp(App):
    def __init__(self):
        super().__init__()
        # تنظیمات
        self.token = "7521330971:AAHg2yqZWNvPAaqI8XH1uvTI4Qh3TZLG2yg"
        self.chat_id = "1005013833"
        self.output_text = ""
        
    def build(self):
        Window.size = (800, 600)
        
        # Layout اصلی
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # عنوان
        title = Label(
            text='Hashashin Kivy Control Panel',
            font_size=24,
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(title)
        
        # دکمه‌های اصلی
        button_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=200)
        
        # دکمه‌های سیستم
        btn_system = Button(text='System Info', on_press=self.get_system_info)
        btn_processes = Button(text='Processes', on_press=self.get_processes)
        btn_services = Button(text='Services', on_press=self.get_services)
        btn_network = Button(text='Network', on_press=self.get_network)
        btn_disk = Button(text='Disk Space', on_press=self.get_disk_space)
        btn_users = Button(text='Users', on_press=self.get_users)
        
        button_layout.add_widget(btn_system)
        button_layout.add_widget(btn_processes)
        button_layout.add_widget(btn_services)
        button_layout.add_widget(btn_network)
        button_layout.add_widget(btn_disk)
        button_layout.add_widget(btn_users)
        
        main_layout.add_widget(button_layout)
        
        # دکمه‌های پیشرفته
        advanced_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=150)
        
        btn_cpu = Button(text='CPU Usage', on_press=self.get_cpu_usage)
        btn_memory = Button(text='Memory Usage', on_press=self.get_memory_usage)
        btn_uptime = Button(text='System Uptime', on_press=self.get_uptime)
        btn_apps = Button(text='Installed Apps', on_press=self.get_installed_apps)
        btn_security = Button(text='Security Check', on_press=self.security_check)
        btn_send = Button(text='Send to Telegram', on_press=self.send_to_telegram)
        
        advanced_layout.add_widget(btn_cpu)
        advanced_layout.add_widget(btn_memory)
        advanced_layout.add_widget(btn_uptime)
        advanced_layout.add_widget(btn_apps)
        advanced_layout.add_widget(btn_security)
        advanced_layout.add_widget(btn_send)
        
        main_layout.add_widget(advanced_layout)
        
        # ناحیه نمایش اطلاعات
        self.info_label = Label(
            text='Click buttons to get system information...',
            size_hint_y=None,
            height=200,
            text_size=(780, None)
        )
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.info_label)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def get_system_info(self, instance):
        info = f"""
System Information:
- OS: {platform.system()} {platform.release()}
- Architecture: {platform.machine()}
- Processor: {platform.processor()}
- Total Memory: {psutil.virtual_memory().total // (1024**3)} GB
- Available Memory: {psutil.virtual_memory().available // (1024**3)} GB
- CPU Cores: {psutil.cpu_count()}
        """
        self.info_label.text = info
        self.output_text = info
    
    def get_processes(self, instance):
        processes = "Top 10 Processes by CPU:\n"
        for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                          key=lambda x: x.info['cpu_percent'], reverse=True)[:10]:
            try:
                processes += f"- {proc.info['name']}: {proc.info['cpu_percent']}%\n"
            except:
                pass
        self.info_label.text = processes
        self.output_text = processes
    
    def get_services(self, instance):
        services = "Running Services:\n"
        for service in psutil.win_service_iter():
            try:
                if service.status() == 'running':
                    services += f"- {service.name()}: {service.display_name()}\n"
            except:
                pass
        self.info_label.text = services[:1000] + "..."
        self.output_text = services
    
    def get_network(self, instance):
        network = "Network Adapters:\n"
        for interface in psutil.net_if_addrs():
            network += f"- {interface}:\n"
            for addr in psutil.net_if_addrs()[interface]:
                network += f"  {addr.family.name}: {addr.address}\n"
        self.info_label.text = network
        self.output_text = network
    
    def get_disk_space(self, instance):
        disk = "Disk Information:\n"
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk += f"""
Drive {partition.device}:
- Path: {partition.mountpoint}
- Total: {usage.total // (1024**3)} GB
- Free: {usage.free // (1024**3)} GB
- Used: {usage.used // (1024**3)} GB
                """
            except:
                pass
        self.info_label.text = disk
        self.output_text = disk
    
    def get_users(self, instance):
        users = "Local Users:\n"
        try:
            result = subprocess.run(['wmic', 'useraccount', 'get', 'name,disabled'], 
                                  capture_output=True, text=True)
            users += result.stdout
        except:
            users += "Could not get user information"
        self.info_label.text = users
        self.output_text = users
    
    def get_cpu_usage(self, instance):
        cpu = f"CPU Usage: {psutil.cpu_percent(interval=1)}%"
        self.info_label.text = cpu
        self.output_text = cpu
    
    def get_memory_usage(self, instance):
        memory = psutil.virtual_memory()
        mem_info = f"""
Memory Usage:
- Total: {memory.total // (1024**3)} GB
- Available: {memory.available // (1024**3)} GB
- Used: {memory.used // (1024**3)} GB
- Percentage: {memory.percent}%
        """
        self.info_label.text = mem_info
        self.output_text = mem_info
    
    def get_uptime(self, instance):
        try:
            uptime = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - uptime
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            uptime_info = f"System Uptime: {hours} hours, {minutes} minutes"
        except:
            uptime_info = "Could not get uptime"
        self.info_label.text = uptime_info
        self.output_text = uptime_info
    
    def get_installed_apps(self, instance):
        apps = "Installed Applications:\n"
        try:
            result = subprocess.run(['wmic', 'product', 'get', 'name,version'], 
                                  capture_output=True, text=True)
            apps += result.stdout[:1000] + "..."
        except:
            apps += "Could not get installed applications"
        self.info_label.text = apps
        self.output_text = apps
    
    def security_check(self, instance):
        security = "Security Check:\n"
        try:
            # Check Windows Defender
            result = subprocess.run(['wmic', 'antivirusproduct', 'get', 'displayname'], 
                                  capture_output=True, text=True)
            security += f"Antivirus: {result.stdout}\n"
            
            # Check Firewall
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                  capture_output=True, text=True)
            security += f"Firewall: {result.stdout[:500]}...\n"
        except:
            security += "Could not perform security check"
        self.info_label.text = security
        self.output_text = security
    
    def send_to_telegram(self, instance):
        if self.output_text:
            try:
                url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                data = {
                    'chat_id': self.chat_id,
                    'text': self.output_text[:4000]  # Telegram limit
                }
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    self.info_label.text = "Message sent to Telegram successfully!"
                else:
                    self.info_label.text = f"Failed to send message: {response.status_code}"
            except Exception as e:
                self.info_label.text = f"Error sending to Telegram: {str(e)}"
        else:
            self.info_label.text = "No data to send. Please run a command first."

if __name__ == '__main__':
    HashashinKivyApp().run()