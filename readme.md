####  1. Use this command to request the current communication settings.
>aXU<cr><lf>

Response:
>aXU,A=a,M=[M],T=[T],C=[C],I=[I],B=[B],D=[D],P=[P],S=[S], L=[L],N=[N],V=[V]<cr><lf>

Settings Fields
* a   Device address
* XU  Device settings command in ASCII and NMEA 0183
* XXU Device settings command in SDI-12
* [A] Address
    * 0 (default) ... 9, A ... Z, a ... z
* [M] Communication protocol:
    * A = ASCII, automatic
    * a = ASCII, automatic with CRC
    * P = ASCII, polled
    * p = ASCII, polled, with CRC
    * N = NMEA 0183 v3.0, automatic
    * Q = NMEA 0183 v3.0, query (= polled)
    * S = SDI-12 v1.3
    * R = SDI-12 v1.3 continuous measurement
* [C] Serial interface:
    * 1 = SDI-12
    * 2 = RS-232
    * 3 = RS-485
    * 4 = RS-422
* [I] Automatic repeat interval for Composite data message: 
    * 1 ... 3600 s, 0 = no automatic repeat
* [B] Baud rate: 
    * 1200
    * 2400
    * 4800
    * 9600
    * 19200
    * 38400
    * 57600
    * 115200
* [D] Data bits:
    * 7
    * 8
* [P] Parity:
    * O = Odd
    * E = Even
    * N = None
* [S] Stop bit": Nos:
    * 1
    * 2
* [L] RS-485 line delay:
    * 0 ... 10000 ms. Defines the delay between the last character of the queryand the first character of the response message from the transmitter. During the delay, thetransmitter is disabled. Effective in ASCII, polled and NMEA 0183 query protocols. Effectivewhen RS-485 is selected (C = 3).
* [N] Name of the device: WXT536 (read-only)
* [V] Software version: for example, 1.00 (read-only)
* [H] Parameter locking:
    * 0 = Parameters can be changed
    * 1 = Parameters locked. This prevents accidental changes, for instance, in RS- 485 use when there isinterference.
* <cr><lf> Response terminator


####  2. Use this command to change communication settings.
>aXU,A=x,M=x,C=x,I=x,B=x,D=x,P=x,S=x,L=x<cr><lf>

####  3. This command performs software reset on the device.
>aXZ<cr><lf>

####  4. This command resets the rain and hail accumulation and duration parameters Rc, Rd, Hc,and Hd.
>aXZRU<cr><lf>

####  5. This command resets the rain and hail intensity parameters Ri, Rp, Hi, and Hp.
>aXZRI<cr><lf>

####  6. This command interrupts all ongoing measurements except rain measurement and restartsthem.
>aXZM<cr><lf>

####  7. Abbreviations and Units:
* Sn  Wind speed minimum
    * m/s, km/h, mph, knots
* Sm  Wind speed average
    * m/s, km/h, mph, knots
* Sx  Wind speed maximum
    * m/s, km/h, mph, knots
* Dn  Wind direction minimum
    * deg
* Dm  Wind direction average
    * deg
* Dx  Wind direction maximum
    * deg
* Pa  Air pressure
    * hPa, Pa, bar, mmHg, inHg
* Ta  Air temperature
    * °C, °F
* Tp  Internal temperature
    * °C, °F
* Ua  Relative humidity
    * %RH
* Rc  Rain accumulation
    * mm, in
* Rd  Rain duration
    * s
* Ri  Rain intensity
    * mm/h, in/h
* Rp  Rain peak intensity
    * mm/h, in/h
* Hc  Hail accumulation
    * hits/cm2, hits/in2, hits
* Hd  Hail duration
    * s
* Hi  Hail intensity
    * hits/cm2h, hits/in2h,hits/h
* Hp  Hail peak intensity
    * hits/cm2h, hits/in2h,hits/h
* Th  Heating temperature
    * °C, °F
* Vh  Heating voltage
    * V
* Vs  Supply voltage
    * V
* Vr  3.5 V ref. voltage
    * V
* Id  Information field
    * Alphanumeric

####  8. This command queries the address of the device on the bus.
>?<cr><lf>

####  9. This command checks that a device responds to a data recorder or another device. It asks asensor to acknowledge its presence on the bus.
>a<cr><lf>

####  10. This command requests the wind data message.
>aR1<cr><lf>

