import asyncio
import time

import httpx
import pytest

from api_pagamentos import app


@pytest.mark.asyncio
@pytest.mark.parametrize("quantidade_requisicoes", [5, 20, 50])
async def test_performance_pagamentos(quantidade_requisicoes):

    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        async def fazer_requisicao():
            response = await client.get("/processar")
            return response

        inicio = time.perf_counter()

        respostas = await asyncio.gather(
            *[
                fazer_requisicao()
                for _ in range(quantidade_requisicoes)
            ]
        )

        tempo_total = time.perf_counter() - inicio

    # Todos os status devem ser 200
    assert all(
        response.status_code == 200 # valores de status HTTP
        for response in respostas
    )

    # Todas as respostas devem indicar pagamento aprovado
    assert all(
        response.json()["status"] == "pagamento_aprovado"
        for response in respostas
    )

    # Mesmo com 50 requisições simultâneas,
    # o processamento deve terminar antes de 3.5 segundos.
    assert tempo_total < 3.5