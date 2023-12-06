from HousePyEPR import *

analysis=House_PyEPR(HFSSproject_path=r'C:\Users\CHS357\Desktop\Desgin\HFSS\Shoebox',
                     HFSSproject_name=r'YaleCav',
                     HFSSdesign_name=r'SmallChip_shift1',
                     iter_num=r'_01',
                     savingdirectory=r'C:\Users\CHS357\Documents\GitHub\pyEPR\chs357\project_data',
                     savingfilename=r'SmallChip_Update')

analysis.save()
analysis.run()
