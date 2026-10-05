
def validar_lista_tarefas(response):
    dados = response.json()

    assert isinstance(dados, list), "A resposta não é uma lista."

    assert any(
        isinstance(tarefa, dict) and "completed" in tarefa
        for tarefa in dados
    ), "Nenhuma tarefa possui a chave 'completed'."
