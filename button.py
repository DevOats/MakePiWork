from machine import Pin
import time



# Implements an abstraction for a button.
# The button uses GPIO interrupts, however the callbacks are executed on the main application thread.
# Periodically call the execute() function for this.
#
# The following callbacks are implemented: (all callbacks are optional)
# Button Down: - Called when the button goes down.
#                 - Always called
# Button Up:   - Called when the button goes up
#                 - Always called
# Clicked:     - Called when the button goes up after being pressed down.
#                 - When the LongPress callback has been assigned: Only called when no long press has been detected
#                 - When the LongPress callback has NOT been assigned: Always called
# LongPress    - Called when the button has been pressed down for longer than the specified time
#                 - Always called.
#                 - A long press will prevent the ButtonClick from being called after the button goes up
#
class Button:
    
    # Constructor
    def __init__(self,
                 gpioPinNumber: int,
                 downCallback: Callable = None,
                 clickCallback: Callable = None,
                 longPressCallback: Callable = None,
                 buttonUpCallback: Callable = None,
                 longPressTimeMs: int = 1500):
        
        self.buttonDownCallback = downCallback
        self.clickCallback = clickCallback
        self.longPressCallback = longPressCallback
        self.buttonUpCallback = buttonUpCallback
        self.longPressTimeMs = longPressTimeMs
        
        self.longPressHandled = False
        self.buttonState = 1
        self.clickedFlag: bool = False
        self.buttonDownFlag: bool = False
        self.buttonUpFlag: bool = False
        self.buttonDownStartTicks = -1;
        
        self.button = Pin(gpioPinNumber,Pin.IN,Pin.PULL_UP)
        self.button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = self.__button_interruptHandler)


    def __button_interruptHandler(self, buttonPin):
        
        # Disable interrupts while handling this one
        self.button.irq(handler = None)
        
        # If we were Pressed, but we're now Released
        if((self.buttonState == 0) and (self.button.value() == 1)):
            self.buttonState = 1
            self.buttonDownStartTicks = -1
            self.buttonUpFlag = True
            
            if(not self.longPressHandled):
                self.clickedFlag = True
            
            
        # If we were Released, but we're now Pressed
        if((self.buttonState == 1) and (self.button.value() == 0)):
            self.buttonState = 0
            self.buttonDownFlag = True
            self.buttonDownStartTicks = time.ticks_ms() # get millisecond counter
            self.longPressHandled = False
        
        #Re-enable the interrupts
        self.button.irq(handler = self.__button_interruptHandler)


    # Sets the callback for handling when the button is pushed down
    def setCallback_buttonDown(self, callback: Callable):
        self.buttonDownCallback = callback


    # Sets the callback for handling standard button clicks
    def setCallback_click(self, callback: Callable):
        self.clickCallback = callback
    
    
    # sets the callback for handling long presses
    def setCallback_longPress(self, callback: Callable):
        self.longPressCallback = callback
        
        
    # Sets the callback for handling when the button went up
    def setCallback_buttonUp(self, callback: Callable):
        self.buttonUpCallback = callback


    # Clears the state of the button and resets any pending callbacks
    # Note that this will not remove the assigenedd callback methods
    def reset(self):
        self.buttonState = 1
        self.clickedFlag = False
        self.buttonDownFlag = False
        self.buttonUpFlag = False
        self.buttonDownStartTicks = -1
        self.longPressHandled = False


    # Execute this method from your main application loop for the appropriate callbacks to be called
    # This is to prevent lengthy application code to be executed on the interrupt handler routine
    def execute(self):
        
        # Determine if the button has been pushed down
        if(self.buttonDownFlag):
            if(self.buttonDownCallback != None):
                self.buttonDownCallback()
            self.buttonDownFlag = False
            
        
        # Determine if the button has been clicked
        if(self.clickedFlag):
            if(self.clickCallback != None):
                self.clickCallback()   
            self.clickedFlag = False
            
        # Determine if we waited long enough for a long press if the button is still down
        if(self.buttonState == 0 and (self.longPressCallback != None) and (not self.longPressHandled)):
            if(self.buttonDownStartTicks != -1):
                deltaMs = time.ticks_diff(time.ticks_ms(), self.buttonDownStartTicks) # compute time difference
                
                if(deltaMs > self.longPressTimeMs):
                    self.longPressHandled = True
                    self.longPressCallback()
               
        # Determine if the button has been released
        if(self.buttonUpFlag):
            if(self.buttonUpCallback != None):
                self.buttonUpCallback()
            self.buttonUpFlag = False



#
# Demo code from here.
#

def testCallbackButtonDown():
    print("Callback: Button down")

def testCallbackClick():
    print("Callback: Button clicked")
    
def testCallbackLongPress():
    print("Callback: Button long pressed")
    
def testCallbackButtonUp():
    print("Callback: Button Up")


# Demo
if __name__ == '__main__':
    
    print("Button demo code")
    
    # Create a button. Note that the callbacks and longPress delay time could be set in the constructor
    button = Button(15)
                
    # Reset the button state (only here for reference purposes. Not actually needed after instantiating)
    button.reset()
    
    # Assigned the callback handler. Note that all callback handlers are optional
    button.setCallback_buttonDown(testCallbackButtonDown)
    button.setCallback_click(testCallbackClick)
    button.setCallback_longPress(testCallbackLongPress)
    button.setCallback_buttonUp(testCallbackButtonUp)

    
    # In your application logic, periodically call the execute function. This will in turn call the appropriate callback methods.
    # The reason for this is to prevent your application logic from being executed on the interrupt handler thread.
    while(True):
        button.execute()
        time.sleep_ms(1)
        

