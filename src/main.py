from valheim import (
    execute_valheim_action,
    is_vaheim_action_valid,
    get_invalid_valheim_action_message,
)
from sys import argv


def handle_args():
    if len(argv) == 2:
        valheim_action_arg = argv[1]
        if is_vaheim_action_valid(valheim_action_arg):
            execute_valheim_action(valheim_action_arg)
            exit(0)

        get_invalid_valheim_action_message(valheim_action_arg)


def handle_ui():
    while True:
        valheim_action = input(
                "Quelle action ?\n"
                + "1 - pull - Récupérer les fichiers en local\n"
                + "2 - push - Envoyer les fichiers sur le serveur\n"
        ).lower()
        if not is_vaheim_action_valid(valheim_action):
            get_invalid_valheim_action_message(valheim_action)
            continue

        execute_valheim_action(valheim_action)
        break


if __name__ == "__main__":
    handle_args()
    handle_ui()
