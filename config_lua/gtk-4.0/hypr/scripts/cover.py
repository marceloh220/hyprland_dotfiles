#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_cover():
    with open('/tmp/cover', 'r') as f:
        return f.read().strip()