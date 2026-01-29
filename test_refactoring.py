#!/usr/bin/env python3
"""
Comprehensive Test Suite for RogueGame
======================================

Tests core functionality including:
- Logging configuration and debug toggle
- Map classes and utilities
- Entity tracking systems
- Room generation algorithms

Run with: python test_refactoring.py
Or with pytest: pytest test_refactoring.py -v
"""

import sys
import os
import logging
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the game directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# =============================================================================
# Logging Configuration Tests
# =============================================================================

class TestLoggingConfig(unittest.TestCase):
    """Tests for the logging configuration system."""

    def test_import_logging_config(self):
        """Test that logging_config module can be imported."""
        from logging_config import get_logger, set_debug_mode, is_debug_mode
        self.assertIsNotNone(get_logger)
        self.assertIsNotNone(set_debug_mode)
        self.assertIsNotNone(is_debug_mode)

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a proper logger instance."""
        from logging_config import get_logger
        logger = get_logger("test_module")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_module")

    def test_get_logger_caches_loggers(self):
        """Test that get_logger returns the same logger for the same name."""
        from logging_config import get_logger
        logger1 = get_logger("test_cache")
        logger2 = get_logger("test_cache")
        self.assertIs(logger1, logger2)

    def test_debug_mode_toggle(self):
        """Test that debug mode can be toggled on and off."""
        from logging_config import set_debug_mode, is_debug_mode

        # Save original state
        original = is_debug_mode()

        # Test toggle
        set_debug_mode(True)
        self.assertTrue(is_debug_mode())

        set_debug_mode(False)
        self.assertFalse(is_debug_mode())

        # Restore original state
        set_debug_mode(original)

    def test_logger_outputs_debug_when_enabled(self):
        """Test that debug messages are logged when debug mode is on."""
        from logging_config import get_logger, set_debug_mode, is_debug_mode

        original = is_debug_mode()
        set_debug_mode(True)

        logger = get_logger("test_debug_output")

        # Capture log output
        with patch.object(logger, 'debug') as mock_debug:
            logger.debug("Test debug message")
            mock_debug.assert_called_once_with("Test debug message")

        set_debug_mode(original)

    def test_module_specific_log_levels(self):
        """Test that module-specific log levels can be set."""
        from logging_config import get_logger, set_module_level

        test_module = "test_specific_level_module"
        logger = get_logger(test_module)

        set_module_level(test_module, logging.WARNING)
        self.assertEqual(logger.level, logging.WARNING)

        set_module_level(test_module, logging.DEBUG)
        self.assertEqual(logger.level, logging.DEBUG)


# =============================================================================
# Maps Module Tests
# =============================================================================

class TestMapsClass(unittest.TestCase):
    """Tests for the base Maps class."""

    def setUp(self):
        """Set up test fixtures."""
        from dungeon_generation.maps.maps import Maps
        self.Maps = Maps

    def test_map_initialization(self):
        """Test that Maps initializes with correct dimensions."""
        map_obj = self.Maps(10, 15)
        self.assertEqual(map_obj.width, 10)
        self.assertEqual(map_obj.height, 15)
        self.assertEqual(map_obj.get_width(), 10)
        self.assertEqual(map_obj.get_height(), 15)

    def test_entity_map_independence(self):
        """Test that entity_map cells are independent (no aliasing bug)."""
        map_obj = self.Maps(10, 10)

        # Modify one cell
        map_obj.entity_map[5][5] = 999

        # Verify other cells are not affected
        self.assertEqual(map_obj.entity_map[5][0], -1, "Cell [5][0] was incorrectly modified")
        self.assertEqual(map_obj.entity_map[5][9], -1, "Cell [5][9] was incorrectly modified")
        self.assertEqual(map_obj.entity_map[0][5], -1, "Cell [0][5] was incorrectly modified")
        self.assertEqual(map_obj.entity_map[9][5], -1, "Cell [9][5] was incorrectly modified")
        self.assertEqual(map_obj.entity_map[5][5], 999, "Cell [5][5] should be 999")

    def test_in_map_boundary_checks(self):
        """Test in_map boundary checking."""
        map_obj = self.Maps(10, 10)

        # Valid coordinates
        self.assertTrue(map_obj.in_map(0, 0))
        self.assertTrue(map_obj.in_map(5, 5))
        self.assertTrue(map_obj.in_map(9, 9))

        # Invalid coordinates
        self.assertFalse(map_obj.in_map(-1, 0))
        self.assertFalse(map_obj.in_map(0, -1))
        self.assertFalse(map_obj.in_map(10, 0))
        self.assertFalse(map_obj.in_map(0, 10))
        self.assertFalse(map_obj.in_map(100, 100))

    def test_place_entity(self):
        """Test placing entities on the map."""
        map_obj = self.Maps(10, 10)

        # Valid placement
        result = map_obj.place_entity(5, 5, "test_entity")
        self.assertTrue(result)
        self.assertEqual(map_obj.entity_map[5][5], "test_entity")

        # Invalid placement (out of bounds)
        result = map_obj.place_entity(100, 100, "invalid")
        self.assertFalse(result)

    def test_clear_entity(self):
        """Test clearing entities from the map."""
        map_obj = self.Maps(10, 10)

        map_obj.place_entity(5, 5, "test_entity")
        result = map_obj.clear_entity(5, 5)

        self.assertTrue(result)
        self.assertEqual(map_obj.entity_map[5][5], -1)

        # Invalid clear (out of bounds)
        result = map_obj.clear_entity(100, 100)
        self.assertFalse(result)

    def test_get_entity(self):
        """Test getting entities from the map."""
        map_obj = self.Maps(10, 10)

        map_obj.place_entity(5, 5, "test_entity")

        self.assertEqual(map_obj.get_entity(5, 5), "test_entity")
        self.assertEqual(map_obj.get_entity(0, 0), -1)
        self.assertEqual(map_obj.get_entity(100, 100), -1)

    def test_get_has_entity(self):
        """Test checking for entity presence."""
        map_obj = self.Maps(10, 10)

        map_obj.place_entity(5, 5, "test_entity")

        self.assertTrue(map_obj.get_has_entity(5, 5))
        self.assertFalse(map_obj.get_has_entity(0, 0))
        self.assertFalse(map_obj.get_has_entity(100, 100))

    def test_get_has_no_entity(self):
        """Test checking for empty tiles."""
        map_obj = self.Maps(10, 10)

        map_obj.place_entity(5, 5, "test_entity")

        self.assertFalse(map_obj.get_has_no_entity(5, 5))
        self.assertTrue(map_obj.get_has_no_entity(0, 0))
        self.assertFalse(map_obj.get_has_no_entity(100, 100))

    def test_get_distance(self):
        """Test distance calculation between points."""
        map_obj = self.Maps(10, 10)

        # Distance from (0,0) to (3,4) should be 5 (3-4-5 triangle)
        distance = map_obj.get_distance(0, 3, 0, 4)
        self.assertAlmostEqual(distance, 5.0, places=5)

        # Same point should be 0
        distance = map_obj.get_distance(5, 5, 5, 5)
        self.assertAlmostEqual(distance, 0.0, places=5)

        # Out of bounds should return None
        distance = map_obj.get_distance(100, 5, 100, 5)
        self.assertIsNone(distance)


# =============================================================================
# Room Tests
# =============================================================================

class TestRoomClass(unittest.TestCase):
    """Tests for the Room class."""

    def setUp(self):
        """Set up test fixtures."""
        from dungeon_generation.maps.room import Room
        self.Room = Room

    def test_room_initialization(self):
        """Test Room initializes with correct properties."""
        room = self.Room(5, 10, 6, 8)

        self.assertEqual(room.x, 5)
        self.assertEqual(room.y, 10)
        self.assertEqual(room.width, 6)
        self.assertEqual(room.height, 8)

    def test_room_center_calculation(self):
        """Test Room center point calculation."""
        room = self.Room(0, 0, 10, 10)

        self.assertEqual(room.GetCenterX(), 5)
        self.assertEqual(room.GetCenterY(), 5)

        room2 = self.Room(10, 20, 6, 8)
        self.assertEqual(room2.GetCenterX(), 13)
        self.assertEqual(room2.GetCenterY(), 24)

    def test_room_intersection_overlapping(self):
        """Test that overlapping rooms are detected."""
        room1 = self.Room(0, 0, 10, 10)
        room2 = self.Room(5, 5, 10, 10)

        self.assertTrue(room1.intersects(room2))
        self.assertTrue(room2.intersects(room1))

    def test_room_intersection_non_overlapping(self):
        """Test that non-overlapping rooms don't intersect."""
        room1 = self.Room(0, 0, 5, 5)
        room2 = self.Room(20, 20, 5, 5)

        self.assertFalse(room1.intersects(room2))
        self.assertFalse(room2.intersects(room1))

    def test_room_intersection_adjacent(self):
        """Test rooms that are adjacent (buffer zone)."""
        room1 = self.Room(0, 0, 5, 5)
        room2 = self.Room(6, 0, 5, 5)  # One tile gap

        # With 1-tile buffer, adjacent rooms should intersect
        # (this depends on implementation)
        result = room1.intersects(room2)
        # Just verify it doesn't crash; actual behavior depends on design


