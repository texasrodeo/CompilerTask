# Закрытие блоков (символ конца блока - })
def close_blocks(prog):
    lines = prog.split('\n')
    for l in range(0, len(lines) - 1):
        i1 = lines[l].find("    ")
        i2 = lines[l + 1].find("    ")
        if (i2 == -1) & (i1 != -1):
            lines[l] = lines[l] + " }"

    prog = ""

    for l in range(0, len(lines)):
        prog += lines[l] + "\n"

    return prog
