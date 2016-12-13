import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name='progrotron',
    options={"build_exe":{"packages":["pygame"], "include_files":["2084.png", "progrotron_title.png", "sprites/"]}},
    executables=executables
)