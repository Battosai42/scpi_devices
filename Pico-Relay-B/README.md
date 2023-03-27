# Pico-Relay-B

## SCPI Commands
The followingSCPI commands are supported

### *IDN?
Returns device manufacturer and type description

Example:
- *IDN? -> Waveshare, RP4020 8 Channel Pico-Relay-B
    
### *RST
Reset device to state after power up (turns off all relais)

Example:
- *RST -> None
    
### RELAis:CHANnel\<X>, ALL>:STATe \<0, OFF, 1, ON>
Turn relais in channel X on or off. All other relais remain in whatever state they are already in

Example:
- RELAis:CHANnel1:STATe ON -> None
- RELAis:CHANnel0:STATe 0 -> None
    
### RELAis:CHANnel\<X, ALL>:STATe?
Returns the state of channel X

Example:
- RELAis:CHANnel\<X, ALL>:STATe? -> CH\<X>:0
