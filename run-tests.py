import glob
import os
import subprocess
import shutil
import sys

def clean():
    target_dir = "test-results"
    folders = [target_dir, "reports", "build/test-results"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    os.makedirs(target_dir)

def angular_tests():
    if shutil.which("npm") is None:
        print("Erreur : 'npm' n'est pas installé ou n'est pas dans le PATH.")
        return 1

    process = subprocess.run(["npm", "test"], check=False)

    xml_files = glob.glob("reports/**/*.xml", recursive=True)
    for f in xml_files:
        shutil.copy(f, os.path.join("../test-results", os.path.basename(f)))

    return process.returncode

def java_tests():
    gradle_bin = "./gradlew" if os.path.exists("./gradlew") else "gradle"

    if shutil.which("java") is None:
        print("Erreur : JDK n'est pas installé ou n'est pas dans le PATH.")
        return 1

    process = subprocess.run([gradle_bin, "clean", "test"], check=False)

    source_path = os.path.join("build", "test-results", "test", "*.xml")
    for f in glob.glob(source_path):
        shutil.copy(f, os.path.join("../test-results", os.path.basename(f)))

    return process.returncode

def run_tests():
    exit_code = 1
    
    if os.path.exists("karma.conf.js") or os.path.exists("package.json"):
        exit_code = angular_tests()
    elif os.path.exists("build.gradle") or os.path.exists("gradlew"):
        exit_code = java_tests()
    else:
        print("Erreur : Le type de projet n'a pas été reconnu.")
        sys.exit(1)
        
    if exit_code == 0:
        print("\nTous les tests sont passés")
    else:
        print(f"\nLes tests ont échoué, voici le code de sortie : {exit_code}")

    return exit_code

def main():
    clean()

    if len(sys.argv) > 1:
        projects = sys.argv[1:]
        exit_codes = []
        for project in projects:
            if os.path.exists(project):
                os.chdir(project)
                exit_codes.append(run_tests())
                os.chdir('../')
            else:
                print(f"Erreur : Le dossier '{project}' n'existe pas.")
                sys.exit(1)
    
    exit_code = 1 if any(code != 0 for code in exit_codes) else 0
    sys.exit(exit_code)

if __name__ == "__main__":
    main()