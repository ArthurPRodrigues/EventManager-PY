import FreeSimpleGUI as sg

from shared.infra.persistence.sqlite import SQLiteDatabase
from user.application.create_user_use_case import CreateUserInputDto, CreateUserUseCase
from user.application.errors import EmailByRoleAlreadyExistsError
from user.domain.errors import InvalidEmailError, InvalidNameError, InvalidPasswordError
from user.domain.user_role import UserRole
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


def CreateUserView():
    sg.theme("LightBlue2")

    # Obtém as funções (roles) disponíveis do UserRole enum
    roles = [role.value for role in UserRole]

    # --- LAYOUT da janela de Cadastro --- #
    layout = [
        [sg.Button("Back", key="-BACK-"), sg.Push()],
        [
            sg.Text(
                "Register",
                font=("Helvetica", 20),
                justification="center",
                expand_x=True,
            )
        ],
        [sg.HSeparator()],
        [sg.Text("Name", size=(8, 1)), sg.Input(key="-NAME-")],
        [sg.Text("Email", size=(8, 1)), sg.Input(key="-EMAIL-")],
        [
            sg.Text("Password", size=(8, 1)),
            sg.Input(key="-PASSWORD-", password_char="*"),
        ],
        [
            sg.Text("Role", size=(8, 1)),
            sg.Combo(roles, default_value=roles[0], key="-ROLE-", readonly=True),
        ],
        [
            sg.Checkbox(
                "I confirm I am 18 years or older",
                key="-AGE_CONFIRM-",
                enable_events=True,
            )
        ],
        [sg.Button("Create User", key="-CREATE-", disabled=True)],
        [sg.Text("", size=(40, 2), key="-MESSAGE-", text_color="red")],
    ]

    # Cria e exibe a janela
    window = sg.Window("UC01 - Register an user", layout, finalize=True)

    try:
        db = SQLiteDatabase()
        db.initialize()
        users_repository = SqliteUsersRepository(db)
        create_user_use_case = CreateUserUseCase(users_repository)
    except Exception as e:
        sg.popup_error(f"Error initializing data base: {e}")
        return

    while True:
        event, values = window.read()

        # todo: Fazer um retorno para a tela de LOGIN da ana
        if event == sg.WIN_CLOSED or event == "-BACK-":
            break

        if event == "-AGE_CONFIRM-":
            if values["-AGE_CONFIRM-"]:
                window["-CREATE-"].update(disabled=False)
            else:
                window["-CREATE-"].update(disabled=True)

        if event == "-CREATE-":
            name = values["-NAME-"]
            email = values["-EMAIL-"]
            password = values["-PASSWORD-"]
            role_str = values["-ROLE-"]
            age_confirmed = values["-AGE_CONFIRM-"]
            window["-MESSAGE-"].update("")

            if not name or not email or not password or not role_str:
                window["-MESSAGE-"].update("Please, fill all fields.", text_color="red")
                continue

            if not age_confirmed:
                window["-MESSAGE-"].update(
                    "I confirm that I'm 18 years old or older.", text_color="red"
                )
                continue

            try:
                input_dto = CreateUserInputDto(
                    name=name, email=email, password=password, role=UserRole(role_str)
                )

                # Executa o caso de uso
                user = create_user_use_case.execute(input_dto)

                # Exibe mensagem de sucesso
                window["-MESSAGE-"].update(
                    f"'{user.name}' user created!", text_color="green"
                )
                # Limpa os campos após o sucesso
                window["-NAME-"].update("")
                window["-EMAIL-"].update("")
                window["-PASSWORD-"].update("")
                window["-AGE_CONFIRM-"].update(False)
                window["-CREATE-"].update(disabled=True)

            except EmailByRoleAlreadyExistsError:
                window["-MESSAGE-"].update(
                    "Erro: An user with this email and role already exists.",
                    text_color="red",
                )
            except InvalidNameError:
                window["-MESSAGE-"].update("Erro: Invalid name.", text_color="red")
            except InvalidEmailError:
                window["-MESSAGE-"].update("Erro: Invalid Email.", text_color="red")
            except InvalidPasswordError:
                window["-MESSAGE-"].update("Erro: Invalid password.", text_color="red")
            except Exception as e:
                window["-MESSAGE-"].update(
                    f"Unknown error ocurred.: {e}", text_color="red"
                )

    window.close()


if __name__ == "__main__":
    CreateUserView()
