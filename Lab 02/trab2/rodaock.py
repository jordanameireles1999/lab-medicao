import csv
import subprocess
import os
import shutil
import signal

# Função para clonar um repositório
def clone_repository(url, folder):
    subprocess.run(["git", "clone", url, folder])

# Função para executar o CK em um repositório
def run_ck(folder):
    subprocess.run(["java", "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", folder])

# Função para excluir um diretório recursivamente
def delete_folder(folder):
    def onerror(func, path, exc_info):
        # Permissões podem causar problemas na exclusão; aqui, tentamos alterar as permissões para evitar problemas
        os.chmod(path, 0o777)
        func(path)

    shutil.rmtree(folder, onerror=onerror)

# Lê o CSV
csv_file_path = "repositories.csv"
with open(csv_file_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    # Loop pelas linhas do CSV
    for row in reader:
        repository_name = row["Repository"]
        repository_url = row["URL"]

        # Clona o repositório em uma pasta temporária
        temp_folder = "temp_repo"
        clone_repository(repository_url, temp_folder)

        # Executa o CK no repositório clonado
        run_ck(temp_folder)

        # Fecha o processo Git se estiver aberto
        subprocess.run(["git", "clean", "-ffdx"], cwd=temp_folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "gc"], cwd=temp_folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Exclui o repositório clonado após a execução do CK
        delete_folder(temp_folder)
