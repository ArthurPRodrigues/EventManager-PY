#!/usr/bin/env python3
"""
Playground script to run the Friendship Manager GUI interface with real backend integration.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteInputDto,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteInputDto,
)
from friendship.ui.friendship_manager_gui import FriendshipManagerGUI
from shared.composition_root import build_application
from shared.ui.navigation_manager import NavigationManager
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole


def setup_mock_data(app):
    """Cria dados mock usando os casos de uso para testar a interface"""
    print("📊 Criando dados mock...")

    try:
        # Criar usuários mock - quantidade suficiente para testar paginação (dobrado)
        users_data = [
            {
                "name": "João Silva",
                "email": "joao@email.com",
                "password": "123456",
            },  # ID será 1 (usuário atual)
            {
                "name": "Maria Santos",
                "email": "maria@email.com",
                "password": "123456",
            },  # ID será 2
            {
                "name": "Pedro Oliveira",
                "email": "pedro@email.com",
                "password": "123456",
            },  # ID será 3
            {
                "name": "Ana Costa",
                "email": "ana@email.com",
                "password": "123456",
            },  # ID será 4
            {
                "name": "Carlos Lima",
                "email": "carlos@email.com",
                "password": "123456",
            },  # ID será 5
            {
                "name": "Julia Pereira",
                "email": "julia@email.com",
                "password": "123456",
            },  # ID será 6
            {
                "name": "Roberto Souza",
                "email": "roberto@email.com",
                "password": "123456",
            },  # ID será 7
            {
                "name": "Fernanda Alves",
                "email": "fernanda@email.com",
                "password": "123456",
            },  # ID será 8
            {
                "name": "Lucas Mendes",
                "email": "lucas@email.com",
                "password": "123456",
            },  # ID será 9
            {
                "name": "Camila Rocha",
                "email": "camila@email.com",
                "password": "123456",
            },  # ID será 10
            {
                "name": "Bruno Ferreira",
                "email": "bruno@email.com",
                "password": "123456",
            },  # ID será 11
            {
                "name": "Larissa Martins",
                "email": "larissa@email.com",
                "password": "123456",
            },  # ID será 12
            {
                "name": "Rafael Cardoso",
                "email": "rafael@email.com",
                "password": "123456",
            },  # ID será 13
            {
                "name": "Mariana Silva",
                "email": "mariana@email.com",
                "password": "123456",
            },  # ID será 14
            {
                "name": "Diego Santos",
                "email": "diego@email.com",
                "password": "123456",
            },  # ID será 15
            {
                "name": "Isabela Lima",
                "email": "isabela@email.com",
                "password": "123456",
            },  # ID será 16
            {
                "name": "Thiago Costa",
                "email": "thiago@email.com",
                "password": "123456",
            },  # ID será 17
            {
                "name": "Natália Pereira",
                "email": "natalia@email.com",
                "password": "123456",
            },  # ID será 18
            {
                "name": "Guilherme Alves",
                "email": "guilherme@email.com",
                "password": "123456",
            },  # ID será 19
            {
                "name": "Bianca Souza",
                "email": "bianca@email.com",
                "password": "123456",
            },  # ID será 20
            {
                "name": "Mateus Oliveira",
                "email": "mateus@email.com",
                "password": "123456",
            },  # ID será 21
            {
                "name": "Vanessa Mendes",
                "email": "vanessa@email.com",
                "password": "123456",
            },  # ID será 22
            {
                "name": "André Rocha",
                "email": "andre@email.com",
                "password": "123456",
            },  # ID será 23
            {
                "name": "Carolina Ferreira",
                "email": "carolina@email.com",
                "password": "123456",
            },  # ID será 24
            {
                "name": "Felipe Martins",
                "email": "felipe@email.com",
                "password": "123456",
            },  # ID será 25
            # Novos usuários adicionados (dobrado)
            {
                "name": "Rodrigo Silva",
                "email": "rodrigo@email.com",
                "password": "123456",
            },  # ID será 26
            {
                "name": "Amanda Santos",
                "email": "amanda@email.com",
                "password": "123456",
            },  # ID será 27
            {
                "name": "Gabriel Oliveira",
                "email": "gabriel@email.com",
                "password": "123456",
            },  # ID será 28
            {
                "name": "Letícia Costa",
                "email": "leticia@email.com",
                "password": "123456",
            },  # ID será 29
            {
                "name": "Vinícius Lima",
                "email": "vinicius@email.com",
                "password": "123456",
            },  # ID será 30
            {
                "name": "Patrícia Pereira",
                "email": "patricia@email.com",
                "password": "123456",
            },  # ID será 31
            {
                "name": "Eduardo Souza",
                "email": "eduardo@email.com",
                "password": "123456",
            },  # ID será 32
            {
                "name": "Juliana Alves",
                "email": "juliana@email.com",
                "password": "123456",
            },  # ID será 33
            {
                "name": "Márcio Mendes",
                "email": "marcio@email.com",
                "password": "123456",
            },  # ID será 34
            {
                "name": "Priscila Rocha",
                "email": "priscila@email.com",
                "password": "123456",
            },  # ID será 35
            {
                "name": "Fabiano Ferreira",
                "email": "fabiano@email.com",
                "password": "123456",
            },  # ID será 36
            {
                "name": "Adriana Martins",
                "email": "adriana@email.com",
                "password": "123456",
            },  # ID será 37
            {
                "name": "Leandro Cardoso",
                "email": "leandro@email.com",
                "password": "123456",
            },  # ID será 38
            {
                "name": "Cristiane Silva",
                "email": "cristiane@email.com",
                "password": "123456",
            },  # ID será 39
            {
                "name": "Renato Santos",
                "email": "renato@email.com",
                "password": "123456",
            },  # ID será 40
            {
                "name": "Simone Lima",
                "email": "simone@email.com",
                "password": "123456",
            },  # ID será 41
            {
                "name": "Marcelo Costa",
                "email": "marcelo@email.com",
                "password": "123456",
            },  # ID será 42
            {
                "name": "Elaine Pereira",
                "email": "elaine@email.com",
                "password": "123456",
            },  # ID será 43
            {
                "name": "Alexandre Alves",
                "email": "alexandre@email.com",
                "password": "123456",
            },  # ID será 44
            {
                "name": "Daniela Souza",
                "email": "daniela@email.com",
                "password": "123456",
            },  # ID será 45
            {
                "name": "Leonardo Oliveira",
                "email": "leonardo@email.com",
                "password": "123456",
            },  # ID será 46
            {
                "name": "Karina Mendes",
                "email": "karina@email.com",
                "password": "123456",
            },  # ID será 47
            {
                "name": "Fábio Rocha",
                "email": "fabio@email.com",
                "password": "123456",
            },  # ID será 48
            {
                "name": "Tatiana Ferreira",
                "email": "tatiana@email.com",
                "password": "123456",
            },  # ID será 49
            {
                "name": "Gustavo Martins",
                "email": "gustavo@email.com",
                "password": "123456",
            },  # ID será 50
        ]

        created_users = []
        for user_data in users_data:
            try:
                user_dto = CreateUserInputDto(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=user_data["password"],
                    role=UserRole.CLIENT,
                )
                user = app.create_user_use_case.execute(user_dto)
                created_users.append(user)
                print(f"  ✅ Usuário criado: {user.name} (ID: {user.id})")
            except Exception as e:
                print(f"  ⚠️  Usuário {user_data['name']} já existe ou erro: {e}")

        # Criar amizades COM o usuário atual (João - ID=1) - dobrado para testar paginação
        friendships_with_current_user = [
            {
                "requester": "joao@email.com",
                "requested": "maria@email.com",
            },  # João → Maria
            {
                "requester": "pedro@email.com",
                "requested": "joao@email.com",
            },  # Pedro → João
            {"requester": "ana@email.com", "requested": "joao@email.com"},  # Ana → João
            {
                "requester": "joao@email.com",
                "requested": "carlos@email.com",
            },  # João → Carlos
            {
                "requester": "julia@email.com",
                "requested": "joao@email.com",
            },  # Julia → João
            {
                "requester": "joao@email.com",
                "requested": "roberto@email.com",
            },  # João → Roberto
            {
                "requester": "fernanda@email.com",
                "requested": "joao@email.com",
            },  # Fernanda → João
            {
                "requester": "joao@email.com",
                "requested": "lucas@email.com",
            },  # João → Lucas
            {
                "requester": "camila@email.com",
                "requested": "joao@email.com",
            },  # Camila → João
            {
                "requester": "joao@email.com",
                "requested": "bruno@email.com",
            },  # João → Bruno
            {
                "requester": "larissa@email.com",
                "requested": "joao@email.com",
            },  # Larissa → João
            {
                "requester": "joao@email.com",
                "requested": "rafael@email.com",
            },  # João → Rafael
            {
                "requester": "mariana@email.com",
                "requested": "joao@email.com",
            },  # Mariana → João
            {
                "requester": "joao@email.com",
                "requested": "diego@email.com",
            },  # João → Diego
            {
                "requester": "isabela@email.com",
                "requested": "joao@email.com",
            },  # Isabela → João
            {
                "requester": "joao@email.com",
                "requested": "thiago@email.com",
            },  # João → Thiago
            {
                "requester": "natalia@email.com",
                "requested": "joao@email.com",
            },  # Natália → João
            {
                "requester": "joao@email.com",
                "requested": "guilherme@email.com",
            },  # João → Guilherme
            # Novos amigos adicionados (dobrado)
            {
                "requester": "bianca@email.com",
                "requested": "joao@email.com",
            },  # Bianca → João
            {
                "requester": "joao@email.com",
                "requested": "mateus@email.com",
            },  # João → Mateus
            {
                "requester": "vanessa@email.com",
                "requested": "joao@email.com",
            },  # Vanessa → João
            {
                "requester": "joao@email.com",
                "requested": "andre@email.com",
            },  # João → André
            {
                "requester": "carolina@email.com",
                "requested": "joao@email.com",
            },  # Carolina → João
            {
                "requester": "joao@email.com",
                "requested": "felipe@email.com",
            },  # João → Felipe
            {
                "requester": "rodrigo@email.com",
                "requested": "joao@email.com",
            },  # Rodrigo → João
            {
                "requester": "joao@email.com",
                "requested": "amanda@email.com",
            },  # João → Amanda
            {
                "requester": "gabriel@email.com",
                "requested": "joao@email.com",
            },  # Gabriel → João
            {
                "requester": "joao@email.com",
                "requested": "leticia@email.com",
            },  # João → Letícia
            {
                "requester": "vinicius@email.com",
                "requested": "joao@email.com",
            },  # Vinícius → João
            {
                "requester": "joao@email.com",
                "requested": "patricia@email.com",
            },  # João → Patrícia
            {
                "requester": "eduardo@email.com",
                "requested": "joao@email.com",
            },  # Eduardo → João
            {
                "requester": "joao@email.com",
                "requested": "juliana@email.com",
            },  # João → Juliana
            {
                "requester": "marcio@email.com",
                "requested": "joao@email.com",
            },  # Márcio → João
            {
                "requester": "joao@email.com",
                "requested": "priscila@email.com",
            },  # João → Priscila
            {
                "requester": "fabiano@email.com",
                "requested": "joao@email.com",
            },  # Fabiano → João
            {
                "requester": "joao@email.com",
                "requested": "adriana@email.com",
            },  # João → Adriana
        ]

        # Criar amizades SEM relação com o usuário atual (para garantir que não aparecem na lista) - dobrado
        friendships_without_current_user = [
            {
                "requester": "leandro@email.com",
                "requested": "cristiane@email.com",
            },  # Leandro → Cristiane
            {
                "requester": "renato@email.com",
                "requested": "simone@email.com",
            },  # Renato → Simone
            {
                "requester": "marcelo@email.com",
                "requested": "elaine@email.com",
            },  # Marcelo → Elaine
            {
                "requester": "alexandre@email.com",
                "requested": "daniela@email.com",
            },  # Alexandre → Daniela
            {
                "requester": "leonardo@email.com",
                "requested": "karina@email.com",
            },  # Leonardo → Karina
            {
                "requester": "fabio@email.com",
                "requested": "tatiana@email.com",
            },  # Fábio → Tatiana
            {
                "requester": "gustavo@email.com",
                "requested": "rodrigo@email.com",
            },  # Gustavo → Rodrigo
            {
                "requester": "maria@email.com",
                "requested": "pedro@email.com",
            },  # Maria → Pedro (sem João)
            {
                "requester": "ana@email.com",
                "requested": "carlos@email.com",
            },  # Ana → Carlos (sem João)
            {
                "requester": "amanda@email.com",
                "requested": "gabriel@email.com",
            },  # Amanda → Gabriel
        ]

        print("\n🔗 Criando amizades COM o usuário atual (devem aparecer na lista):")
        for friendship_data in friendships_with_current_user:
            try:
                # Enviar convite
                invite_dto = SendFriendshipInviteInputDto(
                    requester_client_email=friendship_data["requester"],
                    requested_client_email=friendship_data["requested"],
                )
                friendship = app.send_friendship_invite_use_case.execute(invite_dto)
                print(
                    f"  📤 Convite enviado: {friendship_data['requester']} → {friendship_data['requested']}"
                )

                # Aceitar o convite
                accept_dto = AcceptFriendshipInviteInputDto(friendship_id=friendship.id)
                app.accept_friendship_invite_use_case.execute(accept_dto)
                print(f"  ✅ Convite aceito: ID {friendship.id}")

            except Exception as e:
                print(f"  ⚠️  Erro ao criar/aceitar amizade: {e}")

        print(
            "\n🚫 Criando amizades SEM o usuário atual (NÃO devem aparecer na lista):"
        )
        for friendship_data in friendships_without_current_user:
            try:
                # Enviar convite
                invite_dto = SendFriendshipInviteInputDto(
                    requester_client_email=friendship_data["requester"],
                    requested_client_email=friendship_data["requested"],
                )
                friendship = app.send_friendship_invite_use_case.execute(invite_dto)
                print(
                    f"  📤 Convite enviado: {friendship_data['requester']} → {friendship_data['requested']}"
                )

                # Aceitar o convite
                accept_dto = AcceptFriendshipInviteInputDto(friendship_id=friendship.id)
                app.accept_friendship_invite_use_case.execute(accept_dto)
                print(f"  ✅ Convite aceito: ID {friendship.id}")

            except Exception as e:
                print(f"  ⚠️  Erro ao criar/aceitar amizade: {e}")

        print("\n📊 Dados mock criados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar dados mock: {e}")


def main():
    print("🚀 Starting Friendship Manager GUI with Backend Integration...")
    print("📋 This version uses real backend functionality!")
    print("🎯 Testing friendship listing with mock data")
    print("-" * 70)

    try:
        # Build application with all dependencies
        app = build_application()

        # Setup mock data for testing
        setup_mock_data(app)

        print("-" * 70)
        print("🖥️  Opening Friendship Manager GUI with NavigationManager...")

        # Create NavigationManager and start with FriendshipManagerGUI
        navigator = NavigationManager(use_cases=app)
        navigator.push_screen(FriendshipManagerGUI)

        print("✅ GUI closed successfully!")

    except Exception as e:
        print(f"❌ Error running the application: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
