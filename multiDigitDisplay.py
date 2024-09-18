from sevenSegmentDraw import SevenSegmentDigit

#Represents a multi Digit Seven Segment Display
class MultiDigitDisplay:

    def __init__(self,
                 frameBuf: framebuf.FrameBuffer,
                 x: int,
                 y: int,
                 digitCount: int = 2,
                 digitWidth:int = 15,
                 digitHeight: int = 30,
                 digitSpacing: int = 6,
                 segmentThickness: int = 4,
                 displayLeadingZeros: bool = True,
                 autoCenter: bool = False
                 ):
    
        self.display = frameBuf
        self.x = x
        self.y = y
        self.digitWidth = digitWidth
        self.digitSpacing = digitSpacing
        self.segmentThickness = segmentThickness
        self.digitCount = digitCount
        self.digits = []
        self.number = 0
        self.displayLeadingZeros = displayLeadingZeros
        self.autoCenter = autoCenter
        self.decimalSeperatorIndex = -1
        self.height = digitHeight
        self.width = (digitWidth * digitCount) + (digitSpacing * (digitCount - 1))
        self.xPosOffset = 0
        self.digitsDrawn = self.digitCount
        
        # Instatiate the individual digits and calculate their x positions
        xPos = x
        for i in range(digitCount):
            digit = SevenSegmentDigit(self.display, xPos, y, digitWidth, digitHeight, segmentThickness)
            self.digits.append(digit)
            xPos += digitWidth + digitSpacing
            
    
    # draws the specified number to the frame buffer.
    # Optionally a decimal separator index can be specified. Set to -1 to disable
    def displayNumber(self,
                      number: int,
                      decimalSeparatorIndex: int = -1):
        
        self.number = number
        self.decimalSeperatorIndex = decimalSeparatorIndex
        
        self.__drawNumber()
        self.__drawDecimalSeparator()
        
        
    def __drawNumber(self):
        
        num:int = self.number
        digitIndex = 1
        
        digitsToDraw = [0] * self.digitCount
        digitShowCount = 0
              
        # First get the individual numbers that needs the be drawn at the specific digit
        for i in range(self.digitCount -1, -1, -1):
            
            modulus = digitIndex * 10
            drawDigit = (num > 0
                         or self.displayLeadingZeros
                         or i == self.digitCount -1)
 
            if(drawDigit):
                digitVal : int = num % modulus
                digitShowCount += 1
            else:
                digitVal = -1

            digitsToDraw[i] = digitVal
            num = int(num / 10)
            digitIndex + 1

        
        # When AutoCentering has been enabled, move the X position of the digits according to the number of digits drawn
        if(self.autoCenter):
            self.digitsDrawn = digitShowCount
            self.__performAutoCentering()


        # Let the individual digits draw their numbers
        for i in range(self.digitCount -1, -1, -1):
            val = digitsToDraw[i]
            if(val != -1):
                self.digits[i].displayNumber(val)
        
        
    def __performAutoCentering(self):
        
        # Fully clear the bounding recangle, because the segments migth not overlap the previous drawings
        self.display.rect(self.x, self.y, self.width, self.height, 0, 1)
        
        #set new X positions for the digits
        extraSpace = (self.digitCount - self.digitsDrawn) * (self.digitWidth + self.digitSpacing)
        
        self.xPosOffset = int(extraSpace / 2)
        xPos = self.x + self.xPosOffset
        
        for i in range(self.digitCount - self.digitsDrawn, self.digitCount):
            digit = self.digits[i]
            digit.setX(xPos)
            xPos += self.digitWidth + self.digitSpacing
        

    def __drawDecimalSeparator(self):
        
        if((self.decimalSeperatorIndex >= 0) and (self.decimalSeperatorIndex <= self.digitsDrawn)):

            # The bottom right decimal position
            xPos = self.x + (self.digitsDrawn * (self.digitWidth + self.digitSpacing)) + self.xPosOffset - self.digitSpacing
            
            # Count the decimal separator index positions backwards
            xPos -= self.decimalSeperatorIndex * (self.digitWidth + self.digitSpacing)
            
            xCenterAdjust = int((self.digitSpacing - self.segmentThickness) / 2)
            xPos += xCenterAdjust
            yPos = self.y + self.height - self.segmentThickness
            self.display.rect(xPos, yPos, self.segmentThickness, self.segmentThickness, 1, 1)
        
    
    
if __name__=='__main__':
    print("This library is not intended to be executed directly")
    
