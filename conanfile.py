from conans import ConanFile, CMake, tools


class S2geometryConan(ConanFile):
    name = "s2geometry"
    version = "0.9.0"
    license = "Apache Liense 2.0"
    author = "Chris Collins <kuroneko@sysadninjas.net>"
    url = "https://github.com/kuroneko/conan-s2geometry"
    description = "S2 Geometry Library"
    topics = ("spherical geometry")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    build_requires = [
        "gtest/[>=1.8.0]"
    ]

    def source(self):
        git = tools.Git(folder="s2geometry")
        git.clone(url="https://github.com/google/s2geometry", branch="v%s"%(self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("s2geometry/CMakeLists.txt", "project(s2-geometry)",
                              '''project(s2-geometry)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder="s2geometry")
        return cmake        

    def build(self):
        cmake = self._configure_cmake()
        cmake.configure(source_folder="s2geometry")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["s2"]

