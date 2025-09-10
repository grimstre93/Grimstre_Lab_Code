import string
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

def list_characters():
    # List all printable ASCII characters using chr()
    return ''.join(chr(i) for i in range(32, 127))

def encrypt_message(message, shift=3):
    # Encrypt message using a simple Caesar cipher
    encrypted = []
    for char in message:
        if 32 <= ord(char) <= 126:
            shifted = (ord(char) - 32 + shift) % 95 + 32
            encrypted.append(chr(shifted))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def decrypt_message(encrypted, shift=3):
    # Decrypt message using a simple Caesar cipher
    decrypted = []
    for char in encrypted:
        if 32 <= ord(char) <= 126:
            shifted = (ord(char) - 32 - shift) % 95 + 32
            decrypted.append(chr(shifted))
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def message_to_binary(message):
    # Convert each character to its binary representation using ord()
    return ' '.join(format(ord(char), '08b') for char in message)

def process_message():
    message = input_text.get("1.0", tk.END).strip()
    words = message.split()
    if len(words) > 10000:
        messagebox.showerror("Error", "Message exceeds 10,000 words.")
        return

    encrypted = encrypt_message(message)
    binary_code = message_to_binary(encrypted)
    byte_message = encrypted.encode('utf-8')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Show timestamp
    timestamp_text.config(state='normal')
    timestamp_text.delete("1.0", tk.END)
    timestamp_text.insert(tk.END, f"Message processed at: {timestamp}")
    timestamp_text.config(state='disabled')

    encrypted_text.config(state='normal')
    encrypted_text.delete("1.0", tk.END)
    encrypted_text.insert(tk.END, encrypted)
    encrypted_text.config(state='disabled')

    binary_text.config(state='normal')
    binary_text.delete("1.0", tk.END)
    binary_text.insert(tk.END, binary_code)
    binary_text.config(state='disabled')

    bytes_text.config(state='normal')
    bytes_text.delete("1.0", tk.END)
    bytes_text.insert(tk.END, str(byte_message))
    bytes_text.config(state='disabled')

    interpreted_text.config(state='normal')
    interpreted_text.delete("1.0", tk.END)
    interpreted_text.insert(tk.END, "")  # Clear previous interpretation
    interpreted_text.config(state='disabled')

    # Store information for storage and interpretation
    global last_message_data
    last_message_data = {
        "timestamp": timestamp,
        "message": message,
        "encrypted": encrypted,
        "binary": binary_code,
        "bytes": byte_message
    }

def interpret_encrypted():
    if not last_message_data or not last_message_data.get("encrypted"):
        messagebox.showinfo("Info", "No encrypted message to interpret. Please encrypt a message first.")
        return
    decrypted = decrypt_message(last_message_data["encrypted"])
    interpreted_text.config(state='normal')
    interpreted_text.delete("1.0", tk.END)
    interpreted_text.insert(tk.END, decrypted)
    interpreted_text.config(state='disabled')

def refresh_fields():
    input_text.delete("1.0", tk.END)
    timestamp_text.config(state='normal')
    timestamp_text.delete("1.0", tk.END)
    timestamp_text.config(state='disabled')
    encrypted_text.config(state='normal')
    encrypted_text.delete("1.0", tk.END)
    encrypted_text.config(state='disabled')
    binary_text.config(state='normal')
    binary_text.delete("1.0", tk.END)
    binary_text.config(state='disabled')
    bytes_text.config(state='normal')
    bytes_text.delete("1.0", tk.END)
    bytes_text.config(state='disabled')
    interpreted_text.config(state='normal')
    interpreted_text.delete("1.0", tk.END)
    interpreted_text.config(state='disabled')

def store_message():
    if not last_message_data or not last_message_data.get("message"):
        messagebox.showinfo("Info", "No message to store. Please encrypt a message first.")
        return
    try:
        with open("messages_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Timestamp: {last_message_data['timestamp']}\n")
            f.write(f"Original Message: {last_message_data['message']}\n")
            f.write(f"Encrypted Message: {last_message_data['encrypted']}\n")
            f.write(f"Binary: {last_message_data['binary']}\n")
            f.write(f"Bytes: {last_message_data['bytes']}\n")
            f.write("-" * 60 + "\n")
        messagebox.showinfo("Success", "Message stored successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to store message: {e}")

# Tkinter GUI setup
root = tk.Tk()
root.title("Binary Code Message Software")

# Printable ASCII characters
tk.Label(root, text="Printable ASCII characters:").pack(anchor='w')
ascii_text = scrolledtext.ScrolledText(root, height=2, width=95, state='normal')
ascii_text.pack(fill='x')
ascii_text.insert(tk.END, list_characters())
ascii_text.config(state='disabled')

# Input message
tk.Label(root, text="Enter your message (up to 10,000 words):").pack(anchor='w')
input_text = scrolledtext.ScrolledText(root, height=4, width=95)
input_text.pack(fill='x')

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Encrypt button
encrypt_btn = tk.Button(button_frame, text="Encrypt Message", command=process_message)
encrypt_btn.pack(side='left', padx=5)

# Refresh button
refresh_btn = tk.Button(button_frame, text="Refresh", command=refresh_fields)
refresh_btn.pack(side='left', padx=5)

# Storage button
storage_btn = tk.Button(button_frame, text="Store Message", command=store_message)
storage_btn.pack(side='left', padx=5)

# Interpret button
interpret_btn = tk.Button(button_frame, text="Interpret Encrypted", command=interpret_encrypted)
interpret_btn.pack(side='left', padx=5)

# Timestamp display
timestamp_text = scrolledtext.ScrolledText(root, height=1, width=95, state='disabled')
timestamp_text.pack(fill='x')

# Encrypted message
tk.Label(root, text="Encrypted message:").pack(anchor='w')
encrypted_text = scrolledtext.ScrolledText(root, height=2, width=95, state='disabled')
encrypted_text.pack(fill='x')

# Encrypted message in binary
tk.Label(root, text="Encrypted message in binary:").pack(anchor='w')
binary_text = scrolledtext.ScrolledText(root, height=4, width=95, state='disabled')
binary_text.pack(fill='x')

# Encrypted message as bytes
tk.Label(root, text="Encrypted message as bytes:").pack(anchor='w')
bytes_text = scrolledtext.ScrolledText(root, height=2, width=95, state='disabled')
bytes_text.pack(fill='x')

# Interpreted (decrypted) message
tk.Label(root, text="Interpreted (decrypted) message:").pack(anchor='w')
interpreted_text = scrolledtext.ScrolledText(root, height=2, width=95, state='disabled')
interpreted_text.pack(fill='x')

# For storing the last processed message
last_message_data = {}

root.mainloop()
