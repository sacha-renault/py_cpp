import subprocess
import sys
import platform

def has_openmp():
    code = """
    #include <omp.h>
    int main() { return 0; }
    """
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode='w+', delete=True) as temp_file:
        temp_file.write(code)
        temp_file.flush()
        
        try:
            # Attempt to compile the test program with OpenMP flag
            subprocess.check_output([sys.executable, "-c", "from distutils.ccompiler import new_compiler; \
                                    compiler = new_compiler(); \
                                    compiler.compile(['{}'], extra_postargs=['-fopenmp'])".format(temp_file.name)],
                                    stderr=subprocess.STDOUT)
            openmp_available = True
        except subprocess.CalledProcessError:
            openmp_available = False
    return openmp_available

def get_openmp_flags():
    system = platform.system()

    if system == "Windows":
        # Windows
        return ['/openmp'], []
    elif system == "Darwin":
        # macOS (Apple's Clang does not support OpenMP by default)
        # You may need to install the LLVM version of Clang with brew to get OpenMP support
        return ['-Xpreprocessor', '-fopenmp'], ['-lomp']
    elif system == "Linux":
        # Linux
        return ['-fopenmp'], ['-fopenmp']
    else:
        # Other systems
        return [], []
