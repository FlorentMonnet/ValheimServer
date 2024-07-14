from utils.color import ENCODING_COLOR
def print_message(message: str, color: ENCODING_COLOR, header:str = "") -> None:
    header = header + " " if header else header
    print(f"{color}{header}{message}{ENCODING_COLOR.ENDC}")

def print_error(message:str, exit=True) -> None:
    print_message(message,color=ENCODING_COLOR.FAIL,header="[ERR]")
    if exit:
        exit(1)

def print_warning(message:str) -> None:
    print_message(message,color=ENCODING_COLOR.WARNING,header="[WARN]")

def print_info(message:str) -> None:
    print_message(message,color=ENCODING_COLOR.OKBLUE,header="[INFO]")

def print_debug(message:str) -> None:
    print_message(message,color=ENCODING_COLOR.OKCYAN,header="[DEBUG]")

def print_success(message:str) -> None:
    print_message(message,color=ENCODING_COLOR.OKGREEN,header="[SUCCESS]")

def print_header(message:str) -> None:
    print_message(message,color=ENCODING_COLOR.HEADER)
