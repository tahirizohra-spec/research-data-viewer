import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

class ResearchDataViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Research Data Visualizer")
        self.geometry("900x600")

        self.df = None
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="x")

        ttk.Button(frame, text="Importer fichier CSV", command=self.load_csv).pack(side="left", padx=10)
        ttk.Button(frame, text="Afficher statistiques", command=self.show_stats).pack(side="left", padx=10)
        ttk.Button(frame, text="Tracer courbe", command=self.plot_graph).pack(side="left", padx=10)
        ttk.Button(frame, text="Exporter JSON", command=self.export_json).pack(side="left", padx=10)

        self.text = tk.Text(self, height=25)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return

        try:
            self.df = pd.read_csv(filepath)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, f"Fichier chargé : {os.path.basename(filepath)}\n")
            self.text.insert(tk.END, str(self.df.head()))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def show_stats(self):
        if self.df is None:
            messagebox.showwarning("Attention", "Veuillez importer un fichier CSV.")
            return
        stats = self.df.describe(include="all")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, str(stats))

    def plot_graph(self):
        if self.df is None:
            messagebox.showwarning("Attention", "Importer un CSV d'abord.")
            return

        numeric_cols = self.df.select_dtypes(include="number").columns
        if len(numeric_cols) < 2:
            messagebox.showerror("Erreur", "Le graphique nécessite au moins 2 colonnes numériques.")
            return

        x = numeric_cols[0]
        y = numeric_cols[1]

        plt.figure(figsize=(6,4))
        plt.plot(self.df[x], self.df[y])
        plt.title(f"{y} en fonction de {x}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def export_json(self):
        if self.df is None:
            messagebox.showwarning("Attention", "Importer un CSV d'abord.")
            return

        data_json = self.df.to_json(orient="records", indent=4)

        filepath = filedialog.asksaveasfilename(defaultextension=".json")
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data_json)
            messagebox.showinfo("Succès", "Fichier JSON exporté.")

if __name__ == "__main__":
    app = ResearchDataViewer()
    app.mainloop()
