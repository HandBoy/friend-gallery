def test_on_testing_env(app):
    assert app.config["ENV"] == "test"
    assert app.config["SECRET_KEY"] == "other-secret-key"
