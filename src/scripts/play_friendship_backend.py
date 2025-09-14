#!/usr/bin/env python3
"""
Script playground para testar os casos de uso de amizade.

Este script:
1. Reseta o banco de dados (remove e recria)
2. Monta o app com um banco separado
3. Cria alguns usuários
4. Executa cada caso de uso de friendship
5. Imprime resultados e captura exceções esperadas

==============================================================================
PROMPT PARA REPLICAR ESTE FORMATO COM IA:
==============================================================================

"Crie um script playground Python para testar casos de uso de [MÓDULO/FUNCIONALIDADE].

Estrutura desejada:
1. Shebang #!/usr/bin/env python3
2. Docstring explicando o que o script faz
3. Imports organizados (externos primeiro, depois internos)
4. Função print_separator(title) para organizar a saída visual
5. Funções separadas para cada grupo de testes (ex: create_test_data, test_use_case_1, etc.)
6. Função main() que orquestra todos os testes
7. if __name__ == "__main__": main()

Padrões de saída:
- Use ✓ para sucessos
- Use ⚠ para erros esperados/tratados
- Use ✗ para erros inesperados
- Use separadores visuais com = (60 chars)
- Organize testes em seções com print_separator()

Tratamento de erros:
- Capture exceções específicas esperadas
- Mostre mensagens clara sobre o que está sendo testado
- Continue execução mesmo com erros (quando apropriado)

Reset de dados:
- Remova/recrie banco ou dados de teste no início
- Garanta ambiente limpo para cada execução"

==============================================================================
"""

import os
import sys
from pathlib import Path

from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteInputDto,
)
from friendship.application.delete_friendship_use_case import DeleteFriendshipInputDto
from friendship.application.errors import (
    FriendshipAlreadyExistsError,
    FriendshipNotFoundError,
    RequestedNotFoundError,
    RequesterNotFoundError,
)
from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsInputDto,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteInputDto,
)
from friendship.domain.errors import FriendshipAlreadyAcceptedError
from shared.composition_root import build_application
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole

# Adiciona o diretório src ao path para imports
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))


