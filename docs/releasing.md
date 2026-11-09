# Release Guide

The package distribution is named `byteme-tarot`.
The Python import package is named `tarot_package`.

## 1. Prepare the release

Use the reviewed release code from `main`. Confirm that:

- The working tree is clean.
- GitHub Actions passes.
- Tests cover the package functions.
- `pyproject.toml` contains the intended version and package metadata.

Install development dependencies:

```bash
pipenv install --dev
```

## 2. Test, build, and check

Run from the repository root:

```bash
pipenv run python -m pytest tests/ -v
pipenv run python -m build
pipenv run python -m twine check dist/*
```

Before uploading, confirm that `dist/` contains only the intended release files.

## 3. Upload to TestPyPI

TestPyPI is a separate practice package index. It does not run automated tests.

Create an account at https://test.pypi.org/ and an API token.
The first upload of a new project requires an account-wide token.

For version 0.1.0:

```bash
pipenv run python -m twine upload --repository testpypi \
  dist/byteme_tarot-0.1.0-py3-none-any.whl \
  dist/byteme_tarot-0.1.0.tar.gz
```

Enter the TestPyPI API token at the hidden prompt.
Never commit tokens or include them in documentation.

For later releases, replace the version in the filenames.

## 4. Check a clean installation

Use a new temporary environment to avoid relying on the local editable installation.

On macOS or Linux:

```bash
python3 -m venv /tmp/byteme-tarot-release-check

/tmp/byteme-tarot-release-check/bin/python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --no-deps byteme-tarot==0.1.0

/tmp/byteme-tarot-release-check/bin/python -I -c \
  'from tarot_package import daily_reading; print(daily_reading("Uuree", topic="study", tone="programmer"))'
```

Use a fresh environment path for each trial.
The `--no-deps` option is appropriate because this package currently has no runtime dependencies.

Also inspect the TestPyPI page for the README and package metadata.

## 5. Recorded TestPyPI trial

Version 0.1.0 was uploaded and checked on November 9, 2026:

- All 546 existing tests passed.
- The wheel and source archive built successfully.
- Both files passed `twine check`.
- Both uploads were accepted by TestPyPI.
- The package installed in a separate environment.
- A complete daily reading ran successfully.

Package page:
https://test.pypi.org/project/byteme-tarot/0.1.0/

The existing test suite primarily covers the card model, card data, and lookup.
This successful trial does not replace the remaining function tests.

The build also reported a deprecation warning for the license metadata format.

## 6. Publish to PyPI

Before publishing:

- Complete the remaining function tests.
- Update the deprecated license metadata format.
- Obtain team review of the final release.
- Rebuild and check any changed release files.
- Repeat the TestPyPI trial if the release files change.

PyPI and TestPyPI use separate accounts and API tokens.

Upload the final verified files to real PyPI using:

```bash
pipenv run python -m twine upload \
  dist/byteme_tarot-0.1.0-py3-none-any.whl \
  dist/byteme_tarot-0.1.0.tar.gz
```

Use a PyPI token, not a TestPyPI token.

After publication, install the intended version from PyPI in another clean environment and run a reading.

An uploaded filename cannot be replaced. If a published release needs changes, use a new version.

## Official references

- Packaging tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- TestPyPI guide: https://packaging.python.org/en/latest/guides/using-testpypi/