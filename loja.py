# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

from math import prod
import re


pedidos = []                      # todos os pedidos da loja: lista solta, global
class Cliente:
    def __init__(
        self,
        nome,
        cpf,
        email,
        rua,
        cidade,
        cep,
        tipo
    ):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = "A"
        

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
        cliente = Cliente(
            cliente_nome,
            cliente_cpf,
            cliente_email,
            rua,
            cidade,
            cep,
            tipo_cliente
        )
        p = Pedido(numero, cliente)
        pedidos.append(p)
        return p


def add_item(pedido, produto, quantidade, preco):
    produto = Produto(produto, preco)
    item = ItemDoPedido(produto, quantidade)
    pedido.itens.append(item)


def total(pedido):
    total = 0
    for i in pedido.itens:
        total = total + i.quantidade * i.produto.preco
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
    return total(pedido) - calcular_desconto(pedido.cliente.tipo, total(pedido))


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


def descrever_status(s):
    if s == "A":
        return "aberto"
    elif s == "P":
        return "pago"
    else:
        return "cancelado"


def relatorio():
    for p in pedidos:
        print("Pedido", p.numero, "-", p.cliente.nome, "-", p.cliente.cidade)
        print("  status:", descrever_status(p.get_status()))
        for i in p.itens:
            print("  ", i.quantidade, "x", i.produto.nome, "= R$ %.2f" % (i.quantidade * i.produto.preco))
        if len(p.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(p), calcular_desconto(p.cliente.tipo, total(p)), calcular_valor_a_pagar(p)))


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
A = novo_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(A, "Caderno", 2, 15.5)
add_item(A, "Caneta", 5, 2.5)

novo_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

C = novo_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(C, "Livro", 1, 89.5)

novo_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

E = novo_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

F = novo_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
add_item(F, "Fone", 1, 60.0)

novo_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

g = novo_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
add_item(g, "Fone", 2, 60.0)

print("pagar 1:", pagar(A))
print("pagar 3:", pagar(C))
print("pagar 5:", pagar(E))
print("pagar 6:", pagar(F))
print("cancelar 5:", cancelar(E))
print("cancelar 1:", cancelar(A))

relatorio()
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", quantidade_abertos())