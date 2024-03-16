import os
import subprocess
import requests
import yaml
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
GH_TOKEN = os.environ["GH_TOKEN"]
GH_USER = "CdaProd"
API_URL = "https://api.github.com"
REPOS_DIR = Path("cda_REPOS")

# Configure headers for GitHub API requests
headers = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repos_with_prefix(prefix: str):
    repos, page = [], 1
    while True:
        url = f"{API_URL}/users/{GH_USER}/repos?type=owner&per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories: {response.text}")
        batch = response.json()
        if not batch:
            break
        repos.extend([repo for repo in batch if repo['name'].startswith(prefix)])
        page += 1
    return repos

def configure_repo(repo):
    try:
        repo_name = repo['name']
        repo_path = REPOS_DIR / repo_name

        # Ensure repo directory exists
        repo_path.mkdir(parents=True, exist_ok=True)

        # Clone or update repository
        if list(repo_path.glob('*')):  # Check if directory is non-empty
            subprocess.run(["git", "-C", str(repo_path), "pull"], check=True)
        else:
            subprocess.run(["git", "clone", repo['ssh_url'], str(repo_path)], check=True)

        # Load or create cda.yml
        cda_config_path = repo_path / "cda.yml"
        if cda_config_path.exists():
            with cda_config_path.open() as file:
                cda_config = yaml.safe_load(file)
        else:
            cda_config = {}

        dockerfile_content = cda_config.get("dockerfile", "FROM python:3.8-slim\nCOPY . /app\nWORKDIR /app\nCMD python app.py")
        (repo_path / "Dockerfile").write_text(dockerfile_content)

        workflow_path = repo_path / ".github" / "workflows" / "docker-build-and-push.yml"
        workflow_path.parent.mkdir(parents=True, exist_ok=True)

        workflow_config = {
            "name": "Docker Build and Push",
            "on": ["push"],
            "jobs": {
                "build": {
                    "runs-on": "self-hosted",
                    "steps": [
                        {"uses": "actions/checkout@v2"},
                        {
                            "name": "Set up QEMU",
                            "uses": "docker/setup-qemu-action@v1"
                        },
                        {
                            "name": "Set up Docker Buildx",
                            "uses": "docker/setup-buildx-action@v1"
                        },
                        {
                            "name": "Log in to Docker Hub",
                            "uses": "docker/login-action@v1",
                            "with": {
                                "username": "${{ secrets.DOCKERHUB_USERNAME }}",
                                "password": "${{ secrets.DOCKERHUB_TOKEN }}"
                            }
                        },
                        {
                            "name": "Log in to GitHub Container Registry",
                            "uses": "docker/login-action@v1",
                            "with": {
                                "registry": "ghcr.io",
                                "username": "${{ github.repository_owner }}",
                                "password": "${{ secrets.GH_TOKEN }}"
                            }
                        },
                        {
                            "name": "Build and push",
                            "uses": "docker/build-push-action@v2",
                            "with": {
                                "context": ".",
                                "push": "true",
                                "tags": [
                                    f"docker.io/{GH_USER}/{repo_name}:latest",
                                    f"ghcr.io/{GH_USER}/{repo_name}:latest"
                                ],
                                "platforms": "linux/amd64,linux/arm64"
                            }
                        }
                    ]
                }
            }
        }

        workflow_path.write_text(yaml.dump(workflow_config, sort_keys=False))

    except Exception as e:
        print(f"Error configuring repository '{repo['name']}': {e}")

def main():
    try:
        repos = get_repos_with_prefix("cda")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(configure_repo, repo) for repo in repos]
            for future in as_completed(futures):
                future.result()
    except Exception as e:
        print(f"Script execution error: {e}")

if __name__ == "__main__":
    main()