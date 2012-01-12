
project(ext_dynmod_example)

cmake_minimum_required(VERSION 2.6)

find_library(libSC "libSC" PATHS_SUFFIXES "../../lib")
find_library(libSCd "libSCd" PATHS_SUFFIXES "../../lib")

find_library(libPM "libPM" PATHS_SUFFIXES "../../lib")
find_library(libPMd "libPMd" PATHS_SUFFIXES "../../lib")

include_directories("../../include/libsc" "../../include/libtgf" "../../include/libsys" "../../include/libpm")
add_library(ext_dynmod SHARED cpp/ext_dynmod.cpp)
target_link_libraries(ext_dynmod debug ${libSCd} ${libPMd})
target_link_libraries(ext_dynmod optimized ${libSC} ${libPM})
