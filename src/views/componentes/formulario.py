import tkinter as tk
from ..estilo.constantes import CoresTema, FontesTema


class CampoFormulario(tk.Frame):
    """Componente reutilizável para campo de formulário com rótulo e entrada de texto."""

    def __init__(self, pai, rotulo: str, largura: int = 28, **kwargs):
        super().__init__(pai, bg=CoresTema.COR_SURFACE, **kwargs)
        tk.Label(
            self,
            text=rotulo,
            font=FontesTema.FONTE_LABEL_SM,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO_SOFT
        ).pack(anchor="w")

        self.entry = tk.Entry(
            self,
            width=largura,
            font=FontesTema.FONTE_LABEL,
            bg=CoresTema.COR_SURFACE,
            fg=CoresTema.COR_TEXTO,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=CoresTema.COR_BORDA,
            highlightcolor=CoresTema.COR_ACCENT
        )
        self.entry.pack(fill="x", pady=(2, 0))

    def get(self) -> str:
        return self.entry.get()

    def limpar(self) -> None:
        self.entry.delete(0, tk.END)
