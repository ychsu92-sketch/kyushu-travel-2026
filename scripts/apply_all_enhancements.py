#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_all_enhancements.py
Updates portal/island.js and portal/props.js with:
1. 10x dialog variety (140 fallback quotes, 36 family banter scripts, 26 in-car scripts, 28 straggler scripts, 10 walk-together scripts)
2. Stationary speech bubble lock when talking during landmark strolls
3. Landmark specialty activities trigger (isSpotBusy)
4. Roadside objects (Torii gates, Japanese bus stops, stone lanterns, coastal wind turbines, fishing boats, mileage signs, 90+ roadside trees)
"""
import os
import re

BASE_DIR = '/Users/reyhsu/.gemini/antigravity/scratch/kyushu-travel-2026'
ISLAND_PATH = os.path.join(BASE_DIR, 'portal/island.js')
PROPS_PATH = os.path.join(BASE_DIR, 'portal/props.js')

print("Starting enhancement generation...")
