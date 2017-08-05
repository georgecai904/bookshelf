import time

def run_bash_command(command):
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    print(process.communicate())

while True:
    run_bash_command("python manage.py runcrons")
    time.sleep(60)