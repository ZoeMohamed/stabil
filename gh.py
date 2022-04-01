from mimetypes import init
from secrets import randbelow


class Tes():


    def __init__(self):
        self.comp_arr = [100]
        self.voltage = None

    def tes(self):   
        self.comp_arr.append(215)
        last_volt= self.comp_arr[0]
        real_time_volt =  self.comp_arr[-1]
        if(len(self.comp_arr ) == 2):
            if(abs(real_time_volt - last_volt)) > 100:
                print("tegangan gak Normal")
                print(abs(last_volt - real_time_volt))
                self.comp_arr.remove(real_time_volt if abs(real_time_volt - last_volt) > 100  else last_volt)
                self.voltage = real_time_volt
                print(real_time_volt)
                print(self.comp_arr)

                # real_time_volt = self.comp_arr[0]
                # print(real_time_volt)

            else:
                # Delete the latest voltage 
                print("tegangan Normal")
                self.comp_arr.remove(real_time_volt if abs(real_time_volt - last_volt) > 100  else last_volt)
                print(real_time_volt)
                print(self.comp_arr)

    def tesp(self):
        print(self.voltage)



                

x = Tes()

x.tes()
x.tesp()
