# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: contracts.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x63ontracts.proto\x12\tcontracts\"t\n\x0bNewsMessage\x12\r\n\x05Title\x18\x01 \x01(\t\x12\x0c\n\x04\x42ody\x18\x02 \x01(\t\x12\x11\n\tTimestamp\x18\x03 \x01(\x03\x12\n\n\x02ID\x18\x04 \x01(\t\x12)\n\x02ML\x18\x05 \x01(\x0b\x32\x1d.contracts.ModelServiceAnswer\"?\n\rParsedArticle\x12\r\n\x05Title\x18\x01 \x01(\t\x12\x0c\n\x04\x42ody\x18\x02 \x01(\t\x12\x11\n\tTimestamp\x18\x03 \x01(\x03\"U\n\x12ModelServiceAnswer\x12+\n\nCategories\x18\x01 \x03(\x0b\x32\x17.contracts.CategoryInfo\x12\x12\n\nEmbeddings\x18\x02 \x03(\x01\"\\\n\x0c\x43\x61tegoryInfo\x12\x15\n\x08\x43\x61tegory\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bProbability\x18\x02 \x01(\x01H\x01\x88\x01\x01\x42\x0b\n\t_CategoryB\x0e\n\x0c_Probability2`\n\x0cModelService\x12P\n\x15GetModelServiceAnswer\x12\x16.contracts.NewsMessage\x1a\x1d.contracts.ModelServiceAnswer\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'contracts_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NEWSMESSAGE._serialized_start=30
  _NEWSMESSAGE._serialized_end=146
  _PARSEDARTICLE._serialized_start=148
  _PARSEDARTICLE._serialized_end=211
  _MODELSERVICEANSWER._serialized_start=213
  _MODELSERVICEANSWER._serialized_end=298
  _CATEGORYINFO._serialized_start=300
  _CATEGORYINFO._serialized_end=392
  _MODELSERVICE._serialized_start=394
  _MODELSERVICE._serialized_end=490
# @@protoc_insertion_point(module_scope)