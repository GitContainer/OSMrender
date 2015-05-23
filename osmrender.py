import sqlite3, math
from PIL import Image, ImageDraw, ImageFont

con = sqlite3.connect('test.db')

with con:
  cur = con.cursor()
  cur.execute('SELECT * FROM bounds')
  bounds = cur.fetchall()
  minlat, minlon, maxlat, maxlon = bounds[0]

  imgwidth = 1920.0
  imgheight = 1080.0
  latdist = 111.3    #distance between two latitudes in km
  londist = math.cos((maxlat - minlat + minlat) * (math.pi / 180.0)) * latdist
  
  xdist = maxlon - minlon
  if (xdist < 0):
    xdist = xdist * -1
  lonkm = xdist * londist  #map x distance in km
  
  ydist = maxlat - minlat
  if (ydist < 0):
    ydist = ydist * -1
  latkm = ydist * latdist  #map y distance in km
  
  imgratio = imgwidth / imgheight  #1920.0 / 1080.0 = 1.777
  osmratio = lonkm / latkm
  
  height = imgheight
  width = imgwidth
  if osmratio > imgratio:
    height = imgwidth * osmratio  #decrease height to keep the ratio
  elif osmratio < imgratio:
    width = imgheight * osmratio  #decrease width to keep the ratio
  
  pxfactor = width / lonkm    #pixel per km

  #create white image
  imagebuffer = Image.new('RGBA', (1920,1080), 'white')
  #create a draw object
  drawbuffer = ImageDraw.Draw(imagebuffer)
  
  cur.execute('SELECT id, v FROM way_tag WHERE k = "highway"')
  highways = cur.fetchall()
  nhw = len(highways)
  for h in range(0, nhw):
    id = highways[h][0]
    v = highways[h][1]
    cur.execute('SELECT n.lat, n.lon FROM way_nd as w JOIN node as n ON w.ref = n.id WHERE w.id = (?)', (id,))
    points = cur.fetchall()
    np = len(points)
    for i in range(0, np):
      lat, lon = points[i]
      x = int((lon - minlon) * londist * pxfactor)
      y = int((maxlat - lat) * latdist * pxfactor)
      points[i] = x, y
    if v == 'motorway' or v == 'motorway_link' or v == 'trunk' or v == 'trunk_link' or v == 'primary' or v == 'primary_link':
      width = 8
      color = 'red'
    elif v == 'secondary' or v == 'tertiary':
      width = 6
      color = 'blue'
    elif v == 'residential' or v == 'living_street' or v == 'unclassified' or v == 'service':
      width = 4
      color = 'blue'
    elif v == 'track' or v == 'bridleway' or v == 'cycleway' or v == 'footway' or v == 'path' or v == 'pedestrian' or v == 'steps':
      width = 2
      color = 'lightgrey'
    elif v == 'road':
      width = 2
      color = 'black'
    else:
      width = 3
      color = 'lime'
    for i in range(0, np-1):
      drawbuffer.line((points[i][0], points[i][1], points[i+1][0], points[i+1][1]), fill=color, width=width)
  imagebuffer.show()

  #save image
  #imagebuffer.save('test.jpg', 'JPEG', quality=95)
