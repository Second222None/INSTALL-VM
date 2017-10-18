#!/bin/bash
# 123456 pwd
sed -i -r '/^ubuntu/s#ubuntu:([^:]+):(.*)#ubuntu:123456:\2#' shadow