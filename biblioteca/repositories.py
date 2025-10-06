from abc import ABC, abstractmethod
from typing import Optional
from .models import Book, Member

# Usamos uma Classe Base Abstrata (ABC) para definir a "interface" do repositório.
class LoanRepository(ABC):
    @abstractmethod
    def is_book_loaned(self, book: Book) -> bool:
        ...

    @abstractmethod
    def count_loans_by_member(self, member: Member) -> int:
        ...

    @abstractmethod
    def save_loan(self, book: Book, member: Member) -> None:
        ...

    @abstractmethod
    def find_loaner_of(self, book: Book) -> Optional[str]:
        ...

    @abstractmethod
    def remove_loan(self, book: Book) -> None:
        ...