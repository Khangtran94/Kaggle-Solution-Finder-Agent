import io
import zipfile
import requests
import yaml

from minsearch import VectorSearch
from sentence_transformers import SentenceTransformer

def read_repo_data(repo_owner, repo_name, branch="main"):
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/{branch}"
    resp = requests.get(url)
    resp.raise_for_status()

    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    repository_data = []

    for file_info in zf.infolist():
        if file_info.filename.endswith("_data/competitions.yml"):
            with zf.open(file_info) as f:
                competitions = yaml.safe_load(
                    f.read().decode("utf-8", errors="ignore")
                )
                repository_data.append({
                    "filename": file_info.filename,
                    "content": competitions
                })

    return repository_data

def extract_completed_competitions(project_docs):
    results = []

    for doc in project_docs:
        content = doc.get("content")

        if isinstance(content, dict):
            competitions = content.get("competitions", [])
        elif isinstance(content, list):
            competitions = content
        else:
            continue

        for comp in competitions:
            if str(comp.get("done", "")).lower() == "true":
                results.append({
                    "title": comp.get("title"),
                    "metric": comp.get("metric"),
                    "link": comp.get("link"),
                    "done": True,
                    "solutions": comp.get("solutions", [])
                })

    return results

def build_vector_index(completed_competitions):
    model = SentenceTransformer("multi-qa-distilbert-cos-v1")

    texts, docs = [], []

    for comp in completed_competitions:
        solutions = comp["solutions"]

        text = (
            f"Competition title: {comp['title']}. "
            f"Evaluation metric: {comp['metric']}. "
            f"This competition has {len(solutions)} solutions. "
            f"Solution ranks include {', '.join(s.get('rank','') for s in solutions)}. "
            f"Solution types include {', '.join(s.get('kind','') for s in solutions)}."
        )

        texts.append(text)
        docs.append({**comp, "solution_count": len(solutions)})

    embeddings = model.encode(
        texts, batch_size = 32,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    vindex = VectorSearch()
    vindex.fit(embeddings, docs)

    return model, vindex