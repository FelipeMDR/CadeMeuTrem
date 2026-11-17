# Release 4 — Histórico e entrega final

**Entrega:** 17/11/2026, junto com a Release 3, a pedido do professor (prevista para 19/11) · **Branch em andamento:**
`dev/release-4` · **Baseline:** tag `release4` (criada após a revisão do PR)

## O que foi entregue

- **Histórico de empréstimos (A17, RFS19):** em **Histórico** no menu.
  - Período obrigatório da retirada, com padrão do primeiro dia do mês até hoje; as duas datas entram no período.
  - Datas inválidas ou período invertido impedem a consulta e mostram a correção.
  - Filtros por pessoa e objeto (inclusive inativos) e situação (Abertos ou Devolvidos), combinados por E.
  - Ordem de retirada e identificador decrescentes; totais de exibidos, abertos e devolvidos.
- **Regressão e instalação (A18):** 129 de 129 aprovados ([relatório](relatorio_testes.md)).
  - CT08: histórico, com período inclusivo, invertido e inválido, padrões, filtros e cadastros atuais.
  - CT11: nenhuma página usa arquivo de fora da aplicação, e o servidor atende só em 127.0.0.1.
  - CT12: pendências e histórico medidos com 100 pessoas, 500 objetos e 1.000 empréstimos, todos abaixo de 100 ms.
  - CT10: a cópia de segurança feita com o sistema encerrado restaura os dados.
  - CT14: o README foi seguido num clone limpo do GitHub, com 129 de 129 aprovados.
- **Manual e documentação (A19):**
  - [manual do usuário](../../manual_do_usuario.md);
  - README consolidado, com cópia de segurança e execução sem internet;
  - dados de exemplo com devoluções do mês anterior;
  - DRE 3.4 com todos os requisitos atendidos, MRB 2.4 e cronograma XML v2.6
    ([acompanhamento](acompanhamento_cronograma.md));
  - [roteiro da apresentação da R3 e da R4](../../09_Roteiro_Discussao_R3_R4.pdf) e [evidências](evidencias/).

## Situação final dos requisitos

Os 19 requisitos funcionais (RFS01 a RFS19) estão implementados e testados, e os 6 requisitos não funcionais (RNF01 a
RNF06) estão atendidos, como registram a seção 5 do DRE 3.4 e a MRB 2.4.

## Pendências para a dupla

- [ ] Revisar os Pull Requests da R3 e da R4.
- [ ] Abrir o XML v2.6 no ProjectLibre, salvar o `.pod` e lançar as horas reais.
- [ ] Fazer o merge na `main` e criar as tags `release3` e `release4` (A16.2 e A20.1).
- [ ] Demonstrar a R3 e a R4 (A16.3 e A20.2).
- [ ] Regularizar a cobrança da conta no GitHub: a verificação automática dos testes (GitHub Actions) não está rodando.
