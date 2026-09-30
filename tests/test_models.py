from ittop_journal.models import AuthToken, ScheduleLesson, parse_many


def test_models_allow_forward_compatible_fields() -> None:
    token = AuthToken.model_validate({"access_token": "x", "new_field": True})
    assert token.access_token == "x"
    assert token.model_extra == {"new_field": True}


def test_schedule_list_envelope_is_preserved_as_models() -> None:
    lessons = parse_many(
        ScheduleLesson,
        {"items": [{"subject": "Math", "teacher": "T", "backend_flag": 1}]},
    )
    assert lessons[0].subject == "Math"
    assert lessons[0].model_extra == {"backend_flag": 1}
