# Publish DT lll on GitHub

GitHub profile: [github.com/noturtrishanjit](https://github.com/noturtrishanjit)

The profile link does not identify a repository name. Replace `YOUR_REPO_NAME` below with the repository name you create, for example `dt-lll`.

## 1. Create the GitHub repository

On GitHub:

1. Open [github.com/new](https://github.com/new).
2. Set **Owner** to `noturtrishanjit`.
3. Choose a repository name such as `dt-lll`.
4. Add the description: `A tiny CPU-first language-model experiment with a local chat app.`
5. Choose **Public**.
6. Do not add a README, `.gitignore`, or license in the GitHub form because this project already contains its own README and ignore rules.
7. Create the repository.

## 2. Check the files before uploading

From the extracted project folder:

```bash
git status --short
git check-ignore -v checkpoints/*.pt 2>/dev/null || true
```

The `.gitignore` intentionally excludes:

- `.venv/`
- Python caches
- `.pt`, `.gguf`, `.safetensors`, and other model artifacts in `checkpoints/`
- Training logs
- Local editor and Manus state

This keeps the public repository small and prevents accidentally publishing large or private artifacts.

## 3. Initialize and commit

Run these commands from the DT lll project root:

```bash
git init
git branch -M main
git add README.md .gitignore GITHUB_PUBLIC_RELEASE.md checkpoints/README.md model data docs website server.py server_pretrained.py *.bat *.sh *.toml plan.md
git status --short
git commit -m "Initial public DT lll release"
```

Review the staged files before pushing. Do not run `git add .` if you have local checkpoints or private files you do not want to publish.

## 4. Connect and push

Using HTTPS:

```bash
git remote add origin https://github.com/noturtrishanjit/YOUR_REPO_NAME.git
git push -u origin main
```

Using SSH:

```bash
git remote add origin git@github.com:noturtrishanjit/YOUR_REPO_NAME.git
git push -u origin main
```

GitHub may ask you to authenticate. Never put a GitHub password or personal access token inside the repository or a script.

## 5. After publishing

Open:

```text
https://github.com/noturtrishanjit/YOUR_REPO_NAME
```

Check that:

- The README renders correctly.
- `README.md` explains the model limits.
- No `.pt` checkpoint or secret appears in the file list.
- The Windows launcher and Python files are present.
- Dataset files have clear provenance and licensing notes.

## Optional release files

The repository can be used without committing model weights. If you later publish a checkpoint, use a release asset or a model-hosting service and document:

- Exact checkpoint filename
- SHA-256 checksum
- Model configuration
- Training-data version
- License and permitted use
- Expected RAM and CPU requirements

Do not claim that the current custom DT lll model is GGUF-compatible unless a real llama.cpp conversion and load test has succeeded.
