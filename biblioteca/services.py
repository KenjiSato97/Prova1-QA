from .models import Book, Member
from .repositories import LoanRepository

# Exceção customizada para a lógica de empréstimos
class LoanException(Exception):
    pass

class LoanService:
    MAX_LOANS_PER_MEMBER = 3

    def __init__(self, loan_repository: LoanRepository):
        self._repo = loan_repository

    def borrow_book(self, book: Book, member: Member) -> None:
        """Empresta um livro se todas as regras de negócio forem satisfeitas."""
        
        # RN01: Verifica se o livro já está emprestado
        if self._repo.is_book_loaned(book):
            raise LoanException("Livro já está emprestado.")
        
        # RN02: Verifica se o membro atingiu o limite de empréstimos
        if self._repo.count_loans_by_member(member) >= self.MAX_LOANS_PER_MEMBER:
            raise LoanException("Membro atingiu o limite de empréstimos.")
        
        # RN03: Se tudo estiver OK, salva o empréstimo
        self._repo.save_loan(book, member)

    def return_book(self, book: Book, member: Member) -> None:
        """Devolve um livro se o empréstimo for válido."""
        loaner_id = self._repo.find_loaner_of(book)
        
        # RN04: Verifica se o empréstimo existe e pertence ao membro
        if not loaner_id or loaner_id != member.id:
            raise LoanException("Este livro não foi emprestado por este membro.")
            
        # RN05: Se tudo estiver OK, remove o empréstimo
        self._repo.remove_loan(book)