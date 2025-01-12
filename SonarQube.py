import os
import time
import subprocess
import webbrowser
import requests
import psutil

# Set relative paths
sonarqube_path = os.path.join(os.getcwd(), "sonarqube-24.12.0.100206", "bin", "windows-x86-64")
scanner_path = os.path.join(os.getcwd(), "sonar-scanner-cli-6.2.1.4610-windows-x64", "bin")
sonar_url = "http://localhost:9000"

# Check if SonarQube is already running
def is_sonarqube_running():
    try:
        response = requests.get(sonar_url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Start SonarQube
def start_sonarqube():
    print("Starting SonarQube...")
    os.chdir(sonarqube_path)
    subprocess.Popen(["StartSonar.bat"], shell=True)
    print(f"SonarQube has started. Please open {sonar_url} in your browser.")

# Stop SonarQube
def stop_sonarqube():
    print("Stopping SonarQube...")
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if "java" in proc.info['name'] and "sonar" in " ".join(proc.info['cmdline']):
                proc.terminate()
                print(f"Terminated process: {proc.info['pid']} - {proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    print("SonarQube has been stopped.")

# Open SonarQube in the browser
def open_sonarqube():
    print("Do you want to open the SonarQube webpage? (Y/N)")
    choice = input().strip().lower()
    if choice == 'y':
        webbrowser.open(sonar_url)
        print("Browser opened.")
    elif choice == 'n':
        print("Exiting the program.")
        exit()
    else:
        print("Invalid input. Please enter Y or N.")
        open_sonarqube()

# Run Sonar Scanner
def run_sonar_scanner(sonar_token, project_key):
    print("Running Sonar Scanner...")
    os.chdir(scanner_path)
    subprocess.run([
        ".\sonar-scanner.bat",
        f"-Dsonar.projectKey={sonar_token}",
        f"-Dsonar.sources=.",
        f"-Dsonar.host.url={sonar_url}",
        f"-Dsonar.token={project_key}",
    ], shell=True)

# Main program
def main():
    if is_sonarqube_running():
        print("SonarQube is already running.")
    else:
        # Start SonarQube
        start_sonarqube()
        print("Waiting for SonarQube to start...")
        time.sleep(30)  # Adjust waiting time if necessary
        # Open browser
        open_sonarqube()

    while True:
        # Manually input project_key and sonar_token
        project_key = input("Please enter the Sonar Project Key: ").strip()
        sonar_token = input("Please enter the SonarQube Token: ").strip()

        # Run Sonar Scanner
        run_sonar_scanner(project_key, sonar_token)

        print("Done!")
        print("Do you want to scan another project? (Enter 'q' to quit, any other key to continue)")
        if input().strip().lower() == "q":
            break
        else:
            continue

    # Stop SonarQube
    stop_sonarqube()

if __name__ == "__main__":
    main()
