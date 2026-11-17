# Release 3 — Pendências e atrasos

**Entrega:** 17/11/2026, junto com a Release 4, a pedido do professor (prevista para 12/11) · **Branch em andamento:**
`dev/release-3` · **Baseline:** tag `release3` (criada após a revisão do PR)

## O que foi entregue

- **Relatório de pendências e atrasos (A14, RFS18):** em **Pendências** no menu.
  - Mostra os empréstimos sem devolução: objeto (nome e identificador), categoria, pessoa, retirada, previsão, situação
    (No prazo ou Atrasado) e dias de atraso.
  - Filtros por pessoa (inclusive inativas), categoria atual do objeto e somente atrasados, combinados por E.
  - Atrasados primeiro; dentro de cada situação, previsão e identificador crescentes. Vencer hoje não é atraso.
  - Totais de empréstimos exibidos e de atrasados, também no resultado vazio ("Nenhuma pendência encontrada.").
  - Linhas atrasadas destacadas em vermelho.
- **Mudança #21, orientação do professor:** o objeto deixa de ter código
  ([issue #21](https://github.com/FelipeMDR/CadeMeuTrem/issues/21)).
  - Cada unidade física é identificada pelo identificador gerado pelo sistema, e nomes iguais são permitidos (duas
    furadeiras são dois objetos).
  - Empréstimos e relatórios mostram o objeto como nome e identificador, por exemplo "Furadeira (3)".
  - Bancos criados antes da R3 são migrados ao abrir, sem perder dados.
  - Esforço absorvido pela reserva B03.
- **Testes (A15):** 115 de 115 aprovados ([relatório](relatorio_testes.md)).
  - CT07: pendências, com datas relativas ao dia da execução.
  - CT09: telas em português, erros junto ao formulário e confirmação de exclusões.
  - CT12: relatório de pendências em até 48 ms com 100 pessoas, 500 objetos e 1.000 empréstimos (limite: 2 s).
  - CT03 reescrito para objetos sem código, e migração de banco da R2 no CT10.
  - A saída dos testes não mostra mais os avisos internos do Chrome.
- **Documentos (A16.1):**
  - DRE 3.3: mudança #21 e situação do RFS18, RNF01 e RNF04;
  - MRB 2.3: CT03 e CT07 revistos, resultados da R3;
  - cronograma XML v2.5: [acompanhamento de 17/11](acompanhamento_cronograma.md);
  - [evidências](evidencias/).

## Pendências para a dupla

- [ ] Revisar o Pull Request da R3.
- [x] Sincronizar o `.pod` com o XML v2.6, que consolida o acompanhamento da R3 e da R4 (17/11).
- [x] Fazer o merge na `main` e criar a tag `release3` (A16.2), em 17/11.
- [ ] Demonstrar com a R4 (A16.3).

## Fora desta release

Histórico de empréstimos (RFS19), regressão final, verificação de instalação e pacote final, na R4.
