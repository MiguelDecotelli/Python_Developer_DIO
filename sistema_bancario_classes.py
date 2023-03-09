from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):

        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta():
    def __init__(self, cliente, numero, saldo=0):
        self._cliente = cliente
        self._numero = numero
        self._agencia = '0001'
        self._saldo = saldo
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Saldo insuficiente")

        elif valor - saldo:
            self._saldo -= valor
            print("Saque realizado com sucesso")
            return True

        else:
            print("Valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Valor informado é inválido.")
            return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == 'Saque']
        )

        limite_excedido = valor > self._limite
        saques_excedidos = numero_saques >= self._limite_saques
        
        if limite_excedido:
            print("O limite máximo para saque é de R$ 500,00")

        elif saques_excedidos:
            print("Limite de saques diários atingido.")    
        
        else:
            super().sacar(valor)
            
        return False

    def __str__(self):
        return f"""\
            Titular:\t{self.cliente.nome}
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
        """


class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__, "valor": transacao.valor})

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def main():
    operacoes_bancarias(menu_acesso)


def operacoes_bancarias(menu):
    clientes = []
    contas = []
    conta_corrente = 1

    while True:
        opcao = input(menu_acesso)

        if opcao == 'cco':
            conta = criar_conta(conta_corrente, clientes, contas)

            if conta:
                contas.append(conta)
                conta_corrente += 1

        elif opcao == 'ccl':
            cadastrar_cliente(clientes)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
           sacar(clientes)

        elif opcao == 'e':
            extrato_conta(clientes)

        elif opcao == 'q':
            print("\nVolte sempre! Você é muito importante para nós!\n")
            break
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada")

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe um cliente com esse CPF cadastrado!")
        return
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (DD-MM-AAAA): ")
    endereco = input(
        "Endereço (Logradouro - Nº - Bairro - Cidade/Estado (Sigla)): ")
    
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, favor cadastre-se antes de criar uma conta!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!!")

def listar_contas(contas):
    for conta in contas:
        print(str(conta))

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Este cliente não possui conta.")
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!.")
        return

    valor = float(input("Informe o valor para depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor para saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def extrato_conta(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(" EXTRATO ".center(25, "="), end='\n\n')
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        print(" EXTRATO ".center(25, "="), end='\n\n')
        extrato = "Extrato sem movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}: R$ {transacao['valor']:.2f}\n"

    print(extrato)
    print(f"Saldo: atual é de R$ {conta.saldo:.2f}")



menu_acesso = """\n
=========================MENU=========================
[cco] Criar Conta
[ccl] Cadastrar Cliente
[lc] Listar Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

==>"""

if __name__ == "__main__":
    main()