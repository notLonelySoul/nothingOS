from PIL import Image

def format_string(info: str, max_limit: int):
	
    cu = 0
    for i in info: cu += 1 if i.isupper() else cu
	
    if cu >= 10: max_limit-= 5
    if len(info) > max_limit: rs = info[:max_limit] + '...'
    else: rs = info
    return rs

def get_domme_color(img):
	# Get width and height of Image
	width, height = img.size

	# Initialize Variable
	r_total = 0
	g_total = 0
	b_total = 0

	count = 0

	# Iterate through each pixel
	for x in range(0, width):
		for y in range(0, height):
			# r,g,b value of pixel
			r, g, b = img.getpixel((x, y))

			r_total += r
			g_total += g
			b_total += b
			count += 1

	return (int(round(r_total/count, 0)), int(round(g_total/count, 0)), int(round(b_total/count, 0)))