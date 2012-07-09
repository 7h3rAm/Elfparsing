#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2012-06 Jonathan Salwan - http://www.twitter.com/jonathansalwan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import Elfparsing.flags as flags
from struct import unpack

"""
Class Elf -  This class parse ELF file and return all informations
             about this format.
"""
class Elf(object):
   def __init__(self, filename=None):
      # Core
      self.filename     = None
      self.mmapBinary   = None

      # ElfHeader
      self.e_ident      = None
      self.e_type       = 0x0000
      self.e_machine    = 0x0000
      self.e_version    = 0x00000000L
      self.e_entry      = 0x0000000000000000L
      self.e_phoff      = 0x0000000000000000L
      self.e_shoff      = 0x0000000000000000L
      self.e_flags      = 0x00000000L
      self.e_ehsize     = 0x0000
      self.e_phentsize  = 0x0000
      self.e_phnum      = 0x0000
      self.e_shentsize  = 0x0000
      self.e_shnum      = 0x0000
      self.e_shstrndx   = 0x0000

      # Program Header
      self.phdr_l = []
      # Section Header
      self.shdr_l = []
      # Symbos Header
      self.sym_l = []

      if filename:
         self.loadFile(filename)

   """ Load Binary File """
   def loadFile(self, filename):
      self.filename = filename
      try:
         File = open(filename, "r")
         self.mmapBinary = File.read()
         File.close()
      except Exception, e:
         print e
         return (False)
      self.__setHeaderElf()
      self.__setShdr()
      self.__setPhdr()
      self.__setSym()
      return (True)

   """ Load Binary code """
   def loadCode(self, code):
      self.mmapBinary = code
      if self.mmapBinary == None:
         return (False)
      self.__setHeaderElf()
      self.__setShdr()
      self.__setPhdr()
      self.__setSym()
      return (True)

   """ Return binary maped """
   def getMmapBinary(self):
      if self.mmapBinary == None:
         print "Erro - getMmapBinary(): No file loaded"
      else:
         return (self.mmapBinary)

   """ Parse ELF header """
   def __setHeaderElf(self):
      try:
         self.e_ident   = self.mmapBinary[:15]
         self.e_type    = unpack("<H", self.mmapBinary[16:18])[0]
         self.e_machine = unpack("<H", self.mmapBinary[18:20])[0]
         self.e_version = unpack("<I", self.mmapBinary[20:24])[0]
         if unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS32:
            self.e_entry      = unpack("<I", self.mmapBinary[24:28])[0]
            self.e_phoff      = unpack("<I", self.mmapBinary[28:32])[0]
            self.e_shoff      = unpack("<I", self.mmapBinary[32:36])[0]
            self.e_flags      = unpack("<I", self.mmapBinary[36:40])[0]
            self.e_ehsize     = unpack("<H", self.mmapBinary[40:42])[0]
            self.e_phentsize  = unpack("<H", self.mmapBinary[42:44])[0]
            self.e_phnum      = unpack("<H", self.mmapBinary[44:46])[0]
            self.e_shentsize  = unpack("<H", self.mmapBinary[46:48])[0]
            self.e_shnum      = unpack("<H", self.mmapBinary[48:50])[0]
            self.e_shstrndx   = unpack("<H", self.mmapBinary[50:52])[0]
         elif unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS64:
            self.e_entry      = unpack("<Q", self.mmapBinary[24:32])[0]
            self.e_phoff      = unpack("<Q", self.mmapBinary[32:40])[0]
            self.e_shoff      = unpack("<Q", self.mmapBinary[40:48])[0]
            self.e_flags      = unpack("<I", self.mmapBinary[48:52])[0]
            self.e_ehsize     = unpack("<H", self.mmapBinary[52:54])[0]
            self.e_phentsize  = unpack("<H", self.mmapBinary[54:56])[0]
            self.e_phnum      = unpack("<H", self.mmapBinary[56:58])[0]
            self.e_shentsize  = unpack("<H", self.mmapBinary[58:60])[0]
            self.e_shnum      = unpack("<H", self.mmapBinary[60:62])[0]
            self.e_shstrndx   = unpack("<H", self.mmapBinary[62:64])[0]
         return True
      except:
         print "Error - setHeaderElf()"
         return False

   """ Parse Program header """
   def __setPhdr(self):
      if not self.isElf():
         return
      pdhr_num = self.e_phnum
      base = self.mmapBinary[self.e_phoff:]
      try:
         for i in range(pdhr_num):
            if unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS32:
               phdr = {
                        'p_type'    : unpack("<I", base[0:4])[0],
                        'p_offset'  : unpack("<I", base[4:8])[0],
                        'p_vaddr'   : unpack("<I", base[8:12])[0],
                        'p_paddr'   : unpack("<I", base[12:16])[0],
                        'p_filesz'  : unpack("<I", base[16:20])[0],
                        'p_memsz'   : unpack("<I", base[20:24])[0],
                        'p_flags'   : unpack("<I", base[24:28])[0],
                        'p_align'   : unpack("<I", base[28:32])[0]
                      }
            elif unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS64:
               phdr = {
                        'p_type'    : unpack("<I", base[0:4])[0],
                        'p_offset'  : unpack("<I", base[4:8])[0],
                        'p_vaddr'   : unpack("<Q", base[8:16])[0],
                        'p_paddr'   : unpack("<Q", base[16:24])[0],
                        'p_filesz'  : unpack("<Q", base[24:32])[0],
                        'p_memsz'   : unpack("<Q", base[32:40])[0],
                        'p_flags'   : unpack("<Q", base[40:48])[0],
                        'p_align'   : unpack("<Q", base[48:56])[0]
                      }
            self.phdr_l.append(phdr)
            base = base[self.e_phentsize:]
      except:
         print "Error setPhdr() - in parsing Phdr"
         return False
      return True

   """ Parse Section header """
   def __setShdr(self):
      if not self.isElf():
         return
      shdr_num = self.e_shnum
      base = self.mmapBinary[self.e_shoff:]
      for i in range(shdr_num):
         try:
            if unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS32:
               shdr = {
                        'str_name'     : None,
                        'sh_name'      : unpack("<I", base[0:4])[0],
                        'sh_type'      : unpack("<I", base[4:8])[0],
                        'sh_flags'     : unpack("<I", base[8:12])[0],
                        'sh_addr'      : unpack("<I", base[12:16])[0],
                        'sh_offset'    : unpack("<I", base[16:20])[0],
                        'sh_size'      : unpack("<I", base[20:24])[0],
                        'sh_link'      : unpack("<I", base[24:28])[0],
                        'sh_info'      : unpack("<I", base[28:32])[0],
                        'sh_addralign' : unpack("<I", base[32:36])[0],
                        'sh_entsize'   : unpack("<I", base[36:40])[0]
                     }
            elif unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS64:
               shdr = {
                        'str_name'     : None,
                        'sh_name'      : unpack("<I", base[0:4])[0],
                        'sh_type'      : unpack("<I", base[4:8])[0],
                        'sh_flags'     : unpack("<Q", base[8:16])[0],
                        'sh_addr'      : unpack("<Q", base[16:24])[0],
                        'sh_offset'    : unpack("<Q", base[24:32])[0],
                        'sh_size'      : unpack("<Q", base[32:40])[0],
                        'sh_link'      : unpack("<Q", base[40:48])[0],
                        'sh_info'      : unpack("<Q", base[48:56])[0],
                        'sh_addralign' : unpack("<Q", base[56:64])[0],
                        'sh_entsize'   : unpack("<Q", base[64:72])[0]
                     }
            self.shdr_l.append(shdr)
            base = base[self.e_shentsize:]
         except:
            print "Error setShdr() - in parsing String table"
            return False

      # set name in section table from string table
      string_table =  self.mmapBinary[(self.shdr_l[self.e_shstrndx]["sh_offset"]):]
      for i in range(shdr_num):
         self.shdr_l[i]["str_name"] = string_table[self.shdr_l[i]["sh_name"]:].split('\0')[0]
      return True

   """ Parse Symbols header """
   def __setSym(self):
      off_string_table = self.getSectionDataByName(".strtab", "sh_offset")
      off_sym_table = self.getSectionDataByName(".symtab", "sh_offset")
      symbols_size = self.getSectionDataByName(".symtab", "sh_entsize")
      symbols_num = self.getSectionDataByName(".symtab", "sh_size")

      if off_string_table == False or off_sym_table == False:
         #print "No symbols table found"
         return False

      if not symbols_num or not symbols_size:
         symbols_num = 0
      else:
         symbols_num /= symbols_size
      string_t = self.mmapBinary[off_string_table:]
      symbols_t = self.mmapBinary[off_sym_table:]
      for i in range(symbols_num):
         try:
            if unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS32:
               sym = {
                        'str_name'  : None,
                        'st_name'   : unpack("<I", symbols_t[0:4])[0],
                        'st_value'  : unpack("<I", symbols_t[4:8])[0],
                        'st_size'   : unpack("<I", symbols_t[8:12])[0],
                        'st_info'   : unpack("<B", symbols_t[12:13])[0],
                        'st_other'  : unpack("<B", symbols_t[13:14])[0],
                        'st_shndx'  : unpack("<H", symbols_t[14:16])[0]
                     }
            elif unpack("<B", self.e_ident[flags.EI_CLASS])[0] == flags.ELFCLASS64:
               sym = {
                        'str_name'  : None,
                        'st_name'   : unpack("<I", symbols_t[0:4])[0],
                        'st_info'   : unpack("<B", symbols_t[4:5])[0],
                        'st_other'  : unpack("<B", symbols_t[5:6])[0],
                        'st_shndx'  : unpack("<H", symbols_t[6:8])[0],
                        'st_value'  : unpack("<Q", symbols_t[8:16])[0],
                        'st_size'   : unpack("<Q", symbols_t[16:24])[0]
                     }
            self.sym_l.append(sym)
            symbols_t = symbols_t[symbols_size:]
         except:
            print "Error setSym() - in parsing Symbols table"
            return False

      # set name in sym table from string table
      for i in range(symbols_num):
         self.sym_l[i]["str_name"] = string_t[self.sym_l[i]["st_name"]:].split('\0')[0]
      return True

   """ Return false or true if is a ELF file """
   def isElf(self):
      try:
         if self.mmapBinary[:4] == "\x7fELF":
            return True
         else:
            return False
      except:
         print "Error - isElf()"

   """ Return architecture code """
   def getArch(self):
      try:
         return (hex(unpack("<B", self.e_ident[flags.EI_CLASS])[0]))
      except:
         print "Error - getArch()"

   def getEtype(self):
      return (self.e_type)

   def getEmachine(self):
      return (self.e_machine)

   def getEversion(self):
      return (self.e_version)

   def getEentry(self):
      return (self.e_entry)

   def getEntryPoint(self):
      return (self.getEentry())

   def getEphoff(self):
      return (self.e_phoff)

   def getEshoff(self):
      return (self.e_shoff)

   def getEflags(self):
      return (self.e_flags)

   def getEehsize(self):
      return (self.e_ehsize)

   def getEphentsize(self):
      return (self.e_phentsize)

   def getEphnum(self):
      return (self.e_phnum)

   def getEshentsize(self):
      return (self.e_shentsize)

   def getEshnum(self):
      return (self.e_shnum)

   def HowManySections(self):
      return (self.getEshnum())

   def getEshstrndx(self):
      return (self.e_shstrndx)

   def getPhdrList(self):
      return (self.phdr_l)

   def getShdrList(self):
      return (self.shdr_l)

   def getSymList(self):
      return (self.sym_l)

   """ Return True or False if symbols were found in binary """
   def symbolsFound(self):
      if not self.sym_l:
         return (False)
      return (True)

   """
   Return section header by Name.
   Exemple - getSectionByName(".text")
   """
   def getSectionByName(self, section_name):
      for shdr in self.shdr_l:
         if shdr["str_name"] == section_name:
            return shdr
      return None

   """
   Return section data by Name.
   Exemple - getSectionDataByName(".text", "sh_addr")
   """
   def getSectionDataByName(self, section_name, data):
      shdr_num = self.e_shnum
      for i in range(shdr_num):
         if self.shdr_l[i]["str_name"] == section_name:
            try:
               return (self.shdr_l[i][data])
            except:
               print "Error - getSectionDataByName() - No '%s' in Shdr" %(data)
      return None

   """
   Return section data by addr.
   Exemple - getSectionDataByAddr(0x8049080, "str_name")
   This exemple return the string name of section 0x8049080
   'str_name' is real string name based on 'sh_name' in string table.
   """
   def getSectionDataByAddr(self, section_addr, data):
      shdr_num = self.e_shnum
      for i in range(shdr_num):
         if self.shdr_l[i]["sh_addr"] == section_addr:
            try:
               return (self.shdr_l[i][data])
            except:
               print "Error - getSectionDataByAddr() - No '%s' in Shdr" %(data)
      return None

   """
   Return section opcodes by name.
   section_text = extractSectionByName(".text")
   After, 'section_text' contains all opcodes of this section.
   """
   def extractSectionByName(self, section_name):
      size = self.getSectionDataByName(section_name, "sh_size")
      offset = self.getSectionDataByName(section_name, "sh_offset")
      try:
         return (self.mmapBinary[offset:offset+size])
      except:
         print "Error - extractSectionByName() - out of range"

   """
   Return section opcodes by name.
   section_text = extractSectionByAddr(0x8049080)
   After, 'section_text' contains all opcodes of this section.
   """
   def extractSectionByAddr(self, section_addr):
      size = self.getSectionDataByAddr(section_addr, "sh_size")
      offset = self.getSectionDataByAddr(section_addr, "sh_offset")
      try:
         return (self.mmapBinary[offset:offset+size])
      except:
         print "Error - extractSectionByName() - out of range"

   """ Return number of entry in symbols table """
   def HowManyEntrySymbols(self):
      return (len(self.sym))

   """
   Return addr by symbol name.
   Ex: addr_main = getSymbolAddrByName("main")
   """
   def getSymbolAddrByName(self, sym_name):
      for sym in self.sym_l:
         if sym["str_name"] == sym_name:
            return sym["st_value"]
      return None

   """
   Return name by symbol addr.
   Ex: name = getSymbolNameByAddr(0x8049090)
   """
   def getSymbolNameByAddr(self, sym_addr):
      for sym in self.sym_l:
         if sym["st_value"] == sym_addr:
            return sym["str_name"]
      return None

   """
   Return symbol by symbol name.
   Ex: sym = getSymbolByName("main")
   """
   def getSymbolByName(self, sym_name):
      for sym in self.sym_l:
         if sym["str_name"] == sym_name:
            return sym
      return None
