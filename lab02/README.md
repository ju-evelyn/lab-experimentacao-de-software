# Lab 02

## Instalação de Dependências

Para executar estes scripts, você irá precisar do Python 3.10 (ou superior),
do Java 8 (ou superior) e do Maven instalados na sua máquina.

```sh
# Instalação de dependências
python3 -m venv venv
pip install -r requirements
```

Crie um arquivo `.env` com base no `.env.example` com o seu token do GitHub.

```sh
## Ativar venv

# No Windows (PowerShell)
venv\Scripts\activate

# No Linux (Bash)
source ./venv/bin/activate
```

## Rodar scripts

```sh
py main.py
```
