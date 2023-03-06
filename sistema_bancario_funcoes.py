def main():
    operacoes_bancarias(menu_acesso)


def operacoes_bancarias(menu):
    AGENCIA = '0001'
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    clientes = []
    contas = []
    conta_corrente = 1


    while True:
        opcao = input(menu_acesso)

        if opcao == 'cco':
            # conta_corrente = len(contas) + 1
            conta = criar_conta(AGENCIA, conta_corrente, clientes)

            if conta:
                contas.append(conta)
                conta_corrente += 1

        elif opcao == 'ccl':
            cadastrar_cliente(clientes)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'd':
            try:
                valor = float(input("Informe o valor para depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError or valor <= 0:
                print("Favor informe um valor inteiro válido.")

        elif opcao == 's':
            valor = float(input("Informe o valor para saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == 'e':
            extrato_conta(saldo, extrato=extrato)

        elif opcao == 'q':
            print("\nVolte sempre! Você é muito importante para nós!\n")
            break
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada")


def cadastrar_cliente(clientes):
    cpf = input("CPF (somente números): ")
    for cliente in clientes:
        if cliente['CPF'] == cpf:
            print("Cliente já cadastrado")
            return

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (DD-MM-AAAA): ")
    endereco = input(
        "Endereço (Logradouro - Nº - Bairro - Cidade/Estado (Sigla)): ")
    clientes.append({"Nome": nome, "Data de nascimento": data_nascimento,
                     "CPF": cpf, "Endereco": endereco})
    print("Cliente cadastrado com sucesso")


def criar_conta(agencia, conta_corrente, clientes):
    cpf = input("CPF (somente números): ")
    for cliente in clientes:
        if cliente['CPF'] == cpf:
            print("Conta criada com sucesso!!")
            return {"Agência": agencia, "Conta corrente": conta_corrente, "Cliente": cliente}

    print("Cliente não encontrado, favor cadastre-se antes de criar uma conta!")
    return

def listar_contas(contas):
    for conta in contas:
        detalhes_conta = f"""\n
        Agência: {conta["Agência"]}
        C/C: {conta["Conta corrente"]}
        Titular: {conta["Cliente"]["Nome"]}
        """
    print(detalhes_conta)
        
def depositar(saldo, valor, extrato, /):

    saldo += valor
    extrato += f"Depósito de R$ {valor:.2f},\n"
    print("Depósito realizado com sucesso!")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques < limite_saques:
        if valor > limite:
            print("O limite máximo para saque é de R$ 500,00")
        else:
            if valor > saldo:
                print("Saldo insuficiente")
            else:
                saldo -= valor
                extrato += f"Saque de R$ {valor:.2f},\n"
                print("Saque realizado com sucesso")
                numero_saques += 1
    else:
        print("Limite de saques diários atingido.")

    return saldo, extrato, numero_saques


def extrato_conta(saldo, /, *, extrato):
    if extrato == "":
        print(" EXTRATO ".center(25, "="), end='\n\n')
        print("Extrato sem movimentações")
    else:
        extrato = extrato[:-1].replace(",", ".")
        print(" EXTRATO ".center(25, "="), end='\n\n')
        print(f"{extrato}\n\nSaldo: R$ {saldo:.2f}")


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
