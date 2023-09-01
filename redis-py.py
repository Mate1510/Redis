import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
except redis.ConnectionError:
    print("Não foi possível conectar ao servidor Redis.")
    exit(1)


def adicionar_tarefa():
    try:
        task = r.incr('task')
        description = input("Informe a descrição da tarefa: ")
        r.set(f'task_{task}', description.encode('utf-8'))
        print(f"Tarefa adicionada com ID: {task}.")
    except redis.RedisError:
        print("Erro ao adicionar tarefa.")


def listar_tarefas():
    try:
        task_count = int(r.get('task') or 0)

        if task_count == 0:
            print("Nenhuma tarefa encontrada.")
            return

        for i in range(1, task_count + 1):
            description = r.get(f'task_{i}')
            if description:
                print(f"ID: {i} - Descrição: {description.decode('utf-8')}")
    except redis.RedisError:
        print("Erro ao listar tarefas.")


def atualizar_tarefa():
    try:
        task_id = input("Informe o ID da tarefa a ser atualizada: ")

        if r.exists(f'task_{task_id}'):
            new_description = input("Informe a nova descrição: ")
            r.set(f'task_{task_id}', new_description.encode('utf-8'))
            print(f"Tarefa com ID {task_id} foi atualizada.")
        else:
            print(f"Nenhuma tarefa encontrada com ID {task_id}")
    except redis.RedisError:
        print("Erro ao atualizar tarefa.")


def remover_tarefa():
    try:
        task_id = input("Informe o ID da tarefa a ser removida: ")

        if r.delete(f'task_{task_id}'):
            print(f"Tarefa com ID {task_id} foi removida.")
        else:
            print(f"Nenhuma tarefa encontrada com ID {task_id}")
    except redis.RedisError:
        print("Erro ao remover tarefa.")


if __name__ == "__main__":
    while True:
        print("\nLista de Tarefas")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Atualizar Tarefa")
        print("4. Remover Tarefa")
        print("5. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            adicionar_tarefa()
        elif opcao == '2':
            listar_tarefas()
        elif opcao == '3':
            atualizar_tarefa()
        elif opcao == '4':
            remover_tarefa()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("\n\nOpção inválida! Tente novamente.")
