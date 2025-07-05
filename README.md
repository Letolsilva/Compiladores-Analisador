<h1 align="center" font-size="200em"><b>📘 Compilador Pascal--: Analisador Léxico, Sintático e Interpretador</b></h1>
<div align = "center" >

[![requirement](https://img.shields.io/badge/IDE-Visual%20Studio%20Code-informational)](https://code.visualstudio.com/docs/?dv=linux64_deb)
![Linguagem](https://img.shields.io/badge/Linguagem-Python-orange)
</div>

## ✒️ Descrição
Este projeto contempla as **etapas 1, 2, 3 e 4 do Trabalho Prático** da disciplina de Compiladores. Foram implementadas as funcionalidades de **análise léxica, análise sintática** e um **interpretador para uma linguagem intermediária**, simulando uma máquina virtual capaz de executar instruções em forma de tuplas.

## 🧠 Objetivo

Implementar um compilador parcial para Pascal--, realizando a leitura de um código-fonte `.pmm`, analisando sua validade léxica e sintática, e posteriormente **interpretando uma representação intermediária em tuplas**.

---

## 📦 Módulos do Projeto

### 🔹 Módulo 1 — Analisador Léxico

Identifica e classifica os **tokens** do código-fonte (palavras-chave, operadores, símbolos, etc.) e informa a **linha e coluna** de cada item.

**Exemplo de saída:**
```
Token: KEYWORD, Lexema: program, Linha: 1, Coluna: 1
Token: IDENTIFIER, Lexema: exemplo, Linha: 1, Coluna: 9
```

---

### 🔸 Módulo 2 — Analisador Sintático

Verifica se os tokens formam uma estrutura sintaticamente válida, com base na **gramática da linguagem Pascal--**.

**Exemplo de erro sintático:**
```
Erro sintático na linha 10, coluna 5: esperado 'end' antes de 'else'
```

---

### 🔹 Módulo 3 — Interpretador para Linguagem Intermediária

Foi implementado um **interpretador** para executar listas de **tuplas de instruções**, que simulam um código intermediário. Cada tupla representa uma operação como soma, subtração, atribuição, saltos condicionais, leitura, escrita, entre outras.

**Exemplo de instruções:**
```python
[
    ("=", "a", 10, None),
    ("=", "b", 5, None),
    ("+", "c", "a", "b"),
    ("CALL", "PRINT", "c", None)
]
```

**Funcionalidades suportadas:**
- Operações aritméticas, lógicas e relacionais
- Atribuições e operadores unários
- Saltos condicionais (`IF`) e incondicionais (`JUMP`)
- Labels e controle de fluxo
- Comandos de entrada (`SCAN`) e saída (`PRINT`)
- Tratamento de variáveis não inicializadas e labels inexistentes

---

## ⚙️ Como Executar

1. Certifique-se de estar na branch `Modulo3`:

```bash
git checkout Modulo3
```

2. Execute o interpretador com um arquivo `.py` contendo a lista de tuplas:

```bash
python main.py caminho/do/arquivo.py
```

Exemplo:

```bash
python main.py tests/teste_if.py
```

---

## ✅ Funcionalidades Gerais

- Análise léxica com identificação e erro de tokens
- Análise sintática com verificação da estrutura do código
- Execução de código intermediário baseado em tuplas
- Simulação real de programas com entrada e saída via terminal
- Modularização clara e legibilidade do código
- Detecção e mensagens claras de erro

---

## 📌 Conclusão

O projeto foi dividido em etapas para facilitar o aprendizado e a organização. Primeiro, implementamos a análise léxica, depois partimos para a análise sintática. Isso nos ajudou a compreender melhor como um compilador identifica e interpreta o código-fonte em etapas bem definidas.

Na terceira e quarta etapas, avançamos para a criação de um interpretador capaz de executar uma representação intermediária do código por meio de tuplas. Essa fase foi fundamental para entendermos o funcionamento interno de uma máquina virtual simples, desde o controle de fluxo até operações aritméticas, lógicas e de entrada/saída.

Também testamos o interpretador com programas completos escritos em Pascal--, que simulam a execução real: solicitando informações ao usuário com `readln` e exibindo os resultados com `writeln`. Isso tornou possível validar que a conversão para o código intermediário e sua execução no interpretador estão funcionando corretamente, inclusive com interação via terminal.

---

## Contato
<div>
 <p align="justify"> Anna Laura Moura Santana</p>
 <a href="https://t.me/annalaurams">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:nalauramoura@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>nalauramoura@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Jullia Fernandes</p>
 <a href="https://t.me/JulliaFernandes">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:julliacefet@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>julliacefet@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Letícia de Oliveira</p>
 <a href="https://t.me/letolsilva">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:letolsilva22@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>letolsilva22@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Thaissa Vitoria Guimarães Daldegan de Sousa</p>
 <a href="https://t.me/thaissadaldegan">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:thaissavivi@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>thaissavivi@gmail.com</i>
</a>
