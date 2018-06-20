from conans import ConanFile, tools
import os
import platform
import subprocess

class QtHelper:
    @staticmethod
    def package_id(conanFile):
        version_info = subprocess.check_output(['qmake', '--version'])
        conanFile.info.settings.compiler.qmake_version = version_info

    @staticmethod
    def make(conanFile, args=[]):
        if platform.system() == "Windows":
            conanFile.run("nmake %s" % " ".join(args))
        else:
            conanFile.run("make %s" % " ".join(args))

    @staticmethod
    def qmake(conanFile, args=[]):
        cmd = "qmake %s" % (" ".join(args))
        conanFile.run(cmd)

class QtSingleApplicationConan(ConanFile):
    name = "qtsingleapplication"
    version = "0.0.1"
    license = "BSD"
    url = "https://github.com/benlau/qt-solutions"
    description = "QtSingleApplication"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src*", "*.pri", "buildlib/*"

    def package_id(self):
        version_info = subprocess.check_output(['qmake', '--version'])
        self.info.settings.compiler.qmake_version = version_info

    def build(self):
        QtHelper.qmake(self, ["%s/buildlib/buildlib.pro" % self.source_folder])
        QtHelper.make(self)
        
    def package(self):
        self.copy("src/*.h", dst="include", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False, links=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Qt5Solutions_SingleApplication"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
