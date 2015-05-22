#coding: utf-8

#Convert OSM v0.6 (XML) to a lightweight sqlite3 database.
#Several fields (visible, timestamp, user, ...) are missing, but you get a small db.
#This python script need some time to process big files. You might like to run it on a PC/MAC.

from xml.sax import make_parser, handler
import sqlite3

class OsmHandler(handler.ContentHandler):

	def __init__(self):
		self.write_nodes = False
		self.write_ways = False
		self.write_relations = False
		self.tag_id = -1
		self.tag_parent = "osm"
		self.con = sqlite3.connect("test.db")
		self.cur = self.con.cursor()
		#First delete all records in all tables
		self.cur.execute("DELETE FROM osm")
		self.cur.execute("DELETE FROM bounds")
		self.cur.execute("DELETE FROM node")
		self.cur.execute("DELETE FROM node_tag")
		self.cur.execute("DELETE FROM way")
		self.cur.execute("DELETE FROM way_nd")
		self.cur.execute("DELETE FROM way_tag")
		self.cur.execute("DELETE FROM relation")
		self.cur.execute("DELETE FROM relation_member")
		self.cur.execute("DELETE FROM relation_tag")
		self.con.commit()
	
	def startElement(self, name, attrs):
		if name == "node":
			if self.write_nodes == False:
				self.write_nodes = True
				print "Writing Nodes"
			self.tag_parent = "node"
			if "id" in attrs:
				self.tag_id = long(attrs["id"])
			if "lat" in attrs:
				lat = float(attrs["lat"])
			if "lon" in attrs:
				lon = float(attrs["lon"])
			self.cur.execute("INSERT INTO node VALUES (?, ?, ?)", (self.tag_id, lat, lon))
			self.con.commit()
		elif name == "tag":
			if "k" in attrs:
				k = attrs["k"]
			if "v" in attrs:
				v = attrs["v"]
			#tag_parent = node, way or relation
			s = "INSERT INTO " + self.tag_parent + "_tag VALUES (?, ?, ?)"
			self.cur.execute(s, (self.tag_id, k, v))
			self.con.commit()
		elif name == "way":
			if self.write_ways == False:
				self.write_ways = True
				print "Writing Ways"
			self.tag_parent = "way"
			if "id" in attrs:
				self.tag_id = long(attrs["id"])
			self.cur.execute("INSERT INTO way VALUES ("+ str(self.tag_id) + ")")
			self.con.commit()
		elif name == "nd":
			if "ref" in attrs:
				ref = long(attrs["ref"])
			#tag_parent = way
			self.cur.execute("INSERT INTO way_nd VALUES (?, ?)", (self.tag_id, ref))
			self.con.commit()
		elif name == "relation":
			if self.write_relations == False:
				self.write_relations = True
				print "Writing Relations"
			self.tag_parent = "relation"
			if "id" in attrs:
				self.tag_id = long(attrs["id"])
			self.cur.execute("INSERT INTO relation VALUES (" + str(self.tag_id) + ")")
			self.con.commit()
		elif name == "member":
			if "type" in attrs:
				type = attrs["type"]
			if "ref" in attrs:
				ref = long(attrs["ref"])
			if "role" in attrs:
				role = attrs["role"]
			#tag_parent = relation
			self.cur.execute("INSERT INTO relation_member VALUES (?, ?, ?, ?)", (self.tag_id, type, ref, role))
			self.con.commit()
		elif name == "osm":
			if "version" in attrs:
				version = attrs["version"]
			if "generator" in attrs:
				generator = attrs["generator"]
			if "copyright" in attrs:
				copyright = attrs["copyright"]
			if "license" in attrs:
				license = attrs["license"]
			self.cur.execute("INSERT INTO osm VALUES (?, ?, ?, ?)", (version, generator, copyright, license))
			self.con.commit()
		elif name == "bounds":
			if "minlat" in attrs:
				minlat = float(attrs["minlat"])
			if "minlon" in attrs:
				minlon = float(attrs["minlon"])
			if "maxlat" in attrs:
				maxlat = float(attrs["maxlat"])
			if "maxlon" in attrs:
				maxlon = float(attrs["maxlon"])
			self.cur.execute("INSERT INTO bounds VALUES (?, ?, ?, ?)", (minlat, minlon, maxlat, maxlon))
			self.con.commit()
		else:
			print "Tag-Name: " + name + " is not supported, yet!"

	def endElement(self, name):
		if name == "node" or name == "way" or name == "relation":
			self.tag_parent = "osm"
			
	def __del__(self):
		self.con.close()
				
parser = make_parser()
oh = OsmHandler()
parser.setContentHandler(oh)
parser.parse("map.osm")
print "Finished"
