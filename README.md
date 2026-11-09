# TF-11 - Object Calisthenics

## 1. Normalização

A normalização consiste em armazenar cada informação em apenas um local do sistema. Na loja original, os dados da cliente Ana apareciam repetidos em mais de um pedido. Após a refatoração, foi criado um único objeto Cliente, e os pedidos passaram a apontar para ele, evitando duplicação de dados e inconsistências.

## 2. Obsessão por tipos primitivos

O CPF deixou de ser uma simples string e passou a ser uma classe responsável por validar seus próprios dados. Isso impede que valores inválidos circulem pelo sistema. O Dinheiro passou a armazenar centavos inteiros para evitar problemas de precisão causados pelo uso de números float em cálculos financeiros.

## 3. Diga, não pergunte

Antes da refatoração, o código consultava o status do pedido para decidir qual ação executar. Depois, as regras passaram a ficar dentro da própria classe Pedido através dos métodos pagar() e cancelar(). Isso melhora o encapsulamento e concentra as regras de negócio em um único lugar.

## 4. Fail First

A versão original possuía vários ifs aninhados, formando estruturas difíceis de ler e manter. Com a técnica Fail First, os casos inválidos são tratados imediatamente por retornos antecipados. Além disso, o uso de polimorfismo permitiu eliminar vários if/elif/else relacionados aos tipos de cliente.

## 5. Modularização

- Pessoa: representa os dados pessoais do cliente.
- Endereco: representa os dados de localização do cliente.
- Cliente: reúne pessoa, endereço e tipo de cliente.
- Produto: representa um produto da loja.
- ItemDoPedido: relaciona um produto e sua quantidade.
- ItensDoPedido: gerencia a coleção de itens de um pedido.
- Pedido: contém as regras de negócio relacionadas a um pedido.
- Pedidos: gerencia todos os pedidos cadastrados no sistema.
- Cpf: valida e representa um CPF.
- Email: valida e representa um e-mail.
- Cep: valida e representa um CEP.
- Dinheiro: representa valores monetários.
- Status: representa o estado atual de um pedido.
- TipoNormal: calcula descontos para clientes normais.
- TipoVip: calcula descontos para clientes VIP.
- TipoFuncionario: calcula descontos.
  