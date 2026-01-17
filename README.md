# 🛒 Sistema de Loja Virtual (CLI) — v1.0

Projeto final da disciplina de **Programação Orientada a Objetos (POO)**.

O sistema simula as principais operações de um **e-commerce via terminal (CLI)**, aplicando conceitos fundamentais de **Orientação a Objetos**, **persistência de dados em arquivos JSON** e **regras de negócio configuráveis**.

---

## 🚀 Guia de Instalação e Execução

### ✅ Pré-requisitos

* Python **3.8 ou superior**

---

### 📥 Clonando o repositório

```bash
git clone https://github.com/jefimdevfull/loja-final.git
```

---

### 📂 Acessando o projeto

```bash
cd loja-final
```

---

### ▶️ Executando o sistema

⚠️ **Importante:** navegue até a pasta `src` antes de executar o programa, pois os arquivos de configuração são carregados a partir dela.

```bash
cd src
python main.py
```

---

## 🧱 Arquitetura e Estrutura do Projeto

O sistema foi organizado em módulos para garantir **alta coesão**, **baixo acoplamento** e **manutenibilidade**.

```
loja-final/
│
├── src/                      # Código-fonte
│   ├── main.py               # Controller / View (menus e fluxos)
│   ├── produto.py            # Model: produtos e estoque
│   ├── cliente.py            # Model: clientes e validações
│   ├── carrinho.py           # Regra de negócio do carrinho
│   ├── pedido.py             # Model: pedidos e status
│   ├── pagamento.py          # Serviço: validação financeira
│   ├── frete.py              # Serviço: cálculo de frete via JSON
│   ├── excecoes.py           # Exceções personalizadas
│   ├── dados.py               # Persistência em arquivos JSON
│   └── settings.json         # Configurações externas (frete)
│
└── README.md                 # Documentação do projeto
```

---

## 🏆 Destaques Técnicos

O projeto atende aos critérios de avaliação por meio dos seguintes recursos:

### 🔹 Modelagem Orientada a Objetos

* Herança
* Encapsulamento (`@property`)
* Polimorfismo
* Composição entre classes

---

### 🔹 Qualidade de Código

* Uso de **Type Hints** em métodos críticos

Exemplo:

```python
def calcular_total(self) -> float:
```

---

### 🔹 Tratamento de Erros Semântico

Implementação de exceções personalizadas, como:

* `EstoqueInsuficienteErro`
* `PagamentoRecusadoErro`
* `LojaErro`

Evita o uso de exceções genéricas e melhora a legibilidade do código.

---

### 🔹 Configuração Externa

As regras de frete são carregadas dinamicamente a partir do arquivo:

```
settings.json
```

Permitindo:

* Alterar valores
* Ajustar prazos
* Incluir novos estados

Sem necessidade de modificar o código-fonte.

---

### 🔹 Persistência de Dados

Os dados são armazenados automaticamente em arquivos JSON:

* Clientes
* Produtos
* Pedidos

Garantindo persistência entre execuções do sistema.

---

## ✅ Funcionalidades do Sistema

### 📋 Cadastros (CRUD)

* Cadastro de clientes com:

  * Validação de CPF
  * Validação de e-mail
  * Controle de unicidade

* Cadastro de produtos com:

  * Controle de estoque
  * Validação de preço
  * Status ativo/inativo

---

### 🛒 Vendas

* Carrinho de compras dinâmico
* Adição e remoção de itens
* Cálculo automático de subtotal
* Verificação de estoque em tempo real

---

### 💳 Financeiro e Logística

* Cálculo de frete por UF
* Regras baseadas em configuração externa
* Processamento de pagamento
* Baixa automática no estoque

---

### 📊 Relatórios Gerenciais

* Faturamento total
* Ticket médio
* Análise de pedidos por status

---

## 👥 Equipe e Atribuições

### 👤 **Cícero Andreilson Santos Meneses**

**Responsabilidades:**

* Modelagem e implementação das classes de **Produto** e **Estoque**
* CRUD de produtos
* Validações de preço, estoque e SKU
* Apoio à persistência de dados

---

### 👤 **Cícero Jeferson Santos de Araújo**

**Responsabilidades:**

* Estrutura geral do projeto
* Implementação das classes de **Cliente** e **Endereço**
* Validações de CPF e e-mail
* Organização do repositório GitHub
* Documentação do sistema

---

### 👤 **Josley Vinícius Bastos da Silva**

**Responsabilidades:**

* Desenvolvimento do **Carrinho de Compras**
* Gerenciamento de itens
* Regras de adição, remoção e cálculo de subtotal

---

### 👤 **Lívia Maria de Oliveira Ferreira**

**Responsabilidades:**

* Implementação das classes de **Pedido** e **Pagamento**
* Controle de status do pedido
* Cálculo do valor total
* Aplicação de frete
* Registro de pagamentos

---

📌 **Projeto acadêmico desenvolvido para fins educacionais.**
