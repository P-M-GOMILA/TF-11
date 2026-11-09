
from math import prod
import re


class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email


class Endereco:
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep


               
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
        self.pessoa = Pessoa(
            nome,
            Cpf(cpf),
            Email(email)
        )

        self.endereco = Endereco(
            rua,
            cidade,
            Cep(cep)
        )

        self.tipo = tipo

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class ItensDoPedido:
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def esta_vazia(self):
        return len(self.itens) == 0

    def calcular_total(self):
        total = 0

        for item in self.itens:
            total += (
                item.quantidade *
                item.produto.preco
            )

        return total

    def listar(self):
        return self.itens


class Pedidos:
    def __init__(self):
        self.pedidos = {}

    def adicionar(self, pedido):
        self.pedidos[pedido.numero] = pedido

    def listar(self):
        return self.pedidos.values()

pedidos = Pedidos()

class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")

        self.valor = valor


class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")

        if "@" not in valor:
            raise ValueError("email invalido")

        self.valor = valor


class Cep:
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")

        self.valor = valor


class Status:
    def __init__(self, codigo):
        self.codigo = codigo

    def descricao(self):
        if self.codigo == "A":
            return "aberto"

        if self.codigo == "P":
            return "pago"

        return "cancelado"

    def esta_aberto(self):
        return self.codigo == "A"


class Dinheiro:
    def __init__(self, valor):
        self.centavos = round(valor * 100)

    def somar(self, outro):
        return Dinheiro((self.centavos + outro.centavos) / 100)

    def subtrair(self, outro):
        return Dinheiro((self.centavos - outro.centavos) / 100)

    def multiplicar(self, quantidade):
        return Dinheiro((self.centavos * quantidade) / 100)

    def percentual(self, porcentagem):
        return Dinheiro(
            (self.centavos * porcentagem / 100) / 100
        )

    def __str__(self):
        return "R$ %.2f" % (self.centavos / 100)

    def valor(self):
        return self.centavos / 100
  
class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = itens = ItensDoPedido()    
        self.status = Status("A")
        

    def get_status(self):
        return self.status.codigo

    def set_status(self, v):
        self.status = Status(v)





def novo_pedido(n, nome, cpf, email, rua, cidade, cep, tipo):
    try:

        cliente = Cliente(
            nome,
            cpf,
            email,
            rua,
            cidade,
            cep,
            tipo
        )

        pedido = Pedido(n, cliente)

        pedidos.adicionar(pedido)

        return pedido

    except ValueError as erro:
        print("pedido", n, "recusado:", erro)
        return None

def add_item(pedido, produto, quantidade, preco):
    produto = Produto(produto, preco)
    item = ItemDoPedido(produto, quantidade)
    pedido.itens.adicionar(item)


def total(pedido):
    return pedido.itens.calcular_total()


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
        if not pedido.itens.esta_vazia():
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


def descrever_status(status):
    return status.descricao()

def relatorio():
    for p in pedidos.listar():
        print("Pedido", p.numero, "-", p.cliente.pessoa.nome, "-", p.cliente.endereco.cidade)
        print("  status:", descrever_status(p.status))
        for item in p.itens.listar():
            print("  ", item.quantidade, "x", item.produto.nome, "= R$ %.2f" % (item.quantidade * item.produto.preco))
        if not p.itens.esta_vazia():
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(p), calcular_desconto(p.cliente.tipo, total(p)), calcular_valor_a_pagar(p)))


def arrecadado():
    total = 0
    for p in pedidos.listar():
        if p.get_status() == "P":
            total = total + calcular_valor_a_pagar(p)
    return total


def quantidade_abertos():
    q = 0
    for p in pedidos.listar():
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