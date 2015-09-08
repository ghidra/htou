
#
# This script is licensed as public domain.
#

# http://docs.python.org/2/library/struct.html

from xml.etree import ElementTree as ET
from xml.dom import minidom
import itertools
import os
import struct
import array
import logging
import binascii

log = logging.getLogger("ExportLogger")


def enum(**enums):
	return type('Enum', (), enums)
PathType = enum(
	ROOT        = "ROOT-",
	MODELS      = "MODE-",
	ANIMATIONS  = "ANIM-",
	TRIGGERS    = "TRIG-",
	MATERIALS   = "MATE-",
	TECHNIQUES  = "TECH-",
	TEXTURES    = "TEXT-",
	MATLIST     = "MATL-",
	OBJECTS     = "OBJE-",
	SCENES      = "SCEN-")

# Options for file utils
class FOptions:
	def __init__(self):
		self.useSubDirs = True
		self.fileOverwrite = False
		self.paths = {}
		self.exts = {
						PathType.MODELS : "mdl",
						PathType.ANIMATIONS : "ani",
						PathType.TRIGGERS : "xml",
						PathType.MATERIALS : "xml",
						PathType.TECHNIQUES : "xml",
						PathType.TEXTURES : "png",
						PathType.MATLIST : "txt",
						PathType.OBJECTS : "xml",
						PathType.SCENES : "xml"
					}
		self.preserveExtTemp = False


#--------------------
# Errors container
#--------------------
	
class ErrorsMem:
	def __init__(self):
		self.errors = {}
		self.seconds = []

	def Get(self, name, defaultValue = None):
		try:
			return self.errors[name]
		except KeyError:
			if defaultValue is not None:
				self.errors[name] = defaultValue
			return defaultValue

	def Delete(self, name):
		if name in self.errors:
			del self.errors[name]

	def Cleanup(self):
		emptyList = []
		for name in self.errors.keys():
			try:
				if not self.errors[name]:
					emptyList.append(name)
			except TypeError:
				pass
		for name in emptyList:
			del self.errors[name]

	def Names(self):
		return self.errors.keys()

	def Second(self, index):
		try:
			return self.seconds[index]
		except IndexError:
			return None

	def SecondIndex(self, second):
		try:
			return self.seconds.index(second)
		except ValueError:
			index = len(self.seconds)
			self.seconds.append(second)
			return index

	def Clear(self):
		self.errors.clear()
		self.seconds.clear()


#--------------------
# File utilities
#--------------------

# Get a file path for the object 'name' in a folder of type 'pathType'
def GetFilepath(pathType, name, fOptions):

	# Get the root path
	rootPath = fOptions.paths[PathType.ROOT]

	# Append the relative path to get the full path
	fullPath = rootPath
	if fOptions.useSubDirs:
		fullPath = os.path.join(fullPath, fOptions.paths[pathType])

	# Compose filename
	filename = name
	if type(filename) is list or type(filename) is tuple:
		filename = os.path.sep.join(filename)

	# Add extension to the filename, if present we can preserve the extension
	ext = fOptions.exts[pathType]
	if ext and (not fOptions.preserveExtTemp or os.path.extsep not in filename):
		filename += os.path.extsep + ext
		#filename = bpy.path.ensure_ext(filename, ".mdl")
	fOptions.preserveExtTemp = False

	# Replace all characters besides A-Z, a-z, 0-9 with '_'
	#filename = bpy.path.clean_name(filename)

	# Compose the full file path
	fileFullPath = os.path.join(fullPath, filename)

	# Get the Urho path (relative to root)
	fileUrhoPath = os.path.relpath(fileFullPath, rootPath)
	fileUrhoPath = fileUrhoPath.replace(os.path.sep, '/')

	# Return full file path and relative file path
	return (fileFullPath, fileUrhoPath)


# Check if 'filepath' is valid
def CheckFilepath(fileFullPaths, fOptions):

	fileFullPath = fileFullPaths
	if type(fileFullPaths) is tuple:
		fileFullPath = fileFullPaths[0]

	# Create the full path if missing
	fullPath = os.path.dirname(fileFullPath)
	if not os.path.isdir(fullPath):
		try:
			os.makedirs(fullPath)
			log.info( "Created path {:s}".format(fullPath) )
		except Exception as e:
			log.error("Cannot create path {:s} {:s}".format(fullPath, e))

	if os.path.exists(fileFullPath) and not fOptions.fileOverwrite:
		log.error( "File already exists {:s}".format(fileFullPath) )
		return False

	return True


#--------------------
# XML formatters
#--------------------

def FloatToString(value):
	return "{:g}".format(value)

def Vector3ToString(vector):
	return "{:g} {:g} {:g}".format(vector[0], vector[1], vector[2])

def Vector4ToString(vector):
	return "{:g} {:g} {:g} {:g}".format(vector[0], vector[1], vector[2], vector[3])

def XmlToPrettyString(elem):
	rough = ET.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough)
	pretty = reparsed.toprettyxml(indent="\t")
	i = pretty.rfind("?>")
	if i >= 0:
		pretty = pretty[i+2:]
	return pretty.strip()


#--------------------
# XML writers
#--------------------

