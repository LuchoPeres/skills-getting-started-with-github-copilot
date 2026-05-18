import pytest
from src import app as app_module


@pytest.mark.asyncio
async def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = await client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


@pytest.mark.asyncio
async def test_get_activities_returns_activity_list(client):
    # Arrange / Act
    response = await client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, dict)
    assert "Chess Club" in json_data
    assert "participants" in json_data["Chess Club"]


@pytest.mark.asyncio
async def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(app_module.activities[activity_name]["participants"])

    # Act
    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == initial_count + 1


@pytest.mark.asyncio
async def test_signup_for_existing_participant_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


@pytest.mark.asyncio
async def test_signup_for_unknown_activity_returns_not_found(client):
    # Arrange
    email = "student@example.com"

    # Act
    response = await client.post(
        "/activities/Nonexistent/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


@pytest.mark.asyncio
async def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    initial_count = len(app_module.activities[activity_name]["participants"])

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]
    assert len(app_module.activities[activity_name]["participants"]) == initial_count - 1


@pytest.mark.asyncio
async def test_remove_nonexistent_participant_returns_bad_request(client):
    # Arrange
    activity_name = "Gym Class"
    email = "notregistered@mergington.edu"

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not registered for this activity"
