import unittest
from transparent_classroom.api.interfaces import fields


class TestAttributes(unittest.TestCase):
    """
    Test Attributes Class

    Test class for validating the named API attributes object.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the named attributes to test with.

        :return: None

        """

        self.attribute1 = fields.NamedAPIAttribute(name="Hello")
        self.attribute2 = fields.NamedAPIAttribute(name="World")
        self.attribute3 = fields.NamedAPIAttribute(name="Hello")

    def test_comparator(self) -> None:
        """
        Test the class/object comparator.

        :return: None

        """

        self.assertNotEqual(self.attribute1, self.attribute2)
        self.assertEqual(self.attribute1, self.attribute3)

    def test_hash(self) -> None:
        """
        Test the class/object hashing.

        :return: None

        """

        self.assertNotEqual(hash(self.attribute1), hash(self.attribute2))
        self.assertEqual(hash(self.attribute1), hash(self.attribute3))

    def test_repr(self) -> None:
        """
        Test the str/repr conversions methods.

        :return: None

        """

        self.assertEqual(str(self.attribute1), "Attribute `Hello`")
        self.assertEqual(str(self.attribute2), "Attribute `World`")
        self.assertEqual(str(self.attribute1), str(self.attribute3))
        self.assertEqual(repr(self.attribute1), "Attribute `Hello`")
        self.assertEqual(repr(self.attribute2), "Attribute `World`")
        self.assertEqual(repr(self.attribute1), repr(self.attribute3))

    def test_properties(self) -> None:
        """
        Test the get/set methods for the class properties.

        :return: None

        """

        self.assertEqual(self.attribute1.name, "Hello")
        self.assertEqual(self.attribute2.name, "World")
        self.assertEqual(self.attribute3.name, "Hello")

        self.attribute1.name = "Goodbye"
        self.assertEqual(self.attribute1.name, "Goodbye")
        self.assertNotEqual(self.attribute1.name, self.attribute3.name)


class TestFields(unittest.TestCase):
    """
    Test Fields Class

    Test class for validating the base Field class.

    Attributes:


    """

    def setUp(self) -> None:
        """
        Set up the fields to test with.

        :return: None

        """

        self.field1 = fields.Field(name="id", value=1)
        self.field2 = fields.Field(name="first_name", value="Hello")
        self.field3 = fields.Field(name="last_name", value="World")


if __name__ == '__main__':
    unittest.main()
