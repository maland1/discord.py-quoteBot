import subprocess

def update_bot():
    try:
        # Run the git pull command for the "release" branch
        process = subprocess.Popen(
            ["git", "pull", "origin", "release"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # Capture the standard output and error output
        stdout, stderr = process.communicate()

        # Check if the pull was successful
        if process.returncode == 0:
            print("Pull from 'release' branch was successful.")
        else:
            print(f"Pull from 'release' branch failed with error:\n{stderr}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
def restart_bot():
        # restart pi
        process = subprocess.Popen(
            ["sudo", "reboot"], stdout=subprocess.PIPE)