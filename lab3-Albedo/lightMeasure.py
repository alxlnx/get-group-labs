#!/usr/bin/python3
#  NOT REALLY MEASURING ANYTHING, IDK WHY THE FILE HAS THIS NAME

import lightFunctions as j

photoNames =  [ "mercury_white.png",
                "filament_blue_11.png",
                "filament_green_11.png",
                "filament_red_11.png",
                "filament_white_11.png",
                "filament_yellow_11.png" ]

j.readIntensity(photoNames[5], "test.png", "mercury", "white")