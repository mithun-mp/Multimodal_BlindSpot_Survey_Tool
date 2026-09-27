from blindspot.semantic.analyzer import get_exact_analyzer

a = get_exact_analyzer()
cases = [
    'i am healthy but still hospitalized',
    'i am not healthy but still hospitalized',
    'He is a Good boy but very naughty',
    'He is a good boy',
    'He is very naughty',
    'i am healthy',
    'i am not healthy',
    'the way she looked him was so romantic',
    'the king had a injury in his left leg',
    'The package arrived on Monday',
    'The table has four legs',
    'She felt delighted with the outcome',
    'The engine broke down completely'
]
for c in cases:
    lbl, conf, r = a.analyze(c)
    print(f"{c!r:45} -> {lbl.value:8} ({conf*100:.0f}%) [{r}]")
