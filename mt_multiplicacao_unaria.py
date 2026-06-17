"""
MT para validar multiplicacao em notacao unaria (corrigida).

Formato: 1^a X 1^b = 1^c
Ex: 111X11=111111 (3x2=6 ACEITA), 111X11=11111 (3x2=5 REJEITA)

Estrategia:
  Marca 1s de A com A, copia B marcando resultado com C, restaura B.
"""

class TM:
    def __init__(self, tape):
        self.tape = list(tape) + ['_'] * 2000
        self.head = 0
        self.state = 'q0'
        self.steps = 0
        self.max_steps = 20000
        self.log = []

    def run(self):
        while self.state not in ('q_acc', 'q_rej') and self.steps < self.max_steps:
            self.steps += 1
            s = self.tape[self.head]

            if self.state == 'q0':
                if s == '1':
                    self.tape[self.head] = 'A'
                    self.head += 1
                    self.state = 'q_to_X'
                elif s == 'X':
                    self.state = 'q_ver_fim'
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_to_X':
                if s == 'X':
                    self.head += 1
                    self.state = 'q_markB'
                elif s in ('A', '1'):
                    self.head += 1
                else:
                    self.head += 1

            elif self.state == 'q_markB':
                if s == '1':
                    self.tape[self.head] = 'B'
                    self.head += 1
                    self.state = 'q_to_eq'
                elif s == '=':
                    self.state = 'q_unmarkB_right'
                    self.head -= 1  # volta pro X
                elif s == 'B':
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_to_eq':
                if s == '=':
                    self.head += 1
                    self.state = 'q_markC'
                elif s == 'B':
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_markC':
                if s == '1':
                    self.tape[self.head] = 'C'
                    self.head -= 1
                    self.state = 'q_backB'
                elif s == 'C':
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_backB':
                if s == '=':
                    self.head -= 1
                    self.state = 'q_find_nextB'
                else:
                    self.head -= 1

            elif self.state == 'q_find_nextB':
                if s == '1':
                    self.tape[self.head] = 'B'
                    self.head += 1
                    self.state = 'q_to_eq'
                elif s == 'B':
                    self.head -= 1
                elif s == 'X':
                    self.state = 'q_unmarkB_right'
                    self.head -= 1
                else:
                    self.head -= 1

            elif self.state == 'q_unmarkB_right':
                # Volta ate o X, depois vai p/ direita restaurando B->1
                if s == 'X':
                    self.head += 1
                    self.state = 'q_unmarkB_go'
                elif s in ('A', '1', '_'):
                    self.head += 1
                else:
                    self.head -= 1

            elif self.state == 'q_unmarkB_go':
                if s == 'B':
                    self.tape[self.head] = '1'
                    self.head += 1
                elif s == '=':
                    self.head -= 1
                    self.state = 'q_backA'
                elif s == '1':
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_backA':
                if s == 'X':
                    self.head -= 1
                    self.state = 'q_find_nextA'
                else:
                    self.head -= 1

            elif self.state == 'q_find_nextA':
                if s == '1':
                    self.tape[self.head] = 'A'
                    self.head += 1
                    self.state = 'q_to_X'
                elif s == 'A':
                    self.head -= 1
                elif s == '_':
                    self.head += 1
                    self.state = 'q_ver_fim'
                else:
                    self.head -= 1

            elif self.state == 'q_ver_fim':
                # Primeiro encontra '=', depois verifica resultado
                if s == '=':
                    self.head += 1
                    self.state = 'q_ver_R'
                elif s in ('A', 'B'):
                    self.tape[self.head] = '1'
                    self.head += 1
                elif s in ('1', 'X'):
                    self.head += 1
                elif s == '_':
                    self.state = 'q_rej'
                else:
                    self.head += 1

            elif self.state == 'q_ver_R':
                if s == 'C':
                    self.head += 1
                elif s == '1':
                    self.state = 'q_rej'
                elif s == '_':
                    self.state = 'q_acc'
                else:
                    self.head += 1

        return self.state == 'q_acc'


def test(tape, expected):
    tm = TM(tape)
    r = tm.run()
    s = 'ACEITA' if r else 'REJEITA'
    es = 'ACEITA' if expected else 'REJEITA'
    ok = 'OK' if r == expected else 'FALHA'
    print(f"  {ok}: '{tape:20s}' -> {s:8s} (esp: {es:8s}) [{tm.steps:4d} passos]")
    return r == expected


if __name__ == '__main__':
    print("Testes MULTIPLICACAO UNARIA:")
    print("="*65)
    casos = [
        ('111X11=111111', True),    # 3x2=6
        ('11X11=1111', True),       # 2x2=4
        ('1X111=111', True),        # 1x3=3
        ('1X1=1', True),            # 1x1=1
        ('111X111=111111111', True),# 3x3=9
        ('1111X11=11111111', True), # 4x2=8
        ('111X11=11111', False),    # 3x2=5
        ('11X11=111', False),       # 2x2=3
        ('111X11=1111111', False),  # 3x2=7
        ('1X1=11', False),          # 1x1=2
        ('11X11=11111', False),     # 2x2=5
        ('11111X111=111111111111111', True), # 5x3=15
    ]
    tot = 0
    for tape, exp in casos:
        if test(tape, exp): tot += 1
    print(f"\n{tot}/{len(casos)} OK")
