import pytest
from biblioteca.models import Book, Member
from biblioteca.repositories import LoanRepository
from biblioteca.services import LoanService, LoanException

# Fixtures do Pytest são funções que preparam dados ou estado para os testes.
# Elas ajudam a evitar a duplicação de código.
@pytest.fixture
def available_book():
    return Book(id="1", title="Clean Code")

@pytest.fixture
def loaned_book():
    return Book(id="2", title="The Pragmatic Programmer")

@pytest.fixture
def member_with_no_loans():
    return Member(id="101", name="Alice")

@pytest.fixture
def member_with_max_loans():
    return Member(id="102", name="Bob")

# O argumento 'mocker' é injetado automaticamente pelo plugin pytest-mock.
@pytest.fixture
def mock_repo(mocker):
    # Cria um mock que se conforma à interface do LoanRepository
    return mocker.create_autospec(LoanRepository, instance=True)

# --- Testes para borrow_book ---

def test_borrow_book_when_conditions_are_met_succeeds(
    mock_repo, available_book, member_with_no_loans
):
    """RN03: Testa o caminho de sucesso para o empréstimo de um livro."""
    # Cenário (Arrange)
    mock_repo.is_book_loaned.return_value = False
    mock_repo.count_loans_by_member.return_value = 0
    service = LoanService(mock_repo)

    # Ação (Act)
    service.borrow_book(available_book, member_with_no_loans)

    # Assertiva (Assert)
    # Verifica se o método de salvar foi chamado com os argumentos corretos
    mock_repo.save_loan.assert_called_once_with(available_book, member_with_no_loans)

def test_borrow_book_when_book_is_already_loaned_raises_exception(
    mock_repo, loaned_book, member_with_no_loans
):
    """RN01: Testa a falha ao tentar emprestar um livro já emprestado."""
    # Cenário
    mock_repo.is_book_loaned.return_value = True
    service = LoanService(mock_repo)

    # Ação & Assertiva
    with pytest.raises(LoanException, match="Livro já está emprestado."):
        service.borrow_book(loaned_book, member_with_no_loans)
    
    # Garante que o método de salvar nunca foi chamado
    mock_repo.save_loan.assert_not_called()

def test_borrow_book_when_member_has_reached_loan_limit_raises_exception(
    mock_repo, available_book, member_with_max_loans
):
    """RN02: Testa a falha quando o membro atingiu seu limite de empréstimos."""
    # Cenário
    mock_repo.is_book_loaned.return_value = False
    mock_repo.count_loans_by_member.return_value = 3
    service = LoanService(mock_repo)

    # Ação & Assertiva
    with pytest.raises(LoanException, match="Membro atingiu o limite de empréstimos."):
        service.borrow_book(available_book, member_with_max_loans)

    mock_repo.save_loan.assert_not_called()

# --- Testes para return_book ---

def test_return_book_when_loan_exists_succeeds(
    mock_repo, loaned_book, member_with_no_loans
):
    """RN05: Testa o caminho de sucesso para a devolução de um livro."""
    # Cenário
    mock_repo.find_loaner_of.return_value = member_with_no_loans.id
    service = LoanService(mock_repo)
    
    # Ação
    service.return_book(loaned_book, member_with_no_loans)
    
    # Assertiva
    mock_repo.remove_loan.assert_called_once_with(loaned_book)

@pytest.mark.parametrize("loaner_id", [None, "999"])
def test_return_book_when_loan_does_not_exist_for_member_raises_exception(
    mocker, loaned_book, member_with_no_loans, loaner_id
):
    """RN04: Testa falhas ao devolver livro não emprestado pelo membro."""
    # Cenário
    mock_repo = mocker.create_autospec(LoanRepository, instance=True)
    mock_repo.find_loaner_of.return_value = loaner_id
    service = LoanService(mock_repo)
    
    # Ação & Assertiva
    with pytest.raises(LoanException, match="Este livro não foi emprestado por este membro."):
        service.return_book(loaned_book, member_with_no_loans)
        
    mock_repo.remove_loan.assert_not_called()