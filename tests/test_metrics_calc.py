from metrics.metrics_calc import is_test_file, parse_lcov


def test_is_test_file():
    assert is_test_file("tests/test_api.py")
    assert is_test_file("src/api_test.py")
    assert is_test_file("ui/app.spec.js")
    assert not is_test_file("src/app.js")


def test_parse_lcov(tmp_path):
    lcov = tmp_path / "lcov.info"
    lcov.write_text("LF:10\nLH:7\nBRF:4\nBRH:3\n")
    data = parse_lcov(str(lcov))
    assert round(data["line_rate"], 2) == 0.7
    assert round(data["branch_rate"], 2) == 0.75
