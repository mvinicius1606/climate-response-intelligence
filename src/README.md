# Módulos da aplicação

- `data/`: manifests e acesso às fontes;
- `quality/`: profiling, regras e relatórios;
- `decision_engine/`: score determinístico e justificativa estruturada;
- `ai/`: explicação opcional fundamentada.

A UI chama esses módulos; domain logic não deve migrar para Streamlit. Cada package ainda é um placeholder documentado.
