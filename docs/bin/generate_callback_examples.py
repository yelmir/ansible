#!/usr/bin/env python
# (c) 2018 Sam Doran <sdoran@redhat.com>
# (c) 2018 Ansible Project
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import glob
import os
import six

from ansi2html import Ansi2HTMLConverter

_output_template = six.u("""<div class='callback-example f9 b9'>
<pre>
{body}
</pre>
</div>
""")


def convert_file(file, scheme='xterm', dark_bg=True, full=False, inline=True, ensure_trailing_newline=True):
    conv = Ansi2HTMLConverter(scheme=scheme, dark_bg=dark_bg, inline=inline)
    f = open(os.path.abspath(file), 'r')
    ansi = ' '.join(f.readlines())
    # ansi = conv.apply_regex(ansi)
    html = conv.convert(ansi, full=full, ensure_trailing_newline=ensure_trailing_newline)
    f.close()
    return html


def write_file(text, output_path):

    output_dir = os.path.dirname(output_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fname = output_path.replace('.ts', '.html')

    print('Writing file {}'.format(os.path.basename(fname)))

    with open(fname, 'w') as out:
        out.write(text)


def main():
    examples_dir = '../../docs/docsite/rst/plugins/callback_examples'
    example_files = glob.glob('{}/*.ts'.format(examples_dir))

    for file in example_files:
        html = convert_file(file)
        output_text = _output_template.format(body=html)

        write_file(output_text, file)

        # out = open(OUTPUT_DIR + '/' + file + '.html','w')
        # out.write(html)
        # f.close()
        # out.close()


if __name__ == '__main__':
    main()
