from cx_Freeze import setup, Executable

setup(
    name="Image Enhancer",
    version="1.0",
    description="Aplikasi penjernih gambar",
    executables=[Executable("app.py")],
)