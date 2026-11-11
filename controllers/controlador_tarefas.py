import os
import sys

if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.modelo_tarefas import ModeloTarefas


class ControladorTarefas:
    def __init__(self):
        self.modelo = ModeloTarefas()

    def listar_tarefas(self):
        df = self.modelo.carregar()
        colunas = ["id", "titulo", "categoria", "prioridade", "status"]
        for coluna in colunas:
            if coluna not in df.columns:
                df[coluna] = ""
        return df[colunas]

    def adicionar_tarefa(self, titulo, categoria, prioridade):
        df = self.modelo.carregar()

        if "id" not in df.columns:
            df["id"] = range(1, len(df) + 1)

        novo_id = 1 if df.empty else int(df["id"].max()) + 1

        nova_tarefa = {
            "id": novo_id,
            "titulo": titulo,
            "categoria": categoria,
            "prioridade": prioridade,
            "status": "Pendente",
        }

        df.loc[len(df)] = nova_tarefa
        self.modelo.salvar(df)

    def concluir_tarefa(self, id_tarefa):
        df = self.modelo.carregar()

        if "id" in df.columns and "status" in df.columns:
            df.loc[df["id"] == id_tarefa, "status"] = "Concluída"
            self.modelo.salvar(df)

    def excluir_tarefa(self, id_tarefa):
        df = self.modelo.carregar()

        if "id" in df.columns:
            df = df[df["id"] != id_tarefa]
            self.modelo.salvar(df)
