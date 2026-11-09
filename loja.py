# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(self, numero, cliente_nome, cliente_cpf, cliente_email, rua, cidade, cep, tipo_cliente):
        self.numero = numero            # numero do pedido
        self.cliente_nome = cliente_nome    # os dados do cliente se repetem em CADA pedido dele
        self.cliente_cpf = cliente_cpf
        self.cliente_email = cliente_email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo_cliente = tipo_cliente          # tipo do cliente: "N" normal, "V" vip, "F" funcionario
        self.itens = []       # cada item e uma lista: [produto, qtd, preco]
        self.status = "A"         # A = aberto, P = pago, C = cancelado

    def get_status(self):
        return self.status

    def set_status(self, v):
        self.status = v


def valida(cliente_email, cliente_cpf, cep):
    if len(cliente_email) > 0:
        if "@" in cliente_email:
            if len(cliente_cpf) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, cliente_nome, cliente_cpf, cliente_email, rua, cidade, cep, tipo_cliente):
    r = valida(cliente_email, cliente_cpf, cep)
    if r != "ok":
        print("pedido", numero, "recusado:", r)
        return None
    else:
        p = Pedido(numero, cliente_nome, cliente_cpf, cliente_email, rua, cidade, cep, tipo_cliente)
        pedidos.append(p)
        return p


def add_item(pedido, produto, quantidade, valor):
    pedido.itens.append([produto, quantidade, valor])


def total(pedido):
    total = 0
    for i in pedido.itens:
        total = total + i[1] * i[2]
    return total


def calcular_desconto(tipo_cliente, total_pedido):
    if tipo_cliente == "V":
        d = total_pedido * 0.10
    elif tipo_cliente == "F":
        d = total_pedido * 0.20
    else:
        d = 0
    return d


def calcular_valor_a_pagar(pedido):
    return total(pedido) - calcular_desconto(pedido.tipo_cliente, total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def st_txt(s):
    if s == "A":
        return "aberto"
    elif s == "P":
        return "pago"
    else:
        return "cancelado"


def relatorio():
    for p in pedidos:
        print("Pedido", p.numero, "-", p.cliente_nome, "-", p.cidade)
        print("  status:", st_txt(p.get_status()))
        for i in p.itens:
            print("  ", i[1], "x", i[0], "= R$ %.2f" % (i[1] * i[2]))
        if len(p.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(p), calcular_desconto(p.tipo_cliente, total(p)), calcular_valor_a_pagar(p)))


def arrecadado():
    total = 0
    for p in pedidos:
        if p.get_status() == "P":
            total = total + calcular_valor_a_pagar(p)
    return total


def quantidade_abertos():
    q = 0
    for p in pedidos:
        if p.get_status() == "A":
            q = q + 1
    return q


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
a = novo_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(a, "Caderno", 2, 15.5)
add_item(a, "Caneta", 5, 2.5)

novo_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

c = novo_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(c, "Livro", 1, 89.5)

novo_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

e = novo_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

f = novo_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
add_item(f, "Fone", 1, 60.0)

novo_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

g = novo_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
add_item(g, "Fone", 2, 60.0)

print("pagar 1:", pagar(a))
print("pagar 3:", pagar(c))
print("pagar 5:", pagar(e))
print("pagar 6:", pagar(f))
print("cancelar 5:", cancelar(e))
print("cancelar 1:", cancelar(a))

relatorio()
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", quantidade_abertos())