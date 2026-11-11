from pathlib import Path

import pandas as pd

class ModeloTarefas:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        self.arquivo = base_dir / "dados" / "tarefas.csv"

    def carregar(self):
        if not self.arquivo.exists():
            self.arquivo.parent.mkdir(parents=True, exist_ok=True)
            df_vazio = pd.DataFrame(
                columns=["ID", "Titulo", "Categoria", "Prioridade", "Status"]
            )
            df_vazio.to_csv(self.arquivo, index=False)

        return pd.read_csv(self.arquivo)

    def salvar(self, df):
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.arquivo, index=False)