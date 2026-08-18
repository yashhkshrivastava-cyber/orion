from services.auth_service import ROLE_DEFAULT_DATA_ACCESS, ROLE_PAGES, can_access_page


def test_viewer_defaults_do_not_include_data_access():
    assert ROLE_DEFAULT_DATA_ACCESS["viewer"] == (False, False)


def test_editor_defaults_ods_only():
    assert ROLE_DEFAULT_DATA_ACCESS["editor"] == (True, False)


def test_admin_defaults_both():
    assert ROLE_DEFAULT_DATA_ACCESS["admin"] == (True, True)


def test_viewer_without_flags_cannot_open_data_page():
    user = {"role": "viewer", "is_active": True, "ods_access": False, "dw_access": False}
    assert can_access_page(user, "data") is False
    assert can_access_page(user, "admin") is False
    assert ROLE_PAGES["viewer"] == {"home", "dashboard"}


def test_viewer_with_ods_flag_can_open_data_page():
    user = {"role": "viewer", "is_active": True, "ods_access": True, "dw_access": False}
    assert can_access_page(user, "data") is True
