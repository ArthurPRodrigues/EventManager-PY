#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados mock de usuários e convites de amizade.
Este script cria usuários, envia convites e aceita alguns deles, deixando outros pendentes.
"""

import os
import sys

# Adicionar o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteInputDto,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteInputDto,
)
from shared.composition_root import build_application
from user.application.create_user_use_case import CreateUserInputDto
from user.domain.user_role import UserRole


def limpar_banco_dados():
    """Remove o arquivo do banco de dados para começar com estado limpo."""
    print("🗑️  Limpando banco de dados...")

    db_path = os.path.join("data", "app.db")

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"  ✅ Banco de dados removido: {db_path}")
        except Exception as e:
            print(f"  ⚠️  Erro ao remover banco de dados: {e}")
    else:
        print(f"  ℹ️  Banco de dados não encontrado: {db_path}")


def criar_usuarios_mock(app):
    """Cria usuários mock no sistema."""
    print("👥 Criando usuários mock...")

    usuarios_data = [
        {"name": "João Silva", "email": "joao@email.com", "password": "123456"},
        {"name": "Maria Santos", "email": "maria@email.com", "password": "123456"},
        {"name": "Pedro Oliveira", "email": "pedro@email.com", "password": "123456"},
        {"name": "Ana Costa", "email": "ana@email.com", "password": "123456"},
        {"name": "Carlos Lima", "email": "carlos@email.com", "password": "123456"},
        {"name": "Julia Pereira", "email": "julia@email.com", "password": "123456"},
        {"name": "Roberto Souza", "email": "roberto@email.com", "password": "123456"},
        {"name": "Fernanda Alves", "email": "fernanda@email.com", "password": "123456"},
        {"name": "Lucas Mendes", "email": "lucas@email.com", "password": "123456"},
        {"name": "Camila Rocha", "email": "camila@email.com", "password": "123456"},
        {"name": "Bruno Ferreira", "email": "bruno@email.com", "password": "123456"},
        {"name": "Larissa Martins", "email": "larissa@email.com", "password": "123456"},
        {"name": "Rafael Cardoso", "email": "rafael@email.com", "password": "123456"},
        {"name": "Mariana Silva", "email": "mariana@email.com", "password": "123456"},
        {"name": "Diego Santos", "email": "diego@email.com", "password": "123456"},
        {"name": "Isabela Lima", "email": "isabela@email.com", "password": "123456"},
        {"name": "Thiago Costa", "email": "thiago@email.com", "password": "123456"},
        {"name": "Natália Pereira", "email": "natalia@email.com", "password": "123456"},
        {
            "name": "Guilherme Alves",
            "email": "guilherme@email.com",
            "password": "123456",
        },
        {"name": "Bianca Souza", "email": "bianca@email.com", "password": "123456"},
        {"name": "Mateus Oliveira", "email": "mateus@email.com", "password": "123456"},
        {"name": "Vanessa Mendes", "email": "vanessa@email.com", "password": "123456"},
        {"name": "André Rocha", "email": "andre@email.com", "password": "123456"},
        {
            "name": "Carolina Ferreira",
            "email": "carolina@email.com",
            "password": "123456",
        },
        {"name": "Felipe Martins", "email": "felipe@email.com", "password": "123456"},
        {"name": "Rodrigo Silva", "email": "rodrigo@email.com", "password": "123456"},
        {"name": "Amanda Santos", "email": "amanda@email.com", "password": "123456"},
        {
            "name": "Gabriel Oliveira",
            "email": "gabriel@email.com",
            "password": "123456",
        },
        {"name": "Letícia Costa", "email": "leticia@email.com", "password": "123456"},
        {"name": "Vinícius Lima", "email": "vinicius@email.com", "password": "123456"},
        {
            "name": "Patrícia Pereira",
            "email": "patricia@email.com",
            "password": "123456",
        },
        {"name": "Eduardo Souza", "email": "eduardo@email.com", "password": "123456"},
        {"name": "Juliana Alves", "email": "juliana@email.com", "password": "123456"},
        {"name": "Márcio Mendes", "email": "marcio@email.com", "password": "123456"},
        {"name": "Priscila Rocha", "email": "priscila@email.com", "password": "123456"},
        {
            "name": "Fabiano Ferreira",
            "email": "fabiano@email.com",
            "password": "123456",
        },
        {"name": "Adriana Martins", "email": "adriana@email.com", "password": "123456"},
        {"name": "Leandro Cardoso", "email": "leandro@email.com", "password": "123456"},
        {
            "name": "Cristiane Silva",
            "email": "cristiane@email.com",
            "password": "123456",
        },
        {"name": "Renato Santos", "email": "renato@email.com", "password": "123456"},
        {"name": "Simone Lima", "email": "simone@email.com", "password": "123456"},
        {"name": "Marcelo Costa", "email": "marcelo@email.com", "password": "123456"},
        {"name": "Elaine Pereira", "email": "elaine@email.com", "password": "123456"},
        {
            "name": "Alexandre Alves",
            "email": "alexandre@email.com",
            "password": "123456",
        },
        {"name": "Daniela Souza", "email": "daniela@email.com", "password": "123456"},
        {
            "name": "Leonardo Oliveira",
            "email": "leonardo@email.com",
            "password": "123456",
        },
        {"name": "Karina Mendes", "email": "karina@email.com", "password": "123456"},
        {"name": "Fábio Rocha", "email": "fabio@email.com", "password": "123456"},
        {
            "name": "Tatiana Ferreira",
            "email": "tatiana@email.com",
            "password": "123456",
        },
        {"name": "Gustavo Martins", "email": "gustavo@email.com", "password": "123456"},
    ]

    usuarios_criados = []
    for dados_usuario in usuarios_data:
        try:
            dto_usuario = CreateUserInputDto(
                name=dados_usuario["name"],
                email=dados_usuario["email"],
                password=dados_usuario["password"],
                role=UserRole.CLIENT,
            )
            usuario = app.create_user_use_case.execute(dto_usuario)
            usuarios_criados.append(usuario)
            print(f"  ✅ Usuário criado: {usuario.name} (ID: {usuario.id})")
        except Exception as e:
            print(f"  ⚠️  Usuário {dados_usuario['name']} já existe ou erro: {e}")

    return usuarios_criados


def enviar_convites_amizade(app, convites):
    """Envia convites de amizade."""
    print("📤 Enviando convites de amizade...")

    convites_enviados = []
    for dados_convite in convites:
        try:
            dto_convite = SendFriendshipInviteInputDto(
                requester_client_email=dados_convite["requester"],
                requested_client_email=dados_convite["requested"],
            )
            amizade = app.send_friendship_invite_use_case.execute(dto_convite)
            convites_enviados.append(amizade)
            print(
                f"  📤 Convite enviado: {dados_convite['requester']} → {dados_convite['requested']} (ID: {amizade.id})"
            )
        except Exception as e:
            print(
                f"  ⚠️  Erro ao enviar convite {dados_convite['requester']} → {dados_convite['requested']}: {e}"
            )

    return convites_enviados


def aceitar_convites_amizade(app, convites_para_aceitar):
    """Aceita convites de amizade."""
    print("✅ Aceitando convites de amizade...")

    for convite in convites_para_aceitar:
        try:
            dto_aceitar = AcceptFriendshipInviteInputDto(friendship_id=convite.id)
            app.accept_friendship_invite_use_case.execute(dto_aceitar)
            print(f"  ✅ Convite aceito: ID {convite.id}")
        except Exception as e:
            print(f"  ⚠️  Erro ao aceitar convite ID {convite.id}: {e}")


def configurar_dados_mock(app):
    """Configura todos os dados mock no banco de dados."""
    print("📊 Configurando dados mock...")

    # Criar usuários
    criar_usuarios_mock(app)

    # Definir convites que serão aceitos (amizades estabelecidas)
    convites_aceitos = [
        {"requester": "joao@email.com", "requested": "maria@email.com"},
        {"requester": "pedro@email.com", "requested": "joao@email.com"},
        {"requester": "ana@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "carlos@email.com"},
        {"requester": "julia@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "roberto@email.com"},
        {"requester": "fernanda@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "lucas@email.com"},
        {"requester": "camila@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "bruno@email.com"},
        {"requester": "larissa@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "rafael@email.com"},
        {"requester": "mariana@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "diego@email.com"},
        {"requester": "isabela@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "thiago@email.com"},
        {"requester": "natalia@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "guilherme@email.com"},
        {"requester": "bianca@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "mateus@email.com"},
        {"requester": "vanessa@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "andre@email.com"},
        {"requester": "carolina@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "felipe@email.com"},
        {"requester": "rodrigo@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "amanda@email.com"},
        {"requester": "gabriel@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "leticia@email.com"},
        {"requester": "vinicius@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "patricia@email.com"},
        {"requester": "eduardo@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "juliana@email.com"},
        {"requester": "marcio@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "priscila@email.com"},
        {"requester": "fabiano@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "adriana@email.com"},
    ]

    # Definir convites que serão deixados pendentes (não aceitos)
    convites_pendentes = [
        {"requester": "tatiana@email.com", "requested": "joao@email.com"},
        {"requester": "gustavo@email.com", "requested": "joao@email.com"},
        {"requester": "karina@email.com", "requested": "joao@email.com"},
        {"requester": "leonardo@email.com", "requested": "joao@email.com"},
        {"requester": "daniela@email.com", "requested": "joao@email.com"},
        {"requester": "alexandre@email.com", "requested": "joao@email.com"},
        {"requester": "joao@email.com", "requested": "elaine@email.com"},
        {"requester": "joao@email.com", "requested": "marcelo@email.com"},
        {"requester": "joao@email.com", "requested": "simone@email.com"},
        {"requester": "joao@email.com", "requested": "renato@email.com"},
    ]

    # Definir convites entre outros usuários (não relacionados ao usuário atual)
    convites_outros_usuarios = [
        {"requester": "leandro@email.com", "requested": "cristiane@email.com"},
        {"requester": "renato@email.com", "requested": "simone@email.com"},
        {"requester": "marcelo@email.com", "requested": "elaine@email.com"},
        {"requester": "alexandre@email.com", "requested": "daniela@email.com"},
        {"requester": "leonardo@email.com", "requested": "karina@email.com"},
        {"requester": "fabio@email.com", "requested": "tatiana@email.com"},
        {"requester": "gustavo@email.com", "requested": "rodrigo@email.com"},
        {"requester": "maria@email.com", "requested": "pedro@email.com"},
        {"requester": "ana@email.com", "requested": "carlos@email.com"},
        {"requester": "amanda@email.com", "requested": "gabriel@email.com"},
    ]

    # Enviar e aceitar convites aceitos
    convites_enviados_aceitos = enviar_convites_amizade(app, convites_aceitos)
    aceitar_convites_amizade(app, convites_enviados_aceitos)

    # Enviar convites pendentes (não aceitar)
    enviar_convites_amizade(app, convites_pendentes)

    # Enviar convites entre outros usuários
    enviar_convites_amizade(app, convites_outros_usuarios)

    print("✅ Dados mock configurados com sucesso!")


def main():
    """Função principal do script."""
    print("🚀 Populando banco de dados com dados mock...")
    print("-" * 50)

    try:
        # Limpar banco de dados para começar com estado limpo
        limpar_banco_dados()

        print("-" * 50)

        # Construir aplicação com todas as dependências
        app = build_application()

        # Configurar dados mock
        configurar_dados_mock(app)

        print("-" * 50)
        print("✅ Banco de dados populado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao executar o script: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
