import main


def test_projects_view_success():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get("/projects")
    assert r.status_code == 200
