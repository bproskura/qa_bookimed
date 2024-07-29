from scipy.spatial import distance


class ColorDetector:

    def __init__(self):
        self.COLORS = {
            "RED": [255, 0, 0],
            "GREEN": [0, 255, 0],
            "BLUE": [0, 0, 255],
            "WHITE": [255, 255, 255],
            "BLACK": [0, 0, 0],
            "YELLOW": [255, 255, 0],
            "TURQUOISE": [64, 224, 208],
            "VIOLET": [238, 130, 238],
            "PINK": [255, 192, 203],
        }

    @staticmethod
    def _parse_color_string(color_string: str) -> list:
        """
        Function to parse a string in form 'rgb(r, g, b)' or 'rgba(r, g, b, a)'
        into a list of integers [r, g, b] or [r, g, b, a] respectively
        """
        color_string = color_string.replace(" ", "")  # Remove spaces
        color_string = color_string[color_string.find("(") + 1:-1]  # Remove 'rgb(' or 'rgba(' and ')'
        color_list = [int(c) for c in color_string.split(",")]  # Convert to list of integers
        return color_list

    def get_main_color(self, input_color: str) -> str:
        """
        Function to get the main color from RGB/RGBA input
        :param input_color: A list representing RGB (3 elements) or RGBA (4 elements) color
        :return: The name of the main color from predefined COLORS
        """
        input_color = self._parse_color_string(input_color)
        if len(input_color) == 4:  # If input is RGBA, ignore the alpha channel
            input_color = input_color[:3]

        distances = {color_name: distance.euclidean(input_color, rgb) for color_name, rgb in self.COLORS.items()}
        return min(distances, key=distances.get)

    # examples:
    # print(get_main_color('rgb(210, 0, 50)'))  # Outputs: 'RED'
    # print(get_main_color('rgba(43, 43, 43, 1)'))  # Outputs: 'BLACK'


def get_color(color: str) -> str:
    return ColorDetector().get_main_color(color)


