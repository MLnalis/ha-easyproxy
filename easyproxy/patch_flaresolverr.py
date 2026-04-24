#!/usr/bin/env python3
import re

path = "/app/flaresolverr/src/utils.py"
with open(path, "r") as f:
    src = f.read()

src = src.replace(
    "driver_executable_path=driver_exe_path",
    'driver_executable_path="/usr/bin/chromedriver"'
)

old_sandbox = "options.add_argument('--no-sandbox')"
new_sandbox = """options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless=new')
    options.add_argument('--no-zygote')
    options.add_argument('--single-process')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--remote-debugging-port=0')"""

if old_sandbox in src:
    src = src.replace(old_sandbox, new_sandbox, 1)
    print("[OK] Flag Chromium aggiunti")
else:
    print("[WARN] Pattern --no-sandbox non trovato, skippo")

src = re.sub(r'([ \t]+)start_xvfb_display\(\)', r'\1pass  # xvfb disabled', src)
print("[OK] start_xvfb_display() rimosso")

with open(path, "w") as f:
    f.write(src)

print("[OK] utils.py patchato con successo")
print("--- Verifica flags inseriti ---")
for line in src.splitlines():
    if any(x in line for x in ["no-sandbox", "dev-shm", "headless", "no-zygote", "single-process", "chromedriver"]):
        print(" ", line.strip())