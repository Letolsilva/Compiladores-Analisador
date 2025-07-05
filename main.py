import sys
import os
from analyzer.lexicalAnalysis import LexicalAnalysis
from analyzer.SyntacticAnalysis import SyntacticAnalysis
from analyzer.intermediate_code_generator import IntermediateCodeGenerator
from analyzer.semantic_analysis import SemanticAnalysis, SemanticError
from analyzer.execute import IntermediateCodeExecutor


def print_ast(node, indent=0):
    prefix = "  " * indent
    if node is None:
        print(f"{prefix}None")
        return
    node_type = node.__class__.__name__
    print(f"{prefix}{node_type}(", end="")
    attrs = [a for a in vars(node) if not a.startswith("_")]
    if not attrs:
        print(")")
        return
    print()
    for attr in attrs:
        value = getattr(node, attr)
        print(f"{prefix}  {attr}=", end="")
        if isinstance(value, list):
            print("[")
            for item in value:
                print_ast(item, indent + 2)
            print(f"{prefix}  ]")
        elif hasattr(value, "__class__") and value.__class__.__name__.endswith("Node"):
            print()
            print_ast(value, indent + 2)
        else:
            print(repr(value))
    print(f"{prefix})")


def processar_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return

    print(f"\nArquivo: {os.path.basename(caminho_arquivo)}\n")

    with open(caminho_arquivo, "r", encoding="latin-1") as file:
        source_code = file.read()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho-do-arquivo>")
    else:
        caminho_arquivo = sys.argv[1]
        processar_arquivo(caminho_arquivo)
        path = sys.argv[1]
        code = open(path, encoding="utf-8").read()
        lex = LexicalAnalysis(code)
        tokens = lex.analyze()
        for t in tokens:
            print(f"{t.token_type}({t.value})", end=" ")
        print()
        try:
            parser = SyntacticAnalysis(tokens)
            ast = parser.parse()
            print("Parsing successful!")

            print("\nAST:")
            print_ast(ast)

            try:
                semantic = SemanticAnalysis()
                semantic.analyze(ast)
                print("Semantic analysis successful!")
            except SemanticError as se:
                print(f"Erro semântico: {se}")
            gen = IntermediateCodeGenerator()
            gen.generate_from_ast(ast)
            gen.print_instructions()
        except SyntaxError as e:
            print(f"Erro sintático: {e}")

        print("\n\texecute\n\n")
        executor = IntermediateCodeExecutor(gen.instructions)
        executor.run()