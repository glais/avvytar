from PIL import Image, ImageDraw, ImageFont

# Open the source image as the base avatar and set up for drawing on top
avatar = Image.open('resources/source.png')
draw = ImageDraw.Draw(avatar)

# Get the original size of the image
image_w, image_h = avatar.size

bold = 'resources/Montserrat-Bold.ttf'
semibold = 'resources/Montserrat-SemiBold.ttf'
minfontsize = 120
maxfontsize = 300
margin = image_w / 8
spacer = image_w / 100
writable_w = image_w - (margin * 2)
lines = []
domain = "coconautclub"

# Write .avax font
font = ImageFont.truetype(semibold, minfontsize)
tld = ".avax"
tld_w, tld_h = draw.textsize(tld, font)
loc_x = image_w - tld_w - margin
loc_y = image_h - tld_h - margin

# Shadow
draw.text((loc_x + 8, loc_y + 8), tld, '#111111', font=font)
draw.text((loc_x, loc_y), tld, '#cccccc', font=font)

# Write provisional domain to test size, using minimum font size to see if needs to be enlarged or split
font = ImageFont.truetype(bold, minfontsize)
domain_w, domain_h = draw.textsize(domain, font)

# If size of text is less than desired width, we can increase the size until up to 320
if domain_w < writable_w:
    fontsize = minfontsize
    while domain_w < writable_w and fontsize < maxfontsize:
        fontsize = fontsize + 1
        font = ImageFont.truetype(bold, fontsize)
        domain_w, domain_h = draw.textsize(domain, font)
    if domain_w > writable_w:
        fontsize = fontsize - 1
        font = ImageFont.truetype(bold, fontsize)
        domain_w, domain_h = draw.textsize(domain, font)
    else: 
        font = ImageFont.truetype(bold, fontsize)
        domain_w, domain_h = draw.textsize(domain, font)

# If size of text is more than desired width, we split lines, starting from length 10 which is how many m will fit for this font size
else:
    domainstring = domain
    remaining = len(domainstring)

    while remaining > 0:

        if remaining <= 10:
            linelength = remaining
            line = domainstring[0:len(domainstring)]
            line_w, line_h = draw.textsize(line, font)
            remaining = 0
        
        else:
            linelength = 10
            line = domainstring[0:linelength]
            line_w, line_h = draw.textsize(line, font)

            while line_w < writable_w and remaining > 0:
                linelength = linelength + 1
                line = domainstring[0:linelength]
                remaining = len(domainstring) - len(line)
                line_w, line_h = draw.textsize(line, font)

        if line_w > writable_w:
            lines.append(domainstring[0:linelength-1])
            domainstring = domainstring[linelength-1:len(domainstring)]
            remaining = remaining + 1
        else: 
            lines.append(domainstring[0:linelength])
            domainstring = domainstring[linelength:len(domainstring)]

# If we have multiple lines for a domain  
if lines:
    lineheight = minfontsize * 1.1
    numlines = len(lines)
    combined_h = lineheight + spacer + tld_h
    lineref = list(range(len(lines)-1, -1, -1))
    for num in range(0, numlines):
        multiple = num + 1
        line = lines[lineref[num]]
        line_w, line_h = draw.textsize(line, font)
        line_h = lineheight + spacer
        loc_x = image_w - line_w - margin
        loc_y = image_h - (line_h * multiple) - margin - tld_h
        draw.text((loc_x + 8, loc_y + 8), line, '#111111', font=font)
        draw.text((loc_x, loc_y), line, '#ffffff', font=font)

# If the domain is just one line
else:
    lineheight = fontsize * 1.1
    loc_x = image_w - domain_w - margin
    loc_y = image_h - lineheight - margin - spacer - tld_h
    draw.text((loc_x + 8, loc_y + 8), domain, '#111111', font=font)
    draw.text((loc_x, loc_y), domain, '#ffffff', font=font)

# Show avatar
avatar.resize((400,400), Image.ANTIALIAS)