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
            if extrato == "":
                print(" EXTRATO ".center(30, "#"), end='\n\n')
                print("Extrato sem movimentações")
            else:
                extrato = extrato[:-1].replace(",", ".")
                print(" EXTRATO ".center(30, "#"), end='\n\n')
                print(f"{extrato}\n\nSaldo: R$ {saldo:.2f}\n")

        elif opcao == "q":
            print("\nVolte sempre! Você é muito importante para nós!\n")
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