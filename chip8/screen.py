"""
Copyright (C) 2012 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

A Chip 8 Screen - see the README file for more information.
"""
# I M P O R T S ###############################################################

import numpy as np
import pygame as pg
import struct

from pygame import display, HWSURFACE, DOUBLEBUF, Color, draw

# C O N S T A N T S ###########################################################

# Various screen modes
SCREEN_MODE_NORMAL = 'normal'
SCREEN_MODE_EXTENDED = 'extended'

# The height of the screen in pixels. Note this may be augmented by the
# scale_factor set by the initializer.
SCREEN_HEIGHT = {
    SCREEN_MODE_NORMAL: 32,
    SCREEN_MODE_EXTENDED: 64
}
DEFAULT_HEIGHT = SCREEN_HEIGHT[SCREEN_MODE_NORMAL]

# The width of the screen in pixels. Note this may be augmented by the
# scale_factor set by the initializer.
SCREEN_WIDTH = {
    SCREEN_MODE_NORMAL: 64,
    SCREEN_MODE_EXTENDED: 128
}
DEFAULT_WIDTH = SCREEN_WIDTH[SCREEN_MODE_NORMAL]

# The depth of the screen is the number of bits used to represent the color
# of a pixel.
SCREEN_DEPTH = 8

# The colors of the pixels to draw. The Chip 8 supports two colors: 0 (off)
# and 1 (on). The format of the colors is in RGBA format.
PIXEL_COLORS = {
    0: Color(0, 0, 0, 255),
    1: Color(250, 250, 250, 255)
}

# C L A S S E S ###############################################################

