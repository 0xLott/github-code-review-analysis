import file_manager
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

pull_requests_dataset_file = '../dataset/pullrequest.json'
pull_requests_refined_data = []


def diferenca_em_minutos(datetime1, datetime2):
    dt1 = datetime.strptime(datetime1, "%Y-%m-%dT%H:%M:%SZ")
    dt2 = datetime.strptime(datetime2, "%Y-%m-%dT%H:%M:%SZ")
    difference = abs(dt1 - dt2)
    return difference.total_seconds() / 60


def alteracoes(data):
    return data['changedFiles'] + data['deletions'] + data['additions']


def tamanho_pr_feedback_final():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'tamanho_pr': alteracoes(pull_request),
            'status': pull_request['state']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    # Gráfico Swarm Plot
    plt.figure(figsize=(10, 6))
    sns.stripplot(x='status', y='tamanho_pr', data=df, color='black', jitter=True,
                  size=5)  # Adicionando jitter para melhor visualização
    plt.ylim(0, 10)  # Focar no intervalo de 0 a 10

    # Adicionar título e rótulos
    plt.title("Distribuição do Tamanho dos PRs por Status (MERGED/CLOSED) - Violin Plot com Jitter")
    plt.xlabel("Status do PR")
    plt.ylabel("Tamanho do Pull Request (0-10)")

    # Mostrar o gráfico
    plt.show()


def tempo_dos_prs_feedback_final():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'tempo_analise': diferenca_em_minutos(pull_request['closetAt'], pull_request['createAt']),
            'status': pull_request['state']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    plt.figure(figsize=(10, 6))
    sns.stripplot(x='status', y='tempo_analise', data=df, jitter=True, size=6)
    plt.title("Distribuição do Tempo de Análise dos PRs por Status (MERGED/CLOSED)")
    plt.xlabel("Status do PR")
    plt.ylabel("Tempo de Análise (minutos)")

    # Mostrar o gráfico
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='status', y='tempo_analise', data=df)
    plt.title("Tempo de Análise dos PRs por Status (MERGED/CLOSED)")
    plt.xlabel("Status do PR")
    plt.ylabel("Tempo de Análise (minutos)")

    plt.show()


def descricao_feedback_final():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'descricaoLength': len(pull_request['description']),
            'status': pull_request['state']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)
    # Criar o gráfico Violin Plot com foco no intervalo de 0 a 5000
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='status', y='descricaoLength', data=df)
    plt.ylim(0, 5000)  # Focar no intervalo de 0 a 5000

    # Adicionar título e rótulos
    plt.title("Distribuição do Comprimento das Descrições dos PRs por Status (MERGED/CLOSED) - Violin Plot")
    plt.xlabel("Status do PR")
    plt.ylabel("Comprimento da Descrição (número de caracteres)")

    # Mostrar o gráfico
    plt.show()


def get_interacoes(data):
    return data['participantsCount'] + data['commentsCount'] + data['reviewsCount']


def interacoes_feedback_final():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'interacoes': get_interacoes(pull_request),
            'status': pull_request['state']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    plt.figure(figsize=(10, 6))
    sns.stripplot(x='status', y='interacoes', data=df, jitter=True, size=6)
    plt.title("Distribuição do Número de Interações por Status (MERGED/CLOSED) - Strip Plot")
    plt.xlabel("Status do PR")
    plt.ylabel("Número de Interações")

    # Mostrar o gráfico
    plt.show()


def pr_tamanho_quantidade_reviews():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'pr_tamanho': alteracoes(pull_request),
            'reviews': pull_request['reviewsCount']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    # Criar o gráfico de Barras
    plt.figure(figsize=(10, 6))
    # Agrupar os dados por faixas de tamanho
    size_bins = [0, 2, 5, 10, 15, 20, 25, 30]  # Defina suas faixas conforme necessário
    df['size_category'] = pd.cut(df['pr_tamanho'], bins=size_bins)
    mean_reviews = df.groupby('size_category')['reviews'].mean().reset_index()

    sns.barplot(x='size_category', y='reviews', data=mean_reviews, palette='Blues')
    plt.title("Média do Número de Revisões por Faixa de Tamanho do PR")
    plt.xlabel("Faixa de Tamanho do PR (número de alterações)")
    plt.ylabel("Média do Número de Revisões")
    plt.xticks(rotation=45)

    # Mostrar o gráfico
    plt.show()


def tempo_dos_prs_reviews():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'pr_diferenca': diferenca_em_minutos(pull_request['closetAt'], pull_request['createAt']),
            'reviews': pull_request['reviewsCount']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='pr_diferenca', y='reviews', data=df, s=100, alpha=0.7)
    plt.title("Relação entre Tempo de Análise dos PRs e Número de Revisões")
    plt.xlabel("Tempo de Análise (minutos)")
    plt.ylabel("Número de Revisões")

    # Mostrar o gráfico
    plt.show()


def descricao_reviews():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'descricaoLength': len(pull_request['description']),
            'reviews': pull_request['reviewsCount']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='descricaoLength', y='reviews', data=df, s=100, alpha=0.7)
    plt.title("Relação entre Tamanho da Descrição dos PRs e Número de Revisões")
    plt.xlabel("Tamanho da Descrição (número de caracteres)")
    plt.ylabel("Número de Revisões")

    # Criar o gráfico Scatter Plot
    plt.figure(figsize=(10, 6))
    # Definir faixas de tamanho da descrição
    description_bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Ajuste conforme necessário
    df['description_category'] = pd.cut(df['descricaoLength'], bins=description_bins)

    sns.boxplot(x='description_category', y='reviews', data=df)
    plt.title("Distribuição do Número de Revisões por Faixa de Tamanho da Descrição dos PRs")
    plt.xlabel("Faixa de Tamanho da Descrição (número de caracteres)")
    plt.ylabel("Número de Revisões")
    plt.xticks(rotation=45)

    # Mostrar o gráfico
    plt.show()


def interacoes_reviews():
    data = file_manager.load_json_file(pull_requests_dataset_file)

    for pull_request in data:
        pr_data = {
            'interacoes': get_interacoes(pull_request),
            'reviews': pull_request['reviewsCount']
        }
        pull_requests_refined_data.append(pr_data)

    df = pd.DataFrame(pull_requests_refined_data)

    plt.figure(figsize=(10, 6))
    # Definir faixas de interações
    interaction_bins = [0, 5, 10, 15, 20, 25, 30]  # Ajuste conforme necessário
    df['interaction_category'] = pd.cut(df['interacoes'], bins=interaction_bins)

    # Calcular a média do número de revisões por faixa de interações
    mean_reviews = df.groupby('interaction_category')['reviews'].mean().reset_index()

    sns.barplot(x='interaction_category', y='reviews', data=mean_reviews, palette='Blues')
    plt.title("Média do Número de Revisões por Faixa de Interações")
    plt.xlabel("Faixa de Interações")
    plt.ylabel("Média do Número de Revisões")
    plt.xticks(rotation=45)

    plt.show()


if __name__ == '__main__':
    # tamanho_pr_feedback_final()
    # tempo_dos_prs_feedback_final()
    # descricao_feedback_final()
    # interacoes_feedback_final()
    # pr_tamanho_quantidade_reviews()
    # tempo_dos_prs_reviews()
    # descricao_reviews()
    # interacoes_reviews()
