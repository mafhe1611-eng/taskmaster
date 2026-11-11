import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from views.tela_graficos import TelaGraficos

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.controlador_tarefas import ControladorTarefas


class TelaTarefas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TaskMaster Pro")
        self.geometry("980x560")
        self.minsize(880, 480)

        self.configure(bg="#0B1120")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#0B1120")
        self.style.configure("TLabel", background="#0B1120", foreground="#E5E7EB", font=("Segoe UI", 10, "bold"))
        self.style.configure("TEntry", fieldbackground="#111827", foreground="#F9FAFB", borderwidth=0)
        self.style.map("TEntry", fieldbackground=[("focus", "#111827")])
        self.style.configure("TCombobox", fieldbackground="#111827", foreground="#F9FAFB")
        self.style.map("TCombobox", fieldbackground=[("focus", "#111827")])
        self.style.configure("Treeview", background="#111827", foreground="#F9FAFB", rowheight=30, fieldbackground="#111827", borderwidth=1, relief="solid")
        self.style.map("Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", background="#1E293B", foreground="#E2E8F0", font=("Segoe UI", 10, "bold"), relief="flat")
        self.style.configure("TButton", background="#2563EB", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), padding=(16, 8))
        self.style.map("TButton", background=[("active", "#1D4ED8")], foreground=[("active", "#FFFFFF")])

        self.controlador = ControladorTarefas()
        self._montar_interface()
        self.carregar_tarefas()

    def _montar_interface(self):
        topo = ttk.Frame(self, padding=(18, 18, 18, 10))
        topo.pack(fill="x")

        banner = tk.Frame(topo, bg="#111827", bd=0, highlightthickness=1, highlightbackground="#1E3A8A")
        banner.pack(fill="x", pady=(0, 10))

        titulo = tk.Label(banner, text="TaskMaster Pro", bg="#111827", fg="#F8FAFC", font=("Segoe UI", 22, "bold"), padx=18, pady=12)
        titulo.pack(anchor="w")

        subtitulo = tk.Label(banner, text="Gerencie suas tarefas com foco, ordem e produtividade.", bg="#111827", fg="#93C5FD", font=("Segoe UI", 10), padx=18)
        subtitulo.pack(anchor="w", pady=(0, 12))

        self.kpis_frame = tk.Frame(self, bg="#0B1120")
        self.kpis_frame.pack(fill="x", padx=18, pady=(0, 12))

        self.kpi_total = self._criar_kpi_card(self.kpis_frame, "Total de tarefas", "0", "#2563EB")
        self.kpi_concluidas = self._criar_kpi_card(self.kpis_frame, "Concluídas", "0", "#10B981")
        self.kpi_pendentes = self._criar_kpi_card(self.kpis_frame, "Pendentes", "0", "#F59E0B")

        frame_form = ttk.Frame(self, padding=(18, 12, 18, 10))
        frame_form.pack(fill="x")

        ttk.Label(frame_form, text="Título:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.entrada_titulo = ttk.Entry(frame_form, width=35)
        self.entrada_titulo.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(frame_form, text="Categoria:").grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.entrada_categoria = ttk.Entry(frame_form, width=24)
        self.entrada_categoria.grid(row=0, column=3, padx=5, pady=8)

        ttk.Label(frame_form, text="Prioridade:").grid(row=0, column=4, padx=5, pady=8, sticky="w")
        self.entrada_prioridade = ttk.Combobox(frame_form, values=["Alta", "Média", "Baixa"], width=12, state="readonly")
        self.entrada_prioridade.grid(row=0, column=5, padx=5, pady=8)
        self.entrada_prioridade.set("Alta")

        ttk.Button(frame_form, text="Adicionar tarefa", command=self.adicionar_tarefa).grid(
            row=0, column=6, padx=8, pady=8, ipadx=10, ipady=4
        )

        frame_lista = tk.Frame(self, bg="#0B1120", bd=1, relief="solid", highlightbackground="#1E3A8A", highlightthickness=1, padx=8, pady=8)
        frame_lista.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        colunas = ("ID", "Título", "Categoria", "Prioridade", "Status")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings", selectmode="browse", height=18)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=70, minwidth=70, anchor="center")
        self.tree.column("Título", width=260, minwidth=220, anchor="w")
        self.tree.column("Categoria", width=170, minwidth=140, anchor="center")
        self.tree.column("Prioridade", width=120, minwidth=110, anchor="center")
        self.tree.column("Status", width=150, minwidth=120, anchor="center")

        self.tree.tag_configure("linha-par", background="#111827")
        self.tree.tag_configure("linha-impar", background="#0F172A")

        self.tree.pack(fill="both", expand=True)

        botoes = ttk.Frame(self, padding=(18, 0, 18, 18))
        botoes.pack(fill="x")

        ttk.Button(botoes, text="Concluir tarefa", command=self.concluir_tarefa).pack(side="left", padx=5)
        ttk.Button(botoes, text="Excluir tarefa", command=self.excluir_tarefa).pack(side="left", padx=5)
        ttk.Button(botoes, text="Atualizar lista", command=self.carregar_tarefas).pack(side="left", padx=5)
        ttk.Button(botoes, text="Abrir gráficos", command=self.abrir_graficos).pack(side="left", padx=5)

    def _criar_kpi_card(self, container, titulo, valor, cor):
        card = tk.Frame(container, bg="#111827", bd=1, relief="solid", highlightbackground=cor, highlightthickness=2)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))

        tk.Label(card, text=titulo, bg="#111827", fg="#CBD5E1", font=("Segoe UI", 9), padx=14).pack(anchor="w", pady=(10, 0))
        valor_label = tk.Label(card, text=valor, bg="#111827", fg=cor, font=("Segoe UI", 21, "bold"), padx=14)
        valor_label.pack(anchor="w", pady=(0, 10))
        return valor_label

    def _atualizar_kpis(self):
        tarefas = self.controlador.listar_tarefas()
        total = len(tarefas)
        status = tarefas["status"].fillna("").astype(str).str.lower()
        concluidas = int((status == "concluída").sum() + (status == "concluida").sum())
        pendentes = int((status == "pendente").sum())

        self.kpi_total.config(text=str(total))
        self.kpi_concluidas.config(text=str(concluidas))
        self.kpi_pendentes.config(text=str(pendentes))

    def abrir_graficos(self):
        TelaGraficos(self.controlador)

    def carregar_tarefas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tarefas = self.controlador.listar_tarefas()
        for index, tarefa in tarefas.iterrows():
            tag = "linha-par" if index % 2 == 0 else "linha-impar"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    tarefa["id"],
                    tarefa["titulo"],
                    tarefa["categoria"],
                    tarefa["prioridade"],
                    tarefa["status"],
                ),
                tags=(tag,),
            )

        self._atualizar_kpis()

    def adicionar_tarefa(self):
        titulo = self.entrada_titulo.get().strip()
        categoria = self.entrada_categoria.get().strip()
        prioridade = self.entrada_prioridade.get().strip()

        if not titulo or not categoria:
            messagebox.showwarning("Dados incompletos", "Preencha título e categoria.")
            return

        self.controlador.adicionar_tarefa(titulo, categoria, prioridade)
        self.entrada_titulo.delete(0, tk.END)
        self.entrada_categoria.delete(0, tk.END)
        self.entrada_prioridade.set("Alta")
        self.carregar_tarefas()

    def concluir_tarefa(self):
        item = self.tree.focus()
        if not item:
            messagebox.showinfo("Seleção", "Selecione uma tarefa para concluir.")
            return

        id_tarefa = int(self.tree.item(item, "values")[0])
        self.controlador.concluir_tarefa(id_tarefa)
        self.carregar_tarefas()

    def excluir_tarefa(self):
        item = self.tree.focus()
        if not item:
            messagebox.showinfo("Seleção", "Selecione uma tarefa para excluir.")
            return

        id_tarefa = int(self.tree.item(item, "values")[0])
        self.controlador.excluir_tarefa(id_tarefa)
        self.carregar_tarefas()


if __name__ == "__main__":
    app = TelaTarefas()
    app.mainloop()