class Chip8Screen(object):
    """
    A class to emulate a Chip 8 Screen. The original Chip 8 screen was 64 x 32
    with 2 colors. In this emulator, this translates to color 0 (off) and color
    1 (on).
    """
    def __init__(self, scale_factor, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH):
        """
        Initializes the main screen. The scale factor is used to modify
        the size of the main screen, since the original resolution of the
        Chip 8 was 64 x 32, which is quite small.
n
        :param scale_factor: the scaling factor to apply to the screen
        :param height: the height of the screen
        :param width: the width of the screen
        """
        self.height = height
        self.width = width
        self.scale_factor = scale_factor
        self.surface = None
        self.surfaceArray = None

    
    def init_display(self):
        """
        Attempts to initialize a screen with the specified height and width.
        The screen will by default be of depth SCREEN_DEPTH, and will be
        double-buffered in hardware (if possible).
        """
        self.surface = display.set_mode(
            ((self.width * self.scale_factor),
             (self.height * self.scale_factor)),
            0,
            SCREEN_DEPTH)
        display.set_caption('CHIP8 Emulator')
        self.clear_screen()
        self.clear_array()
        self.update()

    @staticmethod
    def to_bytestring(pixels):
        def _to_bytestring(col):
            return struct.pack('BBBB', *PIXEL_COLORS[col])
        return ''.join(map(_to_bytestring, pixels.flatten()))

    def render_screen(self):
         """
         for x_pos in range(self.width):
            for y_pos in range(self.height):
                pixel_color = self.surfaceArray[x_pos][y_pos]
                x_base = x_pos * self.scale_factor
                y_base = y_pos * self.scale_factor
                draw.rect(self.surface,
                  PIXEL_COLORS[pixel_color],
                  (x_base, y_base, self.scale_factor, self.scale_factor))
         """
         pixels = np.array(self.surfaceArray)
         data = Chip8Screen.to_bytestring(pixels.T)
         texture = pg.image.frombuffer(data, (64, 32), 'RGBA')
         texture = pg.transform.scale(texture, (self.width * self.scale_factor, self.height * self.scale_factor))
         self.surface.blit(texture, texture.get_rect())
         
    def draw_pixel(self, x_pos, y_pos, pixel_color):
        """
        Turn a pixel on or off at the specified location on the screen. Note
        that the pixel will not automatically be drawn on the screen, you
        must call the update() function to flip the drawing buffer to the
        display. The coordinate system starts with (0, 0) being in the top
        left of the screen.

        :param x_pos: the x coordinate to place the pixel
        :param y_pos: the y coordinate to place the pixel
        :param pixel_color: the color of the pixel to draw
        """
        '''
        x_base = x_pos * self.scale_factor
        y_base = y_pos * self.scale_factor
        draw.rect(self.surface,
                  PIXEL_COLORS[pixel_color],
                  (x_base, y_base, self.scale_factor, self.scale_factor))
        '''
        self.surfaceArray[x_pos][y_pos] = pixel_color

    def get_pixel(self, x_pos, y_pos):
        """
        Returns whether the pixel is on (1) or off (0) at the specified
        location.

        :param x_pos: the x coordinate to check
        :param y_pos: the y coordinate to check
        :return: the color of the specified pixel (0 or 1)
        """
        '''
        x_scale = x_pos * self.scale_factor
        y_scale = y_pos * self.scale_factor
        '''
        return self.surfaceArray[x_pos][y_pos]

    def clear_screen(self):
        """
        Turns off all the pixels on the screen (writes color 0 to all pixels).
        """
        self.surface.fill(PIXEL_COLORS[0])
        self.clear_array()
        
    def clear_array(self):
        self.surfaceArray = [[0 for i in range(self.height)] for j in range(self.width)]

    @staticmethod
    def update():
        """
        Updates the display by swapping the back buffer and screen buffer.
        According to the pygame documentation, the flip should wait for a
        vertical retrace when both HWSURFACE and DOUBLEBUF are set on the
        surface.
        """
        display.flip()

    def get_width(self):
        """
        Returns the current value of the screen width.

        :return: the width of the screen
        """
        return self.width

    def get_height(self):
        """
        Returns the current value of the screen height.

        :return: the height of the screen
        """
        return self.height

    @staticmethod
    def destroy():
        """
        Destroys the current screen object.
        """
        display.quit()

    def set_extended(self):
        """
        Sets the screen mode to extended.
        """
        self.destroy()
        self.height = SCREEN_HEIGHT[SCREEN_MODE_EXTENDED]
        self.width = SCREEN_WIDTH[SCREEN_MODE_EXTENDED]
        self.init_display()

    def set_normal(self):
        """
        Sets the screen mode to normal.
        """
        self.destroy()
        self.height = SCREEN_HEIGHT[SCREEN_MODE_NORMAL]
        self.width = SCREEN_WIDTH[SCREEN_MODE_NORMAL]
        self.init_display()

    def scroll_down(self, num_lines):
        """
        Scroll the screen down by num_lines.
        
        :param num_lines: the number of lines to scroll down 
        """
        for y_pos in xrange(self.height - num_lines, -1, -1):
            for x_pos in xrange(self.width):
                pixel_color = self.get_pixel(x_pos, y_pos)
                self.draw_pixel(x_pos, y_pos + num_lines, pixel_color)

        # Blank out the lines above the ones we scrolled
        for y_pos in xrange(num_lines):
            for x_pos in xrange(self.width):
                self.draw_pixel(x_pos, y_pos, 0)

        self.update()

    def scroll_left(self):
        """
        Scroll the screen left 4 pixels.
        """
        for y_pos in xrange(self.height):
            for x_pos in xrange(4, self.width):
                pixel_color = self.get_pixel(x_pos, y_pos)
                self.draw_pixel(x_pos - 4, y_pos, pixel_color)

        # Blank out the lines to the right of the ones we just scrolled
        for y_pos in xrange(self.height):
            for x_pos in xrange(self.width - 4, self.width):
                self.draw_pixel(x_pos, y_pos, 0)

        self.update()

    def scroll_right(self):
        """
        Scroll the screen right 4 pixels.
        """
        for y_pos in xrange(self.height):
            for x_pos in xrange(self.width - 4, -1, -1):
                pixel_color = self.get_pixel(x_pos, y_pos)
                self.draw_pixel(x_pos + 4, y_pos, pixel_color)

        # Blank out the lines to the left of the ones we just scrolled
        for y_pos in xrange(self.height):
            for x_pos in xrange(4):
                self.draw_pixel(x_pos, y_pos, 0)

        self.update()

# E N D   O F   F I L E ########################################################
