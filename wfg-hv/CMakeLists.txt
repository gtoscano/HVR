cmake_minimum_required(VERSION 3.14)
project(wfg)

include(FetchContent)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

SET(CMAKE_CXX_FLAGS "-O3 -march=native")

set(THREADS_PREFER_PTHREAD_FLAG ON)

find_package(Threads REQUIRED)

file(GLOB_RECURSE SRC_FILES src/wfg.c src/read.c)

add_executable(wfg ${SRC_FILES})

target_include_directories(wfg PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(wfg PUBLIC Threads::Threads )
install(TARGETS wfg RUNTIME DESTINATION /usr/local/bin)

