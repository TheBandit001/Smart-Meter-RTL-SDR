import subprocess

proc = subprocess.Popen(
    ["rtlamr", "-filterid=12345678", "-format=json"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)

while True:
    line = proc.stdout.readline()
    if line:
        print(line.strip())
