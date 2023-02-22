import subprocess
import time
subprocess.Popen(['python', './Compras/sender1.py']),
time.sleep(5)
processes = [ subprocess.Popen(['python', './ConsultasInventario2/app.py',]), subprocess.Popen(['python', './ConsultasInventario1/app.py'])]
for process in processes:
    process.wait()
