from zecpath_hiring.ai.screening_ai.transcript_processing import normalize_transcript_text


def test_transcript_cleanup_removes_fillers_repeated_words_and_broken_punctuation():
    result = normalize_transcript_text("Um... I I actually built -- built the API,, and and launched it")

    assert result["normalized_text"] == "I built the api, and launched it."
    assert result["interrupted_speech"] is True
    assert result["partial_answer"] is False
