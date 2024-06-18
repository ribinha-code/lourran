import time

# Funções de inicialização
def inicializar_produtos():
    return [
        {'id': 1, 'nome': 'Maçã', 'preço': 1.50, 'estoque': 10},
        {'id': 2, 'nome': 'Banana', 'preço': 0.75, 'estoque': 20},
        {'id': 3, 'nome': 'Laranja', 'preço': 1.20, 'estoque': 15},
        {'id': 4, 'nome': 'Pera', 'preço': 1.80, 'estoque': 8}
    ]

def inicializar_carrinho():
    return []

def inicializar_compras_passadas():
    return []

# Variáveis globais para controle de login
usuario_logado = None
tipo_usuario = None

# Funções relacionadas aos produtos
def visualizar_produtos(produtos):
    print("              --------------------------------")
    print("              |     Produtos disponíveis     |")
    print("              --------------------------------")
    for produto in produtos:
        print(f"ID: {produto['id']}, Nome: {produto['nome']}, Preço: R${produto['preço']:.2f}, Estoque: {produto['estoque']} unidades")

def acessar_pagina_produto(produtos, carrinho):
    global usuario_logado, tipo_usuario

    # Se não estiver logado, solicita login/cadastro
    if usuario_logado is None:
        menu_login()

    # Exibir produtos disponíveis
    visualizar_produtos(produtos)

    if tipo_usuario == 'Cliente':
        produto_id = int(input("Digite o ID do produto: "))
        produto = next((p for p in produtos if p['id'] == produto_id), None)
        if produto:
            print(f"Produto selecionado: {produto['nome']} - R${produto['preço']:.2f} - {produto['estoque']} unidades disponíveis\n")
            adicionar_ao_carrinho(produto, carrinho)
        else:
            print("Produto não encontrado.")
    else:
        print("Acesso não autorizado para funcionários.")

def adicionar_ao_carrinho(produto, carrinho):
    quantidade = int(input(f"Quantas unidades de {produto['nome']} você deseja adicionar ao carrinho? "))
    if quantidade > produto['estoque']:
        print("Quantidade solicitada maior que a disponível em estoque.\n")
    else:
        produto['estoque'] -= quantidade
        item = next((item for item in carrinho if item['produto']['id'] == produto['id']), None)
        if item:
            item['quantidade'] += quantidade
        else:
            carrinho.append({'produto': produto.copy(), 'quantidade': quantidade})
        print(f"{quantidade} unidades de {produto['nome']} adicionadas ao carrinho.")

def alterar_quantidade(carrinho):
    produto_id = int(input("Digite o ID do produto no carrinho: "))
    item = next((item for item in carrinho if item['produto']['id'] == produto_id), None)
    if item:
        nova_quantidade = int(input(f"Nova quantidade para {item['produto']['nome']}: "))
        if nova_quantidade > item['produto']['estoque'] + item['quantidade']:
            print("Quantidade solicitada maior que a disponível em estoque.\n")
        else:
            item['produto']['estoque'] += item['quantidade'] - nova_quantidade
            item['quantidade'] = nova_quantidade
            print(f"Quantidade de {item['produto']['nome']} atualizada para {nova_quantidade}.")
    else:
        print("Produto não encontrado no carrinho.\n1")

def consultar_carrinho(carrinho):
    print('-----------------------------------')
    print("|       Carrinho de compras       |")
    print('-----------------------------------')
    if not carrinho:
        print("Seu carrinho está vazio.\n")
    else:
        for item in carrinho:
            produto = item['produto']
            quantidade = item['quantidade']
            print(f"{produto['nome']} - {quantidade} unidades - R${produto['preço'] * quantidade:.2f}")

# Funções relacionadas ao menu de login/cadastro
def menu_login():
    global usuario_logado, tipo_usuario

    while True:
        print('--------------------------------------')
        print('|            Opção de Login          |')
        print('--------------------------------------')
        print('|           1- Login                 |')
        print('|           2- Cadastrar             |')
        print('|           0- Voltar                |')
        print('--------------------------------------')
        print()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            fazer_login()
            if usuario_logado:
                return
        elif opcao == '2':
            fazer_cadastro()
        elif opcao == '0':
            return
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.\n")

def fazer_login():
    global usuario_logado, tipo_usuario

    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    # Verifica se o usuário está na lista de clientes
    for usuario in cadastro_cliente:
        if usuario["email"] == email and usuario["senha"] == senha:
            print(f"Bem-vindo(a), {usuario['nome']}!")
            usuario_logado = usuario
            tipo_usuario = 'Cliente'
            return

    # Verifica se o usuário está na lista de funcionários
    for usuario in cadastro_funcionario:
        if usuario["email"] == email and usuario["senha"] == senha:
            print(f"Bem-vindo(a), {usuario['nome']}!")
            usuario_logado = usuario
            tipo_usuario = 'Funcionário'
            return

    print("Email ou senha incorretos. Tente novamente.\n")

