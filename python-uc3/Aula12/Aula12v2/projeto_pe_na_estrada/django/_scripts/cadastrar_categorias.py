
import os
import sys
import json

from pathlib import Path

# ==========================================================
# 1. DIRETÓRIOS DO PROJETO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DJANGO_DIR = BASE_DIR / "django"

DADOS_DIR = BASE_DIR / "_dados"

ARQUIVO_DADOS = DADOS_DIR / "categorias.json"


# ==========================================================
# 2. CONFIGURAÇÃO DO AMBIENTE DJANGO
# ==========================================================

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

import django

django.setup()


# ==========================================================
# 3. IMPORTAÇÃO DO MODEL
# ==========================================================

from apps.produtos.models import Categoria


# ==========================================================
# 4. FUNÇÃO DE CADASTRO
# ==========================================================

def cadastrar_categorias():

    print("\n======================================")
    print("CADASTRO DE CATEGORIAS")
    print("======================================\n")

    # Verifica se o arquivo existe.
    if not ARQUIVO_DADOS.exists():
        print(f"ERRO: Arquivo não encontrado: {ARQUIVO_DADOS}")
        return

    # Carrega o arquivo JSON.
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            categorias = json.load(arquivo)

    except json.JSONDecodeError as erro:
        print(f"ERRO: JSON inválido: {erro}")
        return

    # Contadores.
    cadastradas = 0
    existentes = 0

    # Percorre os dados.
    for dados in categorias:

        nome = dados["nome"]

        descricao = dados.get("descricao", "")

        categoria, criada = Categoria.objects.get_or_create(
            nome=nome,
            defaults={
                "descricao": descricao
            }
        )

        if criada:
            cadastradas += 1
            print(f"[OK] Categoria cadastrada: {nome}")

        else:
            existentes += 1
            print(f"[EXISTENTE] Categoria já cadastrada: {nome}")

    # ======================================================
    # 5. RESUMO
    # ======================================================

    print("\n======================================")
    print("RESUMO DA OPERAÇÃO")
    print("======================================")

    print(f"Total no arquivo: {len(categorias)}")
    print(f"Novas categorias: {cadastradas}")
    print(f"Já existentes: {existentes}")
    print(f"Total no banco: {Categoria.objects.count()}")

    print("\nProcessamento finalizado!")


# ==========================================================
# 6. EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    cadastrar_categorias()
