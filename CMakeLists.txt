cmake_minimum_required(VERSION 3.0)
project(ActivitySdk)
IF(COMMAND TOOLCHAIN_INIT)
    TOOLCHAIN_INIT()
ENDIF()
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/build")
set(LIBRARY_OUTPUT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/build/lib")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated")
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    message("CMAKE_BUILD_TYPE: Debug")
    add_definitions(-DDEBUG)
    add_definitions(-DSODEBUG)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0")
elseif(CMAKE_BUILD_TYPE STREQUAL "Profile")
    message("CMAKE_BUILD_TYPE: Profile")
    add_definitions(-DNDEBUG)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O1")
else()
    message("CMAKE_BUILD_TYPE: Release")
    add_definitions(-DNDEBUG)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O3")
endif()

INCLUDE_DIRECTORIES(
	/usr/include/jsoncpp
	include
	/opt/aibee/opencv/include
	/opt/aibee/grpc/include
	/opt/aibee/protobuf/include
        /opt/aibee/opencv/include
)

# switch when build in linux, should use ln instead
include_directories(/root/scheduler)
include_directories(/root/tf_include)

# link_directories(${FACESDK_HOME}/lib)
link_directories(/root/body_sdk/percept/x86/3rd_lib/tensorrt)
link_directories(/opt/aibee/protobuf/lib)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../HTS/lib)
link_directories(${CMAKE_CURRENT_SOURCE_DIR}/../monitoring/lib)
link_directories(/opt/aibee/prometheus/usr/local/lib/)

file(GLOB_RECURSE CXX_SRCS "${CMAKE_SOURCE_DIR}/src/*.cpp" "${CMAKE_SOURCE_DIR}/face_processing/*.cpp" )
add_library(activitysdk SHARED ${CXX_SRCS})
set (extra_libs ${extra_libs} prometheusmetrics)
target_link_libraries(activitysdk ${LIBS} ${extra_libs} cryptofile ssl crypto dl pthread)

