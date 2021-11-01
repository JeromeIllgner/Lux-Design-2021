def read_turn_updates():
    try:
        updates = []
        while True:
            line = input()
            updates.append(line)

            if line == "D_DONE":
                yield updates
                updates.clear()

    except EOFError as eof:
        raise SystemExit(eof)