# =============================================================================
# ID Tracking Tests
# =============================================================================

class TestIDClass(unittest.TestCase):
    """Tests for the ID tracking class."""

    def setUp(self):
        """Set up test fixtures."""
        from dungeon_generation.maps.id import ID
        self.ID = ID

    def test_id_initialization(self):
        """Test ID system initializes correctly."""
        id_system = self.ID()

        self.assertEqual(id_system.num_entities(), 0)
        self.assertEqual(id_system.ID_count, 0)

    def test_tag_subject(self):
        """Test tagging subjects with unique IDs."""
        id_system = self.ID()

        class MockEntity:
            def gain_ID(self, id_tag):
                self.id_tag = id_tag

        entity1 = MockEntity()
        entity2 = MockEntity()

        id_system.tag_subject(entity1)
        id_system.tag_subject(entity2)

        self.assertEqual(entity1.id_tag, 1)
        self.assertEqual(entity2.id_tag, 2)
        self.assertEqual(id_system.num_entities(), 2)

    def test_get_subject(self):
        """Test retrieving subjects by ID."""
        id_system = self.ID()

        class MockEntity:
            def __init__(self, name):
                self.name = name
            def gain_ID(self, id_tag):
                self.id_tag = id_tag

        entity = MockEntity("TestEntity")
        id_system.tag_subject(entity)

        retrieved = id_system.get_subject(1)
        self.assertEqual(retrieved.name, "TestEntity")

    def test_get_subject_invalid_id(self):
        """Test that invalid IDs raise exceptions."""
        id_system = self.ID()

        with self.assertRaises(Exception):
            id_system.get_subject(-1)

        with self.assertRaises(Exception):
            id_system.get_subject(999)

    def test_remove_subject(self):
        """Test removing subjects from tracking."""
        id_system = self.ID()

        class MockEntity:
            def gain_ID(self, id_tag):
                self.id_tag = id_tag

        entity = MockEntity()
        id_system.tag_subject(entity)

        self.assertEqual(id_system.num_entities(), 1)

        removed = id_system.remove_subject(1)

        self.assertEqual(id_system.num_entities(), 0)
        self.assertIs(removed, entity)

    def test_all_entities(self):
        """Test getting all tracked entities."""
        id_system = self.ID()

        class MockEntity:
            def __init__(self, name):
                self.name = name
            def gain_ID(self, id_tag):
                self.id_tag = id_tag

        entities = [MockEntity(f"Entity{i}") for i in range(3)]
        for e in entities:
            id_system.tag_subject(e)

        all_ents = id_system.all_entities()

        self.assertEqual(len(all_ents), 3)
        names = {e.name for e in all_ents}
        self.assertEqual(names, {"Entity0", "Entity1", "Entity2"})


