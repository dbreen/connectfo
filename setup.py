from cx_Freeze import setup, Executable

setup(
        name = "connectfo",
        version = "0.1",
        description = "Connect Fo'!",
        executables = [Executable("connectfo.py")],
        includes = ('game',)
)
