"""
Máquina de Turing para copiar uma sequência binária separada por '#'.

Entrada:  101#
Saída:    101#101

Estratégia:
  1. Percorre a sequência antes do '#' da esquerda para a direita,
     procurando '0' ou '1' ainda não marcados (X/Y).
  2. Para cada '0' encontrado, substitui por 'X' e escreve '0' no
     final da fita (após '#').
  3. Para cada '1' encontrado, substitui por 'Y' e escreve '1' no
     final da fita.
  4. Após escrever, retorna ao início da fita (posição 0).
  5. Quando só resta '#' no caminho (tudo marcado), vai para
     a fase de restauração: percorre a fita restaurando X->0, Y->1.
  6. Ao final, verifica se chegou ao fim.
"""

def simulate_copy_mt(tape_input):
    tape = list(tape_input) + ['_'] * 500
    head = 0
    state = 'q0'
    steps = 0
    max_steps = 10000
    write_val = None

    print(f"Entrada: {''.join(tape[:60]).rstrip('_')}")

    while state not in ('q_accept', 'q_reject') and steps < max_steps:
        symbol = tape[head]
        steps += 1

        if state == 'q0':
            if symbol == '0':
                tape[head] = 'X'
                write_val = '0'
                head += 1
                state = 'q_to_hash'
            elif symbol == '1':
                tape[head] = 'Y'
                write_val = '1'
                head += 1
                state = 'q_to_hash'
            elif symbol == '#':
                # Todos os símbolos foram marcados, restaurar
                state = 'q_to_start_rest'
                head -= 1
            elif symbol in ('X', 'Y'):
                head += 1
            elif symbol == '_':
                state = 'q_reject'
            else:
                head += 1

        elif state == 'q_to_hash':
            if symbol == '#':
                head += 1
                state = 'q_write_at_end'
            elif symbol == '_':
                state = 'q_reject'
            else:
                head += 1

        elif state == 'q_write_at_end':
            if symbol == '_':
                tape[head] = write_val
                state = 'q_rewind_to_start'
                head -= 1
            else:
                head += 1

        elif state == 'q_rewind_to_start':
            if symbol == '_':
                head -= 1
            elif head == 0:
                state = 'q0'
            else:
                head -= 1

        elif state == 'q_to_start_rest':
            if head == -1:
                head = 0
                state = 'q_rest'
            elif symbol == '_':
                head += 1
                state = 'q_rest'
            else:
                head -= 1

        elif state == 'q_rest':
            if symbol == 'X':
                tape[head] = '0'
                head += 1
            elif symbol == 'Y':
                tape[head] = '1'
                head += 1
            elif symbol == '#':
                head += 1
                state = 'q_verify'
            elif symbol in ('0', '1'):
                head += 1
            elif symbol == '_':
                state = 'q_reject'
            else:
                head += 1

        elif state == 'q_verify':
            if symbol == '_':
                state = 'q_accept'
            elif symbol in ('0', '1'):
                head += 1
            else:
                state = 'q_reject'

        if steps <= 30 or steps % 10 == 0:
            tape_vis = ''.join(tape[:60]).rstrip('_')
            print(f"Passo {steps:4d} | {state:18s} | cabeça={head:3d} | lê='{symbol}' | fita: {tape_vis[:55]}")

    tape_vis = ''.join(tape[:60]).rstrip('_')
    result = state == 'q_accept'
    print(f"  → {tape_vis}")
    print(f"  → {'ACEITA' if result else 'REJEITA'} ({steps} passos)")
    return result, tape_vis


if __name__ == '__main__':
    test_cases = [
        ("101#", "101#101"),
        ("1101#", "1101#1101"),
        ("0#", "0#0"),
        ("1#", "1#1"),
        ("1010#", "1010#1010"),
        ("111#", "111#111"),
    ]

    all_ok = True
    for tape, expected in test_cases:
        print(f"\n{'─'*65}")
        print(f"Teste: {tape:10s} | esperado: {expected}")
        print(f"{'─'*65}")
        result, final_tape = simulate_copy_mt(tape)
        ok = result and final_tape.rstrip('_') == expected
        status = 'OK' if ok else 'FAIL'
        print(f"Status: {status}")
        if not ok:
            all_ok = False
        print()

    print(f"{'='*65}")
    print(f"  Todos os testes: {'PASSARAM ✓' if all_ok else 'FALHARAM ✗'}")
