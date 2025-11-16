import base64

from tamatai.agent import helper


def test_structure_output_creates_pydantic_model():
    config = {
        "description": {
            "name": "Candidate name",
            "role": "Role description",
            "year_experience": "Years of experience",
            "score": "Match score",
            "summary": "Summary",
        }
    }

    Ranking = helper.structure_output(config)
    ranking = Ranking(
        name="Jane Doe",
        role="Backend Engineer",
        year_experience=5,
        score=92,
        summary="Strong match",
    )

    assert ranking.model_dump() == {
        "name": "Jane Doe",
        "role": "Backend Engineer",
        "year_experience": 5,
        "score": 92,
        "summary": "Strong match",
    }


def test_image_to_base64_returns_string():
    image_bytes = b"fake-bytes"

    encoded = helper.image_to_base64(image_bytes)

    assert isinstance(encoded, str)
    assert base64.b64decode(encoded.encode("utf-8")) == image_bytes


def test_format_messages_combines_job_and_cv_images():
    job_images = ["job-image-base64"]
    cv_images = ["cv-one", "cv-two"]

    messages = helper.format_messages(job_images, cv_images)

    assert len(messages) == 1
    content = messages[0]["content"]

    job_entries = [item for item in content if item.get("type") == "image_url"][: len(job_images)]
    cv_entries = [item for item in content if item.get("type") == "image_url"][len(job_images):]

    assert all(item["image_url"]["url"].startswith("data:image/jpeg;base64,") for item in job_entries)
    assert len(job_entries) == len(job_images)
    assert len(cv_entries) == len(cv_images)

    text_blocks = [item for item in content if item.get("type") == "text"]
    assert text_blocks[0]["text"] == "Extract the following job post"
    assert text_blocks[1]["text"] == "Matching with Curiculum Vitae"
