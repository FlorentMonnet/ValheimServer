from enum import Enum
from valheim import (
    pull_valheim_world,
    push_valheim_world,
)
from utils import (
    print_error,
    print_warning,
)


class ValheimAction(Enum):
    PULL = ["1", "pull"]
    PUSH = ["2", "push"]


def get_valheim_action_list() -> list[str]:
    valheim_actions = []
    for valheim_action in ValheimAction:
        valheim_actions += valheim_action.value

    if not valheim_action:
        print_error("Aucune action n'existe pour Valheim")

    return valheim_actions


def get_invalid_valheim_action_message(valheim_action: str) -> None:
    valheim_actions = get_valheim_action_list()
    print_warning(
        f"Une option valide doit être sélectionnée dans le tableau suivant: {valheim_actions},"
        + f"'{valheim_action}' n'est donc pas une option valide."
    )


def is_vaheim_action_valid(valheim_action: str):
    return (
        valheim_action in ValheimAction.PULL.value
        or valheim_action in ValheimAction.PUSH.value
    )


def execute_valheim_action(valheim_action: str) -> None:
    if valheim_action in ValheimAction.PULL.value:
        pull_valheim_world()

    if valheim_action in ValheimAction.PUSH.value:
        push_valheim_world()