####  11. This command requests a pressure, temperature, and humidity data message.
>aR2<cr><lf>

####  12. This command requests the precipitation data message.
>aR3<cr><lf>

####  13. This command requests a supervisor data message containing self-check parameters of the heating system and power supply voltage.
>aR5<cr><lf*

####  14. This command requests all individual messages aR1, aR2, aR3, and aR5 with onecommand.
>aR<cr><lf>

####  15. This command requests a combined data message with user-configurable set of wind,pressure, temperature, humidity, precipitation, and supervisor data.
>aR0<cr><lf>

####  16. With the following command you can check the current wind sensor settings.
>aWU<cr><lf>

Response:
aWU,R=[R],I=[I],A=[A],G=[G],U=[U],D=[D],N=[N],F=[F]<cr><lf>

Setting Fields
[R] Parameter selection.The bit value 0 disables and the bit value 1 enablesthe parameter.
    1st bit     Dn Direction minimum obtained with aR1 and ar1
    2nd bit     Dm Direction average obtained with aR1 and ar1
    3rf bit     Dx Direction maximum obtained with aR1 and ar1
    4th bit     Sn Speed minimum obtained with aR1 and ar1
    5th bit     Sm Speed average obtained with aR1 and ar1
    6th bit     Sx Speed maximum obtained with aR1 and ar1
    7th bit     output mode obtained with aR1 and ar1
    8th bit     spare
    &           delimiter
    9th bit     Dn Direction minimum obtained with aR0 and ar0
    10th bit    Dm Direction average obtained with aR0 and ar0
    11th bit    Dx Direction maximum obtained with aR0 and ar0
    12th bit    Sn Speed minimum obtained with aR0 and ar0
    13th bit    Sm Speed average obtained with aR0 and ar0
    14th bit    Sx Speed maximum obtained with aR0 and ar0
    15th bit    output mode obtained with aR0 and ar0
    16th bit    spare
* [I] Update interval:
    * 1 ... 3600 seconds
* [A] Averaging time:
    * 1 ... 3600 seconds Same period is also used for maximum and minimum calculation.
* [G] Wind speed max/min calculation mode: 1 or 3
    * G =1: Traditional max/mincalculation is performed both for speed and direction.
    * G =3: Gust & lull arecalculated for wind speed, replace the wind speed max/min values.
* [U] Speed unit:
    * M = m/s
    * K = km/h
    * S = mph
    * N = knots
* [D] Direction offset:
    *  -180 ... 180
* [F] Sampling rate. Defines how frequently the wind is measured.:
    * 1 Hz
    * 2 Hz
    * 4 Hz 
    
####  17. Change the settings with the following command.
>aWU,R=x,I=x,A=x,G=x,U=x,D=x,N=x,F=x<cr><lf>

####  18. Use this command to check the current pressure, temperature, and humidity sensor settings.
>aTU<cr><lf>

Response:
>aTU,R=[R],I=[I],P=[P],H=[H]<cr><lf>

Setting Fields
* [R] Parameter selection.The bit value 0 disables and the bit value 1 enablesthe parameter.
    * 1st bit     Pa Air pressure obtained with aR2 and ar2
    * 2nd bit     Ta Air temperature obtained with aR2 and ar2
    * 3rf bit     Tp Internal temperature obtained with aR2 and ar2
    * 4th bit     Ua Air humidity obtained with aR2 and ar2
    * 5th bit     spare
    * 6th bit     spare
    * 7th bit     spare
    * 8th bit     spare
    * &           delimiter
    * 9th bit     Pa Air pressure obtained with aR0 and ar0
    * 10th bit    Ta Air temperature obtained with aR0 and ar0
    * 11th bit    Tp Internal temperature obtained with aR0 and ar0
    * 12th bit    Ua Air humidity obtained with aR0 and ar0
    * 13th bit    spare
    * 14th bit    spare
    * 15th bit    spare
    * 16th bit    spare
* [I] Update interval:
    * 1 ... 3600 seconds
* [P] Pressure unit:
    * H = hPa
    * P = Pascal
    * B = bar
    * M = mmHg 
    * I = inHg
* [T] Temperature unit:
    * C = Celsius
    * F = Fahrenheit

####  19. Change the setting with the following command.
>aTU,R=x,I=x,P=x,T=x<cr><lf>

####  20. Use this command to check the current precipitation sensor settings.
>aRU<cr><lf>

