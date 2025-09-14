#!/usr/bin/env python3
"""
Playground script to run the Friendship Manager GUI interface with real backend integration.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from friendship.ui.friendship_manager_gui import FriendshipManagerGUI
from shared.composition_root import build_application
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole
from friendship.application.send_friendship_invite_use_case import SendFriendshipInviteInputDto
from friendship.application.accept_friendship_invite_use_case import AcceptFriendshipInviteInputDto


def setup_mock_data(app):
    """Cria dados mock usando os casos de uso para testar a interface"""
    print("� Criando dados mock...")
    
    try:
        # Criar usuários mock
        users_data = [
            {"name": "João Silva", "email": "joao@email.com", "password": "123456"},      # ID será 1 (usuário atual)
            {"name": "Maria Santos", "email": "maria@email.com", "password": "123456"},   # ID será 2
            {"name": "Pedro Oliveira", "email": "pedro@email.com", "password": "123456"}, # ID será 3
            {"name": "Ana Costa", "email": "ana@email.com", "password": "123456"},        # ID será 4
            {"name": "Carlos Lima", "email": "carlos@email.com", "password": "123456"},   # ID será 5
            {"name": "Julia Pereira", "email": "julia@email.com", "password": "123456"},  # ID será 6
        ]
        
        created_users = []
        for user_data in users_data:
            try:
                user_dto = CreateUserInputDto(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=user_data["password"],
                    role=UserRole.CLIENT
                )
                user = app.create_user_use_case.execute(user_dto)
                created_users.append(user)
                print(f"  ✅ Usuário criado: {user.name} (ID: {user.id})")
            except Exception as e:
                print(f"  ⚠️  Usuário {user_data['name']} já existe ou erro: {e}")
        
        # Criar convites de amizade relacionadas ao usuário atual (João - ID=1)
        friendships_with_current_user = [
            {"requester": "joao@email.com", "requested": "maria@email.com"},    # João → Maria
            {"requester": "pedro@email.com", "requested": "joao@email.com"},    # Pedro → João
            {"requester": "ana@email.com", "requested": "joao@email.com"},      # Ana → João
            {"requester": "joao@email.com", "requested": "carlos@email.com"},   # João → Carlos
        ]
        
        # Criar amizades SEM relação com o usuário atual (para testar se não aparecem na lista)
        friendships_without_current_user = [
            {"requester": "maria@email.com", "requested": "pedro@email.com"},   # Maria → Pedro
            {"requester": "ana@email.com", "requested": "carlos@email.com"},    # Ana → Carlos
            {"requester": "julia@email.com", "requested": "maria@email.com"},   # Julia → Maria
        ]
        
        print("\n🔗 Criando amizades COM o usuário atual (devem aparecer na lista):")
        for friendship_data in friendships_with_current_user:
            try:
                # Enviar convite
                invite_dto = SendFriendshipInviteInputDto(
                    requester_client_email=friendship_data["requester"],
                    requested_client_email=friendship_data["requested"]
                )
                friendship = app.send_friendship_invite_use_case.execute(invite_dto)
                print(f"  📤 Convite enviado: {friendship_data['requester']} → {friendship_data['requested']}")
                
                # Aceitar o convite
                accept_dto = AcceptFriendshipInviteInputDto(friendship_id=friendship.id)
                app.accept_friendship_invite_use_case.execute(accept_dto)
                print(f"  ✅ Convite aceito: ID {friendship.id}")
                
            except Exception as e:
                print(f"  ⚠️  Erro ao criar/aceitar amizade: {e}")
        
        print("\n🚫 Criando amizades SEM o usuário atual (NÃO devem aparecer na lista):")
        for friendship_data in friendships_without_current_user:
            try:
                # Enviar convite
                invite_dto = SendFriendshipInviteInputDto(
                    requester_client_email=friendship_data["requester"],
                    requested_client_email=friendship_data["requested"]
                )
                friendship = app.send_friendship_invite_use_case.execute(invite_dto)
                print(f"  📤 Convite enviado: {friendship_data['requester']} → {friendship_data['requested']}")
                
                # Aceitar o convite
                accept_dto = AcceptFriendshipInviteInputDto(friendship_id=friendship.id)
                app.accept_friendship_invite_use_case.execute(accept_dto)
                print(f"  ✅ Convite aceito: ID {friendship.id}")
                
            except Exception as e:
                print(f"  ⚠️  Erro ao criar/aceitar amizade: {e}")
        
        print("\n📊 Dados mock criados com sucesso!")
        print("👤 Usuário atual: João Silva (ID: 1)")
        print("📋 Amigos esperados na lista: Maria, Pedro, Ana, Carlos")
        print("🚫 Usuários que NÃO devem aparecer: Julia (não é amiga de João)")
        
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
        print("🖥️  Opening Friendship Manager GUI...")
        
        # Create and show the GUI with use cases injected
        gui = FriendshipManagerGUI(use_cases=app)
        gui.show()

        print("✅ GUI closed successfully!")

    except Exception as e:
        print(f"❌ Error running the application: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
