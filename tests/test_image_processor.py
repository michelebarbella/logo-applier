import unittest
from utils.image_processor import ImageProcessor
from PIL import Image

class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = ImageProcessor()
        self.logo = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
    
    def test_create_logo_with_background_rectangle(self):
        result = self.processor.create_logo_with_background(
            self.logo, '#FFFFFF', 'Rettangolare', padding=10
        )
        self.assertEqual(result.width, 120)
        self.assertEqual(result.height, 120)
    
    def test_create_logo_with_background_circle(self):
        result = self.processor.create_logo_with_background(
            self.logo, '#FF0000', 'Circolare', padding=10
        )
        self.assertIsNotNone(result)
    
    def test_resize_logo_horizontal(self):
        target = Image.new('RGB', (1920, 1080))
        result = self.processor.resize_logo(self.logo, target, 10)
        expected_width = int(1920 * 0.1)
        self.assertEqual(result.width, expected_width)

if __name__ == '__main__':
    unittest.main()