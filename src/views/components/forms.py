from views.style.constants import TmColors, TmFonts
import tkinter as tk



class CampoFormulario(tk.Frame):
    def __init__(self, pai, rotulo: str, largura: int = 28, **kwargs):
        super().__init__(pai, bg=TmColors.COR_SURFACE, **kwargs)
        tk.Label(self, text=rotulo, font=TmFonts.FONTE_LABEL_SM, bg=TmColors.COR_SURFACE,
                 fg=TmColors.COR_TEXTO_SOFT).pack(anchor="w")
        self.entry = tk.Entry(self, width=largura, font=TmFonts.FONTE_LABEL,
                              bg=TmColors.COR_SURFACE, fg=TmColors.COR_TEXTO,
                              relief="solid", bd=1, highlightthickness=1,
                              highlightbackground=TmColors.COR_BORDA,
                              highlightcolor=TmColors.COR_ACCENT)
        self.entry.pack(fill="x", pady=(2, 0))

    def get(self) -> str:
        return self.entry.get()

    def limpar(self):
        self.entry.delete(0, tk.END)