def main():
    operacoes_bancarias(menu)


def operacoes_bancarias(menu):
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    
    while True:
        opcao = input(menu)

        if opcao == "d":
            try:
                deposito = int(input("Informe o valor para depósito: "))
                saldo += deposito
                extrato += f"Depósito de R$ {deposito:.2f},\n"
                print("Depósito realizado com sucesso")

            except ValueError or deposito <= 0:
                print("Favor informe um valor inteiro válido.")

        elif opcao == "s":
            if numero_saques < LIMITE_SAQUES:
                saque = int(input("Informe o valor para saque: "))
                if saque > limite:
                    print("O limite máximo para saque é de R$ 500,00")
                else:
                    if saque > saldo:
                        print("Saldo insuficiente")
                    else:
                        saldo -= saque
                        extrato += f"Saque de R$ {saque:.2f},\n"
                        print("Saque realizado com sucesso")
                        numero_saques += 1
            else:
                print("Limite de saques diários atingido.")

        elif opcao == "e":
            extrato = extrato[:-1].replace(",", ".")
            print(f"Extrato:\n{extrato}")

        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a opção desejada")


menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

==>"""

if __name__ == "__main__":
    main()