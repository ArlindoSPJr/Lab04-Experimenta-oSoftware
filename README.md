# Lab04 — Testes de Hipótese por Dentro

Comparação, por simulação de Monte Carlo, do **t de Welch** e do **Mann-Whitney** na pergunta: *o tempo até o merge de PRs de contribuidores novatos é diferente do de membros do core team?* Os dados reais são PRs do repositório [`pallets/click`](https://github.com/pallets/click).

- GitHub Projects: https://github.com/users/ArlindoSPJr/projects/6
- Dashboard: *(link publicado na Sprint 02)*

## Instalação

Requer Python ≥ 3.11.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Rodar tudo

Um único comando, com semente fixa (42), gera todos os resultados em `results/`:

```bash
python -m lab04.run_all
```

## Abrir o dashboard

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
