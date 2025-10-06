# Prova1-QA
Repositório para a primeira prova de QA

# Projeto: Sistema de Empréstimos de Biblioteca (Python)

Este projeto implementa a lógica de negócio para um sistema de gerenciamento de empréstimos de livros. Foi desenvolvido em Python e utiliza `pytest` e `pytest-mock` para garantir a qualidade e a correção da lógica através de testes unitários.

## 🚀 Estrutura do Projeto

```
biblioteca/
├── __init__.py
├── models.py         # Contém as classes Book e Member
├── repositories.py   # Define a interface (ABC) do repositório
└── services.py       # Contém a classe LoanService e LoanException

tests/
├── __init__.py
└── test_services.py  # Testes unitários para LoanService

.gitignore
README.md
requirements.txt
```

## ✅ Regras de Negócio Testadas

A seguir estão as regras de negócio implementadas na classe `LoanService` e validadas pelos testes em `test_services.py`.

### Empréstimo de Livro (`borrow_book`)

1.  **RN01: Um livro deve estar disponível para ser emprestado.**
    * Um livro que já está emprestado não pode ser emprestado novamente.
    * _Testado em: `test_borrow_book_when_book_is_already_loaned_raises_exception()`_

2.  **RN02: Um membro não pode exceder o limite máximo de empréstimos.**
    * O sistema define um limite de 3 livros emprestados simultaneamente por membro.
    * _Testado em: `test_borrow_book_when_member_has_reached_loan_limit_raises_exception()`_

3.  **RN03: Um empréstimo só pode ser realizado com sucesso se todas as regras forem atendidas.**
    * O livro deve estar disponível e o membro deve estar abaixo do seu limite de empréstimos.
    * _Testado em: `test_borrow_book_when_conditions_are_met_succeeds()`_

### Devolução de Livro (`return_book`)

4.  **RN04: Um membro só pode devolver um livro que ele mesmo pegou emprestado.**
    * O sistema deve verificar se existe um empréstimo ativo para aquele livro e membro específicos.
    * _Testado em: `test_return_book_when_loan_does_not_exist_for_member_raises_exception()`_

5.  **RN05: A devolução de um livro o torna disponível novamente.**
    * Após a devolução, o registro do empréstimo é removido.
    * _Testado em: `test_return_book_when_loan_exists_succeeds()`_

## 🛠️ Como Executar os Testes

1.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Rode os testes com pytest:**
    ```bash
    pytest --cov=biblioteca
    ```
    O comando acima também irá gerar um relatório de cobertura de testes no terminal.

## 📦 Dependências (requirements.txt)

```
pytest
pytest-mock
pytest-cov
```