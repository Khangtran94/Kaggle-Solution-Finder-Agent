import io
import zipfile
import requests
import yaml
from minsearch import Index, VectorSearch
from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.messages import ModelMessagesTypeAdapter

import json
from tqdm.auto import tqdm
import random
import secrets
from pathlib import Path
from datetime import datetime

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

########################################
# PHASE 1 — Data Loading
########################################

def read_repo_data(repo_owner, repo_name, branch='main'):
    """
    Download and parse _data/competitions.yml from a GitHub repo.
    Returns parsed YAML as Python objects.
    """

    prefix = 'https://codeload.github.com'
    url = f'{prefix}/{repo_owner}/{repo_name}/zip/refs/heads/{branch}'
    resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception(f"Failed to download repository: {resp.status_code}")

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename

        if not filename.endswith('_data/competitions.yml'):
            continue

        with zf.open(file_info) as f:
            raw = f.read().decode('utf-8', errors='ignore')
            competitions = yaml.safe_load(raw)

            repository_data.append({
                'filename': filename,
                'content': competitions  # ✅ parsed YAML list
            })

    zf.close()
    return repository_data

def extract_completed_competitions(project_docs):
    results = []

    for doc in project_docs:
        content = doc.get('content')

        # Case 1: top-level dict with 'competitions'
        if isinstance(content, dict):
            competitions = content.get('competitions', [])

        # Case 2: top-level list
        elif isinstance(content, list):
            competitions = content

        else:
            continue

        if not isinstance(competitions, list):
            continue

        for comp in competitions:
            if str(comp.get('done', '')).lower() == 'true':
                results.append({
                    'title': comp.get('title'),
                    'metric': comp.get('metric'),
                    'link': comp.get('link'),
                    'done': True,
                    'solutions': comp.get('solutions', [])  # ✅ keep all solutions
                })

    return results

if __name__ == "__main__":
    ### read repo
    project_docs = read_repo_data('Khangtran94','kaggle-solutions','gh-pages')

    ### extract complete competitions
    completed_competitions = extract_completed_competitions(project_docs)
    print('Number of Kaggle competitions have the solutions:', len(completed_competitions))