Response:
>aRU,R=[R],I=[I],U=[U],S=[S],M=[M],Z=[Z],X=[X],Y=[Y]<cr> <lf>

Setting Fields
* [R] Parameter selection.The bit value 0 disables and the bit value 1 enablesthe parameter.
    * 1st bit     Rc Rain amount obtained with aR3 and ar3
    * 2nd bit     Rd Rain duration obtained with aR3 and ar3
    * 3rf bit     Ri Rain intensity obtained with aR3 and ar3
    * 4th bit     Hc Hail amount obtained with aR3 and ar3
    * 5th bit     Hd Hail duration obtained with aR3 and ar3
    * 6th bit     Hi Hail intensity obtained with aR3 and ar3
    * 7th bit     Rp Rain peak obtained with aR3 and ar3
    * 8th bit     Hp Hail peak obtained with aR3 and ar3
    * &           delimiter
    * 9th bit     Rc Rain amount obtained with aR0 and ar0
    * 10th bit    Rd Rain duration obtained with aR0 and ar0
    * 11th bit    Ri Rain intensity obtained with aR0 and ar0
    * 12th bit    Hc Hail amount obtained with aR0 and ar0
    * 13th bit    Hd Hail duration obtained with aR0 and ar0
    * 14th bit    Hi Hail intensity obtained with aR0 and ar0
    * 15th bit    Rp Rain peak obtained with aR0 and ar0
    * 16th bit    Hp Hail peak obtained with aR0 and ar0
* [I] Update interval: 1 ... 3600 seconds
* [U] Precipitation units:
    * M= metric
    * I= imperial
* [S] Hail units:
    * M= metric
    * I= imperial
* [M] Auto-send mode: 
    * R = precipitation on/off: The transmitter sends a precipitation message 10 seconds after thefirst recognition of precipitation. Rain duration Rd increases in 10 s steps
    * C= tipping bucket: The transmitter sends a precipitation message at each unit increment. Do not use the auto-send mode tipping bucket in polled protocols as it decreases theresolution of the output
    * T= time based: Transmitter sends a precipitation message in the intervals defined in the [I]field. 
* [Z] Counter reset:
    * M = manual reset mode: The counter is reset with aXZRU command.
    * A = automatic reset mode: The counts are reset after each precipitation message
    * L = overflow reset mode. The rain counter or hail counter is reset, when it reaches thepredefined limit.
    * Y = immediate reset: The counts are reset immediately after receiving the command.
* [X]. Rain accumulation limit : 
    * 100...65535. Sets the rain accumulation counter resetting limit. The limit corresponds the range between 1.00 ... 655.35 mm.
* [Y] Hail accumulation limit: 
    * 100 ... 65535 Sets the hail accumulation counter resetting limit. Thelimit corresponds the range between 10.0 ... 6553.5 hits/ cm2.

####  21. Change the setting with the following command.
>aRU,R=x,I=x, U=x,S=x,M=x,Z=x, X=x, Y=x<cr><lf>

####  22. Use this command to check the current supervisor settings.
>aSU<cr><lf>

Response:
>aSU,R=[R],I=[I],S=[S],H=[Y]<cr><lf>

Setting Fields
* [R] Parameter selection.The bit value 0 disables and the bit value 1 enablesthe parameter.
    * 1st bit     Th Heating temperature obtained with aR5 and ar5
    * 2nd bit     Vh Heating voltage obtained with aR5 and ar5
    * 3rf bit     Vs Supply voltage obtained with aR5 and ar5
    * 4th bit     Vr 3.5 V reference voltage obtained with aR5 and ar5
    * 5th bit     Id Information field obtained with aR5 and ar5
    * 6th bit     spare
    * 7th bit     spare
    * 8th bit     spare
    * &           delimiter
    * 9th bit     Th Heating temperature obtained with aR0 and ar0
    * 10th bit    Vh print( Heating voltage obtained with aR0 and ar0
    * 11th bit    Vs Supply voltage obtained with aR0 and ar0
    * 12th bit    Vr 3.5 V reference voltage obtained with aR0 and ar0
    * 13th bit    Id Information field obtained with aR0 and ar0
    * 14th bit    spare
    * 15th bit    spare
    * 16th bit    spare
* [I] Update interval: 
    * 1 ... 3600 seconds
* [S] Error messaging: 
    * Y = enabled
    * N = disabled
* [H] Heating control enable:
    * Y = enabled
    * N = disabled