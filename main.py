import json
from PIL import Image

def text_to_gif(tile_type, input_string, user_id):
    with open('assets/alphabet.json', 'r', encoding='utf-8') as file:
        alphabet = json.load(file)


    background_image = Image.open('assets/background.jpg')
    background_size = background_image.size
    tile = Image.open(tile_type).resize((48, 66)).convert('RGBA')
    gif_path = f'res/res_{user_id}.gif'

    letter_spacing = 48
    input_string = input_string.upper()

    total_width = 0
    letter_widths = {}
    unknown_symbols = []

    for letter in input_string:
        if letter in alphabet:
            letter_length = max(coords[0] for coords in alphabet[letter]) + 1
            letter_widths[letter] = letter_length * tile.size[0]
            total_width += letter_widths[letter]
        else:
            unknown_symbols.append(letter)

    if unknown_symbols:
        print(f"Unknown symbols: {unknown_symbols}")

    total_width += (len(input_string) - 1) * letter_spacing

    frames = []
    start_x = background_size[0] + 1
    for x_offset in range(start_x, 180 - total_width, -letter_spacing):
        frame = background_image.copy()
        current_x = x_offset
        for letter in input_string:
            if letter in alphabet:
                for x, y in alphabet[letter]:
                    x_position = x * tile.size[0] + current_x
                    y_position = y * tile.size[1] + 108
                    if 180 <= x_position < background_size[0]:
                        frame.paste(tile, (x_position, y_position), tile)
                current_x += letter_widths[letter] + letter_spacing
        frames.append(frame)


    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=True
    )

    return gif_path, unknown_symbols
