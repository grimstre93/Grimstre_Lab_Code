# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 15:37:12 2025

@author: samng
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import threading
import time
import json
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import webbrowser

# Handle serial import with error handling
try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("Warning: pyserial not available. Serial functionality disabled.")

class SensorDataCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sensor Data Collection System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize variables
        self.sensors = {}
        self.is_collecting = False
        self.collection_thread = None
        self.serial_connection = None
        self.data = {}
        self.timestamps = []
        
        # Create menu
        self.create_menu()
        
        # Setup UI
        self.setup_ui()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Sensor", command=self.add_sensor_dialog)
        edit_menu.add_command(label="Edit Sensor", command=self.edit_sensor)
        edit_menu.add_command(label="Delete Sensor", command=self.remove_sensor)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All Data", command=self.clear_all_data)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh Data", command=self.refresh_data_view)
        view_menu.add_command(label="Refresh Charts", command=self.update_chart)
        view_menu.add_command(label="Refresh Serial Ports", command=self.refresh_serial_ports)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Label(main_frame, text="ADVANCED SENSOR DATA COLLECTION SYSTEM", 
                          font=("Arial", 16, "bold"), foreground="#3498db")
        header.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration tab
        self.config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.config_frame, text="Sensor Configuration")
        
        # Data View tab
        self.data_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.data_frame, text="Data View")
        
        # Charts tab
        self.charts_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.charts_frame, text="Charts")
        
        # Setup configuration tab
        self.setup_config_tab()
        
        # Setup data view tab
        self.setup_data_tab()
        
        # Setup charts tab
        self.setup_charts_tab()
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(20, 10))
        
        self.start_btn = ttk.Button(button_frame, text="Start Collection", 
                                   command=self.start_collection)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Collection", 
                                  command=self.stop_collection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Export Data", 
                  command=self.export_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_data_view).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Data", 
                  command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="System Ready - Configure sensors to begin")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Add default sensors after UI is fully set up
        self.add_default_sensors()
        
    def setup_config_tab(self):
        # Configuration options frame
        config_options = ttk.LabelFrame(self.config_frame, text="Configuration Options", padding="10")
        config_options.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_options.columnconfigure(1, weight=1)
        
        # Data source selection
        ttk.Label(config_options, text="Data Source:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.data_source = tk.StringVar(value="simulated")
        source_frame = ttk.Frame(config_options)
        source_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Radiobutton(source_frame, text="Simulated Sensors", variable=self.data_source, 
                       value="simulated").pack(side=tk.LEFT)
        
        # Only show serial option if available
        if SERIAL_AVAILABLE:
            ttk.Radiobutton(source_frame, text="Serial Port", variable=self.data_source, 
                           value="serial").pack(side=tk.LEFT, padx=(20, 0))
        else:
            # Disable serial option
            serial_btn = ttk.Radiobutton(source_frame, text="Serial Port (Not Available)", 
                                       variable=self.data_source, value="serial", state=tk.DISABLED)
            serial_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # Serial port configuration (initially hidden)
        self.serial_frame = ttk.Frame(config_options)
        if SERIAL_AVAILABLE:
            ttk.Label(self.serial_frame, text="Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.port_var = tk.StringVar()
            self.port_combo = ttk.Combobox(self.serial_frame, textvariable=self.port_var, width=15)
            self.port_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 15))
            
            ttk.Label(self.serial_frame, text="Baud Rate:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
            self.baud_var = tk.StringVar(value="9600")
            baud_combo = ttk.Combobox(self.serial_frame, textvariable=self.baud_var, width=10, 
                                     values=["9600", "19200", "38400", "57600", "115200"])
            baud_combo.grid(row=0, column=3, sticky=tk.W)
            
            ttk.Button(self.serial_frame, text="Refresh Ports", 
                      command=self.refresh_serial_ports).grid(row=0, column=4, padx=(15, 0))
        
        # Sampling rate
        ttk.Label(config_options, text="Sampling Rate (ms):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.sample_rate_var = tk.StringVar(value="1000")
        ttk.Entry(config_options, textvariable=self.sample_rate_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Data source change binding
        self.data_source.trace('w', self.toggle_serial_config)
        
        # Sensor configuration frame
        sensor_config = ttk.LabelFrame(self.config_frame, text="Sensor Configuration", padding="10")
        sensor_config.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        self.config_frame.columnconfigure(0, weight=1)
        self.config_frame.rowconfigure(1, weight=1)
        
        # Create sensor list with scrollbar
        tree_frame = ttk.Frame(sensor_config)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.sensor_tree = ttk.Treeview(tree_frame, columns=('name', 'type', 'min', 'max', 'unit'), show='headings', height=8)
        self.sensor_tree.heading('name', text='Sensor Name')
        self.sensor_tree.heading('type', text='Type')
        self.sensor_tree.heading('min', text='Min Value')
        self.sensor_tree.heading('max', text='Max Value')
        self.sensor_tree.heading('unit', text='Unit')
        
        self.sensor_tree.column('name', width=150)
        self.sensor_tree.column('type', width=100)
        self.sensor_tree.column('min', width=80)
        self.sensor_tree.column('max', width=80)
        self.sensor_tree.column('unit', width=80)
        
        # Add scrollbar
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.sensor_tree.yview)
        self.sensor_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.sensor_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        sensor_config.columnconfigure(0, weight=1)
        sensor_config.rowconfigure(0, weight=1)
        
        # Sensor controls
        controls_frame = ttk.Frame(sensor_config)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(controls_frame, text="Add Sensor", command=self.add_sensor_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="Edit Sensor", command=self.edit_sensor).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="Remove Sensor", command=self.remove_sensor).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="Refresh List", command=self.refresh_sensor_list).pack(side=tk.LEFT, padx=(10, 0))
        
    def setup_data_tab(self):
        # Create data table with scrollbars
        data_container = ttk.Frame(self.data_frame)
        data_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(data_container, orient=tk.HORIZONTAL)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(data_container, orient=tk.VERTICAL)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.data_tree = ttk.Treeview(data_container, columns=('timestamp'), show='headings', height=15,
                                     xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.data_tree.heading('timestamp', text='Timestamp')
        
        h_scrollbar.config(command=self.data_tree.xview)
        v_scrollbar.config(command=self.data_tree.yview)
        
        self.data_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.rowconfigure(0, weight=1)
        data_container.columnconfigure(0, weight=1)
        data_container.rowconfigure(0, weight=1)
        
        # Data controls
        controls_frame = ttk.Frame(self.data_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(controls_frame, text="Delete Selected", command=self.delete_selected_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="Clear All Data", command=self.clear_data).pack(side=tk.LEFT)
        
    def setup_charts_tab(self):
        # Create matplotlib figure with navigation toolbar
        chart_container = ttk.Frame(self.charts_frame)
        chart_container.pack(fill=tk.BOTH, expand=True)
        
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Sensor Data Over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.grid(True)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, chart_container)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar for chart navigation
        toolbar_frame = ttk.Frame(chart_container)
        toolbar_frame.pack(fill=tk.X)
        
        ttk.Button(toolbar_frame, text="Refresh Chart", command=self.update_chart).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="Save Chart", command=self.save_chart).pack(side=tk.LEFT, padx=5)
        
    def toggle_serial_config(self, *args):
        if self.data_source.get() == "serial":
            if not SERIAL_AVAILABLE:
                messagebox.showerror("Error", "Serial functionality not available. Install pyserial package.")
                self.data_source.set("simulated")
                return
            self.serial_frame.grid(row=0, column=2, sticky=tk.W)
            self.refresh_serial_ports()
        else:
            self.serial_frame.grid_forget()
            
    def refresh_serial_ports(self):
        if not SERIAL_AVAILABLE:
            return
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports:
            self.port_var.set(ports[0])
        self.status_var.set(f"Refreshed serial ports. Found {len(ports)} ports.")
            
    def add_default_sensors(self):
        # Add some default sensors
        default_sensors = [
            {'name': 'Temperature', 'type': 'Analog', 'min': 20, 'max': 30, 'unit': '°C'},
            {'name': 'Humidity', 'type': 'Analog', 'min': 40, 'max': 80, 'unit': '%'},
            {'name': 'Pressure', 'type': 'Analog', 'min': 980, 'max': 1020, 'unit': 'hPa'}
        ]
        
        for sensor in default_sensors:
            self.add_sensor_to_tree(sensor)
            self.sensors[sensor['name']] = sensor
            self.data[sensor['name']] = []
            
    def add_sensor_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Sensor")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Sensor name
        ttk.Label(dialog, text="Sensor Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Sensor type
        ttk.Label(dialog, text="Sensor Type:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        type_var = tk.StringVar(value="Analog")
        ttk.Combobox(dialog, textvariable=type_var, values=["Analog", "Digital"]).grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Min value
        ttk.Label(dialog, text="Min Value:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        min_var = tk.StringVar(value="0")
        ttk.Entry(dialog, textvariable=min_var).grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Max value
        ttk.Label(dialog, text="Max Value:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        max_var = tk.StringVar(value="100")
        ttk.Entry(dialog, textvariable=max_var).grid(row=3, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Unit
        ttk.Label(dialog, text="Unit:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        unit_var = tk.StringVar(value="units")
        ttk.Entry(dialog, textvariable=unit_var).grid(row=4, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def add_sensor():
            if not name_var.get():
                messagebox.showerror("Error", "Sensor name cannot be empty.")
                return
                
            if name_var.get() in self.sensors:
                messagebox.showerror("Error", "Sensor with this name already exists.")
                return
                
            try:
                sensor = {
                    'name': name_var.get(),
                    'type': type_var.get(),
                    'min': float(min_var.get()),
                    'max': float(max_var.get()),
                    'unit': unit_var.get()
                }
                self.add_sensor_to_tree(sensor)
                self.sensors[sensor['name']] = sensor
                self.data[sensor['name']] = []
                dialog.destroy()
                self.status_var.set(f"Added sensor: {sensor['name']}")
            except ValueError:
                messagebox.showerror("Error", "Min and Max values must be numbers.")
            
        ttk.Button(button_frame, text="Add", command=add_sensor).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        dialog.columnconfigure(1, weight=1)
        
    def add_sensor_to_tree(self, sensor):
        self.sensor_tree.insert('', 'end', values=(
            sensor['name'], 
            sensor['type'], 
            sensor['min'], 
            sensor['max'], 
            sensor['unit']
        ))
        
        # Add column to data tree
        if sensor['name'] not in self.data_tree['columns']:
            self.data_tree['columns'] = self.data_tree['columns'] + (sensor['name'],)
            self.data_tree.heading(sensor['name'], text=sensor['name'])
            self.data_tree.column(sensor['name'], width=100)
            
    def edit_sensor(self):
        selected = self.sensor_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sensor to edit.")
            return
            
        item = selected[0]
        values = self.sensor_tree.item(item, 'values')
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Sensor")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Sensor name
        ttk.Label(dialog, text="Sensor Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_var = tk.StringVar(value=values[0])
        ttk.Entry(dialog, textvariable=name_var, state='readonly').grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Sensor type
        ttk.Label(dialog, text="Sensor Type:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        type_var = tk.StringVar(value=values[1])
        ttk.Combobox(dialog, textvariable=type_var, values=["Analog", "Digital"]).grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Min value
        ttk.Label(dialog, text="Min Value:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        min_var = tk.StringVar(value=values[2])
        ttk.Entry(dialog, textvariable=min_var).grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Max value
        ttk.Label(dialog, text="Max Value:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        max_var = tk.StringVar(value=values[3])
        ttk.Entry(dialog, textvariable=max_var).grid(row=3, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Unit
        ttk.Label(dialog, text="Unit:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        unit_var = tk.StringVar(value=values[4])
        ttk.Entry(dialog, textvariable=unit_var).grid(row=4, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def update_sensor():
            try:
                sensor = {
                    'name': name_var.get(),
                    'type': type_var.get(),
                    'min': float(min_var.get()),
                    'max': float(max_var.get()),
                    'unit': unit_var.get()
                }
                self.sensor_tree.item(item, values=(
                    sensor['name'], 
                    sensor['type'], 
                    sensor['min'], 
                    sensor['max'], 
                    sensor['unit']
                ))
                self.sensors[sensor['name']] = sensor
                dialog.destroy()
                self.status_var.set(f"Updated sensor: {sensor['name']}")
            except ValueError:
                messagebox.showerror("Error", "Min and Max values must be numbers.")
            
        ttk.Button(button_frame, text="Update", command=update_sensor).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
        
        dialog.columnconfigure(1, weight=1)
        
    def remove_sensor(self):
        selected = self.sensor_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sensor to remove.")
            return
            
        item = selected[0]
        values = self.sensor_tree.item(item, 'values')
        sensor_name = values[0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove sensor '{sensor_name}'?"):
            self.sensor_tree.delete(item)
            del self.sensors[sensor_name]
            del self.data[sensor_name]
            
            # Remove column from data tree
            columns = list(self.data_tree['columns'])
            if sensor_name in columns:
                columns.remove(sensor_name)
                self.data_tree['columns'] = tuple(columns)
                
            self.status_var.set(f"Removed sensor: {sensor_name}")
            
    def refresh_sensor_list(self):
        # This method refreshes the sensor list view
        self.sensor_tree.delete(*self.sensor_tree.get_children())
        for sensor_name, sensor in self.sensors.items():
            self.add_sensor_to_tree(sensor)
        self.status_var.set("Sensor list refreshed.")
            
    def start_collection(self):
        if not self.sensors:
            messagebox.showwarning("Warning", "Please add at least one sensor before starting collection.")
            return
            
        try:
            sample_rate = int(self.sample_rate_var.get())
            if sample_rate <= 0:
                raise ValueError("Sample rate must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer for sample rate.")
            return
            
        if self.data_source.get() == "serial" and SERIAL_AVAILABLE:
            try:
                self.serial_connection = serial.Serial(
                    port=self.port_var.get(),
                    baudrate=int(self.baud_var.get()),
                    timeout=1
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open serial port: {e}")
                return
                
        self.is_collecting = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Collecting data...")
        
        # Start collection thread
        self.collection_thread = threading.Thread(target=self.collect_data)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        
    def stop_collection(self):
        self.is_collecting = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Collection stopped")
        
        if self.serial_connection and SERIAL_AVAILABLE:
            self.serial_connection.close()
            self.serial_connection = None
            
    def collect_data(self):
        sample_rate = int(self.sample_rate_var.get()) / 1000.0  # Convert to seconds
        
        while self.is_collecting:
            timestamp = datetime.now()
            self.timestamps.append(timestamp)
            
            row_data = [timestamp.strftime("%Y-%m-%d %H:%M:%S")]
            
            # Collect data from each sensor
            for sensor_name, sensor in self.sensors.items():
                if self.data_source.get() == "simulated":
                    # Generate simulated data
                    value = random.uniform(sensor['min'], sensor['max'])
                else:
                    # Read from serial (placeholder implementation)
                    value = random.uniform(sensor['min'], sensor['max'])
                    
                self.data[sensor_name].append(value)
                row_data.append(f"{value:.2f}")
                
            # Update data table
            self.data_tree.insert('', 0, values=row_data)
            
            # Keep only the last 1000 data points
            if len(self.timestamps) > 1000:
                self.timestamps = self.timestamps[-1000:]
                for sensor_name in self.data:
                    self.data[sensor_name] = self.data[sensor_name][-1000:]
                    
            # Update chart
            self.update_chart()
            
            time.sleep(sample_rate)
            
    def update_chart(self):
        self.ax.clear()
        
        for sensor_name in self.sensors:
            if len(self.timestamps) > 0 and len(self.data[sensor_name]) > 0:
                # Use a simple index for x-axis if we have many data points
                if len(self.timestamps) > 50:
                    x = range(len(self.timestamps))
                    self.ax.plot(x, self.data[sensor_name], label=sensor_name)
                    # Set x-axis labels to show time for a few points
                    if len(self.timestamps) > 1:
                        step = max(1, len(self.timestamps) // 5)
                        indices = list(range(0, len(self.timestamps), step))
                        labels = [self.timestamps[i].strftime("%H:%M:%S") for i in indices]
                        self.ax.set_xticks(indices)
                        self.ax.set_xticklabels(labels, rotation=45)
                else:
                    # For fewer points, use actual timestamps
                    self.ax.plot(self.timestamps, self.data[sensor_name], label=sensor_name)
                    plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
        
        self.ax.set_title('Sensor Data Over Time')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.grid(True)
        self.ax.legend()
        
        self.fig.tight_layout()
        self.canvas.draw()
        
    def refresh_data_view(self):
        # Refresh the data view by updating the tree
        self.data_tree.delete(*self.data_tree.get_children())
        
        if self.timestamps:
            for i in range(len(self.timestamps)):
                row_data = [self.timestamps[i].strftime("%Y-%m-%d %H:%M:%S")]
                for sensor_name in self.sensors:
                    row_data.append(f"{self.data[sensor_name][i]:.2f}")
                self.data_tree.insert('', 'end', values=row_data)
                
        self.status_var.set("Data view refreshed.")
        
    def delete_selected_data(self):
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select data rows to delete.")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(selected)} data rows?"):
            for item in selected:
                index = self.data_tree.index(item)
                self.data_tree.delete(item)
                
                # Remove from data arrays
                if index < len(self.timestamps):
                    self.timestamps.pop(index)
                    for sensor_name in self.data:
                        if index < len(self.data[sensor_name]):
                            self.data[sensor_name].pop(index)
            
            self.status_var.set(f"Deleted {len(selected)} data rows.")
            self.update_chart()
            
    def clear_data(self):
        if not self.timestamps:
            messagebox.showinfo("Info", "No data to clear.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.data_tree.delete(*self.data_tree.get_children())
            self.timestamps = []
            for sensor_name in self.data:
                self.data[sensor_name] = []
                
            self.status_var.set("All data cleared.")
            self.update_chart()
            
    def clear_all_data(self):
        self.clear_data()
            
    def save_chart(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            self.status_var.set(f"Chart saved to {filename}")
            
    def export_data(self):
        if not self.timestamps:
            messagebox.showwarning("Warning", "No data to export.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
            
        if filename.endswith('.csv'):
            self.export_csv(filename)
        elif filename.endswith('.json'):
            self.export_json(filename)
        else:
            # Default to CSV
            self.export_csv(filename + '.csv')
            
        messagebox.showinfo("Success", f"Data exported to {filename}")
        
    def export_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write header
            header = ['Timestamp'] + list(self.sensors.keys())
            writer.writerow(header)
            
            # Write data
            for i in range(len(self.timestamps)):
                row = [self.timestamps[i].strftime("%Y-%m-%d %H:%M:%S")]
                for sensor_name in self.sensors:
                    row.append(f"{self.data[sensor_name][i]:.2f}")
                writer.writerow(row)
                
    def export_json(self, filename):
        data_to_export = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'sensor_count': len(self.sensors),
                'data_points': len(self.timestamps)
            },
            'sensors': self.sensors,
            'data': {}
        }
        
        # Add timestamps
        data_to_export['data']['timestamps'] = [ts.isoformat() for ts in self.timestamps]
        
        # Add sensor data
        for sensor_name in self.sensors:
            data_to_export['data'][sensor_name] = self.data[sensor_name]
            
        with open(filename, 'w') as file:
            json.dump(data_to_export, file, indent=2)
            
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Sensor Data Collection System")
        about_window.geometry("500x300")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center the about window
        about_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - about_window.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - about_window.winfo_height()) // 2
        about_window.geometry(f"+{x}+{y}")
        
        # Application info
        ttk.Label(about_window, text="Sensor Data Collection System", 
                 font=("Arial", 16, "bold")).pack(pady=(20, 10))
        
        ttk.Label(about_window, text="Version: 2.0", font=("Arial", 10)).pack(pady=(0, 5))
        
        ttk.Label(about_window, text="A comprehensive system for collecting, monitoring, and analyzing", 
                 font=("Arial", 9)).pack(pady=(0, 5))
        ttk.Label(about_window, text="sensor data from various sources including simulated and serial devices.", 
                 font=("Arial", 9)).pack(pady=(0, 20))
        
        # Contact information
        contact_frame = ttk.LabelFrame(about_window, text="Contact Information", padding="10")
        contact_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(contact_frame, text="Email: samngacha@gmail.com", font=("Arial", 9)).pack(anchor=tk.W, pady=2)
        ttk.Label(contact_frame, text="Phone: +254742859291", font=("Arial", 9)).pack(anchor=tk.W, pady=2)
        
        # Features list
        features_frame = ttk.LabelFrame(about_window, text="Key Features", padding="10")
        features_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        features = [
            "• Support for multiple sensor types and configurations",
            "• Real-time data collection from simulated or serial sources",
            "• Interactive charts with zoom and pan capabilities",
            "• Data export to CSV and JSON formats",
            "• Advanced filtering and data management",
            "• Customizable sampling rates and thresholds"
        ]
        
        for feature in features:
            ttk.Label(features_frame, text=feature, font=("Arial", 8)).pack(anchor=tk.W, pady=1)
        
        # Close button
        ttk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=10)

def main():
    root = tk.Tk()
    app = SensorDataCollector(root)
    root.mainloop()

if __name__ == "__main__":
    main()