import os
import tempfile
import subprocess

import cough

TESTS_DIR = os.path.dirname(__file__)
BUILD_SCRIPT = os.path.join(TESTS_DIR, 'build.ps1')


def test_coff():
    module = cough.ObjectModule()

    # mov rax, 0; ret
    sec_aaaa = cough.Section(b'aaaa', cough.SectionFlags.MEM_EXECUTE, b'\x48\xC7\xC0\x00\x00\x00\x00\xC3')
    module.sections.append(sec_aaaa)

    sym1 = cough.SymbolRecord(b'main', section_number=1, storage_class=symbol.StorageClass.EXTERNAL)
    sym1.value = 0  # offset 0
    module.symbols.append(sym1)

    file_buffer = module.get_buffer()
    with tempfile.NamedTemporaryFile(suffix='.obj', delete=False) as file:
        file.write(file_buffer)
    base, _ = os.path.splitext(file.name)
    exe_path = base + '.exe'
    subprocess.run(['PowerShell.exe', BUILD_SCRIPT, file.name, '/out:' + '"' + exe_path + '"'], check=True)
    subprocess.run([exe_path], check=True)