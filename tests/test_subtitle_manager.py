from modules.utils.subtitle_manager import WriteSRT


def _word(start: float, end: float, text: str) -> dict:
    return {"start": start, "end": end, "word": text}


def test_srt_writer_wraps_word_timestamps_to_two_short_lines():
    result = {
        "segments": [
            {
                "start": 0.0,
                "end": 3.0,
                "text": "",
                "words": [
                    _word(0.0, 0.2, " 이것은"),
                    _word(0.2, 0.4, " 자막을"),
                    _word(0.4, 0.6, " 자연스럽게"),
                    _word(0.6, 0.8, " 나누기"),
                    _word(0.8, 1.0, " 위한"),
                    _word(1.0, 1.2, " 테스트입니다"),
                ],
            }
        ]
    }

    subtitles = list(
        WriteSRT(".").iterate_result(result)
    )

    assert len(subtitles) == 1
    assert subtitles[0][2] == "이것은 자막을 자연스럽게 나누기\n위한 테스트입니다"


def test_srt_writer_breaks_subtitles_at_short_pause():
    result = {
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "",
                "words": [
                    _word(0.0, 0.2, " 첫"),
                    _word(0.2, 0.4, " 문장입니다."),
                    _word(1.2, 1.4, " 다음"),
                    _word(1.4, 1.6, " 문장입니다."),
                ],
            }
        ]
    }

    subtitles = list(
        WriteSRT(".").iterate_result(
            result,
            max_line_width=18,
            max_line_count=2,
            subtitle_pause_threshold=0.6,
        )
    )

    assert [subtitle[2] for subtitle in subtitles] == ["첫 문장입니다.", "다음 문장입니다."]


def test_srt_writer_measures_pause_from_the_previous_word_end():
    result = {
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "",
                "words": [
                    _word(0.0, 0.6, " 첫"),
                    _word(1.1, 1.3, " 문장입니다."),
                ],
            }
        ]
    }

    subtitles = list(
        WriteSRT(".").iterate_result(
            result,
            max_line_width=18,
            max_line_count=2,
            subtitle_pause_threshold=0.6,
        )
    )

    assert [subtitle[2] for subtitle in subtitles] == ["첫 문장입니다."]

def test_srt_writer_allows_options_to_override_default_splitting_rules():
    result = {
        "segments": [
            {
                "start": 0.0,
                "end": 2.0,
                "text": "",
                "words": [
                    _word(0.0, 0.2, " 첫"),
                    _word(0.2, 0.4, " 문장입니다."),
                    _word(1.2, 1.4, " 다음"),
                    _word(1.4, 1.6, " 문장입니다."),
                ],
            }
        ]
    }

    subtitles = list(
        WriteSRT(".").iterate_result(
            result,
            options={
                "max_line_width": 100,
                "max_line_count": 2,
                "subtitle_pause_threshold": 1.0,
            },
        )
    )

    assert [subtitle[2] for subtitle in subtitles] == ["첫 문장입니다. 다음 문장입니다."]