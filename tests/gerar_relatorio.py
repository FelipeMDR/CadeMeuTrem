"""Gera o relatório de testes de uma release a partir da última execução da suíte.

Uso (depois de rodar scripts\\testar.bat):
    .venv\\Scripts\\python tests\\gerar_relatorio.py R1

Lê tests/selenium/saida/resultado.xml e ambiente.txt e grava
docs/releases/<release>/relatorio_testes.md.
"""

import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "tests" / "selenium" / "saida"

CENARIOS = {
    "test_ct01_pessoas": ("CT01", "Manter pessoas (RFS01 a RFS04)"),
    "test_ct02_categorias": ("CT02", "Manter categorias (RFS05 a RFS08)"),
    "test_ct13_protecao": ("CT13", "Validação e proteção (RNF05), cenários antecipados"),
}


def descrever(nome_teste: str) -> tuple[str, str]:
    """test_rfs03_filtro_por_trecho -> ('RFS03', 'Filtro por trecho')."""
    m = re.match(r"test_(rfs\d+|rnf\d+)_(.+)", nome_teste)
    if not m:
        return "—", nome_teste
    descricao = m.group(2).replace("_", " ")
    return m.group(1).upper(), descricao[0].upper() + descricao[1:]


def main(release: str) -> None:
    raiz = ET.parse(SAIDA / "resultado.xml").getroot()
    suite = raiz.find("testsuite") if raiz.tag == "testsuites" else raiz
    momento = datetime.fromisoformat(suite.get("timestamp")).strftime("%d/%m/%Y %H:%M")
    ambiente = (SAIDA / "ambiente.txt").read_text(encoding="utf-8").strip().splitlines()

    grupos: dict[str, list] = {}
    for caso in suite.iter("testcase"):
        modulo = caso.get("classname").split(".")[-1]
        falha = caso.find("failure") if caso.find("failure") is not None else caso.find("error")
        pulado = caso.find("skipped") is not None
        situacao = "Reprovado" if falha is not None else ("Não executado" if pulado else "Aprovado")
        grupos.setdefault(modulo, []).append((caso.get("name"), situacao, float(caso.get("time")), falha))

    total = sum(len(v) for v in grupos.values())
    aprovados = sum(1 for v in grupos.values() for _, s, _, _ in v if s == "Aprovado")

    linhas = [
        f"# Relatório de testes — Release {release[1:] if release.startswith('R') else release}",
        "",
        f"**Execução:** {momento} · **Resultado:** {aprovados} de {total} cenários aprovados · "
        f"**Duração:** {float(suite.get('time')):.1f} s",
        "",
        "Testes funcionais automatizados com Selenium (Chrome headless). Cada execução usa um banco SQLite",
        "temporário; o banco local em `data/` não é alterado. Para repetir: `scripts\\testar.bat`.",
        "",
        "## Ambiente",
        "",
        *[f"- {linha}" for linha in ambiente],
        "",
    ]
    for modulo, casos in grupos.items():
        codigo, titulo = CENARIOS.get(modulo, ("—", modulo))
        ok = sum(1 for _, s, _, _ in casos if s == "Aprovado")
        linhas += [
            f"## {codigo} — {titulo}: {ok}/{len(casos)} aprovados",
            "",
            "| Requisito | Cenário | Resultado | Tempo (s) |",
            "|---|---|---|---|",
        ]
        for nome, situacao, tempo, _ in casos:
            requisito, descricao = descrever(nome)
            linhas.append(f"| {requisito} | {descricao} | {situacao} | {tempo:.2f} |")
        linhas.append("")
        falhas = [(n, f) for n, _, _, f in casos if f is not None]
        for nome, falha in falhas:
            linhas += [f"### Falha em `{nome}`", "", "```", (falha.get("message") or "").strip(), "```", ""]

    destino = RAIZ / "docs" / "releases" / release / "relatorio_testes.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Relatório gravado em {destino.relative_to(RAIZ)} ({aprovados}/{total} aprovados)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "R1")
