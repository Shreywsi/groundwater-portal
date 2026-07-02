from unittest.mock import patch

from django.test import RequestFactory, TestCase

from .views import well_detail


class WellDetailViewTests(TestCase):
    def test_well_detail_includes_lulc(self):
        factory = RequestFactory()

        class MockCursor:
            def __init__(self):
                self.description = [
                    ("id",),
                    ("well_name",),
                    ("village",),
                    ("latitude",),
                    ("longitude",),
                    ("depth_m",),
                    ("water_level_m",),
                    ("status",),
                ]
                self._fetchone_results = [
                    (1, "Well A", "Village A", 23.1, 69.2, 10.0, 4.5, "active"),
                    ("Forest", 12.3),
                    None,
                ]

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def execute(self, *args, **kwargs):
                return None

            def fetchone(self):
                return self._fetchone_results.pop(0)

            def fetchall(self):
                return []

        mock_cursor = MockCursor()

        with patch("groundwater.views.connection.cursor", return_value=mock_cursor):
            response = well_detail(factory.get("/"), 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["lulc"]["class"], "Forest")
        self.assertEqual(response.data["lulc"]["areaHectares"], 12.3)
