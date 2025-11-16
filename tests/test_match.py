from pathlib import Path
from unittest.mock import MagicMock, patch

from tamatai.agent.match import Match


def test_bulk_invokes_scoring_and_returns_results(tmp_path):
    match = Match.__new__(Match)
    match.tmp_dir = tmp_path
    match.scoring = MagicMock(side_effect=[{"score": 0.7}, {"score": 0.9}])

    job_post = b"job"
    files = [b"cv-1", b"cv-2"]

    with patch("tamatai.agent.match.pdf_to_image_base64", return_value=["job-image"]) as pdf_mock:
        results = Match.bulk(match, job_post, files)

    assert results == [{"score": 0.7}, {"score": 0.9}]
    assert pdf_mock.call_count == 1
    job_pdf_path = pdf_mock.call_args.args[0]
    assert isinstance(job_pdf_path, Path)
    assert job_pdf_path.exists()

    assert match.scoring.call_count == len(files)
    for call_args in match.scoring.call_args_list:
        job_images, file_path = call_args.args
        assert job_images == ["job-image"]
        assert not file_path.exists()
