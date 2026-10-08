import os
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# CONFIGURAÇÃO
# ============================================================

# COLOQUE AQUI O CAMINHO DA SUA PASTA "Arquivos SALTA"
PASTA_PRINCIPAL = r"D:\Separadas 2025"

# ============================================================
# FUNÇÕES
# ============================================================

def listar_pastas(caminho):
    """Retorna somente as pastas existentes dentro de um caminho."""
    if not os.path.exists(caminho):
        return []

    return sorted(
        [
            nome for nome in os.listdir(caminho)
            if os.path.isdir(os.path.join(caminho, nome))
        ]
    )


def carregar_cidades():
    """Carrega as cidades existentes na pasta principal."""
    cidades = listar_pastas(PASTA_PRINCIPAL)

    combo_cidade["values"] = cidades

    if cidades:
        combo_cidade.current(0)
        carregar_escolas()
    else:
        combo_escola["values"] = []


def carregar_escolas(event=None):
    """Carrega as escolas da cidade selecionada."""
    cidade = combo_cidade.get()

    if not cidade:
        combo_escola["values"] = []
        return

    caminho_cidade = os.path.join(PASTA_PRINCIPAL, cidade)

    escolas = listar_pastas(caminho_cidade)

    combo_escola["values"] = escolas

    if escolas:
        combo_escola.current(0)
        atualizar_status()
    else:
        combo_escola.set("")
        atualizar_status()


def atualizar_status():
    """Atualiza o texto mostrando cidade e escola selecionadas."""
    cidade = combo_cidade.get()
    escola = combo_escola.get()

    if cidade and escola:
        label_status.config(
            text=f"📍 {cidade}  →  🏫 {escola}"
        )
    else:
        label_status.config(
            text="Selecione uma cidade e uma escola."
        )


def criar_pasta():
    """Cria a pasta da identificação e abre automaticamente."""
    cidade = combo_cidade.get()
    escola = combo_escola.get()
    identificacao = entrada_id.get().strip()

    # Verificações
    if not cidade:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma cidade."
        )
        return

    if not escola:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma escola."
        )
        return

    if not identificacao:
        messagebox.showwarning(
            "Atenção",
            "Digite o número da identificação."
        )
        entrada_id.focus()
        return

    # Impede caracteres que não podem existir em nomes de pastas
    caracteres_invalidos = '<>:"/\\|?*'

    if any(char in identificacao for char in caracteres_invalidos):
        messagebox.showerror(
            "Número inválido",
            "A identificação contém caracteres inválidos."
        )
        entrada_id.focus()
        return

    # Caminho final
    caminho_escola = os.path.join(
        PASTA_PRINCIPAL,
        cidade,
        escola
    )

    caminho_identificacao = os.path.join(
        caminho_escola,
        identificacao
    )

    try:
        # Cria a pasta se ela ainda não existir
        os.makedirs(caminho_identificacao, exist_ok=True)

        # Abre a pasta automaticamente
        os.startfile(caminho_identificacao)

        # Limpa o campo para o próximo aluno
        entrada_id.delete(0, tk.END)
        entrada_id.focus()

        label_ultimo.config(
            text=f"Última identificação: {identificacao}"
        )

    except Exception as erro:
        messagebox.showerror(
            "Erro",
            f"Não foi possível criar/abrir a pasta.\n\n{erro}"
        )


def trocar_escola():
    """Permite escolher outra escola."""
    combo_escola.set("")
    entrada_id.delete(0, tk.END)
    label_ultimo.config(text="Última identificação: —")
    atualizar_status()


# ============================================================
# JANELA
# ============================================================

janela = tk.Tk()

janela.title("Criador de Pastas - Identificações")
janela.geometry("600x430")
janela.resizable(False, False)


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    janela,
    text="Criador de Pastas",
    font=("Arial", 22, "bold")
)

titulo.pack(pady=(25, 5))


subtitulo = tk.Label(
    janela,
    text="Crie rapidamente as pastas das identificações",
    font=("Arial", 11)
)

subtitulo.pack(pady=(0, 20))


# ============================================================
# CIDADE
# ============================================================

frame_cidade = tk.Frame(janela)
frame_cidade.pack(pady=5)

label_cidade = tk.Label(
    frame_cidade,
    text="Cidade:",
    font=("Arial", 11, "bold")
)

label_cidade.pack(side=tk.LEFT, padx=10)

combo_cidade = ttk.Combobox(
    frame_cidade,
    width=40,
    state="readonly"
)

combo_cidade.pack(side=tk.LEFT)

combo_cidade.bind(
    "<<ComboboxSelected>>",
    carregar_escolas
)


# ============================================================
# ESCOLA
# ============================================================

frame_escola = tk.Frame(janela)
frame_escola.pack(pady=10)

label_escola = tk.Label(
    frame_escola,
    text="Escola:",
    font=("Arial", 11, "bold")
)

label_escola.pack(side=tk.LEFT, padx=10)

combo_escola = ttk.Combobox(
    frame_escola,
    width=40,
    state="readonly"
)

combo_escola.pack(side=tk.LEFT)

combo_escola.bind(
    "<<ComboboxSelected>>",
    lambda event: atualizar_status()
)


# ============================================================
# STATUS
# ============================================================

label_status = tk.Label(
    janela,
    text="Selecione uma cidade e uma escola.",
    font=("Arial", 10)
)

label_status.pack(pady=15)


# ============================================================
# IDENTIFICAÇÃO
# ============================================================

label_id = tk.Label(
    janela,
    text="Número da identificação:",
    font=("Arial", 12, "bold")
)

label_id.pack(pady=(10, 5))


entrada_id = tk.Entry(
    janela,
    width=30,
    font=("Arial", 16),
    justify="center"
)

entrada_id.pack(pady=5)

# Pressionar ENTER cria a pasta
entrada_id.bind(
    "<Return>",
    lambda event: criar_pasta()
)


# ============================================================
# BOTÃO CRIAR
# ============================================================

botao_criar = tk.Button(
    janela,
    text="CRIAR E ABRIR PASTA",
    command=criar_pasta,
    font=("Arial", 11, "bold"),
    width=25,
    height=2
)

botao_criar.pack(pady=15)


# ============================================================
# ÚLTIMA IDENTIFICAÇÃO
# ============================================================

label_ultimo = tk.Label(
    janela,
    text="Última identificação: —",
    font=("Arial", 10)
)

label_ultimo.pack(pady=5)


# ============================================================
# TROCAR ESCOLA
# ============================================================

botao_trocar = tk.Button(
    janela,
    text="Trocar escola",
    command=trocar_escola
)

botao_trocar.pack(pady=10)


# ============================================================
# INICIAR
# ============================================================

carregar_cidades()

entrada_id.focus()

janela.mainloop()
