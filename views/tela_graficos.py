import tkinter as tk
from tkinter import ttk


class TelaGraficos(tk.Toplevel):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("TaskMaster Pro - Relatórios")
        self.geometry("980x470")
        self.minsize(900, 420)
        self.configure(bg="#0B1120")

        self._montar_interface()
        self.atualizar_graficos()

    def _montar_interface(self):
        self.header = tk.Frame(self, bg="#111827", padx=18, pady=14)
        self.header.pack(fill="x")

        titulo = tk.Label(
            self.header,
            text="Relatórios e gráficos",
            bg="#111827",
            fg="#F8FAFC",
            font=("Segoe UI", 18, "bold"),
        )
        titulo.pack(anchor="w")

        subtitulo = tk.Label(
            self.header,
            text="Cada gráfico em sua própria página.",
            bg="#111827",
            fg="#93C5FD",
            font=("Segoe UI", 10),
        )
        subtitulo.pack(anchor="w", pady=(6, 0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=18)

        self.tab_barras = tk.Frame(self.notebook, bg="#0B1120")
        self.tab_pizza = tk.Frame(self.notebook, bg="#0B1120")

        self.notebook.add(self.tab_barras, text="Gráfico de barras")
        self.notebook.add(self.tab_pizza, text="Gráfico de pizza")

        self.canvas_barras = tk.Canvas(self.tab_barras, width=430, height=250, bg="#111827", highlightthickness=0)
        self.canvas_barras.pack(fill="both", expand=True, padx=14, pady=14)

        self.canvas_pizza = tk.Canvas(self.tab_pizza, width=430, height=250, bg="#111827", highlightthickness=0)
        self.canvas_pizza.pack(fill="both", expand=True, padx=14, pady=14)

    def atualizar_graficos(self):
        tarefas = self.controlador.listar_tarefas()
        self.canvas_barras.delete("all")
        self.canvas_pizza.delete("all")

        if tarefas.empty:
            self.canvas_barras.create_text(215, 125, text="Sem dados", fill="#94A3B8", font=("Segoe UI", 12, "bold"))
            self.canvas_pizza.create_text(215, 125, text="Sem dados", fill="#94A3B8", font=("Segoe UI", 12, "bold"))
            return

        por_categoria = tarefas["categoria"].value_counts().sort_index()
        por_status = tarefas["status"].value_counts().sort_index()

        self._desenhar_barras(por_categoria)
        self._desenhar_pizza(por_status)

    def _desenhar_barras(self, dados):
        altura = 170
        inicio_x = 40
        inicio_y = 180
        max_valor = max(dados.max(), 1)

        self.canvas_barras.create_text(215, 18, text="Tarefas por categoria", fill="#E2E8F0", font=("Segoe UI", 11, "bold"))

        cores = ["#60A5FA", "#34D399", "#FBBF24", "#F87171", "#A78BFA"]
        for idx, (categoria, valor) in enumerate(dados.items()):
            x = inicio_x + idx * 70
            barra_h = (valor / max_valor) * altura
            y = inicio_y - barra_h
            cor = cores[idx % len(cores)]
            self.canvas_barras.create_rectangle(x, y, x + 40, inicio_y, fill=cor, outline="")
            self.canvas_barras.create_text(x + 20, inicio_y + 18, text=categoria[:3], fill="#E2E8F0", font=("Segoe UI", 9, "bold"))
            self.canvas_barras.create_text(x + 20, y - 10, text=str(valor), fill="#F8FAFC", font=("Segoe UI", 8, "bold"))

    def _desenhar_pizza(self, dados):
        centro_x = 180
        centro_y = 110
        raio = 74
        total = dados.sum()

        self.canvas_pizza.create_text(180, 18, text="Status das tarefas", fill="#E2E8F0", font=("Segoe UI", 11, "bold"))

        cores = ["#38BDF8", "#34D399", "#FBBF24", "#F87171"]
        angulo_inicial = 0

        for idx, (status, valor) in enumerate(dados.items()):
            angulo = (valor / total) * 360 if total else 0
            self.canvas_pizza.create_arc(
                centro_x - raio,
                centro_y - raio,
                centro_x + raio,
                centro_y + raio,
                start=angulo_inicial,
                extent=angulo,
                fill=cores[idx % len(cores)],
                outline="#0B1120",
            )
            angulo_inicial += angulo

        legenda_y = 190
        for idx, (status, valor) in enumerate(dados.items()):
            self.canvas_pizza.create_rectangle(290, legenda_y - 8, 310, legenda_y + 8, fill=cores[idx % len(cores)], outline="")
            self.canvas_pizza.create_text(320, legenda_y, text=f"{status}: {valor}", anchor="w", fill="#E2E8F0", font=("Segoe UI", 9))
            legenda_y += 20
