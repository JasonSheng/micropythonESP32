import m

spi = SPI(baudrate=100000, polarity=1, phase=0, sck=Pin(m.D13), mosi=Pin(m.D11), miso=Pin(m.D12))
sd = sdcard.SDCard(spi, Pin(m.D7))