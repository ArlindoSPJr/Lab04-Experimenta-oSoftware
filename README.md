# Lab04 — Testes de Hipótese por Dentro

Comparação, por simulação de Monte Carlo, do **t de Welch** e do **Mann-Whitney** na pergunta: *o tempo até o merge de PRs de contribuidores novatos é diferente do de membros do core team?* Os dados reais são PRs do repositório [`pallets/click`](https://github.com/pallets/click).

- GitHub Projects: https://github.com/users/ArlindoSPJr/projects/6
- Dashboard: https://lab04-experimentacao-software.streamlit.app/

## Instalação

Requer Python ≥ 3.11.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Rodar tudo

Um único comando roda o pipeline de ponta a ponta, com semente fixa (`SEED = 42`, em `lab04/config.py`), e grava todos os resultados em `results/`:

```bash
python -m lab04.run_all
```

Leva cerca de 10 segundos (10.000 repetições por condição). Rodar de novo gera arquivos idênticos byte a byte.

### O que fica em `results/`

- `params.json`: parâmetros da lognormal ajustada aos tempos de merge reais (`mu`, `sigma`), o `n` por grupo e o arquivo de origem.
- `simulado_exemplo.csv`: um dataset simulado de exemplo (30 PRs por grupo, efeito 0,2), usado no G1 e no G2.
- `exemplo.json`: resultado do t de Welch e do Mann-Whitney aplicados ao dataset de exemplo.
- `simulacao.csv`: taxa de rejeição dos dois testes em cada cenário (base, n pequeno, outliers, assimetria forte) e tamanho de efeito, base do G3 e do G4.
- `tipo1_status.csv`: erro tipo I (efeito 0) de cada teste por cenário, com a classificação em relação aos 5%.
- `poder_vencedor.csv`: para cada cenário e efeito > 0, o teste com mais poder.
- `dados_reais.csv`: os dois testes aplicados aos PRs reais, com estatística, p-valor, tamanho de efeito e conclusão.

## Abrir o dashboard

Publicado no Streamlit Community Cloud: https://lab04-experimentacao-software.streamlit.app/ (atualiza a cada push na `main`). Para abrir localmente (o dashboard só lê `results/`, então rode o `run_all` antes se a pasta estiver vazia):

```bash
streamlit run dashboard/app.py
```

## Testes

```bash
pytest -q
```

## Documentação

- Regras de Git, GitHub e TDD: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Regras de coleta dos dados reais: [`data/REGRAS_COLETA.md`](data/REGRAS_COLETA.md)
- Plano de implementação: [`docs/superpowers/plans/2026-11-03-lab04-testes-hipotese.md`](docs/superpowers/plans/2026-11-03-lab04-testes-hipotese.md)
