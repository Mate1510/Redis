import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def adicionar_tarefa():
    task = r.incr('task')
    description = input("Informe a descrição da tarefa: ")

    r.set(f'task_{task}', description)
    print(f"Tarefa adicionada com ID: {task}.")


def listar_tarefas():
    taskText = r.get('task')

    if taskText is None:
        print("Nenhuma tarefa encontrada.")
        return

    task = int(taskText)

    if task == 0:
        print("Nenhuma tarefa encontrada.")
        return

    for i in range(1, task + 1):
        print(f"ID: {i} - Descrição: {r.get(f'task_{i}').decode('utf-8')}")


def remover_tarefa():
    task = input("Informe o ID da tarefa a ser removida: ")

    if r.delete(f'task_{task}'):
        print(f"Tarefa com ID {task} foi removida.")
    else:
        print(f"Nenhuma tarefa encontrada com ID {task}")


if __name__ == "__main__":
    while True:
        print("\nLista de Tarefas")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Remover Tarefa")
        print("4. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            adicionar_tarefa()
        elif opcao == '2':
            listar_tarefas()
        elif opcao == '3':
            remover_tarefa()
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("\n\nOpção inválida! Tente novamente.")