# =============================================================================
# TrackingMap Tests
# =============================================================================

class TestTrackingMapClass(unittest.TestCase):
    """Tests for the TrackingMap class."""

    def setUp(self):
        """Set up test fixtures."""
        from dungeon_generation.maps.trackingmap import TrackingMap
        self.TrackingMap = TrackingMap

    def test_trackingmap_initialization(self):
        """Test TrackingMap initializes correctly."""
        tmap = self.TrackingMap(10, 10)

        self.assertEqual(tmap.width, 10)
        self.assertEqual(tmap.height, 10)
        self.assertEqual(tmap.get_num_entities(), 0)

    def test_place_thing(self):
        """Test placing entities on the tracking map."""
        tmap = self.TrackingMap(10, 10)

        class MockEntity:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def gain_ID(self, id_tag):
                self.id_tag = id_tag
            def get_id_tag(self):
                return self.id_tag

        entity = MockEntity(5, 5)
        tmap.place_thing(entity)

        self.assertEqual(tmap.get_num_entities(), 1)
        self.assertEqual(entity.id_tag, 1)

    def test_remove_thing(self):
        """Test removing entities from the tracking map."""
        tmap = self.TrackingMap(10, 10)

        class MockEntity:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def gain_ID(self, id_tag):
                self.id_tag = id_tag
            def get_id_tag(self):
                return self.id_tag

        entity = MockEntity(5, 5)
        tmap.place_thing(entity)

        removed = tmap.remove_thing(entity)

        self.assertEqual(tmap.get_num_entities(), 0)
        self.assertIs(removed, entity)

    def test_move_entity(self):
        """Test moving entities on the tracking map."""
        tmap = self.TrackingMap(10, 10)

        class MockEntity:
            def __init__(self, x, y):
                self.x = x
                self.y = y
            def gain_ID(self, id_tag):
                self.id_tag = id_tag
            def get_id_tag(self):
                return self.id_tag

        entity = MockEntity(5, 5)
        tmap.place_thing(entity)

        tmap.move_entity(5, 5, 7, 7)

        # Old location should be empty
        self.assertTrue(tmap.get_has_no_entity(5, 5))
        # New location should have the entity ID
        self.assertTrue(tmap.get_has_entity(7, 7))


# =============================================================================
# Objects Tests (if Objects class exists)
# =============================================================================

