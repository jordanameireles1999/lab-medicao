import csv
import subprocess
import os
import shutil
import pandas as pd
import numpy as np

# Função para clonar um repositório
def clone_repository(url, folder_name):
    temp_folder = os.path.join("temp_repo", folder_name)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    subprocess.run(["git", "clone", url, temp_folder])
    return temp_folder

# Função para executar o CK em um repositório
def run_ck(folder):
    subprocess.run(["java", "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", folder])

# Função para sumarizar métricas
def summarize_metrics(repo_name, repo_url, input_file, output_file):
    df = pd.read_csv(input_file)

    # Calcula métricas sumarizadas
    lcom_median = df['lcom'].median()
    cbo_median = df['cbo'].median()
    dit_max = df['dit'].max()
    loc_sum = df['loc'].sum()

    # Cria um DataFrame para as métricas sumarizadas
    summary = pd.DataFrame({
        'Repository Name': [repo_name],
        'Repository URL': [repo_url],
        'LCOM Median': [lcom_median],
        'CBO Median': [cbo_median],
        'DIT Max': [dit_max],
        'LOC Sum': [loc_sum]
    })

    # Escreve no CSV de saída
    if os.path.exists(output_file):
        summary.to_csv(output_file, mode='a', header=False, index=False)
    else:
        summary.to_csv(output_file, index=False)


# Função para excluir um diretório recursivamente
def delete_folder(folder):
    def onerror(func, path, exc_info):
        os.chmod(path, 0o777)
        func(path)
    shutil.rmtree(folder, onerror=onerror)

# Lê o CSV
csv_file_path = "repositories.csv"
with open(csv_file_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:
        repository_name = row["Repository"]
        repository_url = row["URL"]

        # Clona o repositório
        cloned_folder = clone_repository(repository_url, repository_name)

        # Executa o CK
        run_ck(cloned_folder)

        # Sumariza as métricas
        input_path_for_summary = 'class.csv'
        summary_output_path = 'summary.csv'
        summarize_metrics(repository_name, repository_url, input_path_for_summary, summary_output_path)

        # Limpeza
        subprocess.run(["git", "clean", "-ffdx"], cwd=cloned_folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "gc"], cwd=cloned_folder, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        delete_folder(cloned_folder)
