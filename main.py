from HousePyEPR import *

analysis=House_PyEPR(HFSSproject_path=r'C:\Users\CHS357\Desktop\Desgin\HFSS\Shoebox',
                     HFSSproject_name=r'YaleCav',
                     HFSSdesign_name=r'BigChip_shift',
                     iter_num=r'_87',
                     savingdirectory=r'C:\Users\CHS357\Documents\GitHub\pyEPR\chs357\project_data',
                     savingfilename=r'BigChip')

analysis.save()
analysis.run()