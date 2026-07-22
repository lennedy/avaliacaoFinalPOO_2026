from abc import ABC, abstractmethod
from typing import List


class Endereco:
    def __init__(self, rua: str, numero: int, bairro: str, cidade: str):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade

    def get_rua(self) -> str:
        return self.__rua

    def get_numero(self) -> int:
        return self.__numero

    def get_bairro(self) -> str:
        return self.__bairro

    def get_cidade(self) -> str:
        return self.__cidade

    def exibir_dados(self) -> str:
        return (
            f"Rua: {self.__rua}, nº {self.__numero}\n"
            f"Bairro: {self.__bairro}\n"
            f"Cidade: {self.__cidade}"
        )


class Cliente:
    def __init__(self, nome: str, cpf: str, endereco: Endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas: List["ContaBancaria"] = []

    def get_nome(self) -> str:
        return self.__nome

    def get_cpf(self) -> str:
        return self.__cpf

    def get_endereco(self) -> Endereco:
        return self.__endereco

    def exibir_dados(self) -> str:
        return (
            f"Nome: {self.__nome}\n"
            f"CPF: {self.__cpf}\n"
            f"Endereço:\n{self.__endereco.exibir_dados()}"
        )

    def adicionar_conta(self, conta: "ContaBancaria") -> None:
        if conta not in self.__contas:
            self.__contas.append(conta)


class ContaBancaria(ABC):
    def __init__(self, cliente: Cliente, numero: str, saldo: float):
        self.__cliente = cliente
        self.__numero = numero
        self.__saldo = saldo
        cliente.adicionar_conta(self)
        self.__ativa = True

    def get_cliente(self) -> Cliente:
        return self.__cliente

    def get_titular(self) -> str:
        return self.__cliente.get_nome()

    def get_numero(self) -> str:
        return self.__numero

    def get_saldo(self) -> float:
        return self.__saldo

    def _alterar_saldo(self, novo_saldo: float) -> None:
        self.__saldo = novo_saldo

    def exibir_dados(self) -> str:
        return (
            f"Titular: {self.__cliente.get_nome()}\n"
            f"Número da conta: {self.__numero}\n"
            f"Tipo: {self.get_tipo_conta()}\n"
            f"Saldo: R$ {self.__saldo:.2f}"
        )

    def sacar(self, valor: float) -> bool:
        if valor <= 0 or valor > self.__saldo or self.__ativa == False:
            return False
        self.__saldo -= valor
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            return False
        self.__saldo += valor
        return True

    def transferir(self, valor: float, conta_destino: "ContaBancaria") -> bool:
        if conta_destino is self:
            return False
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False

    @abstractmethod
    def get_tipo_conta(self) -> str:
        pass
    
    @property
    def get_ativa(self) -> bool:
        return self.__ativa
    
    def bloquear_conta(self) -> None:
        self.__ativa = False

    def desbloquear_conta(self) -> None:
        self.__ativa = True



class ContaCorrente(ContaBancaria):
    def __init__(self, cliente: Cliente, numero: str, saldo: float,
                 limite: float, tarifa_mensal: float, limite_por_saque: float, nome_pacote: str):
        super().__init__(cliente, numero, saldo)
        self.__limite = limite
        self.__tarifa_mensal = tarifa_mensal
        self.__limite_por_saque = limite_por_saque
        self.nome_pacote = nome_pacote

    def get_limite(self) -> float:
        return self.__limite

    def get_tarifa_mensal(self) -> float:
        return self.__tarifa_mensal

    def sacar(self, valor: float) -> bool:
        if valor <= 0 or self.get_ativa == False:
            return False
        saldo_disponivel = self.get_saldo() + self.__limite
        if valor > saldo_disponivel or valor > self.__limite_por_saque:
            return False
        self._alterar_saldo(self.get_saldo() - valor)
        return True

    def cobrar_tarifa(self) -> bool:
        return self.sacar(self.__tarifa_mensal)

    def exibir_dados(self) -> str:
        return (
            f"{super().exibir_dados()}\n"
            f"Limite: R$ {self.__limite:.2f}\n"
            f"Tarifa mensal: R$ {self.__tarifa_mensal:.2f}"
        )

    def get_tipo_conta(self) -> str:
        return "Conta Corrente"
    
    def get_limite_por_saque(self) -> float:
        return self.__limite_por_saque


class ContaPoupanca(ContaBancaria):
    def __init__(self, cliente: Cliente, numero: str, saldo: float,
                 taxa_rendimento: float):
        super().__init__(cliente, numero, saldo)
        self.__taxa_rendimento = taxa_rendimento

    def get_taxa_rendimento(self) -> float:
        return self.__taxa_rendimento

    def render_juros(self) -> None:
        rendimento = self.get_saldo() * (self.__taxa_rendimento / 100)
        self._alterar_saldo(self.get_saldo() + rendimento)

    def exibir_dados(self) -> str:
        return (
            f"{super().exibir_dados()}\n"
            f"Taxa de rendimento: {self.__taxa_rendimento:.2f}%"
        )

    def get_tipo_conta(self) -> str:
        return "Conta Poupança"


class ContaSalario(ContaBancaria):
    def __init__(self, cliente: Cliente, numero: str, saldo: float,
                 empresa: str, limite_saques: int):
        super().__init__(cliente, numero, saldo)
        self.__empresa = empresa
        self.__saques_realizados = 0
        self.__limite_saques = limite_saques

    def get_empresa(self) -> str:
        return self.__empresa

    def get_saques_realizados(self) -> int:
        return self.__saques_realizados

    def get_limite_saques(self) -> int:
        return self.__limite_saques

    def receber_salario(self, valor: float) -> None:
        if valor > 0:
            self._alterar_saldo(self.get_saldo() + valor)

    def sacar(self, valor: float) -> bool:
        if self.__saques_realizados >= self.__limite_saques:
            return False
        if super().sacar(valor):
            self.__saques_realizados += 1
            return True
        return False

    def depositar(self, valor: float) -> bool:
        return False

    def transferir(self, valor: float, conta_destino: ContaBancaria) -> bool:
        if conta_destino is self:
            return False
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False

    def exibir_dados(self) -> str:
        return (
            f"{super().exibir_dados()}\n"
            f"Empresa: {self.__empresa}\n"
            f"Saques realizados: {self.__saques_realizados}\n"
            f"Limite de saques: {self.__limite_saques}"
        )

    def get_tipo_conta(self) -> str:
        return "Conta Salário"
