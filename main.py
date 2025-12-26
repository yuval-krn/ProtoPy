import argparse
import socket
import threading
from typing import Any, Callable, TypeAlias

from challenges.echo import echo

ChallengeFn: TypeAlias = Callable[[socket.socket, Any], None]
PORT = 50007
DEFAULT_CHALLENGE = 0
CHALLENGE_MAP: dict[int, ChallengeFn] = {0: echo}


def extract_current_function() -> ChallengeFn:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--challenge",
        "-c",
        required=False,
        default=DEFAULT_CHALLENGE,
        type=int,
    )
    selected_challenge: int = parser.parse_args().challenge
    challenge_func = CHALLENGE_MAP.get(selected_challenge)
    if challenge_func:
        return challenge_func
    else:
        raise RuntimeError(f"Challenge {selected_challenge} is not yet implemented!")


def make_client_thread(
    conn: socket.socket, addr: Any, current_function: ChallengeFn
) -> threading.Thread:
    t = threading.Thread(target=current_function, args=(conn, addr))
    return t


def main():
    current_function = extract_current_function()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT))
        s.listen(5)
        print("Listening on port", PORT)
        while True:
            conn, addr = s.accept()
            ct = make_client_thread(conn, addr, current_function)
            ct.start()


if __name__ == "__main__":
    main()
