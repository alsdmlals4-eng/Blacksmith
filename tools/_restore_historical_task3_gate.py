from pathlib import Path

path = Path('[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md')
text = path.read_text(encoding='utf-8')
old = 'HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED'
new = 'HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED'
if old not in text:
    raise RuntimeError('historical Task3 drift token not found')
path.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
print('historical R3 Task3 token restored without changing current Task3 gate')
