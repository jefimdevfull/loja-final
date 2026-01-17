Markdown

# 🛒 Sistema de Loja Virtual (CLI) - v1.0

Projeto final da disciplina de Programação Orientada a Objetos (POO).
O software simula as operações essenciais de um e-commerce via terminal, aplicando conceitos de Orientação a Objetos, persistência de dados em arquivos e regras de negócio configuráveis.

---

## 🚀 Guia de Instalação e Execução

**Pré-requisitos:** Python 3.8 ou superior.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jefimdevfull/loja-final.git
Acesse a pasta do projeto:

cd loja-final
Execute o sistema: ⚠️ Importante: Navegue até a pasta src antes de rodar o arquivo principal para que as configurações sejam carregadas corretamente.


cd src
python main.py
📂 Arquitetura e Estrutura
O projeto foi organizado em módulos para garantir alta coesão e baixo acoplamento.

Plaintext

loja-final/
│
├── src/                  # Código Fonte
│   ├── main.py           # View/Controller (Menu, Fluxos e Relatórios)
│   ├── produto.py        # Model (Regras de Produto e Estoque)
│   ├── cliente.py        # Model (Dados de Cliente e Validações)
│   ├── carrinho.py       # Lógica de Negócio (Composição de Itens)
│   ├── pedido.py         # Model (Processamento de Venda e Status)
│   ├── pagamento.py      # Serviço (Validação Financeira)
│   ├── frete.py          # Serviço (Cálculo Logístico via JSON)
│   ├── excecoes.py       # Tratamento de Erros Personalizados
│   ├── dados.py          # Persistência (Leitura/Escrita em JSON)
│   └── settings.json     # Configurações Externas (Tabela de Frete)
│
└── README.md             # Documentação do Projeto
🏆 Destaques Técnicos (Critérios de Avaliação)
Para atender aos requisitos de excelência, o sistema implementa:

Modelagem OO Robusta: Uso de Herança, Encapsulamento (@property), Polimorfismo e Composição.

Qualidade de Código (Type Hints): Tipagem estática em métodos críticos (ex: def calcular(self) -> float:) para maior segurança e legibilidade.

Tratamento de Erros Semântico: Implementação de Exceções Customizadas (EstoqueInsuficienteErro, PagamentoRecusadoErro, LojaErro) em vez de erros genéricos.

Configuração Externa: As regras de frete (preços e prazos por estado) são lidas dinamicamente do arquivo settings.json, permitindo alterações sem mexer no código.

Persistência: Dados de Clientes, Produtos e Pedidos são persistidos automaticamente em JSON.

✅ Funcionalidades do Sistema
Cadastros (CRUD):

Gestão de Clientes com validação de CPF e unicidade.

Gestão de Produtos com controle de estoque e status ativo/inativo.

Vendas:

Carrinho de compras dinâmico.

Verificação de disponibilidade de estoque em tempo real.

Financeiro e Logística:

Cálculo de frete parametrizado por UF.

Pagamento com baixa automática no estoque.

Relatórios Gerenciais:

Monitoramento de Faturamento.

Cálculo de Ticket Médio.

Análise de Pedidos por Status.

👥 Equipe e Atribuições
CICERO ANDREILSON SANTOS MENESES

Responsabilidade: Modelagem e implementação das classes relacionadas a Produtos e Estoque, incluindo CRUD de produtos, validações de atributos (preço, estoque, SKU) e métodos especiais. Atuará também no apoio à persistência de dados.

CICERO JEFERSON SANTOS DE ARAÚJO

Responsabilidade: Estrutura geral do projeto e implementação das classes de Cliente e Endereço, com validações de email, CPF e unicidade. Responsável pela organização do repositório GitHub e documentação inicial.

JOSLEY VINICIUS BASTOS DA SILVA

Responsabilidade: Desenvolvimento das classes relacionadas ao Carrinho de Compras e Itens do Carrinho, incluindo regras de negócio para adição/remoção de itens e cálculo de subtotal.

LIVIA MARIA DE OLIVEIRA FERREIRA

Responsabilidade: Implementação das classes de Pedido e Pagamento, contemplando estados do pedido, cálculo de total, aplicação de frete e registro de pagamentos.