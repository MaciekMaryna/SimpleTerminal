#     TODO
# 1) nie działa scrolowanie w oknie odebranych danych


from tkinter import *
from tkinter import Canvas

import serial.tools.list_ports
import functools

my_run_flag = True
bg_univ = '#f0f0f0'

# Program section ######################################################################################################
my_window = Tk()
my_window.config(bg=bg_univ)
my_window.wm_title('Simple terminal')

my_main_frame = Frame(my_window)
my_main_frame.grid(padx=20, pady=20)
ports = serial.tools.list_ports.comports()
serial_obj = serial.Serial()


# def section ##########################################################################################################
def init_com_port(index):
    port_name = str(ports[index])
    port_name_short = port_name.split(" ")[0]
    serial_obj.port = port_name_short
    serial_obj.baudrate = 115200
    serial_obj.open()


def write_serial_port(msg):
    serial_obj.write(str(msg).encode())


def open_port():
    None


def close_port():
    if serial_obj.isOpen():
        serial_obj.close()


def enable_to_close():
    global my_run_flag
    my_run_flag = False
    close_port()
    my_window.quit()
    my_window.destroy()


def clear_revive_canvas():
    print('Find out how to clear recived data canvas.')
    recive_canvas.delete("all")
    recive_canvas.xview_scroll(0)
    recive_canvas.yview_scroll(0)


def read_serial_port():
    if serial_obj.isOpen() and serial_obj.in_waiting:
        packet = serial_obj.readline()
        if packet[0] == 13:
            packet_string = packet[1:].decode('utf').rstrip("\n")
        else:
            packet_string = packet.decode('utf').rstrip("\n")
        Label(recive_data_frame, text=packet_string, font=("Courier", 10), fg="white", bg="black").pack(anchor="w")


# Send data region #####################################################################################################
my_frame_send = Frame(my_main_frame)
my_frame_send.grid(row=0, column=0, padx=10, pady=10)

Label(my_frame_send, text='Dane do wysłania:', font=('Calibri', 13), bg=bg_univ).grid(row=0, column=0, columnspan=5)
send_string = StringVar()
send_entry = Entry(my_frame_send, textvariable=send_string, font=("Courier", 10), border=2, bg="white", width=45)
send_entry.grid(row=1, column=0, columnspan=4, sticky="w")
send_button = Button(my_frame_send, text='Wyślij', font=('Calibri', 11), height=1, width=10,
                     command=functools.partial(write_serial_port, msg=send_string))
send_button.grid(row=1, column=4, sticky="e")


# Recive data region ###################################################################################################
my_frame_recive = Frame(my_main_frame)
my_frame_recive.grid(row=1, column=0, padx=10, pady=10)

Label(my_frame_recive, text='Dane odebrane:', font=('Calibri', 13), bg=bg_univ).grid(row=10, column=0, columnspan=5)
recive_canvas = Canvas(my_frame_recive, width=450, height=450, bg="black")
recive_canvas.grid(row=11, column=0, columnspan=5, rowspan=100)

vsb_recive = Scrollbar(my_frame_recive, orient='vertical', command=recive_canvas.yview)
vsb_recive.grid(row=11, column=5, rowspan=100, sticky='ns')
recive_canvas.configure(yscrollcommand=vsb_recive.set)

recive_data_frame = Frame(recive_canvas, bg='black')
recive_canvas.create_window((20, 20), window=recive_data_frame, anchor="nw")


#  Right buttons region ################################################################################################
my_frame_button = Frame(my_main_frame)
my_frame_button.grid(row=2, column=1, padx=10, pady=10, sticky="s")

close_button = Button(my_frame_button, text="Zamknij port", font=('Calibri', 11), height=1, width=10,
                      command=functools.partial(close_port))
close_button.grid(row=12, column=6)

clear_button = Button(my_frame_button, text="Wyczyść", font=('Calibri', 11), height=1, width=10,
                      command=functools.partial(clear_revive_canvas))
clear_button.grid(row=13, column=6)

exit_button = Button(my_frame_button, text='Wyjście', font=('Calibri', 11), height=1, width=10,
                     command=functools.partial(enable_to_close))
exit_button.grid(row=110, column=6)

#  Choose port region ##################################################################################################
my_frame_ports = Frame(my_main_frame)
my_frame_ports.grid(row=2, column=0, padx=10, pady=10, sticky="s")
Label(my_frame_ports, text='Wybierz port:', font=('Calibri', 13), bg=bg_univ).grid(row=0, column=0)

for one_port in ports:
    com_button = Button(my_frame_ports, text=one_port, font=('Calibri', 11), height=1, width=45,
                        command=functools.partial(init_com_port, index=ports.index(one_port)))
    com_button.grid(row=ports.index(one_port) + 1, column=0)


# my_window.mainloop()
while my_run_flag:
    read_serial_port()
    my_window.update()



