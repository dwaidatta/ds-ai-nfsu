"""Validates quiz/manifest.json and every quiz/data/*.json file against the
schema the quiz engine (quiz/take.html) expects, so a malformed or
out-of-sync quiz file can't reach GitHub Pages.
"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
QUIZ_DIR = REPO_ROOT / "quiz"
DATA_DIR = QUIZ_DIR / "data"
MANIFEST_PATH = QUIZ_DIR / "manifest.json"

VALID_TYPES = {"mcq", "true_false", "multi_select"}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def quiz_files():
    return sorted(DATA_DIR.glob("*.json"))


def test_manifest_is_valid_json_array_of_strings():
    manifest = load_json(MANIFEST_PATH)
    assert isinstance(manifest, list), "manifest.json must be a JSON array"
    assert manifest, "manifest.json must not be empty"
    assert all(isinstance(name, str) and name for name in manifest), (
        "manifest.json entries must all be non-empty strings"
    )


def test_manifest_matches_data_directory():
    manifest = set(load_json(MANIFEST_PATH))
    on_disk = {p.name for p in quiz_files()}
    missing = manifest - on_disk
    orphaned = on_disk - manifest
    assert not missing, f"manifest.json lists files missing from quiz/data: {sorted(missing)}"
    assert not orphaned, f"quiz/data has JSON files not listed in manifest.json: {sorted(orphaned)}"


@pytest.mark.parametrize("path", quiz_files(), ids=lambda p: p.name)
def test_quiz_file_is_valid_json(path):
    load_json(path)  # raises json.JSONDecodeError on malformed JSON


@pytest.mark.parametrize("path", quiz_files(), ids=lambda p: p.name)
def test_quiz_top_level_schema(path):
    data = load_json(path)
    assert isinstance(data, dict), "quiz file must contain a JSON object"

    for field in ("id", "title", "questions"):
        assert field in data, f"missing required field '{field}'"

    assert isinstance(data["id"], str) and data["id"], "'id' must be a non-empty string"
    assert data["id"] == path.stem, (
        f"'id' ({data['id']!r}) must match the filename ({path.stem!r})"
    )

    assert isinstance(data["title"], str) and data["title"].strip(), (
        "'title' must be a non-empty string"
    )

    if "description" in data:
        assert isinstance(data["description"], str), "'description' must be a string"

    if "published" in data:
        assert isinstance(data["published"], bool), "'published' must be a boolean"

    assert isinstance(data["questions"], list) and data["questions"], (
        "'questions' must be a non-empty list"
    )


@pytest.mark.parametrize("path", quiz_files(), ids=lambda p: p.name)
def test_quiz_questions_schema(path):
    data = load_json(path)

    for i, q in enumerate(data["questions"]):
        loc = f"{path.name} question #{i + 1}"
        assert isinstance(q, dict), f"{loc}: must be a JSON object"

        assert isinstance(q.get("question"), str) and q["question"].strip(), (
            f"{loc}: 'question' must be a non-empty string"
        )

        qtype = q.get("type", "mcq")
        assert qtype in VALID_TYPES, f"{loc}: unknown type '{qtype}'"

        options = q.get("options")
        assert isinstance(options, list) and len(options) >= 2, (
            f"{loc}: 'options' must be a list with at least 2 entries"
        )
        assert all(isinstance(o, str) and o.strip() for o in options), (
            f"{loc}: every option must be a non-empty string"
        )
        assert len(options) == len(set(options)), f"{loc}: options must be unique"

        answer = q.get("answer")
        if qtype == "multi_select":
            assert isinstance(answer, list) and answer, (
                f"{loc}: multi_select 'answer' must be a non-empty list"
            )
            assert len(answer) == len(set(answer)), (
                f"{loc}: multi_select 'answer' entries must be unique"
            )
            assert all(a in options for a in answer), (
                f"{loc}: every multi_select answer must be one of 'options'"
            )
        else:
            assert isinstance(answer, str) and answer, f"{loc}: 'answer' must be a non-empty string"
            assert answer in options, f"{loc}: 'answer' must be one of 'options'"

        if qtype == "true_false":
            assert options == ["True", "False"], (
                f"{loc}: true_false 'options' must be exactly ['True', 'False']"
            )

        if "marks" in q:
            marks = q["marks"]
            assert (
                isinstance(marks, (int, float)) and not isinstance(marks, bool) and marks > 0
            ), f"{loc}: 'marks' must be a positive number"

        if "image" in q:
            assert isinstance(q["image"], str) and q["image"].strip(), (
                f"{loc}: 'image' must be a non-empty string path"
            )
            image_path = QUIZ_DIR / q["image"]
            assert image_path.is_file(), (
                f"{loc}: 'image' points to a file that doesn't exist: {q['image']}"
            )


def test_quiz_ids_are_unique():
    ids = [load_json(p)["id"] for p in quiz_files()]
    assert len(ids) == len(set(ids)), "duplicate quiz 'id' values found across quiz/data"
