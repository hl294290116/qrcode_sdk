cmake_minimum_required(VERSION 2.8)
project( scan_image )

SET(CMAKE_INSTALL_PREFIX "build")

# zbar


add_definitions(" -std=c++11 -lstdc++ -lzbar")
set(CMAKE_VERBOSE_MAKEFILEON ON)
set(CMAKE_CXX_COMPILER "/usr/bin/g++")
message(“${CMAKE_CXX_COMPILER})

# opencv
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )


add_library(zbar SHARED IMPORTED)
set_target_properties(zbar PROPERTIES IMPORTED_LOCATION /usr/lib/x86_64-linux-gnu/libzbar.so.0.2.0 )
add_executable( QRCode scan_image.cpp )
# link_directories("/usr/lib/x86_64-linux-gnu")

target_link_libraries( QRCode PUBLIC ${OpenCV_LIBS} zbar)
