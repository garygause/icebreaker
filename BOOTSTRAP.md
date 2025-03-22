# Bootstrap

Steps taken to bootstrap this project.

## Create env:

```bash
# if needed
pip install --user pipenv

pipenv shell
```

## Install dependencies:

```bash
pipenv install langchain langchain-openai
pipenv install langchain-community langchainhub

pipenv install black
pipenv install python-dotenv
```

## Create .env file:

```bash
OPENAI_API_KEY=your_openai_api_key
```

## Set cursor/vscode python interpreter to the pipenv shell:

```bash
which python
```

or

```bash
pipenv run which python
```

- open command palette (ctrl+shift+p)
- select Python: Select Interpreter
- select the one in the pipenv shell
