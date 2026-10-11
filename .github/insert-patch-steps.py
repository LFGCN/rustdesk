#!/usr/bin/env python3
"""Rebuild .github/workflows/flutter-build.yml from an upstream git ref and
re-insert the custom server config patch step after every named checkout."""
import re
import subprocess
import sys


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else 'upstream-1.5.0'
    path = '.github/workflows/flutter-build.yml'
    content = subprocess.check_output(
        ['git', 'show', ref + ':' + path]).decode('utf-8')
    pat = re.compile(
        r'^(?P<ind>[ ]+)- name: Checkout source code[ \t]*\r?\n'
        r'(?P=ind)  uses: actions/checkout@\S+.*\r?\n'
        r'(?P=ind)  with:\r?\n'
        r'(?P=ind)    submodules: recursive\r?\n',
        re.M)

    def rep(m):
        i = m.group('ind')
        return (m.group(0)
                + i + '- name: Patch custom server config\n'
                + i + '  shell: bash\n'
                + i + '  run: |\n'
                + i + '    PY="$(command -v python3 || command -v python)"\n'
                + i + '    "$PY" "$GITHUB_WORKSPACE/.github/patch-custom-server-config.py"\n\n')

    out, n = pat.subn(rep, content)
    if n < 10:
        sys.exit('unexpected named checkout count: %d' % n)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print('inserted %d patch steps after checkout blocks' % n)


if __name__ == '__main__':
    main()