# Write XML to a text file
def WriteXmlFile(xmlContent, filepath, fOptions):
	try:
		file = open(filepath, "w")
	except Exception as e:
		log.error("Cannot open file {:s} {:s}".format(filepath, e))
		return
	try:
		file.write(XmlToPrettyString(xmlContent))
	except Exception as e:
		log.error("Cannot write to file {:s} {:s}".format(filepath, e))
	file.close()


#--------------------
# Binary writers
#--------------------
#http://stackoverflow.com/questions/5649407/hexadecimal-string-to-byte-array-in-python

class BinaryFileWriter:

	# We try to write the file with a single API call to avoid
	# the Editor crashing while reading a not completed file.
	# We set the buffer to 1Mb (if unspecified is 64Kb, and it is
	# 8Kb with multiple file.write calls)

	# Constructor.
	def __init__(self):
		self.filename = None
		self.buffer = None
	
	# Open file stream.
	def open(self, filename):
		self.filename = filename
		self.buffer = array.array('B')
		return True

	def close(self):
		try:
			file = open(self.filename, "wb", 1024 * 1024)
		except Exception as e:
			log.error("Cannot open file {:s} {:s}".format(self.filename, e))
			return
		try:
			self.buffer.tofile(file)
		except Exception as e:
			log.error("Cannot write to file {:s} {:s}".format(self.filename, e))
		file.close()

	# Writes an ASCII string without terminator
	def writeAsciiStr(self, v):
		#self.buffer.extend(bytes(v, "ascii"))
		#a = array.array("B",v)
		self.buffer.extend(array.array("B",bytearray(v, "ascii")))
		#self.buffer.extend(bytearray(v, "ascii"))

	# Writes a 32 bits unsigned int
	def writeUInt(self, v):
		#a=[]
		#a.append(struct.unpack("<I",struct.pack("<I", v)))
		#self.buffer.extend(struct.pack("<I", v))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<I", v))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<I", v)))

	# Writes a 16 bits unsigned int
	def writeUShort(self, v):
		#a=[]
		#a.append(struct.unpack("<H",struct.pack("<H", v)))
		#self.buffer.extend(struct.pack("<H", v))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<H", v))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<H", v)))

	# Writes one 8 bits unsigned byte
	def writeUByte(self, v):
		#a=[]
		#a.append(struct.unpack("<B",struct.pack("<B", v)))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<B", v))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<B", v)))

	# Writes four 32 bits floats .w .x .y .z
	def writeQuaternion(self, v):
		#a=[]
		#a.append(struct.unpack("<4I",struct.pack("<4f", v.w, v.x, v.y, v.z)))
		#self.buffer.extend(struct.pack("<4f", v.w, v.x, v.y, v.z))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<4f", v.w, v.x, v.y, v.z))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<4f", v.w, v.x, v.y, v.z)))

	# Writes three 32 bits floats .x .y .z
	def writeVector3(self, v):
		#a=[]
		#a.append(struct.unpack("<3I",struct.pack("<3f", v.x, v.y, v.z)))
		#self.buffer.extend(struct.pack("<3f", v.x, v.y, v.z))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<3f", v.x, v.y, v.z))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<3f", v.x, v.y, v.z)))
	# Writes a 32 bits float
	def writeFloat(self, v):
		#a=[]
		#a.append(struct.unpack("<I",struct.pack("<f", v)))
		#self.buffer.extend(struct.pack("<f", v))
		#self.buffer.extend(list(itertools.chain.from_iterable(a)))
		a = array.array("B",struct.pack("<f", v))
		self.buffer.extend(a)
		#self.buffer.extend(bytearray.fromhex(struct.pack("<f", v)))

##-----float 32 to 16 bits
'''
#read half float from file and print float
h = struct.unpack(">H",file.read(struct.calcsize(">H")))[0]
fcomp = Float16Compressor()
temp = fcomp.decompress(h)
str = struct.pack('I',temp)
f = struct.unpack('f',str)[0]
print(f)

#write half float to file from float
fcomp = Float16Compressor()
f16 = fcomp.compress(float32)
file.write(struct.pack(">H",f16))
'''
class Float16Compressor:
    def __init__(self):
        self.temp = 0

    def compress(self,float32):
        F16_EXPONENT_BITS = 0x1F
        F16_EXPONENT_SHIFT = 10
        F16_EXPONENT_BIAS = 15
        F16_MANTISSA_BITS = 0x3ff
        F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
        F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

        a = struct.pack('>f',float32)
        b = binascii.hexlify(a)

        f32 = int(b,16)
        f16 = 0
        sign = (f32 >> 16) & 0x8000
        exponent = ((f32 >> 23) & 0xff) - 127
        mantissa = f32 & 0x007fffff

        if exponent == 128:
            f16 = sign | F16_MAX_EXPONENT
            if mantissa:
                f16 |= (mantissa & F16_MANTISSA_BITS)
        elif exponent > 15:
            f16 = sign | F16_MAX_EXPONENT
        elif exponent > -15:
            exponent += F16_EXPONENT_BIAS
            mantissa >>= F16_MANTISSA_SHIFT
            f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
        else:
            f16 = sign
        return f16

    def decompress(self,float16):
        s = int((float16 >> 15) & 0x00000001)    # sign
        e = int((float16 >> 10) & 0x0000001f)    # exponent
        f = int(float16 & 0x000003ff)            # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f = f << 1
                    e -= 1
                e += 1
                f &= ~0x00000400
                #print(s,e,f)
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return int((s << 31) | (e << 23) | f)