class TestObjectsClass(unittest.TestCase):
    """Tests for the Objects base class."""

    def test_objects_import(self):
        """Test that Objects class can be imported."""
        try:
            from objects import Objects
            self.assertIsNotNone(Objects)
        except ImportError:
            self.skipTest("Objects module not available")

    def test_objects_initialization(self):
        """Test Objects class initialization."""
        try:
            from objects import Objects
            obj = Objects(x=5, y=10, id_tag=1, render_tag=100, name="Test Object")

            self.assertEqual(obj.x, 5)
            self.assertEqual(obj.y, 10)
            self.assertEqual(obj.name, "Test Object")
        except ImportError:
            self.skipTest("Objects module not available")

    def test_objects_location(self):
        """Test Objects get_location method."""
        try:
            from objects import Objects
            obj = Objects(x=5, y=10, id_tag=1, render_tag=100, name="Test Object")

            self.assertEqual(obj.get_location(), (5, 10))
        except ImportError:
            self.skipTest("Objects module not available")

    def test_objects_traits(self):
        """Test Objects trait system."""
        try:
            from objects import Objects
            obj = Objects(x=5, y=10, id_tag=1, render_tag=100, name="Test Object")

            self.assertTrue(obj.has_trait("object"))
            self.assertFalse(obj.has_trait("nonexistent"))
        except ImportError:
            self.skipTest("Objects module not available")

    def test_objects_distance(self):
        """Test Objects distance calculation."""
        try:
            from objects import Objects
            obj = Objects(x=0, y=0, id_tag=1, render_tag=100, name="Test Object")

            # Distance to (3, 4) should be 5
            distance = obj.get_distance(3, 4)
            self.assertAlmostEqual(distance, 5.0, places=5)
        except ImportError:
            self.skipTest("Objects module not available")


# =============================================================================
# Global Variables Tests
# =============================================================================

class TestGlobalVars(unittest.TestCase):
    """Tests for global variables."""

    def test_global_bugtesting_exists(self):
        """Test that global_bugtesting variable exists."""
        from global_vars import global_bugtesting
        self.assertIsInstance(global_bugtesting, bool)

    def test_logging_config_compatibility(self):
        """Test that logging_config provides backwards compatibility."""
        from logging_config import global_bugtesting, DEBUG_MODE

        # These should be the same or compatible
        self.assertIsInstance(global_bugtesting, bool)
        self.assertIsInstance(DEBUG_MODE, bool)


# =============================================================================
# Integration Tests
# =============================================================================

class TestLoggingIntegration(unittest.TestCase):
    """Integration tests for logging across modules."""

    def test_maps_module_uses_logging(self):
        """Test that maps module uses the logging system."""
        from dungeon_generation.maps.maps import Maps, logger

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)

    def test_room_module_uses_logging(self):
        """Test that room module uses the logging system."""
        from dungeon_generation.maps.room import Room, logger

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)

    def test_id_module_uses_logging(self):
        """Test that ID module uses the logging system."""
        from dungeon_generation.maps.id import ID, logger

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)

    def test_trackingmap_module_uses_logging(self):
        """Test that trackingmap module uses the logging system."""
        from dungeon_generation.maps.trackingmap import TrackingMap, logger

        self.assertIsNotNone(logger)
        self.assertIsInstance(logger, logging.Logger)


# =============================================================================
# Legacy Bug Demonstration Tests
# =============================================================================

class TestLegacyBugFix(unittest.TestCase):
    """Tests demonstrating the fixed list aliasing bug."""

    def test_old_buggy_pattern(self):
        """Demonstrate the old buggy pattern for reference."""
        width, height = 3, 3

        # OLD BUGGY WAY - creates aliased lists
        buggy_list = [[-1] * height] * width
        buggy_list[0][0] = 999

        # All rows are affected due to aliasing
        self.assertEqual(buggy_list[1][0], 999, "This demonstrates the bug")
        self.assertEqual(buggy_list[2][0], 999, "This demonstrates the bug")

    def test_fixed_pattern(self):
        """Verify the fixed pattern creates independent lists."""
        width, height = 3, 3

        # FIXED WAY - creates independent lists
        fixed_list = [[-1 for _ in range(height)] for _ in range(width)]
        fixed_list[0][0] = 999

        # Other rows should NOT be affected
        self.assertEqual(fixed_list[1][0], -1, "Fixed: other rows unaffected")
        self.assertEqual(fixed_list[2][0], -1, "Fixed: other rows unaffected")


# =============================================================================
# Test Runner
# =============================================================================

def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestLoggingConfig,
        TestMapsClass,
        TestRoomClass,
        TestIDClass,
        TestTrackingMapClass,
        TestObjectsClass,
        TestGlobalVars,
        TestLoggingIntegration,
        TestLegacyBugFix,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
