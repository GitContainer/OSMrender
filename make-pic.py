from PIL import Image, ImageDraw, ImageFont

#create white image
imagebuffer = Image.new('RGBA', (1920,1080), 'white')
#create a draw object
drawbuffer = ImageDraw.Draw(imagebuffer)

drawbuffer.line((50,50,1870,1030), fill='blue', width=5)
font1 = ImageFont.truetype('Helvetica', 36)
font2 = ImageFont.truetype('Courier', 60)
drawbuffer.text((50,400), 'test', fill='black', font=font1)
drawbuffer.text((50,500), 'test', fill='green', font=font2)
drawbuffer.ellipse((500,500,600,600), fill=(255,0,0))
drawbuffer.ellipse((550,550,650,650), fill=(255,128,0))
drawbuffer.ellipse((600,600,700,700), fill=(255,128,128))
drawbuffer.polygon((800,800,800,900,900,800,900,900,800,800), fill='yellow', outline='red')
drawbuffer.rectangle((900,100,1000,200), fill='lime', outline='black')
drawbuffer.rectangle((1000,200,1100,300), fill='lime')
drawbuffer.rectangle((1100,300,1200,400), fill='lime', outline='black')

#save image
imagebuffer.save('test.jpg', 'JPEG', quality=95)
imagebuffer.show()
