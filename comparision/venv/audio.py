import subprocess

# Run audio1.py asynchronously
p1 = subprocess.Popen(["python", "venv\\audio1.py"])

# Wait for audio1.py to complete
p1.wait()
p1.send_signal(signal.CTRL_C_EVENT)
# Run audio2.py after audio1.py completes
subprocess.run(["python", "venv\\audio2.py"])
