

while(True):
    door_close = door_open = batti_off = batti_off = "False"
    lower = input("\nEnter anything\n")
    transcription = lower.lower()
    substrings_lights = ["batti", "vati", "bati", "batii", "bhatti", "bhati"]
    lights_on = ["bala", "vala", "valor", "wala", "on", "baala", "bhala"]
    lights_off = ["nibhau", "nibau", "banda", "wanda", "off", "vanda", "bhanda", "nibha"]

    substrings_doors = ["dhoka", "doka", "dhukha", "dhuka", "duka", "coca", "dukkha", "dhooka", "duca"]
    door_open = ["khola", "kola", "koala", "cola", "open", "kholo", "khula", "khunna"]
    door_close = ["lagau", "laga", "laaga", "lagaa", "close", "laghau"]


    if ("night" in transcription):
        print("\nGN")
        door_close = True
        lights_off = True

    if any(substring in transcription for substring in substrings_lights):
        if any(further in transcription for further in lights_on):
            batti_on = True
            batti_off = False
        elif any(further in transcription for further in lights_off):
            batti_off = True
            batti_on = False
        

    if(any(substring in transcription for substring in substrings_doors)):
        if any(newer in transcription for newer in door_open):
            door_open = True
            door_close = False
        elif any(newer in transcription for newer in door_close):
            door_close = True
            door_open = False
            
    if (batti_off):
        print("Lights Off")
    elif (batti_on):
        print("Lights On")

    if (door_close):
        print("Door Closed")
    elif (door_open):
        print("Door Opened")    
    
