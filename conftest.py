import os
import sys
import pytest
from playwright.sync_api import Page

# Ensure project root is on sys.path so "utils" and "pages" can be imported
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pages.login_page import LoginPage
from pages.admin_users_page import AdminUsersPage


@pytest.fixture
def admin_users_page(page: Page) -> AdminUsersPage:
    """
    Fixture that:
    - Logs in as Admin
    - Navigates to Admin -> User Management -> Users
    and returns an AdminUsersPage object ready to use.
    """
    login_page = LoginPage(page)
    login_page.login_as_admin()

    admin_page = AdminUsersPage(page)
    admin_page.goto_admin_users()
    return admin_page
