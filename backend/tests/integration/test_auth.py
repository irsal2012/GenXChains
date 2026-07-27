"""
Integration Tests — Authentication Endpoints

Tests:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET  /api/v1/auth/me
- PUT  /api/v1/auth/me
- GET  /api/v1/auth/users (admin only)
- Security: unauthenticated access, wrong credentials, duplicate registration
"""
import pytest
from fastapi.testclient import TestClient


class TestRegister:

    def test_register_success(self, client: TestClient):
        resp = client.post("/api/v1/auth/register", json={
            "email": "newuser@test.com",
            "password": "Secure@123",
            "full_name": "New User",
            "role": "demand_planner",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "newuser@test.com"
        assert "password" not in data
        assert "hashed_password" not in data

    def test_register_duplicate_email_returns_409(self, client: TestClient, admin_user):
        resp = client.post("/api/v1/auth/register", json={
            "email": "admin@genxchains.com",  # already exists
            "password": "Secure@123",
            "full_name": "Duplicate",
            "role": "demand_planner",
        })
        assert resp.status_code == 409

    def test_register_duplicate_email_is_case_sensitive_match_only(self, client: TestClient, admin_user):
        """Email is the sole account identity — there is no separate username.
        A distinct email registers successfully even with an identical name."""
        resp = client.post("/api/v1/auth/register", json={
            "email": "unique@test.com",
            "password": "Secure@123",
            "full_name": "Admin User",  # same display name as the existing admin
            "role": "demand_planner",
        })
        assert resp.status_code == 201

    def test_register_invalid_email_returns_422(self, client: TestClient):
        resp = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "Secure@123",
            "full_name": "Test",
            "role": "demand_planner",
        })
        assert resp.status_code == 422

    def test_register_missing_required_fields_returns_422(self, client: TestClient):
        resp = client.post("/api/v1/auth/register", json={"email": "x@x.com"})
        assert resp.status_code == 422


class TestLogin:
    """Login takes a JSON body of {email, password} — see LoginRequest and
    frontend/src/services/authService.ts."""

    def test_login_success(self, client: TestClient, admin_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": "admin@genxchains.com",
            "password": "Admin@123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password_returns_401(self, client: TestClient, admin_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": "admin@genxchains.com",
            "password": "WrongPassword",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user_returns_401(self, client: TestClient):
        resp = client.post("/api/v1/auth/login", json={
            "email": "ghost@test.com",
            "password": "Any@123",
        })
        assert resp.status_code == 401

    def test_login_returns_jwt_token(self, client: TestClient, admin_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": "admin@genxchains.com",
            "password": "Admin@123",
        })
        token = resp.json()["access_token"]
        # JWT has 3 parts separated by dots
        assert len(token.split(".")) == 3


class TestGetMe:

    def test_get_me_authenticated(self, client: TestClient, admin_user, admin_headers):
        resp = client.get("/api/v1/auth/me", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@genxchains.com"
        assert data["role"] == "admin"

    def test_get_me_unauthenticated_returns_401(self, client: TestClient):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_get_me_invalid_token_returns_401(self, client: TestClient):
        resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert resp.status_code == 401


class TestUpdateMe:

    def test_update_full_name(self, client: TestClient, admin_user, admin_headers):
        resp = client.put("/api/v1/auth/me", headers=admin_headers, json={
            "full_name": "Updated Admin Name",
        })
        assert resp.status_code == 200
        assert resp.json()["full_name"] == "Updated Admin Name"

    def test_update_me_unauthenticated_returns_401(self, client: TestClient):
        resp = client.put("/api/v1/auth/me", json={"full_name": "Hacker"})
        assert resp.status_code == 401


class TestAdminUserList:

    def test_admin_can_list_users(self, client: TestClient, admin_user, admin_headers):
        resp = client.get("/api/v1/auth/users", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list) or "items" in data

    def test_non_admin_cannot_list_users(self, client: TestClient, demand_planner_user, planner_headers):
        resp = client.get("/api/v1/auth/users", headers=planner_headers)
        assert resp.status_code in (403, 401)
