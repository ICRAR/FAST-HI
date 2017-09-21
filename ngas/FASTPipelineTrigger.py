import subprocess

# Shoot and forget...
def handle_archive_event(evt):
    cmd = ['submit_debug_graph.sh', '-o', evt.file_id]
    subprocess.Popen(cmd, shell=False)
