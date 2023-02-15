cmake_minimum_required(VERSION 2.8)
project( scan_image )
# zbar


add_definitions(" -std=c++11 -lstdc++ -lzbar")
set(CMAKE_VERBOSE_MAKEFILEON ON)
set(CMAKE_CXX_COMPILER "/usr/bin/g++")
message(“${CMAKE_CXX_COMPILER})

# opencv
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( QRCode QRCode.cpp )
# add_library("zbar" SHARED IMPORTED)
# set_target_properties("zbar" PROPERTIES LINKER_LANGUAGE CXX)

target_link_libraries( QRCode ${OpenCV_LIBS})
