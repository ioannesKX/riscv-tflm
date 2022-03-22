# Lint as: python2, python3
# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Library for converting .tflite and .bmp files to cc arrays"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import argparse
import os


def generate_file(out_fname, array_name, out_string, size):
  ''' Write the out string containing an array of values to a variable in a cc
        file, and create a header file defining the same array. '''
  os.makedirs(os.path.dirname(out_fname), exist_ok=True)
  if out_fname.endswith('.cc'):
    out_cc_file = open(out_fname, 'w')
    # Log cc file name for Make to include in the build.
    out_cc_file.write('#include "' +
                      out_fname.split("genfiles/")[-1].replace('.cc', '.h') +
                      '"\n\n')
    out_cc_file.write('alignas(16) const unsigned char ' + array_name +
                      '[] = {')
    out_cc_file.write(out_string)
    out_cc_file.write('};\n')
    out_cc_file.write('const unsigned int ' + array_name + '_size = ' +
                      str(size) + ';')
    out_cc_file.close()
  elif out_fname.endswith('.h'):
    out_hdr_file = open(out_fname, 'w')
    out_hdr_file.write('extern const unsigned char ' + array_name + '[];\n')
    out_hdr_file.write('extern const unsigned int ' + array_name + '_size' +
                       ';')
    out_hdr_file.close()
  else:
    raise ValueError('input file must be .tflite, .bmp')


def generate_array(input_fname):
  ''' Return array size and string containing an array of data from the input file. '''
  if input_fname.endswith('.tflite'):
    with open(input_fname, 'rb') as input_file:
      out_string = ''
      byte = input_file.read(1)
      size = 0
      while (byte != b''):
        out_string += '0x' + byte.hex() + ','
        byte = input_file.read(1)
        size += 1
      return [size, out_string]
  elif input_fname.endswith('.bmp'):
    img = Image.open(input_fname, mode='r')
    image_bytes = img.tobytes()
    out_string = ""
    for byte in image_bytes:
      out_string += hex(byte) + ","
    return [len(image_bytes), out_string]
  else:
    raise ValueError('input file must be .tflite, .bmp')


def array_name(input_fname):
  base_array_name = 'g_' + input_fname.split('.')[0].split('/')[-1]
  if input_fname.endswith('.tflite'):
    return base_array_name + '_model_data'
  elif input_fname.endswith('.bmp'):
    return base_array_name + '_image_data'


def main():
  """Create cc sources with c arrays with data from each .tflite or .bmp."""
  parser = argparse.ArgumentParser()
  parser.add_argument(
      'output',
      help='base directory for all outputs or a cc or header to generate.')
  parser.add_argument(
      'inputs',
      nargs='+',
      help=
      'input bmp or tflite files to convert. If output is a cc or header only one input may be specified.'
  )
  args = parser.parse_args()

  if args.output.endswith('.cc') or args.output.endswith('.h'):
    assert (len(args.inputs) == 1)
    size, cc_array = generate_array(args.inputs[0])
    generated_array_name = array_name(args.inputs[0])
    generate_file(args.output, generated_array_name, cc_array, size)
  else:
    # Deduplicate inputs to prevent duplicate generated files (ODR issue).
    for input_file in list(dict.fromkeys(args.inputs)):
      output_base_fname = os.path.join(args.output, input_file.split('.')[0])
      if input_file.endswith('.tflite'):
        output_base_fname = output_base_fname + '_model_data'
      elif input_file.endswith('.bmp'):
        output_base_fname = output_base_fname + '_image_data'
      else:
        raise ValueError('input file must be .tflite, .bmp')

      output_cc_fname = output_base_fname + '.cc'
      # Print output cc filename for Make to include it in the build.
      print(output_cc_fname)
      output_hdr_fname = output_base_fname + '.h'
      size, cc_array = generate_array(input_file)
      generated_array_name = array_name(input_file)
      generate_file(output_cc_fname, generated_array_name, cc_array, size)
      generate_file(output_hdr_fname, generated_array_name, cc_array, size)


if __name__ == '__main__':
  main()
