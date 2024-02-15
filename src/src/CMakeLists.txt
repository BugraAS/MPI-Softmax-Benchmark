cmake_minimum_required(VERSION 3.11)

project(softmax)

find_package(MPI REQUIRED)
add_definitions(-DOMPI_SKIP_MPICXX)

add_executable(softmax "")

target_sources(softmax PRIVATE
    main.c
    utils.c
)

target_include_directories(softmax PRIVATE
    include
)

target_link_libraries(softmax PRIVATE
    m
    MPI::MPI_C
)