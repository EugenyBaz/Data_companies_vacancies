from src.interface import user_interaction


def test_user_interaction_len():
    result = user_interaction("менеджер", 100000, "RUR", "", 5)
    assert len(result) == 5