def fazer_cadastro():
    global usuario_logado, tipo_usuario

    print('----------------------------------------------------')
    print('|           1- Cadastro de Cliente                 |')
    print('|           2- Cadastro de Funcionário             |')
    print('|           0- Voltar                              |')
    print('----------------------------------------------------')
    print()
    opcao1 = input('Escolha a opção de cadastro: ')

    if opcao1 == '1':
        novo_usuario = {}
        novo_usuario["nome"] = input("Digite seu nome: ")
        novo_usuario["email"] = input("Digite seu email: ")
        novo_usuario["senha"] = input("Digite sua senha: ")
        cadastro_cliente.append(novo_usuario)
        print("Cadastro de cliente realizado com sucesso!\n")
        usuario_logado = novo_usuario
        tipo_usuario = 'Cliente'
    elif opcao1 == '2':
        novo_usuario = {}
        novo_usuario["nome"] = input("Digite seu nome: ")
        novo_usuario["email"] = input("Digite seu email: ")
        novo_usuario["senha"] = input("Digite sua senha: ")
        cadastro_funcionario.append(novo_usuario)
        print("Cadastro de funcionário realizado com sucesso!\n")
        usuario_logado = novo_usuario
        tipo_usuario = 'Funcionário'
    elif opcao1 == '0':
        return
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.\n")

# Funções relacionadas à compra e finalização
def confirmar_compra(produtos, carrinho, compras_passadas):
    if not carrinho:
        print("Carrinho está vazio. Adicione produtos antes de confirmar a compra.\n")
        return

    consultar_carrinho(carrinho)
    metodo_pagamento = escolher_metodo_pagamento()
    endereco = inserir_endereco()

    numero_pedido = len(compras_passadas) + 1

    compra = {
        'numero_pedido': numero_pedido,
        'data': obter_data_atual(),
        'carrinho': carrinho.copy(),
        'metodo_pagamento': metodo_pagamento,
        'endereco': endereco
    }

    compras_passadas.append(compra)
    carrinho.clear()
    print("Compra confirmada!\n")
    gerar_nota_fiscal(compra)

def escolher_metodo_pagamento():
    print('--------------------------------------------')
    print("|         ESCOLHA O MÉTODO DE PAGAMENTO    |")
    print("|------------------------------------------|")
    print("|            1. Cartão de Crédito          |")
    print("|            2. Pix                        |")
    print("|            3. Boleto                     |")
    print('--------------------------------------------')
    opcao = int(input("Digite o número da opção desejada: "))
    metodos = {1: 'Cartão de Crédito', 2: 'Pix', 3: 'Boleto'}
    metodo = metodos.get(opcao, 'Cartão de Crédito')
    print(f"Método de pagamento escolhido: {metodo}\n")
    return metodo

def inserir_endereco():
    endereco = input("Digite seu endereço: ")
    return endereco

def obter_data_atual():
    return time.strftime('%d/%m/%Y %H:%M:%S')

def gerar_nota_fiscal(compra):
    print(f"Nota Fiscal - Pedido {compra['numero_pedido']}")
    print(f"Data: {compra['data']}")
    total = 0
    for item in compra['carrinho']:
        produto = item['produto']
        quantidade = item['quantidade']
        subtotal = produto['preço'] * quantidade
        total += subtotal
        print(f"{produto['nome']} - {quantidade} unidades - R${subtotal:.2f}")
    print(f"Total: R${total:.2f}")
    print("Método de pagamento:", compra['metodo_pagamento'])
    print("Endereço de entrega:", compra['endereco'])

def consultar_compras_passadas(compras_passadas):
    if not compras_passadas:
        print("Não há compras passadas.\n")
        return

    print("Compras passadas:")
    for compra in compras_passadas:
        print(f"Pedido {compra['numero_pedido']} - Data: {compra['data']}\n")
        total = 0
        for item in compra['carrinho']:
            produto = item['produto']
            quantidade = item['quantidade']
            subtotal = produto['preço'] * quantidade
            total += subtotal
            print(f"{produto['nome']} - {quantidade} unidades - R${subtotal:.2f}")
        print(f"Total do pedido: R${total:.2f}")
        print("Método de pagamento:", compra['metodo_pagamento'])
        print("Endereço de entrega:", compra['endereco'])

# Função principal para o menu
def menu_principal():
    produtos = inicializar_produtos()
    carrinho = inicializar_carrinho()
    compras_passadas = inicializar_compras_passadas()

    while True:
        print('-------------------------------------------------------------------')
        print("|                               MENU                              |")
        print('|-----------------------------------------------------------------|')
        print("|      1. Visualizar produtos                                     |")
        print("|      2. Acessar página do produto e adicionar ao carrinho       |")
        print("|      3. Alterar quantidade de itens no carrinho                 |")
        print("|      4. Consultar carrinho de compras e confirmar compra        |")
        print("|      5. Consultar compras passadas                              |")
        print("|      0. Sair                                                    |")
        print('-------------------------------------------------------------------')
        print()
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            visualizar_produtos(produtos)
        elif opcao == 2:
            acessar_pagina_produto(produtos, carrinho)
        elif opcao == 3:
            alterar_quantidade(carrinho)
        elif opcao == 4:
            consultar_carrinho(carrinho)
            confirmar_compra(produtos, carrinho, compras_passadas)
        elif opcao == 5:
            consultar_compras_passadas(compras_passadas)
        elif opcao == 0:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Lista para armazenar os cadastros de clientes e funcionários
cadastro_cliente = []
cadastro_funcionario = []

# Execução do programa
if __name__ == "__main__":
    menu_principal()