def print_separator(title: str):
    """Imprime um separador visual para organizar a saída."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print("=" * 60)


def reset_database(db_path: str):
    """Remove o banco de dados existente para garantir ambiente limpo."""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Banco de dados removido: {db_path}")
    else:
        print(f"✓ Banco de dados não existia: {db_path}")


def create_test_users(app):
    """Cria usuários de teste."""
    print_separator("CRIANDO USUÁRIOS DE TESTE")

    users = []
    users_data = [
        ("Alice Silva", "alice@email.com", "password123", UserRole.CLIENT),
        ("Bob Santos", "bob@email.com", "password456", UserRole.CLIENT),
        ("Carlos Lima", "carlos@email.com", "password789", UserRole.CLIENT),
        ("Diana Costa", "diana@email.com", "password000", UserRole.CLIENT),
    ]

    for name, email, password, role in users_data:
        try:
            input_dto = CreateUserInputDto(
                name=name, email=email, password=password, role=role
            )
            user = app.create_user_use_case.execute(input_dto)
            users.append(user)
            print(f"✓ Usuário criado: {user.name} ({user.email}) - Role: {user.role}")
        except Exception as e:
            print(f"✗ Erro ao criar usuário {email}: {e}")

    return users


def test_send_friendship_invites(app, users):
    """Testa o envio de convites de amizade."""
    print_separator("TESTANDO ENVIO DE CONVITES DE AMIZADE")

    friendship_invites = []

    # Casos de sucesso
    invite_pairs = [
        (users[0].email, users[1].email),  # Alice -> Bob
        (users[2].email, users[3].email),  # Carlos -> Diana
        (users[1].email, users[2].email),  # Bob -> Carlos
    ]

    for requester_email, requested_email in invite_pairs:
        try:
            input_dto = SendFriendshipInviteInputDto(
                requester_client_email=requester_email,
                requested_client_email=requested_email,
            )
            friendship = app.send_friendship_invite_use_case.execute(input_dto)
            friendship_invites.append(friendship)
            print(
                f"✓ Convite enviado: {requester_email} -> {requested_email} (ID: {friendship.id})"
            )
        except (
            FriendshipAlreadyExistsError,
            RequestedNotFoundError,
            RequesterNotFoundError,
        ) as e:
            print(f"⚠ Erro esperado: {e}")
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")

    # Casos de erro esperados
    print("\n--- Testando casos de erro ---")

    # Tentativa de convite duplicado
    try:
        duplicate_dto = SendFriendshipInviteInputDto(
            requester_client_email=users[0].email, requested_client_email=users[1].email
        )
        app.send_friendship_invite_use_case.execute(duplicate_dto)
        print("✗ Deveria ter gerado erro de convite duplicado")
    except FriendshipAlreadyExistsError as e:
        print(f"✓ Erro esperado capturado: {e}")

    # Usuário inexistente como solicitante
    try:
        invalid_dto = SendFriendshipInviteInputDto(
            requester_client_email="inexistente@email.com",
            requested_client_email=users[0].email,
        )
        app.send_friendship_invite_use_case.execute(invalid_dto)
        print("✗ Deveria ter gerado erro de solicitante não encontrado")
    except RequesterNotFoundError as e:
        print(f"✓ Erro esperado capturado: {e}")

    # Usuário inexistente como solicitado
    try:
        invalid_dto = SendFriendshipInviteInputDto(
            requester_client_email=users[0].email,
            requested_client_email="inexistente@email.com",
        )
        app.send_friendship_invite_use_case.execute(invalid_dto)
        print("✗ Deveria ter gerado erro de solicitado não encontrado")
    except RequestedNotFoundError as e:
        print(f"✓ Erro esperado capturado: {e}")

    return friendship_invites


def test_list_friendships(app, users):
    """Testa a listagem de amizades."""
    print_separator("TESTANDO LISTAGEM DE AMIZADES")

    try:
        # Lista todas as amizades
        input_dto = ListFriendshipsInputDto(page=1, size=10)
        friendships, total = app.list_friendships_use_case.execute(input_dto)

        print(f"Total de amizades encontradas: {total}")
        for friendship in friendships:
            print(f"ID: {friendship.id}")
            print(
                f"  Solicitante: {friendship.requester_name} ({friendship.requester_email})"
            )
            print(
                f"  Solicitado: {friendship.requested_name} ({friendship.requested_email})"
            )
            print(f"  Status: {friendship.status}")
            print(f"  Aceito em: {friendship.accepted_at}")
            print("  ---")

        # Testa filtro por participante
        if users:
            print(f"\n--- Filtrando amizades do usuário {users[0].name} ---")
            filter_dto = ListFriendshipsInputDto(
                page=1, size=10, participant_client_id=users[0].id
            )
            user_friendships, user_total = app.list_friendships_use_case.execute(
                filter_dto
            )
            print(f"Amizades do usuário {users[0].name}: {user_total}")

    except Exception as e:
        print(f"✗ Erro ao listar amizades: {e}")


def test_accept_friendship_invites(app, friendship_invites):
    """Testa a aceitação de convites de amizade."""
    print_separator("TESTANDO ACEITAÇÃO DE CONVITES")

    accepted_friendships = []

    # Aceita alguns convites
    for i, friendship in enumerate(
        friendship_invites[:2]
    ):  # Aceita apenas os 2 primeiros
        try:
            input_dto = AcceptFriendshipInviteInputDto(friendship_id=friendship.id)
            accepted_friendship = app.accept_friendship_invite_use_case.execute(
                input_dto
            )
            accepted_friendships.append(accepted_friendship)
            print(f"✓ Convite aceito: ID {friendship.id}")
            print(f"  Status: {accepted_friendship.status.value}")
            print(f"  Aceito em: {accepted_friendship.accepted_at}")
        except FriendshipAlreadyAcceptedError as e:
            print(f"⚠ Erro esperado: {e}")
        except FriendshipNotFoundError as e:
            print(f"⚠ Erro esperado: {e}")
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")

    # Testa casos de erro
    print("\n--- Testando casos de erro ---")

    # Tentativa de aceitar convite já aceito
    if accepted_friendships:
        try:
            duplicate_dto = AcceptFriendshipInviteInputDto(
                friendship_id=accepted_friendships[0].id
            )
            app.accept_friendship_invite_use_case.execute(duplicate_dto)
            print("✗ Deveria ter gerado erro de convite já aceito")
        except FriendshipAlreadyAcceptedError as e:
            print(f"✓ Erro esperado capturado: {e}")

    # Tentativa de aceitar convite inexistente
    try:
        invalid_dto = AcceptFriendshipInviteInputDto(friendship_id=99999)
        app.accept_friendship_invite_use_case.execute(invalid_dto)
        print("✗ Deveria ter gerado erro de convite não encontrado")
    except FriendshipNotFoundError as e:
        print(f"✓ Erro esperado capturado: {e}")

    return accepted_friendships


def test_delete_friendships(app, friendship_invites):
    """Testa a exclusão de amizades."""
    print_separator("TESTANDO EXCLUSÃO DE AMIZADES")

    # Deleta a última amizade (que não foi aceita)
    if len(friendship_invites) >= 3:
        try:
            friendship_to_delete = friendship_invites[-1]  # Última amizade
            input_dto = DeleteFriendshipInputDto(friendship_id=friendship_to_delete.id)
            deleted_friendship = app.delete_friendship_use_case.execute(input_dto)
            print(f"✓ Amizade deletada: ID {deleted_friendship.id}")
        except FriendshipNotFoundError as e:
            print(f"⚠ Erro esperado: {e}")
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")

    # Testa casos de erro
    print("\n--- Testando casos de erro ---")

    # Tentativa de deletar amizade inexistente
    try:
        invalid_dto = DeleteFriendshipInputDto(friendship_id=99999)
        app.delete_friendship_use_case.execute(invalid_dto)
        print("✗ Deveria ter gerado erro de amizade não encontrada")
    except FriendshipNotFoundError as e:
        print(f"✓ Erro esperado capturado: {e}")


def main():
    """Função principal do script."""
    print_separator("INICIANDO PLAYGROUND DE AMIZADES")

    # Monta o app com banco separado
    db_path = "data/friendship_play.db"

    # Reset do banco para garantir ambiente limpo
    print("Resetando banco de dados...")
    reset_database(db_path)

    print(f"Inicializando aplicação com banco: {db_path}")

    try:
        app = build_application(db_path)
        print("✓ Aplicação inicializada com sucesso")

        # 1. Criar usuários de teste
        users = create_test_users(app)

        if not users:
            print("✗ Nenhum usuário foi criado. Encerrando...")
            return

        # 2. Testar envio de convites
        friendship_invites = test_send_friendship_invites(app, users)

        # 3. Testar listagem de amizades (antes das aceitações)
        test_list_friendships(app, users)

        # 4. Testar aceitação de convites
        test_accept_friendship_invites(app, friendship_invites)

        # 5. Testar listagem de amizades (após as aceitações)
        print_separator("LISTAGEM APÓS ACEITAÇÕES")
        test_list_friendships(app, users)

        # 6. Testar exclusão de amizades
        test_delete_friendships(app, friendship_invites)

        # 7. Listagem final
        print_separator("LISTAGEM FINAL")
        test_list_friendships(app, users)

        print_separator("PLAYGROUND CONCLUÍDO COM SUCESSO")

    except Exception as e:
        print(f"✗ Erro fatal na aplicação: {e}")


if __name__ == "__main__":
    main()
