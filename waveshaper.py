import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
DURATION = 1.0  # seconds

def generate_waveform(wave_type, frequency):
    t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
    if wave_type == "Sine":
        return np.sin(2 * np.pi * frequency * t)
    elif wave_type == "Square":
        return np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == "Sawtooth":
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif wave_type == "Triangle":
        return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    elif wave_type == "Custom Blend":
        sine = np.sin(2 * np.pi * frequency * t)
        square = np.sign(sine)
        triangle = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        return 0.5 * sine + 0.3 * square + 0.2 * triangle
    return np.zeros_like(t)

class WaveformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Waveform Generator & Visualizer")

        self.freq_var = tk.DoubleVar(value=440)
        self.wave_type_var = tk.StringVar(value="Sine")

        self.setup_ui()
        self.plot_waveform()

    def setup_ui(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Wave Type:").pack(side=tk.LEFT)
        wave_menu = ttk.OptionMenu(control_frame, self.wave_type_var, "Sine", "Sine", "Square", "Sawtooth", "Triangle", "Custom Blend")
        wave_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Frequency (Hz):").pack(side=tk.LEFT)
        freq_slider = ttk.Scale(control_frame, from_=20, to=2000, variable=self.freq_var, orient=tk.HORIZONTAL)
        freq_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        generate_btn = ttk.Button(control_frame, text="Generate", command=self.plot_waveform)
        generate_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(control_frame, text="Export WAV", command=self.export_waveform)
        export_btn.pack(side=tk.LEFT, padx=5)

        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_waveform(self):
        self.ax.clear()
        freq = self.freq_var.get()
        wave = generate_waveform(self.wave_type_var.get(), freq)
        t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), endpoint=False)
        self.ax.plot(t[:1000], wave[:1000])  # Just plot first 1000 samples
        self.ax.set_title(f"{self.wave_type_var.get()} Wave @ {freq:.1f} Hz")
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()

    def export_waveform(self):
        freq = self.freq_var.get()
        wave = generate_waveform(self.wave_type_var.get(), freq)
        wave_int16 = np.int16(wave * 32767)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            title="Save waveform as WAV"
        )
        if file_path:
            write(file_path, SAMPLE_RATE, wave_int16)
            print(f"Waveform saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaveformApp(root)
    root.mainloop()
