"""Cria o banco local com os dados de exemplo.

Uso: .venv\\Scripts\\python scripts\\carregar_exemplo.py [--substituir]
"""

import sys
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import db  # noqa: E402

caminho = Path(db.caminho_banco())
if caminho.exists():
    if "--substituir" not in sys.argv:
        sys.exit(f"O banco {caminho} já existe. Use --substituir para apagá-lo e recriar com os dados de exemplo.")
    caminho.unlink()

db.criar_esquema(str(caminho))
with closing(db.abrir(str(caminho))) as conexao:
    conexao.executescript((db.RAIZ / "data" / "exemplo.sql").read_text(encoding="utf-8"))
    pessoas = conexao.execute("SELECT COUNT(*) FROM pessoa").fetchone()[0]
    categorias = conexao.execute("SELECT COUNT(*) FROM categoria").fetchone()[0]
print(f"Banco criado em {caminho}: {pessoas} pessoas e {categorias} categorias de exemplo.")
