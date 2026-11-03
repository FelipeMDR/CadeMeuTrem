# Release 2 — Objetos e empréstimos

**Entrega:** 03/11/2026, antecipada a pedido do professor (prevista para 05/11) · **Branch em andamento:** `dev/release-2` · **Baseline:** tag `release2` (criada após a revisão do PR)

## O que a Aula 22-23 pede e onde está

| # | Exigência | Situação | Onde |
|---|---|---|---|
| 1 | Implementação de mais 2 CRUDs | Feito | Objetos (RFS09 a RFS12) em [`app/objetos.py`](../../../app/objetos.py); empréstimos e devolução (RFS13 a RFS17) em [`app/emprestimos.py`](../../../app/emprestimos.py) |
| 2 | Teste automatizado dos CRUDs com Selenium | Feito: 101/101 aprovados, 37 da R1 e 64 novos (CT03 18, CT04 14, CT05 9, CT06 17, CT10 3 e mais 3 no CT13) | [`tests/selenium/`](../../../tests/selenium/) e [relatório](relatorio_testes.md) |
| 3 | Commits de código, DRE e cronograma na branch em andamento | Feito | Histórico da branch `dev/release-2` |
| 4 | Atualização periódica do cronograma e do DRE, sob controle de versão | Cronograma v2.4 (XML e ProjectLibre) e DRE 3.2 atualizados | [DRE 3.2](../../01_DRE_Cade_Meu_Trem.pdf), [acompanhamento do CRO](acompanhamento_cronograma.md) |
| 5 | Baseline de gerência de configuração (tag) | Pendente: depois do merge do PR | [Gerência de configuração](../../gerencia_configuracao.md) |

## Entregue

- **Objetos (A10):**
  - código obrigatório de 1 a 20 caracteres, gravado sem espaços nas extremidades, em maiúsculas e único;
  - nome obrigatório (até 80), categoria escolhida da lista (nome e identificador), observação (até 250) e ativo Sim/Não;
  - sem categoria cadastrada, a inclusão é impedida e orienta o cadastro em Categorias;
  - disponibilidade calculada: Emprestado, Disponível ou Inativo;
  - consulta por código, trecho do nome, categoria, ativo e disponibilidade, combinados por E, em ordem de nome, código e
    identificador;
  - exclusão com confirmação, bloqueada quando há qualquer empréstimo, aberto ou devolvido.
- **Empréstimos e devolução (A11):**
  - inclusão só com pessoa ativa e objeto ativo e disponível; datas DD/MM/AAAA; retirada até o dia atual (fuso
    America/Sao_Paulo); previsão igual ou posterior à retirada;
  - elegibilidade revalidada na mesma transação da gravação, e índice único no banco: um empréstimo aberto por objeto;
  - alteração só da previsão (enquanto aberto) e da observação;
  - consulta por pessoa, objeto e situação, em ordem de retirada decrescente;
  - exclusão com confirmação, que preserva pessoa e objeto e recalcula a disponibilidade;
  - devolução entre a retirada e o dia atual, sem repetição nem reabertura.
- **Testes (A12):**
  - CT03 (objetos), CT04 (empréstimos), CT05 (regras de empréstimo e devolução) e CT06 (datas, inclusive 31/04 e 29/02);
  - CT10: os dados persistem depois de reiniciar o servidor, e as exclusões de pessoa, categoria e objeto com vínculo são
    bloqueadas pela tela, como a MRB previa para a R2;
  - CT13 completo: parâmetros inválidos nas quatro consultas, HTML e aspas exibidos como texto, limites e formulário sem
    token CSRF recusado.
- **Documentos (A13.1):**
  - DRE 3.2: situação dos requisitos da R2 e proteção CSRF no RNF05;
  - MRB 2.2: resultado de CT03 a CT06, CT10 e CT13;
  - cronograma XML v2.4: [acompanhamento de 03/11](acompanhamento_cronograma.md);
  - [roteiro da apresentação](../../08_Roteiro_Discussao_R2.pdf) e [evidências](evidencias/).

## Correções pedidas depois da R1 (reserva B02)

- **Comentário do professor (29/10):** os testes rodavam rápido demais para acompanhar. `scripts\demonstrar_testes.bat`
  abre o Chrome visível, destaca cada campo, digita letra por letra e mostra o cenário em execução.
- **Revisão técnica de 28/10, achado de prioridade alta:** os formulários aceitavam envio por outro site. Agora todo
  formulário que grava leva um token da sessão (CSRF), e envios sem ele são recusados.
- **Revisão técnica, achado de prioridade baixa:** o caminho do Chrome pode ser informado em `CHROME_BINARIO`.

## Roteiro da demonstração (03/11)

Na ordem em que o professor avalia (detalhes no [roteiro](../../08_Roteiro_Discussao_R2.pdf)):

1. **Cronograma planejado:** no ProjectLibre, o que estava previsto para a R2 (A10 a A13 e B02).
2. **DRE:** seções 3.3 e 3.4, RFS09 a RFS17.
3. **Testes Selenium no modo de demonstração**, mostrando os requisitos:
   - `scripts\demonstrar_testes.bat tests\selenium\test_ct03_objetos.py`;
   - `scripts\demonstrar_testes.bat tests\selenium\test_ct04_emprestimos.py -k rfs13`;
   - `scripts\demonstrar_testes.bat tests\selenium\test_ct05_regras_emprestimo.py -k rfs17`.
4. **Cronograma atualizado:** % físico concluído das atividades da R2.
5. **Tag:** `release2` no GitHub.

## Pendências para a dupla

- [ ] Revisar o Pull Request da R2 (Antony e Felipe) e registrar a revisão.
- [x] Salvar e conferir o [cronograma v2.4 no ProjectLibre](../../03_CRO_Cade_Meu_Trem.pod).
- [ ] Informar as horas reais das atividades concluídas.
- [x] Fazer o merge na `main` e criar a tag `release2` (A13.2), em 03/11.
- [ ] Demonstrar objetos e empréstimos (A13.3, 03/11).

## Fora desta release

Relatório de pendências e atrasos (R3, 12/11) e histórico de empréstimos (R4, 19/11). A situação "Atrasado" e os dias de
atraso entram no relatório da R3; a consulta da R2 mostra apenas Aberto ou Devolvido, como o RFS15 especifica.
