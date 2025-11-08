from search import search_prompt

def main():
    print("Olá, sou seu assistente financeiro, faça sua pergunta! (digite 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ("exit", "sair", "quit"):
            print("Foi um prazer te ajudar. Até logo!")
            break

        chain = search_prompt(user_input)
        print("Assistente: ", chain, "\n")

    if not chain:
        print("Não conseguimos inicializar corretamente. Verifique os logs de erro.")
        return
    
    pass

if __name__ == "__main__":
    main()