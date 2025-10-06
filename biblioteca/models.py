# Usamos dataclasses para criar classes de dados concisas e robustas.
from dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str

@dataclass
class Member:
    id: str
    name: str