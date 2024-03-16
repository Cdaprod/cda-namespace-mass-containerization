[![Docker Build and Push](https://github.com/Cdaprod/cda-namespace-mass-containerization/actions/workflows/deploy-main-script.yml/badge.svg)](https://github.com/Cdaprod/cda-namespace-mass-containerization/actions/workflows/deploy-main-script.yml)

# GitHub Repository Dockerization and CI/CD Automation

This script automates the process of configuring GitHub repositories for Docker containerization and sets up continuous integration and deployment (CI/CD) workflows using GitHub Actions. Designed for efficiency and scalability, it streamlines the setup for Docker and CI/CD across multiple repositories within a GitHub user's account.

## Features

- **Automatic Repository Configuration**: Automatically generates Dockerfiles and GitHub Actions workflows for each repository.
- **Custom Configuration Support**: Supports repository-specific configurations through `cda.yml` files, allowing for custom Docker and CI/CD setups.
- **Concurrency for Efficiency**: Processes multiple repositories in parallel, significantly reducing the time required to configure all repositories.
- **Error Handling**: Implements robust error handling to ensure smooth operation and ease of debugging.

## Prerequisites

- Python 3.6 or later.
- Git installed and configured on your machine.
- A GitHub Personal Access Token with appropriate permissions (e.g., `repo`, `workflow`).
- SSH keys set up for GitHub to allow cloning and pushing without password prompts.

## Setup

1. Clone this repository to your local machine:

git clone 

2. Install required Python packages:

pip install requests PyYAML

3. Create a `.env` file in the root of the project directory and add your GitHub Personal Access Token:

GH_TOKEN=your_github_personal_access_token_here
GH_USER=your_github_username_here

## Configuration

### Global Script Configuration

Edit the `GH_TOKEN` and `GH_USER` constants in the script to match your GitHub Personal Access Token and GitHub username.

### Repository-Specific Configuration

To customize the Dockerfile and GitHub Actions workflow for a specific repository, create a `cda.yml` file in the root of that repository with the following structure:

```yaml
dockerfile: |
FROM python:3.8-slim
COPY . /app
WORKDIR /app
CMD python app.py

workflow:
name: Custom Workflow Name
on: push
tags: ["latest", "1.0"]

Usage

Execute the script from the command line:

python path/to/script.py

The script will process each repository prefixed with cda, automatically configuring them for Docker and setting up GitHub Actions workflows based on the global script settings or cda.yml configurations.

Contributing

Contributions to improve the script or add new features are welcome. Please fork the repository and submit a pull request with your changes.

License

Specify your license here or indicate that the project is open-source and available under the MIT License.

Remember to replace placeholder texts (like `<repository-url>`) with actual information relevant to your project. Adjust the `## Configuration`, `## Usage`, and any other sections as necessary to fit your project's specific needs and guidelines.