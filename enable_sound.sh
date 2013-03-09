#!/bin/bash
sudo modprobe snd-bcm2835
amixer cset numid=3 1
