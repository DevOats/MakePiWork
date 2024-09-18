import framebuf

# Draws a 7 segment numerical display on the specified frame buffer
class SevenSegmentDigit():
    
    
    #Creates a 7 segment numerical display on the specified frame buffer
    def __init__(self,
                 frameBuf: framebuf.FrameBuffer,
                 x: int,
                 y: int,
                 width: int = 25,
                 height: int = 50,
                 segmentThickness: int = 6):
    
        self.buff = frameBuf
        self.currentNumber = 0
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # The thickness of a segment
        self.segWidth = segmentThickness
    
    
    # Draws the specified number on the display.
    # The number should be an integer from 0 to 9. Other values will be ignored
    def displayNumber(self, number: int):
        self.currentNumber = number
        self.__drawSegments(number)
        

    def setX(self, x: int):
        self.x = x
    
    
    def __drawSegments(self, number: int):
        sw = self.segWidth
    
        
        segALit = number in {0, 2, 3, 5, 6, 7, 8, 9}
        segBLit = number in {0, 1, 2, 3, 4, 7, 8, 9}
        segCLit = number in {0, 1, 3, 4, 5, 6, 7, 8, 9}
        segDLit = number in {0, 2, 3, 5, 6, 8, 9}
        segELit = number in {0, 2, 6, 8}
        segFLit = number in {0, 4, 5, 6, 8, 9}
        segGLit = number in {2, 3, 4, 5, 6, 8, 9}
        
        topVertY = self.y + int(sw / 2)
        bottomVertY = self.y + int(self.height / 2) + int(0 * sw) + 1
        
        # Vertical segment height
        vertSegHight = int(self.height / 2) - int(0.5 * sw) - 1
        
        horizSegX = self.x + int(0.5 * sw)
        horizSegWidth = self.width - (1 * sw)
        
        # Boundary rectangle for debugging and development
        # self.buff.rect(self.x, self.y, self.width, self.height, True)
        
        # Draw the segments in two passes.
        # First draw the segments that are lit. Then the segments that shoud be dark.
        # This creates a consistent effect at the ends of the segments
        passIndex = 0
        while (passIndex <= 2):
            drawLitSegments = passIndex == 0
            passIndex += 1
            
            # A segment (top horizontal)
            if(segALit == drawLitSegments):
                self.buff.rect(horizSegX,
                               self.y,
                               horizSegWidth,
                               sw,
                               segALit,
                               1)
            
            # B segment (right top vertical)
            if(segBLit == drawLitSegments):
                self.buff.rect(self.x + self.width - sw,
                               topVertY,
                               sw,
                               vertSegHight,
                               segBLit,
                               1)
                
            # C segment (right bottom vertical
            if(segCLit == drawLitSegments):
                self.buff.rect(self.x + self.width - sw,
                               bottomVertY,
                               sw,
                               vertSegHight,
                               segCLit,
                               1)
            
            # D segment (bottom horizontal)
            if(segDLit == drawLitSegments):
                self.buff.rect(horizSegX,
                               self.y + self.height - sw,
                               horizSegWidth,
                               sw,
                               segDLit,
                               1)
                
            # E segment (left bottom vertical
            if(segELit == drawLitSegments):
                self.buff.rect(self.x,
                               bottomVertY,
                               sw,
                               vertSegHight,
                               segELit,
                               1)
            
            # F segment (left top vertical)
            if(segFLit == drawLitSegments):
                self.buff.rect(self.x,
                               topVertY,
                               sw,
                               vertSegHight,
                               segFLit,
                               1)
            
            # G segment (middle horizontal)
            if(segGLit == drawLitSegments):
                self.buff.rect(horizSegX,
                               self.y + int(self.height / 2) - int(sw / 2),
                               horizSegWidth,
                               sw,
                               segGLit,
                               1)
            
            
 
if __name__=='__main__':
        print("This library is not intended to be executed directly")
    