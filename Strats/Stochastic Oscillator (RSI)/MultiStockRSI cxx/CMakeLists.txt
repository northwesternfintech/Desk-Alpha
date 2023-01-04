cmake_minimum_required(VERSION 3.23)
project (MultiStockRSI_cxx)

set(CMAKE_CXX_STANDARD 14)

add_executable(MultiStockRSI_cxx main.cpp
               MultipleStock_RSI.cpp
               MultipleStock_RSI.h)
